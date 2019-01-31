from .utils import bytes_to_human, intif


class MediaEntry(object):
    def __init__(self, folder, name, **kwargs):
        self.folder = folder
        self.name = name
        self.created = intif(kwargs.pop('created', kwargs.pop('cre', 0)))
        self.modified = intif(kwargs.pop('modified', kwargs.pop('mod', 0)))
        self.size = intif(kwargs.pop('size', kwargs.pop('s', 0)))
        self.group = kwargs.pop('g', None)

    @property
    def path(self):
        return f'{self.folder}/{self.name}'

    @property
    def size_readable(self):
        return bytes_to_human(self.size)

    def __repr__(self):
        return f'<MediaEntry path:{self.path}, size:{self.size_readable}>'


class CommandType(object):
    def __init__(self, name, url, widget, display_name):
        self.name = name
        self.url = url
        self.widget = widget
        self.display_name = display_name


# class ModeType(object):
#     def __init__(self, name, value, display_name, **kwargs):
#         self.name = name
#         self.value = value
#         self.display_name = display_name

#         # self.sub_modes = kwargs.pop('sub_modes', None)
#         # if self.sub_modes:
#         #     if not isinstance(self.sub_modes, list):
#         #         raise AttributeError('sub_modes must be a list of ModeType')
#         #     for v in self.sub_modes:
#         #         if not isinstance(v, ModeType):
#         #             raise AttributeError('every item sub_modes must be a ModeType')

#     def __str__(self):
#         return f"ModeType('{self.name}', '{self.value}', '{self.display_name}')"


class StatusType(object):
    def __init__(self, name, id, **kwargs):
        self.name = name
        self.id = str(id)
        self.location = __name__
        if 'levels' in kwargs:
            self.levels = kwargs.pop('levels')

        if len(kwargs) > 0:
            raise TypeError('Unexpected kwargs: {0}'.format(kwargs.keys()))


class CameraInfo:
    def __init__(self, camera_type, info, **kwargs):
        self.camera_type = camera_type
        # firmware_version is not optional
        self.firmware_version = info.get('firmware_version')

        for key in info:
            setattr(self, key, info[key])
        # for key, value in kwargs.items():
        #     setattr(self, key, value)

    # def __str__(self):
    #     return "{0}".format(self.firmware_version)

    def __repr__(self):
        return f"<CameraInfo type:{self.camera_type}, firmware:{self.firmware_version}>"
