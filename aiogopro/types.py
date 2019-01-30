
class MediaEntry(object):
    def __init__(self, directory, name, created, modified, size):
        self.directory = directory
        self.name = name
        self.created = created
        self.modified = modified
        self.size = size

    @property
    def path(self):
        return f'{self.directory}/{self.name}'


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
