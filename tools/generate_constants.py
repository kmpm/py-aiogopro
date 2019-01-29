from os import path
import argparse

from tests.helpers import load_json, PROJECT_FOLDER
from tools.schema import SchemaType, schema_pythonify

parser = argparse.ArgumentParser(description='Convert schema json to constants.py')
parser.add_argument('source', help='path to json source schema')


def main():
    args = parser.parse_args()

    schema = SchemaType.parse(load_json(args.source))
    schema_pythonify(schema, path.join(PROJECT_FOLDER, 'aiogopro', 'constants.py'))


if __name__ == '__main__':
    main()
