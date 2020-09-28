import sys
import pandas as pd
import sqlite3
import random
from datetime import datetime, date
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QPushButton, QItemDelegate, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE TABLE testtable (
            [timestamp] timestamp,
            type TEXT,
            value INTEGER)
            """)

def insert_value():
    with conn:
        c.execute("INSERT INTO testtable VALUES (:timestamp, :type, :value)",
                {'timestamp': datetime.now(), 'type': 'random', 'value': random.random()})

def getTable():
    c.execute("SELECT * FROM testtable")
    return c.fetchall()

def run(num):
    for i in range(1,num):
        insert_value()



class TableWidget(QTableWidget):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.setStyleSheet('font-size: 35px;')

        nRows, nColumns = self.df.shape
        self.setColumnCount(nColumns)
        self.setRowCount(nRows)

        self.setHorizontalHeaderLabels(('Col X', 'Col y'))
        self.verticalHeader().setSectionResizeMode((QHeaderView.Stretch))
        self.horizontalHeader().setSectionResizeMode((QHeaderView.Stretch))

        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))

class DFEditor(QWidget):
    data = {
        'col x': list('ABCD'),
        'col y': [10, 20, 30, 40]
    }

    df = pd.DataFrame(data)

    def __init(self):
        super().__init__()
        self.resize(1200, 800)

        mainLayout = QVBoxLayout()

        self.table = TableWidget(DFEditor.df)
        mainLayout.addWidget(self.table)

        button_print = QPushButton('Display DF')
        button_print.setStyleSheet('font-size: 30px')
        mainLayout.addWidget(button_print)
        button_print.clicked.connect(self.print_DF_Values)

        button_export = QPushButton('export to CSV')
        button_export.setStyleSheet('font-size: 30px')
        mainLayout.addWidget(button_export)
        button_export.clicked.connect(self.export_to_csv)

        self.setLayout(mainLayout)

    def print_DF_Values(self):
        print(self.table.df)

    def export_to_csv(self):
        self.table.df.to_csv('Data_export.csv', index=False)
        print('CSV file exported.')

if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = DFEditor()
    demo.show()
    run(8)
    viewTable = getTable()
    print(viewTable)

    sys.exit(app.exec_())

