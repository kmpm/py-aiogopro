import unittest
from datetime import datetime
import aiogopro.utils as utils

NOW = datetime(2018, 10, 31, 18, 55, 22)
NOW_STRING = '%12%0a%1f%12%37%16'


class TestUtils(unittest.TestCase):
    def test_generate_datetime(self):
        actual = utils.generate_datetime(NOW)
        self.assertEqual(actual, NOW_STRING)

    def test_parse_datetime(self):
        actual = utils.parse_datetime(NOW_STRING)
        self.assertEqual(actual.strftime('%Y-%m-%d %H:%M:%S'), '2018-10-31 18:55:22')

        actual = utils.parse_datetime(NOW_STRING + '%')  # camera responds with final %
        self.assertEqual(actual.strftime('%Y-%m-%d %H:%M:%S'), '2018-10-31 18:55:22')
