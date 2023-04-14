def key_conversion(key):
    if key == 0 or key == 1 or key == 2:
        return key
    elif key == 'r':
        return 3
    elif key == 'n':
        return 7
    elif key == 'a':
        return 11
    elif key == 3 or key == 4:
        return key + 11
