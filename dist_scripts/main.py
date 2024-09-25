import os
import sys
from PySide6.QtWidgets import QApplication
import ctypes
from i18n import set_language
from main_window import MainWindow
import log
import settings
from time import time, strptime, mktime
import app_wd
from crypto_utils import ecc_signature_verify
import base64


def read_lic_data(fn, key):
    lic_data = {}
    try:
        with open(fn, "rb") as f:
            lines = f.read().decode("utf-8").strip().splitlines()
            for line in lines[:-1]:
                if line.startswith("LIC_"):
                    lic, value = line.split("=")
                    lic_data[lic] = value
            if not ecc_signature_verify(key, "\n".join(lines[:-1]).encode("utf-8"), base64.b64decode(lines[-1])):
                lic_data = {}
    except:
        lic_data = {}
    return lic_data


public_key = """-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEUaYvh9J0FjsbzeN36X4fIDdWNXrf
nYCsngtaI4Z54LAjwCERC3UPx83Iig/4agVcSXXRW4vb3q1GMJ05L1pgpA==
-----END PUBLIC KEY-----"""

lic_data = read_lic_data(os.path.join(app_wd.get(), "lic.txt"), public_key)
try:
    exp_date = mktime(strptime(lic_data["LIC_EXP_DATE"], "%Y-%m-%d"))
except:
    exp_date = None

if exp_date and time() < exp_date:
    log.init()
    settings.load()

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("fo.extractor")
    app = QApplication(sys.argv)

    set_language(settings.get("language"))

    main_window = MainWindow()
    main_window.show()

    os._exit(app.exec())
