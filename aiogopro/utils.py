import math
import os
from datetime import datetime


def bytes_to_human(value):
    """Generates a human readable value from bytes
    Properties
    ----------
    value : int
        integer representing number of bytes
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
    year = 2000 + int(parts[1], 16)
    month = int(parts[2], 16)
    day = int(parts[3], 16)
    hours = int(parts[4], 16)
    minutes = int(parts[5], 16)
    seconds = int(parts[6], 16)
    return datetime(year, month, day, hours, minutes, seconds)


def generate_datetime(value=None):
    if not isinstance(value, datetime):
        value = datetime.now()
    extra = '%'
    if value.minute > 48:
        extra = ''
    return '%{0:02X}%{1:02X}%{2:02X}%{3:02X}%{4:02X}%{5:02X}'.format(
        int(str(value.year)[-2:]),
        value.month,
        value.day,
        value.hour,
        value.minute,
        value.second,
        extra
    ).lower()


def pad_sep(text):
    if text[-1] != os.path.sep:
        return text + os.path.sep
    return text


def strip_sep(text):
    if text[-1] in ['/', '\\']:
        return text[:-1]
    return text


def ensure_dir(file_path):
    file_path = pad_sep(file_path)
    folder = os.path.dirname(file_path)
    if not os.path.exists(folder):
        os.makedirs(folder)


def get_value(data):
    """Returns the value of an Enum or data
    """
    if hasattr(data, 'value'):
        return data.value
    return data


def intif(value):
    """Parse as int if string
    """
    try:
        return int(value, 10)
    except TypeError:
        return value
