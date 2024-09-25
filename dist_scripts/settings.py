import os
import json
from PySide6.QtCore import QDir

__settings = {}


def load():
    global __settings
    try:
        with open(os.path.join(QDir.homePath(), ".fo-extractor-settings.json"), "rb") as f:
            __settings = json.loads(f.read().decode("UTF-8"))
    except:
        __settings = {}
    __settings.setdefault("language", "en")
    __settings.setdefault("utm_zone", 39)


def update(data):
    with open(os.path.join(QDir.homePath(), ".fo-extractor-settings.json"), "wb") as f:
        __settings.update(data)
        f.write(json.dumps(__settings).encode("UTF-8"))


def get(key):
    return __settings.get(key)
