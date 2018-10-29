from aiogopro.utils import bytes_to_human


class CameraInfo:
    def __init__(self, camera_type, info, **kwargs):
        self.camera_type = camera_type
        # firmware_version is not optional
        self.firmware_version = info.get('firmware_version')

        for key in info:
            setattr(self, key, info[key])
        # for key, value in kwargs.items():
        #     setattr(self, key, value)

    def __str__(self):
        msg = "{0}".format(self.firmware_version)

        return msg


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
