import unittest

from aiogopro import parsers
from aiogopro.types import MediaEntry

from .fixtures import load_json


media = {'id': '27250240617507960',
    'media': [
        {'d': '100GOPRO', 'fs': [
            {'n': 'GOPR0256.JPG', 'cre': '1548846642', 'mod': '1548846642', 's': '3792523'},
            {'n': 'GOPR0257.JPG', 'cre': '1548846706', 'mod': '1548846706', 's': '3833533'},
            {'n': 'GOPR0258.JPG', 'cre': '1548846724', 'mod': '1548846724', 's': '3834537'},
            {'n': 'GOPR0259.JPG', 'cre': '1548848888', 'mod': '1548848888', 's': '3894675'},
            {'n': 'GOPR0260.JPG', 'cre': '1548849006', 'mod': '1548849006', 's': '3862504'},
            {'n': 'GOPR0261.JPG', 'cre': '1548849026', 'mod': '1548849026', 's': '3868793'},
            {'n': 'GOPR0262.JPG', 'cre': '1548849048', 'mod': '1548849048', 's': '3899510'}
        ]}]}

MEDIA_LIST_MULTISHOT_SINGLE = load_json('media_list_multishot_single.json')
MEDIA_LIST_A = load_json('media_list_a.json')
MEDIA_LIST_MIX = load_json('media_list_mix.json')


class TestParsers(unittest.TestCase):
    def test_media_list(self):
        parsed = parsers.media_list(media)
        self.assertIsInstance(parsed, list)

        self.assertEqual(7, len(parsed))
        for v in parsed:
            self.assertIsInstance(v, MediaEntry)
            self.assertEqual(v.folder, '100GOPRO')  # 1 folder
            self.assertGreaterEqual(v.size, 3792523)
            self.assertGreaterEqual(v.created, 1548846642)
            self.assertEqual(v.path, f'{v.folder}/{v.name}')

        v = parsed[0]
        self.assertEqual(str(v), '<MediaEntry path:100GOPRO/GOPR0256.JPG, size:3.62MB>')

    def test_multishot_single(self):
        parsed = parsers.media_list(MEDIA_LIST_MULTISHOT_SINGLE)
        self.assertIsInstance(parsed, list)
        start = 299
        self.assertEqual(20, len(parsed))
        for index in range(len(parsed)):
            v = parsed[index]
            self.assertIsInstance(v, MediaEntry)
            self.assertEqual(v.folder, '100GOPRO')  # 1 folder
            self.assertGreaterEqual(v.size, 0)
            self.assertGreaterEqual(v.created, 1548846642)
            self.assertEqual(v.path, f'{v.folder}/{v.name}')
            self.assertEqual(v.name, f'G0010{start + index}.JPG')

    def test_medialist_a(self):
        parsed = parsers.media_list(MEDIA_LIST_A)
        self.assertIsInstance(parsed, list)
        self.assertEqual(66, len(parsed))
        for index in range(len(parsed)):
            v = parsed[index]
            self.assertIsInstance(v, MediaEntry)
            self.assertEqual(v.folder, '100GOPRO')  # 1 folder
            self.assertGreaterEqual(v.size, 0)
            self.assertGreaterEqual(v.created, 1548846642)
            self.assertEqual(v.path, f'{v.folder}/{v.name}')

    def test_media_list_mix(self):
        parsed = parsers.media_list(MEDIA_LIST_MIX)
        self.assertIsInstance(parsed, list)
        self.assertEqual(39, len(parsed))
