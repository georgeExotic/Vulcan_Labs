#!/usr/bin/env python

import math
import time
import timeit
import random
import sys
import serial 
import os
import pickle
import socket
import traceback
import sqlite3
from datetime import datetime, date

# import L2_log as log

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
# import paho.mqtt.client as paho
# style.use('fivethirtyeight')

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
# import RPi.GPIO as GPIO #import I/O interface             #
# from hx711 import HX711 #import HX711 class               #
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QPoint, QRect, QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThreadPool, QRunnable, QThread
from PyQt5.QtWidgets import (QSizePolicy,
        QWidget, QFrame, QRadioButton, QCheckBox)
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLayout, 
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QStatusBar, QTabWidget, QLCDNumber, QTableWidget, QTableWidgetItem, QTableView, QMainWindow, QMessageBox)

from GUI import Ui_MainWindow
from GUI import App
# from vulcanControl import Motor

#Global Variables

# Main window containing all GUI components

                
if __name__ == '__main__':
    # motor = Motor()
    # cellInstance = FakeLoadCell()
    # DB = sqlDatabase()
    app = QApplication(sys.argv)
    # app.setStyle('Fusion')
    # mainWin = Ui_MainWindow()
    mainWin = App()
    styleFile=os.path.join(os.path.split(__file__)[0],"styleVulcan.stylesheet")
    styleSheetStr = open(styleFile,"r").read()
    mainWin.setStyleSheet(styleSheetStr)
    mainWin.show()

    fps = 3
    # timer = QtCore.QTimer()
    # timer.timeout.connect(mainWin.UpdateGUI)
    # timer.setInterval(int(1000/fps))
    # timer.start()

    sys.exit(app.exec_())

