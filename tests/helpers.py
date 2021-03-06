import json
from os import path, makedirs
from unittest import mock

THIS_FOLDER = path.dirname(path.realpath(__file__))
PROJECT_FOLDER = path.abspath(path.join(THIS_FOLDER, '..'))
DOC_FOLDER = path.join(PROJECT_FOLDER, 'doc')
TMP_FOLDER = path.join(THIS_FOLDER, 'tmp')

if not path.exists(TMP_FOLDER):
    makedirs(TMP_FOLDER)


def load_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def dump_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)


def AsyncMock(*args, **kwargs):
    m = mock.MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro
