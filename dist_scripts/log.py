import sys
import os
import logging
from logging.handlers import RotatingFileHandler
import app_wd

__done = False


def init():
    global __done

    if __done:
        return
    __done = True

    log_dir = os.path.join(app_wd.get(), "log")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "app.log")
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        handlers=[
            RotatingFileHandler(filename=log_file, mode="w", maxBytes=1024 * 1024, backupCount=50, encoding="UTF-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )
