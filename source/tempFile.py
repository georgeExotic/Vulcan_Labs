import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThreadPool, QRunnable, QThread
from PyQt5.QtGui import QCursor

from threadClasses import WorkerSignals, Worker
from LoadCell import LoadCell
from vulcanControl import Motor
import RPi.GPIO as GPIO #import I/O interface
from hx711 import HX711 #import HX711 class

class Ui_MainWindow(QWidget):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.threadpool = QThreadPool()
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
            "label1_frame2": [],
            "label2_frame2": [],
            "label3_frame2": [],
            "label4_frame2": [],
            "label5_frame2": [],
            "label6_frame2": [],
            "label7_frame2": [],
            "label8_frame2": [],
        }

        self.grid = QGridLayout()

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
        button.setFixedWidth(80)
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
        button2_frame2 = self.create_buttons("Button 2")
        button3_frame2 = self.create_buttons("Button 3")
        button4_frame2 = self.create_buttons("Button 4")
        button5_frame2 = self.create_buttons("Button 5")
        button6_frame2 = self.create_buttons("Button 6")
        button7_frame2 = self.create_buttons("Button 7")
        button8_frame2 = self.create_buttons("Button 8")

        #-labels
        label1_frame2 = self.create_label("Label 1")
        label2_frame2 = self.create_label("Label 2")
        label3_frame2 = self.create_label("Label 3")
        label4_frame2 = self.create_label("Label 4")
        label5_frame2 = self.create_label("Label 5")
        label6_frame2 = self.create_label("Label 6")
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
        self.widgets["label1_frame2"].append(label1_frame2)
        self.widgets["label2_frame2"].append(label2_frame2)
        self.widgets["label3_frame2"].append(label3_frame2)
        self.widgets["label4_frame2"].append(label4_frame2)
        self.widgets["label5_frame2"].append(label5_frame2)
        self.widgets["label6_frame2"].append(label6_frame2)
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
        self.grid.addWidget(self.widgets["label1_frame2"][-1], 2, 5)
        self.grid.addWidget(self.widgets["label2_frame2"][-1], 3, 5)
        self.grid.addWidget(self.widgets["label3_frame2"][-1], 4, 5)
        self.grid.addWidget(self.widgets["label4_frame2"][-1], 5, 5)
        self.grid.addWidget(self.widgets["label5_frame2"][-1], 6, 5)
        self.grid.addWidget(self.widgets["label6_frame2"][-1], 7, 5)
        self.grid.addWidget(self.widgets["label7_frame2"][-1], 8, 5)
        self.grid.addWidget(self.widgets["label8_frame2"][-1], 9, 5)

    def start(self,widgets):
        self.clear_widgets()
        self.frame2()

    #THREADING

    def print_output(self, s):
        print(f'output: {s}')

    def thread_complete(self):
        print("thread complete")

    def progress_fn(self, n):
        print("%d%% done" % n)

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

        self.threadpool.start(worker)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.setWindowTitle("Test Program")
    window.setFixedWidth(1000)
    window.setFixedHeight(600)
    window.setStyleSheet("background: #161616;")

    window.frame1()

    window.setLayout(window.grid)

    window.show()
    sys.exit(app.exec())