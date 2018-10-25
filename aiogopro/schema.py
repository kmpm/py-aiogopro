
class CommandType:
    def __init__(self, name, url, widget, display_name):
        self.name = name
        self.url = url
        self.widget = widget
        self.display_name = display_name


class ModeType:
    def __init__(self, name, value, display_name):
        self.name = name
        self.value = value
        self.display_name = display_name


class SchemaType:
    def __init__(self, schema_version, version):
        self.schema_version = schema_version
        self.version = version
        self.commands = {}
        self.modes = {}

    def addCommand(self, cmd):
        if 'wifi' not in cmd['network_types']:
            return

        key = cmd['key']
        self.commands[key] = CommandType(
            key,
            cmd['url'],
            cmd['widget_type'],
            cmd['display_name']
        )

    def addMode(self, mode):
        key = mode['path_segment']
        self.modes[key] = ModeType(key, mode['value'], mode['display_name'])


    @staticmethod
    def parse(data):
        parser = SchemaType(data['schema_version'], data['version'])
        for cmd in data['commands']:
            parser.addCommand(cmd)

        for mode in data['modes']:
            parser.addMode(mode)
        return parser


def command_compare(firsts, seconds, firstname='first', secondname='second'):
    for key, cmdA in firsts.items():
        if key in seconds:
            cmdB = seconds[key]
            if cmdA.url != cmdB.url:
                print("Same command {0} different url {1} != {2} ({3}/{4})".format(cmdA.url, cmdB.url, firstname, secondname))
        else:
            print('Only in {2}, Command {0}: {1}'.format(cmdA.name.ljust(47), cmdA.display_name, firstname))


def mode_compare(firsts, seconds, firstname='first', lastname='last'):
    for key, modeA in firsts.items():
        if key in seconds:
            modeB = seconds[key]
            if (modeA.value != modeB.value):
                print("Same mode {0} different value {1} != {2} ({3}/{4})".format(modeA.value, modeB.value, firstname, secondname))
        else:
            print('Only in {2}, Mode {0}: {1}'.format(modeA.name.ljust(20), modeA.display_name, firstname))


def schema_compare(first, second, firstname='first', secondname='second'):
    command_compare(first.commands, second.commands, firstname, secondname)
    command_compare(second.commands, first.commands, secondname, firstname)
    mode_compare(first.modes, second.modes, firstname, secondname)
    mode_compare(second.modes, first.modes, secondname, firstname)

