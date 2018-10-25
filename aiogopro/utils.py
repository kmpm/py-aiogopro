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
