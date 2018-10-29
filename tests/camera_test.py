import unittest
from unittest import mock
import asyncio
from aiogopro import Camera
from tests.helpers import AsyncMock

FAKE_HD7 = {"info": {
        "ap_has_default_credentials": "0",
        "ap_mac": "06416996c50c",
        "ap_ssid": "WsGoPro01",
        "board_type": "0x05",
        "capabilities": "16",
        "firmware_version": "HD7.01.01.51.00",
        "git_sha1": "360b5e9e5aeed5e0f8a12c76431d2a7dec3dc4cd",
        "lens_count": "1",
        "model_name": "HERO7 Black",
        "model_number": 30,
        "serial_number": "C3281324670FFF",
        "update_required": "0"
    }}


def _run(coro):
    """Run the given coroutine."""
    return asyncio.get_event_loop().run_until_complete(coro)


class CameraTest(unittest.TestCase):

    def test_ip(self):
        camera = Camera()
        self.assertEqual(camera._ip, '10.5.5.9')

    @mock.patch('aiogopro.camera.AsyncClient.getJSON', new=AsyncMock(return_value=FAKE_HD7))
    def test_connect(self):
        camera = Camera()
        _run(camera.connect())
        camera._client.getJSON.mock.assert_called_once_with(camera._client, 'http://10.5.5.9/gp/gpControl', timeout=5)
