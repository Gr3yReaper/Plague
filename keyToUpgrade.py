def key_conversion(key):
    if key == 0 or key == 1 or key == 2:
        return key
    elif key == 'r':
        return 3
    elif key == 'n':
        return 7
    elif key == 'a':
        return 11
    elif key == 3 or key == 4 or key == 5 or key == 6 or key == 7 or key == 8:
        return key + 11
    elif key == 'p':
        return 20
    elif key == 9:
        return 22
    elif key == 'z':
        return 23
    elif key == 'x':
        return 24
    elif key == 'c':
        return 25
    elif key == 'v':
        return 26
    elif key == 'b':
        return 27
    elif key == 'm':
        return 28
    elif key == 's':
        return 29
    elif key == 'd':
        return 30
    elif key == 'f':
        return 31
    elif key == 'g':
        return 32
    elif key == 'h':
        return 33
    elif key == 'q':
        return 34
