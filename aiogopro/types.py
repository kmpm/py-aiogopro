class CommandType(object):
    def __init__(self, name, url, widget, display_name):
        self.name = name
        self.url = url
        self.widget = widget
        self.display_name = display_name


class ModeType(object):
    def __init__(self, name, value, display_name):
        self.name = name
        self.value = value
        self.display_name = display_name


class StatusType(object):
    def __init__(self, name, id, **kwargs):
        self.name = name
        self.id = str(id)
        self.location = __name__
        if 'levels' in kwargs:
            self.levels = kwargs.pop('levels')

        if len(kwargs) > 0:
            raise TypeError('Unexpected kwargs: {0}'.format(kwargs.keys()))
