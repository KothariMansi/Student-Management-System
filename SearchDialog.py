from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUiType

from DatabaseManager import DatabaseManager

search_ui, _ = loadUiType("search.ui")

class SearchDialog(QMainWindow, search_ui):

    def __init__(self, parent=None, callback=None):
        super(SearchDialog, self).__init__(parent)
        self.setupUi(self)
        self.db = DatabaseManager(host="localhost", user="root", password="mansi_116", database="school")
        self.loadData()
        self.tbSearch.textChanged.connect(self.filterData)
        self.tableWidget.clicked.connect(self.refocusTbSearch)
        self.callback = callback

    def loadData(self):
        rows = self.db.fetch_query("select id, registration_number, full_name, standard from student;")
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(len(rows[0])  if rows else 0)
        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setHorizontalHeaderLabels(["Id","Registration Number", "Name", "Standard"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.hideColumn(0)  # Hides the first column (id)
        if self.tableWidget.rowCount() > 0:
            self.tableWidget.selectRow(0)

    def filterData(self):
        rows = self.db.fetch_query("select id, registration_number, full_name, standard from student where full_name like %s", (f"%{self.tbSearch.text()}%",))
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(len(rows[0]) if rows else 0)
        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setHorizontalHeaderLabels(["Id", "Registration Number", "Name", "Standard"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.hideColumn(0)
        if self.tableWidget.rowCount() > 0:
            self.tableWidget.selectRow(0)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Up:
            if self.tableWidget.currentRow() > 0:
                self.tableWidget.selectRow(self.tableWidget.currentRow() - 1)
        if e.key() == Qt.Key_Down:
            if self.tableWidget.currentRow() < self.tableWidget.rowCount() - 1:
                self.tableWidget.selectRow(self.tableWidget.currentRow() + 1)
        if e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            selected_Value = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            if self.callback:
                try:
                    self.callback(selected_Value)
                    print(f"Callback invoked with value: {selected_Value}")
                except Exception as ex:
                    print(f"Error invoking callback: {ex}")
            self.close()

    def refocusTbSearch(self):
        self.tbSearch.setFocus()