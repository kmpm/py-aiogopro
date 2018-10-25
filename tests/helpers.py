import json


def load_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data
