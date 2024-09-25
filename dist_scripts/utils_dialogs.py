from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QPixmap


def danger(parent, title, text, buttons=QMessageBox.Ok):
    msg = QMessageBox(QMessageBox.NoIcon, title, text, buttons, parent)
    msg.setIconPixmap(QPixmap(":/icons/error.svg"))
    if parent is None:
        msg.setWindowIcon(QPixmap(":/app.png"))
    return msg.exec()
