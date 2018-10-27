import unittest
from os import path
from tests.helpers import load_json

from aiogopro.schema import SchemaType, schema_compare

THIS_FOLDER = path.dirname(path.realpath(__file__))
DOC_FOLDER = path.join(THIS_FOLDER, '..', 'doc')


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

    def test_hd4_hd7_comparison(self):
        hd7 = SchemaType.parse(load_json(path.join(DOC_FOLDER, 'HD7_01_01_51_00.json')))
        hd4 = SchemaType.parse(load_json(path.join(DOC_FOLDER, 'HD4_02_05_00_00.json')))
        schema_compare(hd4, hd7, 'HD4', 'HD7')


if __name__ == '__main__':
    unittest.main()
