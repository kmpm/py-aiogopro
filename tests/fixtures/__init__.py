import json
from os import path

fixture_path = path.dirname(path.realpath(__file__))


def load_json(filename):
    with open(path.join(fixture_path, filename)) as f:
        data = json.load(f)
    return data
