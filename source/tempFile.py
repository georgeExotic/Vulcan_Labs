import sys
import types
import time
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThreadPool, QRunnable, QThread, pyqtSignal, pyqtSlot, QMutex
from PyQt5.QtGui import QCursor

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
        self.widgets = {
            "title": [],
            "button1_frame1": [],
            "title_frame2": [],
            "button1_frame2": [],
            "button2_frame2": [],
            "button3_frame2": [],
            "button4_frame2": [],
            "button5_frame2": [],
            "button6_frame2": [],
            "button7_frame2": [],
            "button8_frame2": [],
            "button9_frame2": [],
            "button10_frame2": [],
            "label1_frame2": [],
            "label2_frame2": [],
            "label3_frame2": [],
            "label4_frame2": [],
            "label4_1_frame2": [],
            "label5_frame2": [],
            "label5_1_frame2": [],
            "label6_frame2": [],
            "label6_1_frame2": [],
            "label7_frame2": [],
            "label8_frame2": [],
        }

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.grid = QGridLayout(self.centralWidget)
        # self.centralWidget.setLayout(self.grid)

        self.setWindowTitle("Test Program")
        self.setFixedWidth(800)
        self.setFixedHeight(480)
        self.setStyleSheet("background: #161616;")

        self.frame1()

        self.show()


        self.motorConnected = False
        self.cellConnected = False

        self.forceReading = None
        self.readForceStatus = False
        self.topLimit = False
        self.homeLimit = False
        self.positionReading = None

        self.readingPos = False

        self.start_worker_threadManager()
        print("running")

    def clear_widgets(self):
        widgets = self.widgets
        for widget in widgets:
            if widgets[widget] != []:
                widgets[widget][-1].hide()
            for i in range(0, len(widgets[widget])):
                widgets[widget].pop()
        self.widgets = widgets

    def show_frame1(self,widgets):
        self.clear_widgets()
        self.frame1()

    def create_buttons(self,answer):
        button = QPushButton(answer)
        button.setCursor(QtCore.Qt.PointingHandCursor)
        button.setFixedWidth(100)
        button.setStyleSheet(
            "*{border: 4px solid '#ccc';" +
            "border-radius: 15px;" +
            "font-size: 14px;" +
            "color: 'white';" +
            "padding: 5px 5px;" +
            "margin: 0px 0px;}" + 
            "*:hover{background: '#369';}")
        return button

    def create_label(self,label_name):
        label = QLabel(label_name)
        label.setStyleSheet(
            "color: #fff;"
            "font: 14px;")
        return label

    def frame1(self):
        #title widget
        title = QLabel("Test Program")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet(
            "color: #fff;"
            "font: 30px;")
        self.widgets["title"].append(title)

        #button1_frame1
        button1_frame1 = QPushButton("RUN")
        button1_frame1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button1_frame1.setStyleSheet(
            "*{border: 4px solid '#ccc';" +
            "border-radius: 15px;" +
            "font-size: 20px;" +
            "color: 'white';" +
            "padding: 5px 5px;" +
            "margin: 0px 0px;}" + 
            "*:hover{background: '#369';}")
        button1_frame1.clicked.connect(self.start)

        self.widgets["button1_frame1"].append(button1_frame1)

        self.grid.addWidget(self.widgets["title"][-1], 0, 0, 1, 4)
        self.grid.addWidget(self.widgets["button1_frame1"][-1], 1, 0, 1, 4)

    def frame2(self):

        # building widgets - frame 2
        #-title
        title_frame2 = QLabel("testing grounds")
        title_frame2.setAlignment(QtCore.Qt.AlignCenter)
        title_frame2.setWordWrap(True)
        title_frame2.setStyleSheet(
            "font-size: 35px;" +
            "color: 'white';"
        )
        title_frame2.setFixedHeight(60)
        self.widgets["title_frame2"].append(title_frame2)

        #-button1
        button1_frame2 = self.create_buttons("Button 1")
        button1_frame2.clicked.connect(self.show_frame1)
        button2_frame2 = self.create_buttons("Connect Motor")
        button2_frame2.setFixedWidth(140)
        button2_frame2.clicked.connect(self.createMotorInstance)
        button3_frame2 = self.create_buttons("Connect Load Cell")
        button3_frame2.setFixedWidth(160)
        button3_frame2.clicked.connect(self.createCellInstance)
        button4_frame2 = self.create_buttons("Start Reading Force")
        button4_frame2.setFixedWidth(160)
        button4_frame2.clicked.connect(self.start_worker_readForce)
        button5_frame2 = self.create_buttons("Start Checking Flags")
        button5_frame2.setFixedWidth(160)
        button5_frame2.clicked.connect(self.start_worker_checkFlags)
        button6_frame2 = self.create_buttons("Start Reading Pos")
        button6_frame2.setFixedWidth(160)
        button6_frame2.clicked.connect(self.start_worker_readPosition)
        button7_frame2 = self.create_buttons("Up")
        button7_frame2.clicked.connect(self.jogUp)
        # button7_frame2.clicked.connect(self.waitForTopFlag)
        button8_frame2 = self.create_buttons("Down")
        button8_frame2.clicked.connect(self.jogDown)
        button9_frame2 = self.create_buttons("Home")
        button10_frame2 = self.create_buttons("Extract")

        #-labels
        label1_frame2 = self.create_label("Label 1")
        label2_frame2 = self.create_label("Motor: Not Connected")
        label3_frame2 = self.create_label("Load Cell: Not Connected")
        label4_frame2 = self.create_label("Force: --")
        label4_1_frame2 = self.create_label("Thread: --")
        label5_frame2 = self.create_label("Top: -- Home: --")
        label5_1_frame2 = self.create_label("Thread: --")
        label6_frame2 = self.create_label("Pos: --")
        label6_1_frame2 = self.create_label("Thread: --")
        label7_frame2 = self.create_label("Label 7")
        label8_frame2 = self.create_label("Label 8")

        # compile widgets - frame 2
        self.widgets["button1_frame2"].append(button1_frame2)
        self.widgets["button2_frame2"].append(button2_frame2)
        self.widgets["button3_frame2"].append(button3_frame2)
        self.widgets["button4_frame2"].append(button4_frame2)
        self.widgets["button5_frame2"].append(button5_frame2)
        self.widgets["button6_frame2"].append(button6_frame2)
        self.widgets["button7_frame2"].append(button7_frame2)
        self.widgets["button8_frame2"].append(button8_frame2)
        self.widgets["button9_frame2"].append(button9_frame2)
        self.widgets["button10_frame2"].append(button10_frame2)
        self.widgets["label1_frame2"].append(label1_frame2)
        self.widgets["label2_frame2"].append(label2_frame2)
        self.widgets["label3_frame2"].append(label3_frame2)
        self.widgets["label4_frame2"].append(label4_frame2)
        self.widgets["label4_1_frame2"].append(label4_1_frame2)
        self.widgets["label5_frame2"].append(label5_frame2)
        self.widgets["label5_1_frame2"].append(label5_1_frame2)
        self.widgets["label6_frame2"].append(label6_frame2)
        self.widgets["label6_1_frame2"].append(label6_1_frame2)
        self.widgets["label7_frame2"].append(label7_frame2)
        self.widgets["label8_frame2"].append(label8_frame2)

        self.grid.addWidget(self.widgets["title_frame2"][-1], 1, 0)
        self.grid.addWidget(self.widgets["button1_frame2"][-1], 2, 0)
        self.grid.addWidget(self.widgets["button2_frame2"][-1], 3, 0)
        self.grid.addWidget(self.widgets["button3_frame2"][-1], 4, 0)
        self.grid.addWidget(self.widgets["button4_frame2"][-1], 5, 0)
        self.grid.addWidget(self.widgets["button5_frame2"][-1], 6, 0)
        self.grid.addWidget(self.widgets["button6_frame2"][-1], 7, 0)
        self.grid.addWidget(self.widgets["button7_frame2"][-1], 8, 0)
        self.grid.addWidget(self.widgets["button8_frame2"][-1], 9, 0)
        self.grid.addWidget(self.widgets["button9_frame2"][-1], 10, 0)
        self.grid.addWidget(self.widgets["button10_frame2"][-1], 11, 0)
        self.grid.addWidget(self.widgets["label1_frame2"][-1], 2, 5)
        self.grid.addWidget(self.widgets["label2_frame2"][-1], 3, 5)
        self.grid.addWidget(self.widgets["label3_frame2"][-1], 4, 5)
        self.grid.addWidget(self.widgets["label4_frame2"][-1], 5, 5)
        self.grid.addWidget(self.widgets["label4_1_frame2"][-1], 5, 1)
        self.grid.addWidget(self.widgets["label5_frame2"][-1], 6, 5)
        self.grid.addWidget(self.widgets["label5_1_frame2"][-1], 6, 1)
        self.grid.addWidget(self.widgets["label6_frame2"][-1], 7, 5)
        self.grid.addWidget(self.widgets["label6_1_frame2"][-1], 7, 1)
        self.grid.addWidget(self.widgets["label7_frame2"][-1], 8, 5)
        self.grid.addWidget(self.widgets["label8_frame2"][-1], 9, 5)

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
        self.widgets["label4_frame2"][-1].setText(f"Force: {self.forceReading} kg")

    def topLimit_return(self, b):
        self.topLimit = b

    def homeLimit_return(self, b):
        self.homeLimit = b
        self.widgets["label5_frame2"][-1].setText(f'Top: {self.topLimit} Home: {self.homeLimit}')

    def positionReading_return(self, n):
        self.positionReading = n
        self.widgets["label6_frame2"][-1].setText(f'Pos: {self.positionReading}')

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
            self.widgets["label2_frame2"][-1].setText("Motor: Connected")
        else:
            print("motor already connected")

    def createCellInstance(self):
        if self.cellConnected == False:
            self.cellInstance = LoadCell()
            self.cellConnected = True
            self.widgets["label3_frame2"][-1].setText("Load Cell: Connected")
        else:
            print("load cell already connected")

    def jogUp(self):
        positionRead = False
        while positionRead == False:
            if self.readingPos == False:
                self.motor.move(4)
                time.sleep(0.01)
                positionRead = True
            else:
                pass

    def jogDown(self):
        positionRead = False
        while positionRead == False:
            if self.readingPos == False:
                self.motor.move(-4)
                time.sleep(0.01)
                positionRead = True
            else:
                pass

    # THREAD UTILITY FUNCTIONS
    
    def thread_readForce(self, progress_callback, forceReading_callback, topLimit_callback, homeLimit_callback, positionReading_callback):
        while True:
            forceReading = self.cellInstance.readForce()
            forceReading_callback.emit(forceReading)
            time.sleep(0.01)

    def start_worker_readForce(self):
        self.readForceStatus = True
        self.widgets["label4_1_frame2"][-1].setText("Thread: Active")
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
        self.widgets["label5_1_frame2"][-1].setText("Thread: Active")
        self.widgets["label5_frame2"][-1].setText(f'Top: {self.topLimit} Home: {self.homeLimit}')
        self.setWorker(self.thread_checkFlags)

    def thread_readPosition(self, progress_callback, forceReading_callback, topLimit_callback, homeLimit_callback, positionReading_callback):
        while True:
            self.readingPos = True
            position = self.motor.updatePosition()
            positionReading_callback.emit(position)
            self.readingPos = False
            time.sleep(0.1)

    def start_worker_readPosition(self):
        self.widgets["label6_1_frame2"][-1].setText("Thread: Active")
        self.setWorker(self.thread_readPosition)

    def waitForTopFlag(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    sys.exit(app.exec())