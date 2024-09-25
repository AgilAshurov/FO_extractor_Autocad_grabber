from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QInputDialog, QApplication
from PySide6.QtCore import Signal, QFile, QIODevice, Qt
from main_window_ui import Ui_MainWindow
from selector import Cols, select, select_and_sum, write_blocks, zoom
from threading import Thread
from utils_dialogs import danger
from utils_widgets import Cell, create_table, insert_items
from i18n import set_language
import logging
from report import write_report
import os
import openpyxl
import io
import app_wd
import settings
from pyproj import Proj
from multiprocessing import Process, Queue
from queue import Empty


USE_MP = False
USE_ASSETS_FROM_RES = False


def target(q):
    def callback(processed, total):
        q.put({"type": "progress", "processed": processed, "total": total})
    q.put({"type": "result", "items": select(callback)})


class SelectProgressResult:
    __slots__ = ("processed", "total")

    def __init__(self, processed, total):
        self.processed = processed
        self.total = total


class SelectFinishResult:
    __slots__ = ("success", "details")

    def __init__(self, success, details):
        self.success = success
        self.details = details


class MainWindow(QMainWindow, Ui_MainWindow):
    select_progress_signal = Signal(SelectProgressResult)
    select_finish_signal = Signal(SelectFinishResult)

    LANGUAGES = [
        ("English", "en"),
        ("Русский", "ru"),
        ("Azərbaycan", "az")
    ]

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.select_progress_signal.connect(self.__select_progress)
        self.select_finish_signal.connect(self.__select_finish)

        self.progress_bar.setValue(0)

        self.select.clicked.connect(self.select_clicked)
        self.select_and_sum.clicked.connect(self.select_and_sum_clicked)
        self.save.clicked.connect(self.save_clicked)
        self.utm_zone.clicked.connect(self.zone_clicked)
        self.language.clicked.connect(self.language_clicked)

        self.TABLE_CELLS = [Cell(col_desc.name, precision=col_desc.value[1]) for col_desc in Cols]

        create_table(self.table, self.TABLE_CELLS)
        self.table.selectionModel().selectionChanged.connect(self.table_selection_changed)
        self.table_items = []

    def __enable(self, enable):
        self.select.setEnabled(enable)
        self.select_and_sum.setEnabled(enable)
        self.save.setEnabled(enable)
        self.utm_zone.setEnabled(enable)
        self.table.setEnabled(enable)

    def select_clicked(self):
        self.__enable(False)
        self.table.setRowCount(0)
        self.progress_bar.setValue(0)
        self.thread = Thread(target=self.__select)
        self.thread.start()

    def select_and_sum_clicked(self):
        self.__enable(False)
        self.table.setRowCount(0)
        self.progress_bar.setValue(0)
        self.thread = Thread(target=self.__select_and_sum)
        self.thread.start()

    def save_clicked(self):
        fn, ok = QFileDialog.getSaveFileName(self, filter="XLSX (*.xlsx)")
        if not ok:
            return
        if os.path.exists(fn):
            os.remove(fn)
        if USE_ASSETS_FROM_RES:
            f = QFile(":/report.xlsx")
            if not f.open(QIODevice.ReadOnly):
                return
            content = f.readAll()
            f.close()
        else:
            with open(os.path.join(app_wd.get(), "report.xlsx"), "rb") as f:
                content = f.read()
        wb = openpyxl.load_workbook(io.BytesIO(content))
        wb.create_sheet("BLOCKS")
        write_blocks(wb, self.table_items)
        write_report(wb, self.table_items)
        wb.save(fn)
        wb.close()

    def zone_clicked(self):
        utm_zone, ok = QInputDialog().getInt(self, self.tr("Change"), self.tr("UTM zone"), settings.get("utm_zone"))
        if not ok:
            return
        settings.update({"utm_zone": utm_zone})

        proj = Proj(proj="utm", zone=utm_zone, ellps="WGS84", preserve_units=False)
        for item in self.table_items:
            lon, lat = proj(item["X"], item["Y"], inverse=True)
            item["LAT"] = lat
            item["LON"] = lon
        insert_items(self.table, self.TABLE_CELLS, self.table_items)

    def language_clicked(self):
        language_names = []
        current_language_id = settings.get("language")
        current_language_index = 0
        for i, (language_name, language_id) in enumerate(self.LANGUAGES):
            language_names.append(language_name)
            if language_id == current_language_id:
                current_language_index = i
        language_name, ok = QInputDialog().getItem(self, self.tr("Change"), self.tr("Language"), language_names, current_language_index, editable=False)
        if not ok:
            return
        _, language_id = next(filter(lambda language: language[0] == language_name, self.LANGUAGES))
        set_language(language_id)
        self.retranslateUi(self)

    def __select(self):
        try:
            if USE_MP:
                q = Queue()
                p = Process(target=target, args=(q,))
                p.start()
                while p.is_alive():
                    try:
                        data = q.get(timeout=0.5)
                        if data["type"] == "progress":
                            self.select_progress_signal.emit(SelectProgressResult(data["processed"], data["total"]))
                        elif data["type"] == "result":
                            self.select_finish_signal.emit(SelectFinishResult(True, data["items"]))
                            break
                    except Empty:
                        pass
                p.join()
                if p.exitcode:
                    raise RuntimeError(f"exitcode = {p.exitcode}")
            else:
                def callback(processed, total):
                    self.select_progress_signal.emit(SelectProgressResult(processed, total))
                self.select_finish_signal.emit(SelectFinishResult(True, {"f": "select", "data": select(callback, settings.get("utm_zone"))}))
        except Exception as e:
            logging.warning(f"select error: {e}")
            self.select_finish_signal.emit(SelectFinishResult(False, self.tr("Can not get the selected objects")))

    def __select_and_sum(self):
        try:
            def callback(processed, total):
                self.select_progress_signal.emit(SelectProgressResult(processed, total))
            self.select_finish_signal.emit(SelectFinishResult(True, {"f": "select_and_sum", "data": select_and_sum(callback)}))
        except Exception as e:
            logging.warning(f"select error: {e}")
            self.select_finish_signal.emit(SelectFinishResult(False, self.tr("Can not get the selected objects")))

    def __select_progress(self, result):
        self.progress_bar.setValue(result.processed / result.total * 100 if result.total > 0 else 0)

    def __select_finish(self, result):
        if result.success:
            if result.details["f"] == "select":
                self.table_items = result.details["data"]
                insert_items(self.table, self.TABLE_CELLS, self.table_items)
                QMessageBox.information(self, self.tr("Info"), self.tr("Success."))
            else:
                clipboard = QApplication.clipboard()
                clipboard.setText("\n".join(str(x) for x in result.details['data']))
                QMessageBox.information(self, self.tr("Info"), self.tr("Sum") + " " f"{sum(result.details['data'])}" + "\n" + self.tr("Details copied to clipboard"))
        else:
            danger(self, self.tr("Error"), result.details)
        self.__enable(True)

    def table_selection_changed(self, selected, deselected):
        selected = selected.indexes()
        deselected = deselected.indexes()
        if not selected or (selected and deselected and selected[0].row() == deselected[0].row()):
            return
        index = self.table.model().index(selected[0].row(), 0)
        zoom(self.table_items[index.data(Qt.UserRole)]["HANDLE"])
