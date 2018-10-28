import unittest
from os import path
from tests.helpers import load_json, TMP_FOLDER, DOC_FOLDER
from tools.schema import SchemaType, schema_pythonify, schema_compare


class TestSchema(unittest.TestCase):
    def test_hd4(self):
        data = load_json(path.join(DOC_FOLDER, 'HD4_02_05_00_00.json'))
        p = SchemaType.parse(data)
        self.assertEqual(p.schema_version, 2)
        self.assertEqual(p.version, 4.0)
        self.assertIsInstance(p.version, float)
        self.assertIsInstance(p.schema_version, int)
        self.assertEqual(len(p.commands.keys()), 64)
        self.assertEqual(len(p.modes.keys()), 6)

    def test_hd7(self):
        data = load_json(path.join(DOC_FOLDER, 'HD7_01_01_51_00.json'))
        p = SchemaType.parse(data)
        self.assertEqual(p.schema_version, 4, 'expected schema_version=4')
        self.assertEqual(p.version, 2.0, 'expected version=2.0')
        self.assertIsInstance(p.version, float)
        self.assertIsInstance(p.schema_version, int)
        self.assertEqual(len(p.commands.keys()), 88)
        self.assertEqual(len(p.modes.keys()), 7)

    @unittest.skip('To chatty in console')
    def test_hd4_hd7_comparison(self):
        hd7 = SchemaType.parse(load_json(path.join(DOC_FOLDER, 'HD7_01_01_51_00.json')))
        hd4 = SchemaType.parse(load_json(path.join(DOC_FOLDER, 'HD4_02_05_00_00.json')))
        schema_compare(hd4, hd7, 'HD4', 'HD7')

    def test_hd4_pythonify(self):
        hd4 = SchemaType.parse(load_json(path.join(DOC_FOLDER, 'HD4_02_05_00_00.json')))
        schema_pythonify(hd4, path.join(TMP_FOLDER, 'pythonify.py'))


if __name__ == '__main__':
    unittest.main()
