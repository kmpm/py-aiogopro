from utils import bytes_to_human


class MediaInfo:
    def __init__(self, folder, name, size):
        self.folder = folder
        self.name = name
        self.size = size

    @property
    def size_readable(self):
        return bytes_to_human(self.size)

    def __str__(self):
        return "<MediaInfo folder:{0}, name:{1}, size:{2}>".format(self.folder, self.name, self.size)


class Camera:
    def __init__(self):
        pass

    async def connect(self):
        pass

    async def getMode(self):
        pass