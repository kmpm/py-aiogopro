from os import path
from tests.helpers import load_json, DOC_FOLDER, PROJECT_FOLDER
from tools.schema import SchemaType, schema_pythonify


def main():
    hd4 = SchemaType.parse(load_json(path.join(DOC_FOLDER, 'HD4_02_05_00_00.json')))
    schema_pythonify(hd4, path.join(PROJECT_FOLDER, 'aiogopro', 'constants.py'))


if __name__ == '__main__':
    main()
