import sys
import types
import time
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QMainWindow, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThreadPool, QRunnable, QThread, pyqtSignal, pyqtSlot, QMutex
from PyQt5.QtGui import QCursor

from ui_main import ui_main

from threadClasses import WorkerSignals, Worker
from LoadCell import LoadCell
from vulcanControl import Motor
from database import sqlDatabase
import RPi.GPIO as GPIO #import I/O interface
from hx711 import HX711 #import HX711 class

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.threadpool = QThreadPool()
        self.motor = types.SimpleNamespace()
        self.cellInstance = types.SimpleNamespace()
        self.mutex = QMutex()
        self.sdb = sqlDatabase()
###
        self.m_ui = ui_main()
        self.m_ui.setupUi(self)
###

        self.show()

        self.motorConnected = False
        self.cellConnected = False

        self.forceReading = None
        self.readForceStatus = False
        self.topLimit = False
        self.homeLimit = False
        self.positionReading = None
        self.force_threadStarted = 0
        self.position_threadStarted = 0
        self.dataCollect = False
        self.collection_count = 0

        self.jogging = False
        self.jogUpParam = 0.1
        self.jogDownParam = 0.1

        # self.start_worker_threadManager()

        # UI MODIFICATIONS
        self.m_ui.stackedWidget.setCurrentIndex(0)

        # BUTTON FUNCTION MAPPING
        self.m_ui.connectMotor_button.clicked.connect(self.createMotorInstance)
        self.m_ui.connectLoad_button.clicked.connect(self.createCellInstance)
        self.m_ui.jogUp_button.clicked.connect(self.jogUp)
        self.m_ui.jogDown_button.clicked.connect(self.jogDown)
        self.m_ui.home_button_page1.clicked.connect(self.home)
        self.m_ui.stopButton_page1.clicked.connect(self.stop)
        self.m_ui.stopButton_page2.clicked.connect(self.stop)
        self.m_ui.runButton_page2.clicked.connect(self.startRun)
        self.m_ui.exportDataButton.clicked.connect(self.exportData)
        self.m_ui.startDataButton.clicked.connect(self.dataCollectToggle)
        self.m_ui.jogup_comboBox.currentIndexChanged.connect(self.jogParams)
        self.m_ui.jogdown_comboBox.currentIndexChanged.connect(self.jogParams)
        self.m_ui.jogup_lineEdit.textChanged.connect(self.jogParams)
        self.m_ui.jogdown_lineedit.textChanged.connect(self.jogParams)

    def clear_widgets(self):
        widgets = self.widgets
        for widget in widgets:
            if widgets[widget] != []:
                widgets[widget][-1].hide()
            for i in range(0, len(widgets[widget])):
                widgets[widget].pop()
        self.widgets = widgets

    def start(self,widgets):
        self.clear_widgets()
        self.frame2()

    # THREADING STRUCTURE FUNCTIONS

    def print_output(self, s):
        print(f'output: {s}')

    def thread_complete(self):
        print("thread complete")

    def progress_fn(self, n):
        # print("%d%% done" % n)
        print(f'return value: {n}')

    def return_value(self, num):
        print(f'return value: {num}')

    def forceReading_return(self, n):
        self.forceReading = n
        self.m_ui.loadReading_label.setText(f"{self.forceReading} g")
        if self.dataCollect == True:
            self.sdb.insert_data(self.collection_count, self.forceReading, self.positionReading)

    def topLimit_return(self, b):
        self.topLimit = b

    def homeLimit_return(self, b):
        self.homeLimit = b
        self.m_ui.flag_reading_label.setText(f'{self.topLimit}/{self.homeLimit}')

    def positionReading_return(self, n):
        self.positionReading = n
        self.m_ui.positionReading_label.setText(f"{self.positionReading}")

    def saveFile_return(self, b):
        print(b)

    def longer_test_fn(self, progress_callback):
        for n in range(0,5):
            time.sleep(1)
            progress_callback.emit(n*100/4)
        return "--"

    def setWorker(self, fn):
        worker = Worker(fn)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        worker.signals.forceReading.connect(self.forceReading_return)
        worker.signals.topLimit.connect(self.topLimit_return)
        worker.signals.homeLimit.connect(self.homeLimit_return)
        worker.signals.positionReading.connect(self.positionReading_return)
        print(f'worker: {worker}')

        self.threadpool.start(worker)

    # UTILITY FUNCTIONS

    def createMotorInstance(self):
        if self.motorConnected == False:
            self.motor = Motor()
            self.motorConnected = True
            self.m_ui.motorStatus_label.setText("Connected")
            self.start_worker_readPosition()
        else:
            print("motor already connected")

    def createCellInstance(self):
        if self.cellConnected == False:
            self.cellInstance = LoadCell()
            self.cellConnected = True
            self.m_ui.loadStatus_label.setText("Connected")
            self.start_worker_readForce()
            self.start_worker_checkFlags()
        else:
            print("load cell already connected")

    def jogUp(self):
        self.jogging = True
        # self.start_worker_waitForTopFlag()
        self.motor.move(self.jogUpParam)
        time.sleep(0.1)
        self.jogging = False

    def jogDown(self):
        self.jogging = True
        # self.start_worker_waitForHomeFlag()
        self.motor.move(-self.jogDownParam)
        time.sleep(0.1)
        self.jogging = False

    def stop(self):
        self.jogging = True
        self.motor._stop()
        time.sleep(0.1)
        self.jogging = False

    def home(self):
        self.jogging = True
        self.start_worker_waitForHomeFlag()
        self.motor.home()
        time.sleep(0.1)
        self.jogging = False

    def flush(self):
        self.jogging = True
        self.start_worker_waitForTopFlag()
        self.motor.move(40)
        time.sleep(0.1)
        self.jogging = False

    def exportData(self):
        self.sdb.export_data()
        self.start_worker_saveFile()

    def dataCollectToggle(self):
        if self.dataCollect == True:
            self.dataCollect = False
            self.m_ui.startDataButton.setStyleSheet("*{border: 4px solid \'red\'; border-radius: 10px; font: bold 18px \"Arial Black\"; color: \'white\'; padding: 0px 0px; margin-left: 30; background: #555} *:hover{background: \'#369\';}")
        else:
            self.dataCollect = True
            self.collection_count += 1
            self.m_ui.startDataButton.setStyleSheet("*{border: 4px solid \'green\'; border-radius: 10px; font: bold 18px \"Arial Black\"; color: \'white\'; padding: 0px 0px; margin-left: 30; background: #555} *:hover{background: \'#369\';}")

    def startRun(self):
        try:
            layerBefore, lbUnit = float(self.m_ui.layerBefore_lineedit.text()), self.m_ui.layerBefore_comboBox.currentIndex()
            layerAfter, laUnit = float(self.m_ui.layerAfter_lineedit.text()), self.m_ui.layerAfter_comboBox.currentIndex()
            layerCount = int(self.m_ui.layerCount_lineedit.text())

            if type(layerBefore) == float and type(layerAfter) == float and type(layerCount) == int:
                c1, c2, LB, LA, LC = self.checkRunInputs(layerBefore, lbUnit, layerAfter, laUnit, layerCount)
                if c1 == True and c2 == True:

                    ### ###
                    
                    print(f'sent run signal to motor with params LB:{LB}, LA:{LA}, LC:{LC}')
                    self.motor.run(LB, LA, LC)

                    ### ###

                else:
                    print('ERROR - Run Failed')
                    self.m_ui.launchrunErrorPopup()
            else:
                print('ERROR - Run Failed')
                self.m_ui.launchrunErrorPopup()
        except:
            print('ERROR - Invalid Values for Run Command')

    def checkRunInputs(self, layerBefore, lbUnit, layerAfter, laUnit, layerCount):
        LC = layerCount
        if lbUnit == 1:
            LB = layerBefore/1000
        else:
            LB = layerBefore
        if laUnit == 1:
            LA = layerAfter/1000
        else:
            LA = layerAfter
        if LA > LB:
            print('ERROR - Layer After must be smaller than Layer Before')
            check_1 = False
        else:
            check_1 = True
        if (LB * LC) > 30:
            print('ERROR - Compaction Height Limit Reached')
            check_2 = False
        else:
            check_2 = True
        print(f'LB: {LB}, LA {LA}')
        return check_1, check_2, LB, LA, LC

    def openFileNameDialog(self):
        path = QFileDialog.getSaveFileName(self, 'Save file', '',
                                        'CSV (*.csv*)')
        if path != ('', ''):
            print("File path : "+ path[0])

    def jogParams(self):
        if self.m_ui.jogup_comboBox.currentIndex() == 0:
            self.jogUpParam = 0.1
        elif self.m_ui.jogup_comboBox.currentIndex() == 1:
            self.jogUpParam = 0.5
        elif self.m_ui.jogup_comboBox.currentIndex() == 2:
            self.jogUpParam = 1
        elif self.m_ui.jogup_comboBox.currentIndex() == 3:
            self.jogUpParam = 5
        elif self.m_ui.jogup_comboBox.currentIndex() == 4:
            self.jogUpParam = 10
        elif self.m_ui.jogup_comboBox.currentIndex() == 2:
            try:
                self.jogUpParam = self.m_ui.jogup_lineEdit.text()
            except:
                print("Jog up custom input is invalid")
        if self.m_ui.jogdown_comboBox.currentIndex() == 0:
            self.jogDownParam = 0.1
        elif self.m_ui.jogdown_comboBox.currentIndex() == 1:
            self.jogDownParam = 0.5
        elif self.m_ui.jogdown_comboBox.currentIndex() == 2:
            self.jogDownParam = 1
        elif self.m_ui.jogdown_comboBox.currentIndex() == 3:
            self.jogDownParam = 5
        elif self.m_ui.jogdown_comboBox.currentIndex() == 4:
            self.jogDownParam = 10
        elif self.m_ui.jogdown_comboBox.currentIndex() == 2:
            try:
                self.jogDownParam = self.m_ui.jogdown_lineedit.text()
            except:
                print("Jog down custom input is invalid")

    # THREAD UTILITY FUNCTIONS
    
    def thread_readForce(self, progress_callback, forceReading_callback, topLimit_callback, homeLimit_callback, positionReading_callback, saveFile_callback):
        if self.force_threadStarted == 0:
            self.force_threadStarted = 1
            while True:
                forceReading = self.cellInstance.readForce()
                forceReading_callback.emit(forceReading)
                time.sleep(0.01)
        else:
            print("force reading thread already started.")

    def start_worker_readForce(self):
        self.readForceStatus = True
        self.setWorker(self.thread_readForce)

    def threadManager(self, progress_callback, forceReading_callback, topLimit_callback, homeLimit_callback, positionReading_callback, saveFile_callback):
        while True:
            print(f'Active Thread Count: {self.threadpool.activeThreadCount()}')
            time.sleep(1)

    def start_worker_threadManager(self):
        self.setWorker(self.threadManager)

    def thread_checkFlags(self, progress_callback, forceReading_callback, topLimit_callback, homeLimit_callback, positionReading_callback, saveFile_callback):
        while True:
            self.motor._checkLimits()
            topLimit = self.motor.topLimit
            homeLimit = self.motor.homeLimit
            topLimit_callback.emit(topLimit)
            homeLimit_callback.emit(homeLimit)
            time.sleep(0.1)

    def start_worker_checkFlags(self):
        self.setWorker(self.thread_checkFlags)

    def thread_readPosition(self, progress_callback, forceReading_callback, topLimit_callback, homeLimit_callback, positionReading_callback, saveFile_callback):
        if self.position_threadStarted == 0:
            self.position_threadStarted = 1
            while True:
                if self.jogging == False:
                    position = self.motor.updatePosition()
                else:
                    position = None
                positionReading_callback.emit(position)
        else:
            print("position reading thread already started.")

    def start_worker_readPosition(self):
        self.setWorker(self.thread_readPosition)

    def thread_waitForTopFlag(self, progress_callback, forceReading_callback, topLimit_callback, homeLimit_callback, positionReading_callback, saveFile_callback):
        while self.topLimit == False:
            print("false")
        self.motor._stop()
        print("TRUE STOP NOW")

    def start_worker_waitForTopFlag(self):
        self.setWorker(self.thread_waitForTopFlag)

    def thread_waitForHomeFlag(self, progress_callback, forceReading_callback, topLimit_callback, homeLimit_callback, positionReading_callback, saveFile_callback):
        while self.homeLimit == False:
            print("False")
        self.motor._stop()
        print("TRUE STOP NOW")

    def start_worker_waitForHomeFlag(self):
        self.setWorker(self.thread_waitForHomeFlag)

    def start_worker_saveFile(self):
        self.setWorker(self.thread_saveFile)

    def thread_saveFile(self, progress_callback, forceReading_callback, topLimit_callback, homeLimit_callback, positionReading_callback, saveFile_callback):
        print("save file thread started")
        done = False
        while done == False:
            if self.sdb.file_path == True:
                self.sdb.file_path = False
                self.sdb.exportdb()
                done = True
            else:
                pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    sys.exit(app.exec())