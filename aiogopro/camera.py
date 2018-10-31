import json
from yarl import URL

from aiogopro.client import AsyncClient
from aiogopro.infos import CameraInfo
from aiogopro.errors import UnsupportedCameraError
from aiogopro.constants import Status, Command
import aiogopro.utils as utils
import aiogopro.types as types


class Camera:
    def __init__(self, ip='10.5.5.9', mac='AA:BB:CC:DD:EE:FF'):
        self._ip = ip
        self._mac = mac
        self._camera = None  # type: CameraInfo
        self._client = None  # type: AsyncClient

        try:
            from getmac import get_mac_address
            self._mac = get_mac_address(ip="10.5.5.9")
        except ImportError:
            self._mac = mac

    async def _getText(self, url, timeout=None, **kwargs):
        if not self._client:
            self._client = AsyncClient()
        url = "http://{0}{1}".format(self._ip, url)

        # Might be self encoded. Don't mess
        url = URL(url, encoded=kwargs.pop('encoded', False))
        return await self._client.getText(url, timeout=timeout)

    async def _getJSON(self, url, timeout=None, **kwargs):
        if not self._client:
            self._client = AsyncClient()
        url = "http://{0}{1}".format(self._ip, url)

        # Might be self encoded. Don't mess
        url = URL(url, encoded=kwargs.pop('encoded', False))
        return await self._client.getJSON(url, timeout=timeout)

    async def quit(self):
        await self._client.quit()
        self._client = None

    async def connect(self, camera='detect'):
        if camera == 'detect':
            self._camera = await self.getInfo()

        camera = self._camera

        # if it's a session camera we might have to wait some
        if camera.camera_type == "HX":  # Only session cameras.
                connectedStatus = False
                while connectedStatus is False:
                    json_data = await self._getJSON("/gp/gpControl/status")
                    # json_data["status"]["31"]
                    if json_data["status"][Status.wireless.app_count.id] >= 1:
                        connectedStatus = True
        return camera

    async def getInfo(self):
        if self._camera:
            return self._camera

        data = await self._getJSON('/gp/gpControl', timeout=5)
        firmware = data['info']['firmware_version']
        is_usable = False

        for camera in ["HD", "HX", "FS", "H18"]:
            if camera in firmware:
                is_usable = True
                camera_type = camera
                break
        if not is_usable:
            raise UnsupportedCameraError()

        if camera_type == 'HD':
            generation = int(firmware.split('HD')[1][0])
            if generation < 4:
                raise UnsupportedCameraError()

        ci = CameraInfo(camera_type, info=data["info"])
        self._camera = ci
        return ci

    async def getStatus(self, key=None):
        if isinstance(key, types.StatusType):
            value = key.id
        else:
            value = key
        await self.getInfo()
        data = await self._getJSON("/gp/gpControl/status", timeout=5)
        if value:
            return data['status'][value]
        return data

    async def command(self, cmd, value, **kwargs):
        if not isinstance(cmd, types.CommandType):
            raise TypeError('cmd must instance of CommadType')

        url = '/gp/gpControl/{0}'.format(cmd.url)
        if cmd.widget == 'button':
            url = '/gp/gpControl{0}?p={1}'.format(cmd.url, value)
        else:
            raise NotImplementedError('Widget {0} is not implemented'.format(cmd.widget))

        await self.getInfo()
        data = await self._getText(url, timeout=5, **kwargs)
        # fix badly formated json
        if data:
            data = json.loads(data.replace("\\", "/"))
        return data

    async def timeGet(self):
        dtm = await self.getStatus(Status.setup.date_time)
        return utils.parse_datetime(dtm)

    async def timeSync(self, value=None):
        datestr = utils.generate_datetime(value)
        return await self.command(Command.GPCAMERA_SET_DATE_AND_TIME_ID, datestr, encoded=True)

