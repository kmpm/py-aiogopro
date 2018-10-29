import math


def bytes_to_human(value):
    """Generates a human readable value from bytes
    """
    if isinstance(value, str):
        value = float(value)
    size_bytes = value
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    size = round(size_bytes / p, 2)
    storage = "" + str(size) + str(size_name[i])
    return str(storage)


def parse_datetime(value):
    parts = value.split('%')
    year = int(parts[1], 16)
    month = int(parts[2], 16)
    day = int(parts[3], 16)
    hours = int(parts[4], 16)
    minutes = int(parts[5], 16)
    seconds = int(parts[6], 16)
    return "{0:02d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}".format(year, month, day, hours, minutes, seconds)
