# Copyright (c) 2018 Peter Magnusson
import json
import asyncio

from yarl import URL

from aiogopro import utils, types, parsers
from aiogopro.client import AsyncClient
from aiogopro.infos import CameraInfo
from aiogopro.errors import CameraUnsupportedError, CameraBusyError
from aiogopro.constants import Status, Command, Mode, SubMode
from aiogopro.protocols import KeepAliveProtocol


class Camera:
    def __init__(self, ip='10.5.5.9', mac='AA:BB:CC:DD:EE:FF'):
        self._ip = ip
        self._mac = mac
        self._camera = None  # type: CameraInfo
        self._client = None  # type: AsyncClient
        self._keepAlive = None  # type: KeepAliveProtocol

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
        if self._keepAlive:
            self._keepAlive.quit()

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
                    if json_data["status"][Status.Wireless.app_count.id] >= 1:
                        connectedStatus = True
        return camera

    async def keepAlive(self):
        loop = asyncio.get_event_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: KeepAliveProtocol(loop),
            remote_addr=(self._ip, 8554)
        )
        # print('transport:', transport)
        # print('protocol:', protocol)
        self._keepAlive = protocol
        return transport

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
            raise CameraUnsupportedError()

        if camera_type == 'HD':
            generation = int(firmware.split('HD')[1][0])
            if generation < 4:
                raise CameraUnsupportedError()

        ci = CameraInfo(camera_type, info=data["info"])
        self._camera = ci
        return ci

    async def getStatus(self, key=None):
        """Fetches all or parts of camera status
        Parameters
        ----------
        key : int | StatusType, optional
            Key of the status value to get.
            Defaults to None which will return raw status.
        """

        if isinstance(key, types.StatusType):
            value = key.id
        else:
            value = key
        await self.getInfo()
        data = await self._getJSON("/gp/gpControl/status", timeout=5)
        if value:
            return data['status'][value]
        return data

    async def command(self, cmd, param=None, **kwargs):
        """Sends a command to camera
        Parameters
        ----------
        cmd : CommandType
            Which command do you want to execute
        param : value | dict
            If single value it will be added to the ?p= parameter.
            Generates a querystring from dict.
        **kwargs :
            will be passed on to #_getText
        """
        if not isinstance(cmd, types.CommandType):
            raise TypeError('cmd must instance of CommadType')

        url = f'/gp/gpControl/{cmd.url}'
        if cmd.widget == 'button':
            if isinstance(param, dict):
                url = f'/gp/gpControl{cmd.url}?'
                for k, v in param.items():
                    url += f'{k}={v}&'

                if url.endswith('&'):
                    url = url[:-1]
            elif param is not None:
                url = f'/gp/gpControl{cmd.url}?p={param}'
        else:
            raise NotImplementedError(f'Widget `{cmd.widget}` is not implemented')

        await self.getInfo()
        data = await self._getText(url, timeout=5, **kwargs)
        # fix badly formated json
        if data:
            data = json.loads(data.replace("\\", "/"))
        return data

    async def timeGet(self):
        dtm = await self.getStatus(Status.Setup.date_time)
        return utils.parse_datetime(dtm)

    async def timeSync(self, value=None):
        datestr = utils.generate_datetime(value)
        return await self.command(Command.GPCAMERA_SET_DATE_AND_TIME_ID, datestr, encoded=True)

    async def mode(self, mode, submode=0):
        """Helper for changing camera mode using GPCAMERA_SUBMODE command
        Parameters
        ----------
        mode : Enum|integer|string
            Primary mode
        submode : Enum|integer|string, optional
            Submode, defaults to 0
        """
        mode_value = mode
        submode_value = submode
        if hasattr(mode_value, 'value'):
            mode_value = mode_value.value
        if hasattr(submode_value, 'value'):
            submode_value = submode_value.value

        # print(self.gpControlCommand("sub_mode?mode=" + mode + "&sub_mode=" + submode))
        return await self.command(Command.GPCAMERA_SUBMODE, {'mode': mode_value, 'sub_mode': submode_value})

    async def shutter(self, value):
        """Helper for GPCAMERA_SHUTTER command
        Parameters
        ----------
        value : '0' | '1'
            Shutter on or off
        """
        return await self.command(Command.GPCAMERA_SHUTTER, value)

    async def list_media(self):
        json_data = await self._getJSON(Command.GPCAMERA_MEDIA_LIST.url)
        return parsers.media_list(json_data)

    async def get_last_media(self):
        content = await self.list_media()
        v = content[-1]  # last file
        return v.path

    async def is_recording(self):
        value = await self.getStatus(Status.System.system_busy)
        print('is_recording=', value)
        return value == 1

    async def dowload_media(self, path, destination=None):
        if await self.is_recording():
            raise CameraBusyError()
        url = f'http://{self._ip}:8080/videos/DCIM/{path}'
        return await self._client.download(url, destination)

    async def take_photo(self):
        """Helper for taking single photo
        Returns
        -------
        string
            directory/filename of the last captured
        """
        await self.mode(Mode.photo, SubMode.Photo.single)

        await self.shutter(1)
        await asyncio.sleep(1)
        busy = await self.is_recording()
        while busy:
            await asyncio.sleep(1)
            busy = await self.is_recording()

        return await self.get_last_media()
