# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
import app_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(643, 432)
        MainWindow.setWindowTitle(u"FO extractor")
        icon = QIcon()
        icon.addFile(u":/app.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.select = QPushButton(self.centralwidget)
        self.select.setObjectName(u"select")

        self.horizontalLayout.addWidget(self.select)

        self.select_and_sum = QPushButton(self.centralwidget)
        self.select_and_sum.setObjectName(u"select_and_sum")

        self.horizontalLayout.addWidget(self.select_and_sum)

        self.save = QPushButton(self.centralwidget)
        self.save.setObjectName(u"save")

        self.horizontalLayout.addWidget(self.save)

        self.progress_bar = QProgressBar(self.centralwidget)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(24)

        self.horizontalLayout.addWidget(self.progress_bar)

        self.utm_zone = QPushButton(self.centralwidget)
        self.utm_zone.setObjectName(u"utm_zone")

        self.horizontalLayout.addWidget(self.utm_zone)

        self.language = QPushButton(self.centralwidget)
        self.language.setObjectName(u"language")

        self.horizontalLayout.addWidget(self.language)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.table = QTableWidget(self.centralwidget)
        self.table.setObjectName(u"table")
        self.table.setMinimumSize(QSize(0, 150))
        self.table.setMaximumSize(QSize(16777215, 16777215))
        palette = QPalette()
        brush = QBrush(QColor(0, 120, 215, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.HighlightedText, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush)
        palette.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush)
        palette.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush1)
        self.table.setPalette(palette)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(True)

        self.verticalLayout_3.addWidget(self.table)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.select.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.select_and_sum.setText(QCoreApplication.translate("MainWindow", u"Select and sum", None))
        self.save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.utm_zone.setText(QCoreApplication.translate("MainWindow", u"UTM zone", None))
        self.language.setText(QCoreApplication.translate("MainWindow", u"Language", None))
        pass
    # retranslateUi

