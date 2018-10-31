import asyncio
import json
import os
from os import path
from urllib.parse import urlsplit, unquote
import posixpath
import aiohttp

from aiogopro.errors import GoProConnectionError, GoProError, HttpError


class AsyncClient:
    def __init__(self, **kwargs):
        self._session = None
        self.semaphores = asyncio.Semaphore(kwargs.pop('semaphores', 2))
        self.chunk_size = kwargs.pop('chunk_size', 64 * 1024)

    def session(self):
        if not self._session:
            self._session = aiohttp.ClientSession()
        return self._session

    async def quit(self):
        if self.session:
            await self._session.close()
            self._session = None

    async def getText(self, url, timeout=30):
        try:
            async with self.semaphores:
                async with self.session().get(url, timeout=timeout) as resp:
                    message = await resp.text(encoding='utf-8')

                    if resp.status == 200:
                        return message
                if 'json' in resp.content_type:
                    message = json.loads(message.replace("\r\n", "").replace("\n", ""))
                    error = GoProError(url, resp.status, resp.reason, message)
                else:
                    error = HttpError(url, resp.status, resp.reason)
        except aiohttp.client_exceptions.ClientConnectorError as err:
            raise GoProConnectionError('Can not connect', err)

        raise error

    async def getJSON(self, url, timeout=30):
        async with self.semaphores:
            async with self.session().get(url, timeout=timeout) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    raise HttpError(url, resp.status, resp.reason)

    async def download(self, url, filename=None):
        async with self.semaphores:
            if not filename:
                filename = url2filename(url)

            if self.working_path:
                filename = path.join(self.working_path, filename)

            async with self.session().get(url) as resp:
                with open(filename, 'wb') as fd:
                    while True:
                        chunk = await resp.content.read(self.chunk_size)
                        if not chunk:
                            break
                        fd.write(chunk)


def url2filename(url):
    """Return basename corresponding to url.
    >>> print(url2filename('http://example.com/path/to/file%C3%80?opt=1'))
    fileÀ
    >>> print(url2filename('http://example.com/slash%2fname')) # '/' in name
    Traceback (most recent call last):
    ...
    ValueError
    """
    urlpath = urlsplit(url).path
    basename = posixpath.basename(unquote(urlpath))
    if (
        os.path.basename(basename) != basename or
        unquote(posixpath.basename(urlpath)) != basename
    ):
        raise ValueError  # reject '%2f' or 'dir%5Cbasename.ext' on Windows
    return basename
