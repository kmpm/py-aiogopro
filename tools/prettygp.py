import argparse
import json
from collections import OrderedDict
from operator import itemgetter

parser = argparse.ArgumentParser(description='Make gpControl json-dump pretty')
parser.add_argument('source', help="source to prettyfi")
parser.add_argument('--verbose', '-v', action='count')

outgroup = parser.add_mutually_exclusive_group(required=False)
outgroup.add_argument('-o', '--out', dest='out', default=argparse.SUPPRESS, help="File to send the output to")
outgroup.add_argument('-r', '--replace', dest='replace', action='store_true')


def can_be_sorted(v):
    return isinstance(v, list) or isinstance(v, dict) or isinstance(v, OrderedDict)


def load_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def dump_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, sort_keys=False, indent=4, ensure_ascii=False)


def sort_dict(src):
    result = OrderedDict(sorted(src.items()))
    for k, v in result.copy().items():
        if can_be_sorted(v):
            result[k] = sort(v)
    return result


def sort_list(list_to_be_sorted, *keys):
    if not isinstance(list_to_be_sorted, list) or len(list_to_be_sorted) == 0:
        return list_to_be_sorted

    if not keys:
        v = list_to_be_sorted[0]
        if isinstance(v, dict) or isinstance(v, OrderedDict):
            for k in ['id', 'value', 'group', 'key', 'setting_id']:
                if k in v:
                    keys = (k,)
                    break

    if not keys:
        result = list_to_be_sorted
    else:
        result = sorted(list_to_be_sorted, key=itemgetter(*keys))

    # loop through each index in list and sort if possible
    for index in range(len(result)):
        v = result[index]
        if can_be_sorted(v):
            result[index] = sort(v)
    return result


def sort(to_be_sorted):
    if isinstance(to_be_sorted, dict) or isinstance(to_be_sorted, OrderedDict):
        return sort_dict(to_be_sorted)
    elif isinstance(to_be_sorted, list) and len(to_be_sorted) > 1:
        return sort_list(to_be_sorted)
    return to_be_sorted


def main():
    args = parser.parse_args()
    try:
        src = sort(load_json(args.source))

        out = OrderedDict()
        # basics on top
        out['schema_version'] = src.pop('schema_version')
        out['version'] = src.pop('version')
        if args.verbose >= 1:
            print(f'version: {out["version"] }, schema: {out["schema_version"]}')

        # do specific ones but with standard sorting
        # but get tem in the beginning of the structure
        for k in ['info', 'services']:
            if k in src:
                if args.verbose >= 2:
                    print(f'doing {k}')
                out[k] = sort(src.pop(k))

        # following benefit from special sorting
        if 'commands' in src:
            if args.verbose >= 2:
                print('doing commands')
            out['commands'] = sort_list(src.pop('commands'), 'key')
        if 'modes' in src:
            if args.verbose >= 2:
                print('doing modes')
            out['modes'] = sort_list(src.pop('modes'), 'value')
        if 'camera_mode_map' in src:
            if args.verbose >= 2:
                print('doing camera_mode_map')
            out['camera_mode_map'] = sort_list(src.pop('camera_mode_map'), 'mode_value', 'sub_mode_value')

        # do the rest if any without special sorting
        for k, v in src.items():
            if args.verbose >= 2:
                print(f'doing {k}')
            out[k] = sort(v)

        # output result
        if hasattr(args, 'out'):
            if args.verbose > 0:
                print(f"Writing to {args.out}")
            dump_json(out, args.out)
        elif args.replace:
            if args.verbose > 0:
                print(f"Replacing {args.source}")
            dump_json(out, args.source)
        else:
            print(json.dumps(out, sort_keys=False, indent=4, ensure_ascii=False))

        # done
        if args.verbose > 0:
            print('Done!')

    except OSError:
        parser.print_help()
        raise


if __name__ == '__main__':
    main()
