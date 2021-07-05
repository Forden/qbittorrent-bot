import math


def byte_to_human_read(byte):
    if byte == 0:
        return '0 B'
    byte = int(byte)
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    index = int(math.floor(math.log(byte, 1024)))
    power = math.pow(1024, index)
    size = round(byte / power, 2)
    return "{} {}".format(size, size_name[index])
