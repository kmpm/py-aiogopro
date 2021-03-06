import unittest
import json
from aiogopro import constants


class ConstantsTest(unittest.TestCase):
    def test_id(self):
        self.assertEqual(constants.Status.Wireless.app_count.id, "31")

        stuff = json.loads('{"31": "yes", "32": "no"}')
        actual = stuff[constants.Status.Wireless.app_count.id]
        self.assertEqual(actual, 'yes')

    def test_location(self):
        self.assertEqual(constants.Status.System.system_busy.location, 'aiogopro.types')
