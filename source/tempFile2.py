import sys
import types
import time
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThreadPool, QRunnable, QThread, pyqtSignal, pyqtSlot, QMutex
from PyQt5.QtGui import QCursor

from ui_main import ui_main

from threadClasses import WorkerSignals, Worker
from LoadCell import LoadCell
from vulcanControl import Motor
import RPi.GPIO as GPIO #import I/O interface
from hx711 import HX711 #import HX711 class

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.threadpool = QThreadPool()
        self.motor = types.SimpleNamespace()
        self.cellInstance = types.SimpleNamespace()
        self.mutex = QMutex()

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
        self.position_threadStarted = 1

        self.jogging = False

        self.start_worker_threadManager()

        # UI MODIFICATIONS
        self.m_ui.stackedWidget.setCurrentIndex(0)
        # self.m_ui.layerBefore_comboBox.addItem('option 1')

        # BUTTON FUNCTION MAPPING
        self.m_ui.connectMotor_button.clicked.connect(self.createMotorInstance)
        self.m_ui.connectLoad_button.clicked.connect(self.createCellInstance)
        self.m_ui.jogUp_button.clicked.connect(self.jogUp)
        self.m_ui.jogDown_button.clicked.connect(self.jogDown)
        self.m_ui.home_button_page1.clicked.connect(self.home)
        self.m_ui.stopButton_page1.clicked.connect(self.stop)
        self.m_ui.stopButton_page2.clicked.connect(self.stop)
        self.m_ui.runButton_page2.clicked.connect(self.startRun)


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
        # self.widgets["label4_frame2"][-1].setText(f"Force: {self.forceReading} kg")

    def topLimit_return(self, b):
        self.topLimit = b

    def homeLimit_return(self, b):
        self.homeLimit = b
        self.m_ui.flag_reading_label.setText(f'{self.topLimit}/{self.homeLimit}')
        # self.widgets["label5_frame2"][-1].setText(f'Top: {self.topLimit} Home: {self.homeLimit}')

    def positionReading_return(self, n):
        self.positionReading = n
        self.m_ui.positionReading_label.setText(f"{self.positionReading}")
        # self.widgets["label6_frame2"][-1].setText(f'Pos: {self.positionReading}')

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
        self.motor.move(4)
        time.sleep(0.1)
        self.jogging = False

    def jogDown(self):
        self.jogging = True
        self.motor.move(-4)
        time.sleep(0.1)
        self.jogging = False

    def stop(self):
        self.jogging = True
        self.motor._stop()
        time.sleep(1)
        self.jogging = False

    def home(self):
        self.jogging = True
        self.motor.home()
        time.sleep(0.1)
        self.jogging = False

    def startRun(self):
        try:
            layerBefore, lbUnit = float(self.m_ui.layerBefore_lineedit.text()), self.m_ui.layerBefore_comboBox.currentIndex()
            layerAfter = float(self.m_ui.layerAfter_lineedit.text())
            layerCount = int(self.m_ui.layerCount_lineedit.text())
            if type(layerBefore) == float and type(layerAfter) == float and type(layerCount) == int:
                print(layerCount, layerBefore, lbUnit)
            else:
                print('ERROR - Run Failed')
        except:
            print('ERROR - Invalid Values for Run Command')

    # THREAD UTILITY FUNCTIONS
    
    def thread_readForce(self, progress_callback, forceReading_callback, topLimit_callback, homeLimit_callback, positionReading_callback):
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
        # self.widgets["label4_1_frame2"][-1].setText("Thread: Active")
        self.setWorker(self.thread_readForce)

    def threadManager(self, progress_callback, forceReading_callback, topLimit_callback, homeLimit_callback, positionReading_callback):
        while True:
            print(f'Active Thread Count: {self.threadpool.activeThreadCount()}')
            time.sleep(1)

    def start_worker_threadManager(self):
        self.setWorker(self.threadManager)

    def thread_checkFlags(self, progress_callback, forceReading_callback, topLimit_callback, homeLimit_callback, positionReading_callback):
        while True:
            self.motor._checkLimits()
            topLimit = self.motor.topLimit
            homeLimit = self.motor.homeLimit
            topLimit_callback.emit(topLimit)
            homeLimit_callback.emit(homeLimit)
            time.sleep(0.1)

    def start_worker_checkFlags(self):
        # self.widgets["label5_1_frame2"][-1].setText("Thread: Active")
        # self.widgets["label5_frame2"][-1].setText(f'Top: {self.topLimit} Home: {self.homeLimit}')
        self.setWorker(self.thread_checkFlags)

    def thread_readPosition(self, progress_callback, forceReading_callback, topLimit_callback, homeLimit_callback, positionReading_callback):
        if self.position_threadStarted == 0:
            self.position_threadStarted = 1
            while True:
                self.motor._checkConnection()
                if self.jogging == False:
                    position = self.motor.updatePosition()
                    positionReading_callback.emit(position)
                else:
                    pass
            time.sleep(0.1)
        else:
            print("position reading thread already started.")

    def start_worker_readPosition(self):
        # self.widgets["label6_1_frame2"][-1].setText("Thread: Active")
        self.setWorker(self.thread_readPosition)

    def waitForTopFlag(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    sys.exit(app.exec())