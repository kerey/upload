#!/usr/bin/env python

def test(argv):
    print(argv)
    return argv

if __name__ == '__main__':
    try:
        arg = sys.argv[1]
    except IndexError:
        arg = None

    return_val = test(arg)
