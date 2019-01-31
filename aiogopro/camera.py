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
            self._camera = await self.get_info()

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

    async def set_setting(self, param, value):
        param = utils.get_value(param)
        value = utils.get_value(value)
        return await self._client.getText(
            'http://' + self._ip + '/gp/gpControl/setting/' + param + '/' + value, timeout=5
        )

    async def get_info(self):
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

    async def get_status(self, key=None):
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
        await self.get_info()
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

        await self.get_info()
        data = await self._getText(url, timeout=5, **kwargs)
        # fix badly formated json
        if data:
            data = json.loads(data.replace("\\", "/"))
        return data

    async def timeGet(self):
        dtm = await self.get_status(Status.Setup.date_time)
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
        print('shutter', value)
        if value == 1:
            return await self.command(Command.GPCAMERA_SHUTTER, value)
        if value == 0:
            result = await self.command(Command.GPCAMERA_SHUTTER, value)
            await self.ensureAvailable()
            return result

    async def list_media(self):
        json_data = await self._getJSON(Command.GPCAMERA_MEDIA_LIST.url)
        return parsers.media_list(json_data)

    async def get_last_media(self):
        content = await self.list_media()
        v = content[-1]  # last file
        return v.path

    async def is_busy(self):
        """Check if camera is busy
        Returns
        -------
        bool
            True if busy
        """
        value = await self.get_status(Status.System.system_busy)
        return value == 1

    async def ensureAvailable(self):
        busy = await self.is_busy()
        while busy:
            asyncio.sleep(1)
            busy = await self.is_busy()


    async def dowload_media(self, path, destination=None):
        if await self.is_busy():
            raise CameraBusyError()
        url = f'http://{self._ip}:8080/videos/DCIM/{path}'
        return await self._client.download(url, destination)

    async def download_all(self, destination=None):
        """Downloads all media to destination folder
        Parameters
        ----------
        destination : string, optional
            Folder in where to create files. Defaults to cwd.
            Will be created if missing.
        """
        if await self.is_busy():
            raise CameraBusyError()
        files = await self.list_media()
        media_stash = []
        tasks = []
        if destination and destination[-1] in ['/', '\\']:
            destination = destination[:-1]

        for fil in files:
            url = f'http://{self._ip}:8080/videos/DCIM/{fil.path}'
            newname = f'{fil.folder}-{fil.name}'
            newpath = f'{destination or "."}/{newname}'
            media_stash.append(newpath)
            tasks.append(self._client.download(url, f'{fil.folder}-{fil.name}', working_path=destination))
        await asyncio.gather(*tasks)
        return media_stash

    async def capture(self, seconds=0):
        """Helper for capturing
        You have to set proper mode first

        Parameters
        ----------
        seconds: int
            Seconds after which shutter will be set to 0. (default 0 = disabled)

        Returns
        -------
        string
            folder/filename of the last captured
        """
        if await self.is_busy():
            raise CameraBusyError()

        await self.shutter(1)
        if seconds > 0:
            await asyncio.sleep(seconds)
            return await self.shutter(0)

        await asyncio.sleep(1)
        await self.ensureAvailable()  # wait until camera is available
        return await self.get_last_media()

    async def take_photo(self, resetafter=0):
        """Helper for taking single photo

        Parameters
        ----------
        resetafter: int
            Seconds after which shutter will be set to 0. (default 0 = disabled)

        Returns
        -------
        string
            folder/filename of the last captured
        """
        if await self.is_busy():
            raise CameraBusyError()

        await self.mode(Mode.photo, SubMode.Photo.single)
        return self.capture(resetafter)

    async def delete(self, option):
        if isinstance(option, int):
            # This allows you to delete x number of files backwards.
            # Will delete a timelapse/burst entirely as its interpreted as a single file.
            tasks = []
            for _ in range(option):
                tasks.append(self.command(Command.GPCAMERA_DELETE_LAST_FILE_ID))
            return await asyncio.gather(tasks)
        elif isinstance(option, str):
            if option == 'all':
                return await self.command(Command.GPCAMERA_DELETE_ALL_FILES_ID)
            raise ValueError('Option did not contain a permitted value')
        else:
            raise TypeError('Option is of wrong type')

    async def delete_file(self, folder, fil):
        return await self.command(Command.GPCAMERA_DELETE_FILE_ID, f'{folder}/{fil}')
