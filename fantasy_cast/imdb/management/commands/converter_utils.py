def convert_boolean(i):
    return True if i == '1' else False


def convert_int(i):
    return int(i) if i != '\\N' else None
