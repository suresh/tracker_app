import sys
import casparser
from datetime import datetime

from PyQt6.uic import loadUi
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt

# from MainWindow import Ui_MainWindow


class FoliosModel(QtCore.QAbstractTableModel):
    def __init__(self, folios=None):
        super().__init__()
        self.cols = ["folio", "amc", "PAN", "KYC", "PANKYC", "schemes"]
        self.folios = folios or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # return self.folios[index.row()][index.column()]
            # for rowIndex, record in enumerate(self.folios):
            #     print(f'index: {index.row()} -> {record.keys()}')
            #     folio = QTableWidgetItem(record["folio"])
            #     amc = QTableWidgetItem(record["amc"])
            col = self.cols[index.column()]
            value = self.folios[index.row()][col]

            if col == "schemes":
                amt = 0
                for i in range(len(value)):
                    a = value[i]["valuation"]["value"]
                    amt = amt + a
                return f"Rs {amt:10.2f}"

            # Perform per-type checks and render accordingly.
            if isinstance(value, datetime):
                # Render time to YYY-MM-DD.
                return value.strftime("%Y-%m-%d")
            if isinstance(value, float):
                # Render float to 2 dp
                return f"{value:10.2f}"
            if isinstance(value, str):
                # Render strings with quotes
                return '"%s"' % value

            # Default (anything not captured above: e.g. int)
            return value

    def rowCount(self, index):
        return len(self.folios)

    def columnCount(self, index):
        return len(self.folios[0])

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self.cols[section])


# Ui_MainWindow
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setupUi(self)
        loadUi("mainwindow.ui", self)
        json_str = casparser.read_cas_pdf(
            "data/march2021-portfolio.pdf", "3454p3", output="dict"
        )
        self.model = FoliosModel(folios=json_str["folios"])
        self.foliosView.setModel(self.model)
        self.dateLabel.setText(json_str["statement_period"]["to"])


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
