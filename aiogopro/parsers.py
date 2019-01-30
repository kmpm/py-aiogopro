from .types import MediaEntry


def media_list(jsondata):
    content = []
    for d in jsondata['media']:
        for fs in d['fs']:
            content.append(MediaEntry(d['d'], fs['n'], int(fs['cre'], 10), int(fs['mod'], 10), int(fs['s'], 10)))
    return content
