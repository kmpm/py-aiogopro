import json

from .types import MediaEntry


def media_list(jsondata):
    content = []
    #print('parsers.media_list=', json.dumps(jsondata))
    for d in jsondata['media']:
        for fs in d['fs']:
            content += media_entry(d['d'], fs)
    return content


def media_entry(folder, fs):
    """Parse jsondata and return a list of media entries
    Parameters
    ----------
    folder : string
        Name of the folder
    fs : dict
        One _fs_ entry from the media section
    Returns
    -------
    list
        returns a list of 1 or more entries created from fs
    """
    name = fs['n']
    content = []
    if 'b' in fs:  # multishot photo
        lower = int(fs['b'], 10)
        higher = int(fs['l'], 10)
        for i in range(lower, higher, 1):
            content.append(MediaEntry(
                folder=folder,
                name=name.replace(f'{lower}.', f'{i}.'),
                size=0,
                **fs))
    else:
        content.append(MediaEntry(
                folder=folder,
                name=name,
                **fs))
    return content
