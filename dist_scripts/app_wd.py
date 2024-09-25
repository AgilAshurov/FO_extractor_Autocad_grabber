import sys
import os

__done = False
__app_wd = None


def get():
    return __app_wd


def __init():
    global __done, __app_wd

    if __done:
        return
    __done = True

    __app_wd = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))


__init()
