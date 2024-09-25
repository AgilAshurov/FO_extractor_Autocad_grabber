from PySide6.QtWidgets import QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt


class Cell:
    def __init__(self, name, label=None, precision=None):
        self.name = name
        self.label = label or name
        self.precision = precision


def create_table(table, cells):
    table.setRowCount(0)
    table.setColumnCount(len(cells))
    table.setHorizontalHeaderLabels([cell.label for cell in cells])
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


def insert_items(table, cells, items):
    table.setRowCount(0)
    for row, item in enumerate(items):
        table.insertRow(row)
        for col, cell in enumerate(cells):
            value = item.get(cell.name)
            if isinstance(value, tuple):
                value = value[0]
            if isinstance(value, float) and cell.precision is not None:
                value = f"{value:.{cell.precision}f}"
            widget = QTableWidgetItem(str(value if value is not None else ""))
            widget.setFlags(widget.flags() ^ Qt.ItemIsEditable)
            if not col:
                widget.setData(Qt.UserRole, row)
            table.setItem(row, col, widget)
    table.resizeColumnsToContents()
