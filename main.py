import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import uic
import pandas as pd
import sqlite3

con = sqlite3.connect("coffee.sqlite")
cur = con.cursor()


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        a = [str(i + 1) for i in range(len(cur.execute("""SELECT * FROM fer""").fetchall()))]
        data = pd.DataFrame([
            list(i) for i in cur.execute("""SELECT * FROM fer""").fetchall()
        ], columns=['ID', 'сорт', 'обжарка', 'молотый/зерна', 'вкус', 'цена', 'объем'],
            index=a)

        self.model = TableModel(data)
        self.tableView.setModel(self.model)

        self.setCentralWidget(self.tableView)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
