from aiogopro.client import AsyncClient
from aiogopro.infos import CameraInfo
from aiogopro.errors import UnsupportedCameraError
from aiogopro.constants import Status


class Camera:
    def __init__(self, ip='3.5.5.9', mac='AA:BB:CC:DD:EE:FF'):
        self._ip = ip
        self._mac = mac
        self._camera = None  # type: CameraInfo
        self._client = AsyncClient()  # type: AsyncClient

        try:
            from getmac import get_mac_address
            self._mac = get_mac_address(ip="10.5.5.9")
        except ImportError:
            self._mac = mac

    async def _getText(self, url, timeout=None):
        url = "http://{0}/{1}".format(self._ip, url)
        return await self._client.getText(url, timeout=timeout)

    async def _getJSON(self, url, timeout=None):
        url = "http://{0}/{1}".format(self._ip, url)
        return await self._client._getJSON(url, timeout=timeout)

    async def connect(self, camera='detect'):
        if camera == 'detect':
            self._camera = await self.getCameraInfo()

    async def getCameraInfo(self):
        if self._camera:
            return self._camera

        data = self._getJSON('/gp/gpControl', timeout=5)
        firmware = data['info']['firmware_version']
        is_usable = False

        for camera in ["HD", "HX", "FS", "H18"]:
            if camera in firmware:
                is_usable = True
                camera_type = camera
                break
        if not is_usable:
            raise UnsupportedCameraError()

        if camera_type == "HX":  # Only session cameras.
                connectedStatus = False
                while connectedStatus is False:
                    json_data = await self._client.getJSON("/gp/gpControl/status")
                    # json_data["status"]["31"]
                    if json_data["status"][Status.wireless.app_count.id] >= 1:
                        connectedStatus = True

        if camera_type == 'HD':
            generation = firmware.split('HD')[1][0]
            if generation < 4:
                raise UnsupportedCameraError()

        self._camera = CameraInfo(info=data["info"])

    async def getMode(self):
        pass
