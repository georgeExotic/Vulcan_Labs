import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QPushButton, QItemDelegate, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator

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

        #data insertion
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i,j,QTableWidgetItem(str(self.df.iloc[i, j])))

class DFEditor(QWidget):
    data = {
        'col x': list('ABCD'),
        'col Y': [10, 20, 30, 40]
    }

    df = pd.DataFrame(data)

    def __init__(self):
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

    sys.exit(app.exec_())