# Singleton template for using in Configuration and others classes
import sys

from config import logger


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def keyboard_to_regex(keyboard):
    res = ""
    for row in keyboard:
        for button in row:
            res += button + "|"
    return res[:-1]


def errmsg(msg, e=None, code=-1):
    logger.critical('Cricitical error at {}\n{}\n\n{}' % __name__ % msg % e)
    sys.exit(code)
