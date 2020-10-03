#!/usr/bin/env python

import math
import time
import timeit
import random
import sys
import os
import pickle
import socket
import traceback
import sqlite3
from datetime import datetime, date

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
style.use('fivethirtyeight')

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
# import RPi.GPIO as GPIO #import I/O interface             #
# from hx711 import HX711 #import HX711 class               #

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QPoint, QRect, QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThreadPool, QRunnable, QThread
from PyQt5.QtWidgets import (QSizePolicy,
        QWidget, QFrame, QRadioButton)
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLayout, 
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QStatusBar, QTabWidget, QLCDNumber, QTableWidget, QTableWidgetItem, QTableView, QMainWindow, QMessageBox)

# import RPi.GPIO as GPIO #import I/O interface             #
# from hx711 import HX711 #import HX711 class               #

from GUI import Ui_MainWindow
from workerThreading import WorkerSignals, Worker

class sqlDatabase:
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        self.data = []
        self.plotter = None
        self.c.execute("""CREATE TABLE testtable (
            [timestamp] timestamp,
            type TEXT,
            value INTEGER)
            """)
        self.plots = {
            'force': 0,
            'pressure': 0,
            'weight': 0,
            'default': 0
        }

    def insert_value(self,valType,val):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        with self.conn:
            self.c.execute("INSERT INTO testtable VALUES (:timestamp, :type, :value)",
                    {'timestamp': current_time, 'type': valType, 'value': float(val)})

    def clearTable(self):
        print('deleting')
        self.c.execute('DELETE FROM testtable')
        self.data = []
        self.plotter.clear()

    def getTable(self,name='default',order='0'):
        self.c.execute("SELECT * FROM testtable")
        # print(self.c.fetchall())
        self.graph_data(name,order)
        return self.c.fetchall()

    def graph_data(self,name='default',order='0'):
        self.plots[name] = order
        for key, value in self.plots.items():
            if value == 1:
                self.c.execute('SELECT timestamp, value FROM testtable WHERE type = :type', {'type': key})
                self.data.extend(self.c.fetchall())
        self.data.sort()
        print(self.plots)
        if self.data:
            times = []
            vals = []
            if 1 == 1:
                for row in self.data:
                    print(row)
                    d = float(row[0].replace(":",""))
                    times.append(d)
                    vals.append(float(row[1]))
        else:
            times = []
            vals = []

        mainWin.graphWidget.setBackground('#fff')
        pen = pg.mkPen(color=(255,100,100), width=8)
        self.plotter = mainWin.graphWidget.plot(times,vals,pen=pen)
        # plt.plot_date(times,vals,'-')
        # plt.show()

class WorkerThread(QThread):
    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)

    def run(self):
        time.sleep(3)
        self.emit(SIGNAL('threadDone()'))

class newCalibrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calibration')
        self.resize(500,300)
        self.state = 0
        self.setLayout(QFormLayout())
        self.cal_buttons = QWidget()
        self.cal_buttons.setLayout(QHBoxLayout())
        self._initialized = 0
        self.WorkerThread = WorkerThread()
        self.connect(self.WorkerThread, SIGNAL("threadDone()"), self.threadDone, Qt.DirectConnection)

        self.startWindow()
        
    def startWindow(self):
        self.dialog = QLabel('Calibration requires an object of known weight to be placed on the scale')
        self.next_button = QPushButton('Next')
        self.cancel_button = QPushButton('Cancel')
        self.submit_button = QPushButton('Submit')
        self.layout().addRow(self.dialog)
        self.cal_buttons.layout().addWidget(self.cancel_button)
        self.cal_buttons.layout().addWidget(self.next_button)
        self.layout().addRow('', self.cal_buttons)

        # self.next_button.clicked.connect(self.getInputWindow)
        # self.next_button.clicked.connect(self.startCalibration)
        # self.next_button.clicked.connect(self.collectingDataWindow)
        self.next_button.clicked.connect(self.startCalibration)
        self.cancel_button.clicked.connect(self.close)

    def startCalibration(self):
        # i = self.initialized()
        # i = 0
        self.working = 1
        #start calibration
        for i in reversed(range(self.layout().count())):        #Clears components from first window
            self.layout().itemAt(i).widget().deleteLater()
        
        self.dialogText = QLabel('Do not touch scale. Initializing')
        self.layout().addRow('',self.dialogText)
        self.show()

        self.WorkerThread.start()
        self.dialogText.setText('starting')
        
        #fn to perform calibration
        # Ui_MainWindow.setWorker(mainWin, self.calibration_fake)
        # worker.signals.result.connect(self.print_output)
        # worker.signals.finished.connect(self.thread_complete)
        # worker.signals.progress.connect(self.progress_fn)

        # if self.working == 1:
        #     print(1)
        # else:
        #     print('alksdjhfalksjdfhakljh')
                
        # self.dialog = QLabel('wordssss')
        # self.dialogText = QLabel('Place object of known weight on scale and enter weight [g]: ')
        # self.inputWeight = QLineEdit()
        # self.layout().addRow('',self.dialogText)
        # self.layout().addRow('',self.inputWeight)


        # if self.initialized == 1:
        #     self.getInputWindow()

    def threadDone(self):
        self.dialogText.setText('finished')

    def getInputWindow(self):
        self.close()
        # self.knownGrams = 0
        # for i in reversed(range(self.layout().count())):        #Clears components from first window
        #     self.layout().itemAt(i).widget().deleteLater()
        # self.dialogText = QLabel('Place object of known weight on scale and enter weight [g]: ')
        # self.dialog = QLabel('wordssss')
        # # self.cancel_button = QPushButton('Cancel')
        # # self.submit_button = QPushButton('Submit')
        # self.inputWeight = QLineEdit()
        # # buttons = QWidget()
        # # buttons.setLayout(QHBoxLayout())
        # # buttons.layout().addWidget(self.cancel_button)
        # # buttons.layout().addWidget(self.submit_button)
        # self.layout().addRow('',self.dialogText)
        # self.layout().addRow('',self.inputWeight)
        # self.layout().addRow('',buttons)
        # self.layout().resize(300,200)
        self.show()


        # self.inputWeight.textChanged.connect(self.setKnownGrams)
        # self.submit_button.clicked.connect(self.sendKnownInput)
        # self.cancel_button.clicked.connect(self.close)

    def setKnownGrams(self,lineEdit):
        self.knownGrams = self.inputWeight.text()

    def getUserInput(self):
        print('user input started')

    def calibration_fake(self, *args, **kwargs):
        print('Initializing...')
        time.sleep(3)
        self.working = 0
        print(self.working)
        time.sleep(1)
        result = 'complete'
        return self.working

class calibrationWarning(QWidget):
    def __init__(self):
        super().__init__()
        self.ok_button = QPushButton('Ok')
        self.cal_button = QPushButton('Calibrate')
        self.dialog = QLabel("Load cell is not calibrated. Please calibrate.")
        self.setWindowTitle('Warning')

        self.setLayout(QFormLayout())
        self.layout().addRow(self.dialog)
        buttons = QWidget()
        buttons.setLayout(QHBoxLayout())
        buttons.layout().addWidget(self.ok_button)
        # buttons.layout().addWidget(self.cal_button)
        self.layout().addRow('', buttons)

        #Routes front end to back end
        self.ok_button.clicked.connect(self.close)
        self.ok_button.clicked.connect(self.close)
        # self.cal_button.clicked.connect(Ui_MainWindow.Calibration)

#Class handling calibration pop up boxes
class calibrationDialogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300,200)
        self.cancel_button = QPushButton('Cancel')
        self.next_button = QPushButton('Next')
        self.submit_button = QPushButton('Submit')
        self.finish_button = QPushButton('Finish')
        self.dialogText = QLabel('\n\n Calibration requires an object of known weight to be placed on the scale')
        self.warningText = QLabel('\n\nWarning: Continuing will pause the program')
        self.setWindowTitle('Calibration')

        #Initializes layout
        self.setLayout(QFormLayout())
        self.layout().addRow(self.dialogText)
        buttons = QWidget()
        buttons.setLayout(QHBoxLayout())
        buttons.layout().addWidget(self.cancel_button)
        buttons.layout().addWidget(self.next_button)
        self.layout().addRow('', buttons)
        self.layout().addRow('',self.warningText)

        #Routes front end to back end

        self.next_button.clicked.connect(self.getInputWindow)
        self.next_button.clicked.connect(self.startCalibration)
        self.next_button.clicked.connect(self.collectingDataWindow)
        self.cancel_button.clicked.connect(self.close)

    def collectingDataWindow(self):
        self.close()
        self.setWindowTitle('Calibration 3')
        for i in reversed(range(self.layout().count())):        #Clears components from first window
            self.layout().itemAt(i).widget().deleteLater()
        self.dialogText = QLabel('Initializing...')
        self.layout().addRow('',self.dialogText)
        self.show()
        self.close()

    #Second window in calibration branch
    def getInputWindow(self):
        self.close()
        self.setWindowTitle('Calibration 2')
        self.knownGrams = 0
        for i in reversed(range(self.layout().count())):        #Clears components from first window
            self.layout().itemAt(i).widget().deleteLater()
        self.dialogText = QLabel('Place object of known weight on scale and enter weight [g]: ')
        self.inputWeight = QLineEdit()
        buttons = QWidget()
        buttons.setLayout(QHBoxLayout())
        buttons.layout().addWidget(self.cancel_button)
        buttons.layout().addWidget(self.submit_button)
        self.layout().addRow('',self.dialogText)
        self.layout().addRow('',self.inputWeight)
        self.layout().addRow('',buttons)
        # self.layout().resize(300,200)
        self.show()

        self.inputWeight.textChanged.connect(self.setKnownGrams)
        self.submit_button.clicked.connect(self.sendKnownInput)
        self.cancel_button.clicked.connect(self.close)

    def setKnownGrams(self,lineEdit):
        self.knownGrams = self.inputWeight.text()

    def startCalibration(self):
        print("calibration started")
        cellInstance.userCalibrationPart1()

    #Sends known weight from user to Load cell calibration
    def sendKnownInput(self):
        self.close()
        self.setWindowTitle('Calibration 3')
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().deleteLater()
        print(f'user inputted value: {self.knownGrams}')
        # while LoadCell.calibrated == 0:
        #     self.dialogText = QLabel('Calibrating...')
        self.dialogText = QLabel('Calibrating')
        buttons = QWidget()
        buttons.setLayout(QHBoxLayout())
        buttons.layout().addWidget(self.finish_button)
        self.layout().addRow('',self.dialogText)
        self.layout().addRow('',buttons)
        self.show()

        cellInstance.userCalibrationPart2(self.knownGrams)

        while cellInstance.initializing == 1:
            self.dialogText = QLabel('Calibrating.')
            time.sleep(1)
            self.dialogText = QLabel('Calibrating..')
            time.sleep(1)
            self.dialogText = QLabel('Calibrating...')

        self.finish_button.clicked.connect(self.close)

class FakeLoadCell():
    def __init__(self):
        self.recorded_configFile_name = 'calibration.vlabs'
        
        if os.path.isfile(self.recorded_configFile_name):
            with open(self.recorded_configFile_name,'rb') as File:
                self.cell = pickle.load(File)
                self.calibrated = 1
        else:
            self.calibrated = 0
        self.reading = 0
        self.initializing = 0

    def userCalibrationPart1(self):

        self.initializing = 1

        print('getting initial data...')
        # self.reading = self.cell.get_raw_data_mean()
        time.sleep(3)

        self.initializing = 0

    def userCalibrationPart2(self,knownGrams):
        self.initializing = 1

        if knownGrams:
            known_weight_grams = knownGrams
            try:
                value = float(known_weight_grams)
                print(value, 'grams')
            except ValueError:
                print('Expected integer or float and I have got:',
                      known_weight_grams)

        print('calibrating...')
        time.sleep(3)

        self.calibrated = 1
        
        self.initializing = 0

        print("done calibrating")

class LoadCell():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  #set GPIO pind mode to BCM
        self.pd_sckPin=20
        self.dout_pin=21
        self.recorded_configFile_name = 'calibration.vlabs'
        self.cell = HX711(self.dout_pin,self.pd_sckPin)
        if os.path.isfile(self.recorded_configFile_name):
            with open(self.recorded_configFile_name,'rb') as File:
                self.cell = pickle.load(File)   #loading calibrated HX711 object
                self.calibrated = 1
        else:
            self.calibrated = 0
        self.reading = 0
        self.initializing = 0
 
    def userCalibrationPart1(self):
        self.cell = HX711(self.dout_pin,self.pd_sckPin)
        #send the user calibration message
        err = self.cell.zero()
        if err:
            raise ValueError('Tare is unsuccessful.')
        self.initializing = 1
        self.reading = self.cell.get_raw_data_mean()
        self.initializing = 0
        print(f'raw_data_mean: {self.reading}, predicted ratio = {self.reading/198}')

    def userCalibrationPart2(self,knownGrams):
        self.initializing = 1
        self.reading = self.cell.get_data_mean()
        fileName = 'calibration.vlabs'
        print(f'get_data_mean: {self.reading}, predicted ratio = {self.reading/198}')

        if self.reading:
            known_weight_grams = knownGrams
            try:
                value = float(known_weight_grams)
                print(value, 'grams')
            except ValueError:
                print('Expected integer or float and I have got:',
                      known_weight_grams)

            ratio = self.reading / value  # calculate the ratio for channel A and gain 128
            print(ratio)
            self.cell.set_scale_ratio(ratio)  # set ratio for current channel
            print('Ratio is set.')
        else:
            raise ValueError(
                'Cannot calculate mean value. Try debug mode. Variable reading:',
                self.reading)
                    
        print('Saving the HX711 state to swap file on persistant memory')
        with open(fileName, 'wb') as File:
            pickle.dump(self.cell, File)
            File.flush()
            os.fsync(File.fileno())
            # you have to flush, fsynch and close the file all the time.
            # This will write the file to the drive. It is slow but safe.

        if os.path.isfile(self.recorded_configFile_name):
            with open(self.recorded_configFile_name,'rb') as File:
                self.cell = pickle.load(File)   #loading calibrated HX711 object
                self.calibrated = 1
        
        self.initializing = 0

        print("tare is succesful")

                
if __name__ == '__main__':
    # cellInstance = LoadCell()
    cellInstance = FakeLoadCell()
    DB = sqlDatabase()
    app = QApplication(sys.argv)
    mainWin = Ui_MainWindow(DB)
    styleFile=os.path.join(os.path.split(__file__)[0],"vulcan.stylesheet")
    styleSheetStr = open(styleFile,"r").read()
    mainWin.setStyleSheet(styleSheetStr) 
    mainWin.show()

    fps = 3
    timer = QtCore.QTimer()
    timer.timeout.connect(mainWin.UpdateGUI)
    timer.setInterval(int(1000/fps))
    timer.start()

    sys.exit(app.exec_())

