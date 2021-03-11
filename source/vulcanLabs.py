
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
import pandas as pd
import shutil
from datetime import datetime, date
import numpy as np
from scipy import signal

import L2_log as log

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
# style.use('fivethirtyeight')

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import RPi.GPIO as GPIO #import I/O interface             #
from hx711 import HX711 #import HX711 class               #
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QPoint, QRect, QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThreadPool, QRunnable, QThread
from PyQt5.QtWidgets import (QSizePolicy,
        QWidget, QFrame, QRadioButton, QCheckBox)
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLayout, 
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QStatusBar, QTabWidget, QLCDNumber, QTableWidget, QTableWidgetItem, QTableView, QMainWindow, QMessageBox)

from vulcanControl import Motor
from key import VirtualKeyboard
from key import VirtualKeyboard2
from key import VirtualKeyboard3
from key import VirtualKeyboard4
from key import VirtualKeyboard5
from key import VirtualKeyboard6
from key import VirtualKeyboard7

# Main window containing all GUI components
class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupGlobalVars()
        self.setupUi()
        pg.setConfigOptions(antialias=True)

    def setupGlobalVars(self):
        self.modeSelected = 0                                   # 0:motion 1:pressure
        self.connectionState = 0                                # 0:No Connection 1:Connection Secure
        self.IpAdd = socket.gethostbyname(socket.gethostname())
        self.mass = 0
        self.systemState = 0                                    # 0:idle 1:Starting 2:Running 3:Paused 4:Stopped 5:Processing 6:Homed
        self.systemCalibrated = 0           # 0: no 1: calibrated                    
        self.lineEditState = 0
        self.currentlineEdit = 0
        self.force_reading_raw = 0
        self.force_reading_kg = 0
        self.force_reading_N = 0
        self.pressure_reading = 0
        self.position_reading = 0
        self.testValue_y = []

        self.desPos = 0
        self.desPress = 0
        self.curPos = 0
        self.curPress = 0

        self.StartingTime = time.time()
        self.runStartTime = 0

    def setupUi(self):

        # -- INITIALIZATION -- #

        #Initializes window and parameters
        MainWindow = self
        MainWindow.setObjectName("Vulcan Labs")
        MainWindow.resize(1024, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1024, 600))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.closeWindowButton = QPushButton(self.frame)
        self.b = QtGui.QPushButton("Exit", self, clicked=self.close)
        self.b.setGeometry(940,10,60,30)

        #Initializes tab layout
        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1024, 420))
        self.tabWidget.setObjectName("tabWidget")
        self.frame.setStyleSheet("QTabWidget::pane { border: 0; }")
        self.setStyleSheet("""QLineEdit:disabled { padding: 1px; color: #202020; border: 2px solid #A9A6A0; border-radius: 2px; font-weight: bold; background-color: #A9A6A0}""")
        self.setStyleSheet("""QGroupBox { font-weight: bold; font-size: 15px; color: #FFF000; border-radius: 8px;}""")
        self.setStyleSheet("""QLabel->widget { color: #F9F6F0; font-weight: bold; font-size: 14px; }""")
        self.setStyleSheet("""QLabel:disabled { color:#FFF000; font-weight: bold; font-size: 14px; }""")

        # TAB 1 #

        #Inits box area on left
        self.widget = QWidget()
        self.widget.setObjectName("widget")
        self.widget.setStyleSheet("""QLabel:enabled { color: #F9F6F0; font-weight: bold; font-size: 18px; } QComboBox { font-size: 18px; font-weight: bold;} 
                                    QLineEdit:disabled { padding: 1px; color: #202020; border: 2px solid #A9A6A0; border-radius: 2px; font-weight: bold; background-color: #A9A6A0}
                                    QLineEdit:enabled { padding: 1px; color: #202020; border: 2px solid #A9A6A0; border-radius: 2px; font-weight: bold; font-size: 18px; background-color: #fff}
                                    QPushButton { font-weight: bold; font-size: 20px; color: #303030; border: 2px solid #202020; border-radius: 8px; min-width: 10px; background-color: #FF7C0A;} 
                                    QPushButton:disabled {font-weight: bold; font-size: 16px; color: #000; border: 2px solid #202020; border-radius: 8px; min-width: 10px; background-color: #66380d;}""")

        #Inits Logo
        self.pixmap = QPixmap('VulcanLabsLogo.png')
        self.pixmap2 = self.pixmap.scaled(260, 200, QtCore.Qt.KeepAspectRatio) # Logo
        self.labelLogo = QLabel(self.widget)
        self.labelLogo.setPixmap(self.pixmap2)
        self.labelLogo.setGeometry(20,80,300,300)

        self.warningLabel = QLabel(self.frame)
        self.warningLabel.setGeometry(QtCore.QRect(50, 70, 850, 20)) # pos and size
        self.warningLabel.setObjectName("warningLabel")
        self.warningLabel.setText("")
        self.warningLabel.setStyleSheet("""background-color: transparent; color: #ff0""")

        #Inits Mode select dropdown component
        self.comboBox = QComboBox(self.widget)
        self.comboBox.setGeometry(QtCore.QRect(15, 80, 270, 50)) # positioning and sizing
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setContentsMargins(0,0,0,0)
        self.comboBox.setStyleSheet("font-size: 24px; font-weight: bold;")

        #Inits window icon as logo
        self.setWindowIcon(QtGui.QIcon('3DPrinterLogo.png')) # Logo as Icon
        # self.setStyleSheet("background-color: rgb(255, 255, 255)") #Sets background color of GUI

        #Inits initial layer height input
        self.initLayerHeightInput = QLineEdit(self.widget)
        self.initLayerHeightInput.setGeometry(QtCore.QRect(495, 50, 70, 40)) # pos and size
        self.initLayerHeightInput.setObjectName("initLayerHeightInput")
        self.initLayerHeightInput.setText("0.00")

        #Inits initial layer height unit select
        self.initLayerHeightUnitCombobox = QComboBox(self.widget)
        self.initLayerHeightUnitCombobox.setGeometry(QtCore.QRect(585, 50, 70, 40)) # pos and size
        self.initLayerHeightUnitCombobox.setAutoFillBackground(False)
        self.initLayerHeightUnitCombobox.setEditable(False)
        self.initLayerHeightUnitCombobox.setObjectName("initLayerHeightUnitCombobox")
        self.initLayerHeightUnitCombobox.addItem("")
        self.initLayerHeightUnitCombobox.addItem("")

        #Inits initial layer height label
        self.label_9 = QLabel(self.widget)
        self.label_9.setGeometry(QtCore.QRect(360, 50, 130, 20)) # pos and size
        self.label_9.setObjectName("label_9")
        self.label_91 = QLabel(self.widget)
        self.label_91.setGeometry(QtCore.QRect(360, 70, 130, 20)) # pos and size
        self.label_91.setObjectName("label_9")

        self.editLayerHeightButton = QPushButton(self.widget)
        self.editLayerHeightButton.setGeometry(290,55,60,30)
        self.editLayerHeightButton.setText("Edit")
        self.editLayerHeightButton.clicked.connect(self.kbLayer)

        #Inits compaction unit select
        self.compactedLayerHeightComboBox = QComboBox(self.widget)
        self.compactedLayerHeightComboBox.setGeometry(QtCore.QRect(585, 110, 70, 40)) # pos and size
        self.compactedLayerHeightComboBox.setAutoFillBackground(False)
        self.compactedLayerHeightComboBox.setEditable(False)
        self.compactedLayerHeightComboBox.setObjectName("compactedLayerHeightComboBox")
        self.compactedLayerHeightComboBox.addItem("")
        self.compactedLayerHeightComboBox.addItem("")

        self.compactedLayerHeightButton = QPushButton(self.widget)
        self.compactedLayerHeightButton.setGeometry(290,115,60,30)
        self.compactedLayerHeightButton.setText("Edit")
        self.compactedLayerHeightButton.clicked.connect(self.kbCompacted)

        #Inits final layer height input
        self.compactedLayerHeightInput = QLineEdit(self.widget)
        self.compactedLayerHeightInput.setGeometry(QtCore.QRect(495, 110, 70, 40)) # pos and size
        self.compactedLayerHeightInput.setObjectName("compactedLayerHeightInput")
        self.compactedLayerHeightInput.setText("0.00")

        #Inits final layer label
        self.label_10 = QLabel(self.widget)
        self.label_10.setGeometry(QtCore.QRect(360, 110, 130, 20)) # pos and size
        self.label_10.setObjectName("label_10")
        self.label_101 = QLabel(self.widget)
        self.label_101.setGeometry(QtCore.QRect(360, 130, 130, 20)) # pos and size
        self.label_101.setObjectName("label_101")

        #Inits number of layers label
        self.label_11 = QLabel(self.widget)
        self.label_11.setGeometry(QtCore.QRect(360, 230, 150, 20)) # pos and size
        self.label_11.setObjectName("label_11")
        self.label_111 = QLabel(self.widget)
        self.label_111.setGeometry(QtCore.QRect(360, 250, 150, 20)) # pos and size
        self.label_111.setObjectName("label_111")

        #Inits number of layers input
        self.layerCountInput = QLineEdit(self.widget)
        self.layerCountInput.setGeometry(QtCore.QRect(495, 230, 70, 40)) # pos and size
        self.layerCountInput.setObjectName("layerCountInput")
        self.layerCountInput.setText("1")
        self.layerCountInputButton = QPushButton(self.widget)
        self.layerCountInputButton.setGeometry(290,235,60,30)
        self.layerCountInputButton.setText("Edit")
        self.layerCountInputButton.clicked.connect(self.kbLayerCount)

        #Inits desired pressure label
        self.label_12 = QLabel(self.widget)
        self.label_12.setGeometry(QtCore.QRect(360, 170, 150, 20)) # pos and size
        self.label_12.setObjectName("label_12")
        self.label_121 = QLabel(self.widget)
        self.label_121.setGeometry(QtCore.QRect(360, 190, 150, 20)) # pos and size
        self.label_121.setObjectName("label_121")

        #Inits target pressure
        self.targetPressureInput = QLineEdit(self.widget)
        self.targetPressureInput.setGeometry(QtCore.QRect(495, 170, 70, 40)) # pos and size
        self.targetPressureInput.setObjectName("targetPressureInput")
        self.targetPressureInput.setText("0.00")

        self.targetPressureButton = QPushButton(self.widget)
        self.targetPressureButton.setGeometry(290,175,60,30)
        self.targetPressureButton.setText("Edit")
        self.targetPressureButton.clicked.connect(self.kbPressure)

        #Inits mass input
        # self.labelMassInput = QLabel(self.widget)
        # self.labelMassInput.setGeometry(QtCore.QRect(360, 300, 150, 20))
        # self.labelMassInput.setObjectName("labelMassInput")
        # self.lineEditMassInput = QLineEdit(self.widget)
        # self.lineEditMassInput.setGeometry(QtCore.QRect(495, 290, 70, 40))
        # self.lineEditMassInput.setObjectName("lineEditMassInput")
        # self.lineEditMassInput.setText("0.00")
        # self.lineEditMassInputButton = QPushButton(self.widget)
        # self.lineEditMassInputButton.setGeometry(290,295,60,30)
        # self.lineEditMassInputButton.setText("Edit")
        # self.lineEditMassInputButton.clicked.connect(self.kbMass)

        #Inits desired pressure unit select
        self.targetPressureUnitCombobox = QComboBox(self.widget)
        self.targetPressureUnitCombobox.setGeometry(QtCore.QRect(585, 170, 70, 40)) # pos and size
        self.targetPressureUnitCombobox.setAutoFillBackground(False)
        self.targetPressureUnitCombobox.setEditable(False)
        self.targetPressureUnitCombobox.setObjectName("targetPressureUnitCombobox")
        self.targetPressureUnitCombobox.addItem("")
        self.targetPressureUnitCombobox.addItem("")

        #Inits STOP button
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(690, 110, 320, 80)) # pos and size
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(motor.stopRun)

        #Inits Home button
        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(860, 230, 140, 50)) # pos and size
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(motor.Home)

        #Inits Down button
        self.pushButton_5 = QPushButton(self.widget)
        self.pushButton_5.setGeometry(QtCore.QRect(690, 290, 140, 50)) # pos and size
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(lambda x: motor.jogDown(self.comboBox_5.currentIndex()))

        #Inits Up button
        self.pushButton_6 = QPushButton(self.widget)
        self.pushButton_6.setGeometry(QtCore.QRect(690, 230, 140, 50)) # pos and size
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(lambda x: motor.jogUp(self.comboBox_5.currentIndex()))

        #Inits Jogging box area
        self.groupBox_4 = QGroupBox(self.widget)
        self.groupBox_4.setGeometry(QtCore.QRect(810, 200, 300, 180)) # pos and size
        self.groupBox_4.setObjectName("groupBox_4")
        self.groupBox_4.setStyleSheet("""QGroupBox { font-weight: bold; font-size: 18px; color: #F9F6F0; border-radius: 8px;}""")

        #Inits jog step size select
        self.comboBox_5 = QComboBox(self.groupBox_4)
        self.comboBox_5.setGeometry(QtCore.QRect(60, 100, 100, 40)) # pos and size
        self.comboBox_5.setAutoFillBackground(False)
        self.comboBox_5.setEditable(False)
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.setStyleSheet("""font-size: 18px; font-weight: bold;""")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")

        #Inits program group box area
        self.groupBox_6 = QGroupBox(self.widget)
        self.groupBox_6.setGeometry(QtCore.QRect(680, 20, 300, 180)) # pos and size
        self.groupBox_6.setObjectName("groupBox_6")
        self.groupBox_6.setStyleSheet("""QGroupBox { font-weight: bold; font-size: 15px; color: #F9F6F0; border-radius: 8px;}""")

        #Inits pause button
        self.pushButton_3 = QPushButton(self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(800, 40, 100, 50)) # pos and size
        self.pushButton_3.setObjectName("pushButton_3")

        #Inits run button
        self.pushButton_4 = QPushButton(self.widget)
        self.pushButton_4.setGeometry(QtCore.QRect(690, 40, 320, 50)) # pos and size
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.runStartTimer)
        self.pushButton_4.clicked.connect(self.runMotor)

        #Inits resume button
        # self.pushButton_7 = QPushButton(self.widget)
        # self.pushButton_7.setGeometry(QtCore.QRect(910, 40, 100, 50)) # pos and size
        # self.pushButton_7.setObjectName("pushButton_7")
        # self.pushButton_7.clicked.connect(self.newLayer)

        # raise_() brings components to front layer
        self.groupBox_6.raise_()
        self.groupBox_4.raise_()
        self.frame.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_5.raise_()
        self.pushButton_6.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        # self.pushButton_7.raise_()

        # TAB 2 #

        #Inits tab 2
        self.tabWidget.addTab(self.widget, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tab_2.setStyleSheet("""QLabel {font-size: 20px; font-weight: bold;} QPushButton {font-size:18px; font-weight:bold}""")
        self.lcdNumber = QLCDNumber(self.tab_2)                     #VALUE DISPLAY ON TAB 3
        self.lcdNumber.setGeometry(QtCore.QRect(350, 70, 191, 51))
        self.lcdNumber.setObjectName("lcdNumber2")
        self.lcdNumber2 = QLCDNumber(self.tab_2)                     #VALUE DISPLAY ON TAB 3
        self.lcdNumber2.setGeometry(QtCore.QRect(350, 270, 191, 51))
        self.lcdNumber2.setObjectName("lcdNumber2")
        self.lcdNumber3 = QLCDNumber(self.tab_2)                     #VALUE DISPLAY ON TAB 3
        self.lcdNumber3.setGeometry(QtCore.QRect(350, 170, 191, 51))
        self.lcdNumber3.setObjectName("lcdNumber3")
        self.label_21 = QLabel(self.tab_2)
        self.label_21.setGeometry(QtCore.QRect(20, 70, 300, 51))
        self.label_tab2_pressure = QLabel(self.tab_2)
        self.label_tab2_pressure.setGeometry(QtCore.QRect(20, 270, 300, 51))
        self.label_tab2_pressure_units = QLabel(self.tab_2)
        self.label_tab2_pressure_units.setGeometry(QtCore.QRect(550, 270, 300, 51))
        self.label_tab2_force = QLabel(self.tab_2)
        self.label_tab2_force.setGeometry(QtCore.QRect(20, 170, 300, 51))
        self.label_tab2_force_units = QLabel(self.tab_2)
        self.label_tab2_force_units.setGeometry(QtCore.QRect(550, 170, 300, 51))
        self.label_tab2_load_units = QLabel(self.tab_2)
        self.label_tab2_load_units.setGeometry(QtCore.QRect(550, 70, 300, 51))
        self.pushButton_8 = QPushButton(self.tab_2)
        self.pushButton_8.setGeometry(QtCore.QRect(700, 280, 140, 30)) # Calibration Button
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.raise_() # -- Calibration Button

        font = QtGui.QFont()
        font.setPointSize(18)

        #Inits lcd display
        self.lcdNumber = QLCDNumber(self.tab_2)
        self.lcdNumber.setGeometry(QtCore.QRect(350, 70, 191, 51)) # pos and size
        self.lcdNumber.setObjectName("lcdNumber")

        #Inits lcd display 2
        self.lcdNumber2 = QLCDNumber(self.tab_2)
        self.lcdNumber2.setGeometry(QtCore.QRect(350, 270, 191, 51)) # pos and size
        self.lcdNumber2.setObjectName("lcdNumber2")

        #Inits load cell reading label
        self.label_21 = QLabel(self.tab_2)
        self.label_21.setGeometry(QtCore.QRect(20, 70, 300, 51)) # pos and size
        self.label_21.setObjectName("label_21")

        #Inits pressure reading label
        self.label_tab2_pressure = QLabel(self.tab_2)
        self.label_tab2_pressure.setGeometry(QtCore.QRect(20, 270, 300, 51)) # pos and size
        self.label_tab2_pressure.setObjectName("label_tab2_pressure")

        #Inits pressure reading units label
        self.label_tab2_pressure_units = QLabel(self.tab_2)
        self.label_tab2_pressure_units.setGeometry(QtCore.QRect(550, 270, 300, 51)) # pos and size
        self.label_tab2_pressure_units.setObjectName("label_tab2_pressure_units")

        #Inits load cell reading units label
        self.label_tab2_load_units = QLabel(self.tab_2)
        self.label_tab2_load_units.setGeometry(QtCore.QRect(550, 70, 300, 51)) # pos and size
        self.label_tab2_load_units.setObjectName("label_tab2_load_units")

        #Inits calibration button
        self.pushButton_8 = QPushButton(self.tab_2)
        self.pushButton_8.setGeometry(QtCore.QRect(700, 70, 140, 50)) # pos and size
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.raise_() # brings to front

        #Inits tare button
        self.tareButton = QPushButton(self.tab_2)
        self.tareButton.setGeometry(QtCore.QRect(700, 150, 140, 50)) # tare Button
        self.tareButton.setObjectName("tareButton")
        self.tareButton.raise_() # -- tare Button

        self.extractButton = QPushButton(self.tab_2)
        self.extractButton.setGeometry(700, 230, 140, 50)
        self.extractButton.setText("Extract")
        self.extractButton.clicked.connect(self.extractPiston)
        self.extractButton.clicked.connect(motor.cleanUp)
        self.extractButton.raise_()

        # TAB 3 #

        #Init tab 3
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")

        #Init data table area
        self.widget_2 = QWidget(self.tab_3)
        self.widget_2.setGeometry(QtCore.QRect(9, 9, 994, 350)) # pos and size
        self.widget_2.setObjectName("widget_2")

        #Inits refresh plot button
        # self.refreshButton = QPushButton(self.tab_3)
        # self.refreshButton.setGeometry(850, 190, 80, 30)
        # self.refreshButton.setObjectName("button_refresh")
        # self.refreshButton.clicked.connect(DB.getTable)

        self.plotForceCheckbox = QCheckBox(self.tab_3)
        self.plotForceCheckbox.setGeometry(850, 60, 160, 30)
        self.plotForceCheckbox.setText("Plot Force")
        self.plotForceCheckbox.setStyleSheet("""QCheckBox {font-weight: bold; font-size: 20 px; color: #fff;}""")

        self.plotPressureCheckbox = QCheckBox(self.tab_3)
        self.plotPressureCheckbox.setGeometry(850, 100, 160, 30)
        self.plotPressureCheckbox.setText("Plot Pressure")
        self.plotPressureCheckbox.setStyleSheet("""QCheckBox {font-weight: bold; font-size: 20 px; color: #fff;}""")

        self.plotPositionCheckBox = QCheckBox(self.tab_3)
        self.plotPositionCheckBox.setGeometry(850, 140, 160, 30)
        self.plotPositionCheckBox.setText("Plot Position")
        self.plotPositionCheckBox.setStyleSheet("""QCheckBox {font-weight: bold; font-size: 20 px; color: #fff;}""")

        self.clearButton = QPushButton(self.tab_3)
        self.clearButton.setGeometry(850, 240, 80, 30)
        self.clearButton.setObjectName("button_clear")
        self.clearButton.clicked.connect(self.clearPlot)

        self.exportButton = QPushButton(self.tab_3)
        self.exportButton.setGeometry(850, 290, 80, 30)
        self.exportButton.setObjectName("button_export")
        self.exportButton.clicked.connect(self.exportData)

        # TAB 4 #

        #Init tab 4
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")

        #Init communication box area
        self.groupBox_7 = QGroupBox(self.tab_4)
        self.groupBox_7.setGeometry(QtCore.QRect(10, 60, 400, 300)) # pos and size
        self.groupBox_7.setObjectName("groupBox_7")
        self.groupBox_7.setStyleSheet("""QGroupBox { font-weight: bold; font-size: 15px; color: #F9F6F0; border-radius: 8px;}""")

        #Init connection label
        self.connectionLabel = QLabel(self.groupBox_7)
        self.connectionLabel.setGeometry(QtCore.QRect(10, 30, 200, 20)) # pos and size
        self.connectionLabel.setObjectName("connectionLabel")

        #Init IP label
        self.ipLabel = QLabel(self.groupBox_7)
        self.ipLabel.setGeometry(QtCore.QRect(10, 60, 200, 20)) # pos and size
        self.ipLabel.setObjectName("ipLabel")

        #Init Connection IP label
        self.deviceIpLabel = QLabel(self.groupBox_7)
        self.deviceIpLabel.setGeometry(QtCore.QRect(10, 90, 500, 21)) # pos and size
        self.deviceIpLabel.setObjectName("deviceIpLabel")

        self.graphFrame = QFrame(self.tab_3)
        self.graphFrame.setGeometry(9,19,800,360)
        self.graphWidget = pg.PlotWidget(self.graphFrame)
        self.graphWidget.setGeometry(QtCore.QRect(9, 19, 800, 320)) # pos and size
        self.graphWidget.setBackground('w')

        
        self.time_x = [0]  # 100 time points
        self.force_vals = [0]
        self.pressure_vals = [0]
        self.position_vals = [0]
        self.weight_vals = [0]

        # self.graphLegend = self.graphWidget.addLegend()
        self.graphWidget.setTitle("Data Logging", size="16pt")
        self.graphWidget.showGrid(x=True, y=True)
        grayPen = pg.mkPen(color=(120, 120, 120), width=3)
        redPen = pg.mkPen(color=(255,   0,   0), width=3)
        blackPen = pg.mkPen(color=(255, 255, 255), width = 3)
        bluePen = pg.mkPen(color=(0,0,255), width=3)
        self.graphWidget.addItem(pg.InfiniteLine(pos=0, angle=0, pen=blackPen))
        self.forcePlot = self.graphWidget.plot(self.time_x, self.force_vals, name = 'Test Data', pen=grayPen)
        self.pressurePlot = self.graphWidget.plot(self.time_x, self.pressure_vals, name = 'Pressure', pen=redPen)
        self.positionPlot = self.graphWidget.plot(self.time_x, self.position_vals, name = 'Position', pen=grayPen)
        self.weightPlot = self.graphWidget.plot(self.time_x, self.weight_vals, name = 'Weight', pen=bluePen)

        self.startTime = time.monotonic()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.timeout.connect(self.checkKeyboard)
        self.timer.timeout.connect(self.checkHomed)
        self.timer.timeout.connect(self.updateCylinder)
        self.timer.timeout.connect(self.printAbsPos)
        self.timer.timeout.connect(self.newLayer)
        self.timer.start()

        # BOTTOM TAB #

        #Init Bottom Area frame
        self.tabWidget.addTab(self.tab_4, "")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 440, 1000, 261)) # pos and size
        self.frame_2.setObjectName("frame_2")

        #Init bottom box area
        self.groupBox = QGroupBox(self.frame_2)
        self.groupBox.setGeometry(QtCore.QRect(5, 0, 746, 600)) # pos and size
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setStyleSheet("""QGroupBox { font-weight: bold; font-size: 14px; color: #F9F6F0;} QLabel { font-weight: bold; font-size: 12px; }""")

        #Init table layout
        self.tableView = QTableView(self.groupBox)
        self.tableView.setGeometry(QtCore.QRect(10, 25, 735, 200)) # pos and size
        self.tableView.setObjectName("tableView")

        #Init Mode label
        self.Modelabel = QLabel(self.groupBox)
        self.Modelabel.setGeometry(QtCore.QRect(20, 65, 150, 20)) # pos and size
        self.Modelabel.setObjectName("Modelabel")
        self.ModeLineEdit = QLineEdit(self.groupBox)
        self.ModeLineEdit.setGeometry(70, 60, 130, 30)
        self.ModeLineEdit.setObjectName("ModeLineEdit")

        #Init system status label
        self.MotorLabel = QLabel(self.groupBox)
        self.MotorLabel.setGeometry(QtCore.QRect(20, 110, 150, 20)) # pos and size
        self.MotorLabel.setObjectName("label_2")
        self.MotorLineEdit = QLineEdit(self.groupBox)
        self.MotorLineEdit.setGeometry(70, 105, 130, 30)
        self.MotorLineEdit.setObjectName("MotorLineEdit")

        #Init mode label
        self.targetPressureLabel = QLabel(self.groupBox)
        self.targetPressureLabel.setGeometry(QtCore.QRect(220, 35, 150, 20)) # pos and size
        self.targetPressureLabel.setObjectName("targetPressureLabel")
        self.targetPressureLineEdit = QLineEdit(self.groupBox)
        self.targetPressureLineEdit.setGeometry(QtCore.QRect(350, 33, 60, 30))
        self.targetPressureLineEdit.setObjectName("targetPressureLineEdit")
        self.targetPressureLineEdit.setText(self.targetPressureInput.text())
        self.targetPressureLabelUnit = QLabel(self.groupBox)
        self.targetPressureLabelUnit.setGeometry(QtCore.QRect(415, 35, 30, 20)) # pos and size
        self.targetPressureLabelUnit.setObjectName("targetPressureLabelUnit")
        self.targetPressureLabelUnit.setText("kPa")

        #initial layer height label
        self.initLayerHeightLabel = QLabel(self.groupBox)
        self.initLayerHeightLabel.setGeometry(QtCore.QRect(470, 35, 150, 20))
        self.initLayerHeightLabel.setObjectName("initLayerHeightLabel")
        self.initLayerHeightLineEdit = QLineEdit(self.groupBox)
        self.initLayerHeightLineEdit.setGeometry(QtCore.QRect(630, 33, 60, 30))
        self.initLayerHeightLineEdit.setObjectName("initLayerHeightLineEdit")
        self.initLayerHeightLineEdit.setText(self.initLayerHeightInput.text())
        self.initLayerHeightUnitLabel = QLabel(self.groupBox)
        self.initLayerHeightUnitLabel.setGeometry(QtCore.QRect(695, 35, 30, 20))
        self.initLayerHeightUnitLabel.setText("mm")

        #Init layer count label
        self.layerCountLabel = QLabel(self.groupBox)
        self.layerCountLabel.setGeometry(QtCore.QRect(220, 110, 150, 20)) # pos and size
        self.layerCountLabel.setObjectName("layerCountLabel")
        self.layerCountLineEdit = QLineEdit(self.groupBox)
        self.layerCountLineEdit.setGeometry(QtCore.QRect(350, 105, 60, 30))
        self.layerCountLineEdit.setObjectName("initLayerCountLineEdit")
        self.layerCountLineEdit.setText("  __ / "+str(self.layerCountInput.text()))

        #Init desired position label
        self.compactedLayerHeightLabel = QLabel(self.groupBox)
        self.compactedLayerHeightLabel.setGeometry(QtCore.QRect(470, 72, 200, 20)) # pos and size
        self.compactedLayerHeightLabel.setObjectName("compactedLayerHeightLabel")
        self.compactedLayerHeightLineEdit = QLineEdit(self.groupBox)
        self.compactedLayerHeightLineEdit.setGeometry(QtCore.QRect(630, 69, 60, 30))
        self.compactedLayerHeightLineEdit.setObjectName("compactedLayerHeightLineEdit")
        self.compactedLayerHeightLineEdit.setText(self.compactedLayerHeightInput.text())
        self.compactedLayerHeightUnitLabel = QLabel(self.groupBox)
        self.compactedLayerHeightUnitLabel.setGeometry(QtCore.QRect(695, 69, 30, 20))
        self.compactedLayerHeightUnitLabel.setText("mm")

        #Init desired pressure label
        self.currentPressureLabel = QLabel(self.groupBox)
        self.currentPressureLabel.setGeometry(QtCore.QRect(220, 72, 200, 20)) # pos and size
        self.currentPressureLabel.setObjectName("currentPressureLabel")
        self.currentPressureLineEdit = QLineEdit(self.groupBox)
        self.currentPressureLineEdit.setGeometry(QtCore.QRect(350, 69, 60, 30))
        self.currentPressureLineEdit.setObjectName("currentPressureLineEdit")
        self.currentPressureLineEdit.setText(str(self.pressure_reading))
        self.currentPressureLabelUnit = QLabel(self.groupBox)
        self.currentPressureLabelUnit.setGeometry(QtCore.QRect(415, 72, 30, 20)) # pos and size
        self.currentPressureLabelUnit.setObjectName("currentPressureLabelUnit")
        self.currentPressureLabelUnit.setText("kPa")

        #Init current pressure label
        self.currentLayerHeightLabel = QLabel(self.groupBox)
        self.currentLayerHeightLabel.setGeometry(QtCore.QRect(470, 110, 220, 20)) # pos and size
        self.currentLayerHeightLabel.setObjectName("currentLayerHeightLabel")
        self.currentLayerHeightLineEdit = QLineEdit(self.groupBox)
        self.currentLayerHeightLineEdit.setGeometry(QtCore.QRect(630, 105, 60, 30))
        self.currentLayerHeightLineEdit.setObjectName("currentlayerHeightLineEdit")
        self.currentLayerHeightLineEdit.setText(" - - - - ")
        self.currentLayerHeightUnitLabel = QLabel(self.groupBox)
        self.currentLayerHeightUnitLabel.setGeometry(QtCore.QRect(695, 105, 30, 20))
        self.currentLayerHeightUnitLabel.setText("mm")

        #center main window with status bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        #run class fnc to annotate labels properly
        self.retranslateUi(MainWindow)

        #set default index of GUI to tab 0
        self.tabWidget.setCurrentIndex(0)
        self.cylinder = QPixmap('Cylinder.png')
        self.cylinder2 = self.cylinder.scaled(280, 150, QtCore.Qt.KeepAspectRatio) # Logo
        self.cylinderlabel = QLabel(self.frame)
        self.cylinderlabel.setPixmap(self.cylinder2)
        self.cylinderlabel.setStyleSheet("background-color: transparent;")
        self.cylinderlabel.setGeometry(800,395,200,200)
        self.cylinderStart = QPixmap('start.png')
        self.cylinder2Start = self.pixmap.scaled(280, 150, QtCore.Qt.KeepAspectRatio) # Logo
        self.cylLabelStart = QLabel(self.frame)
        self.cylLabelStart.setStyleSheet("background-color: transparent;")
        self.cylLabelStart.setPixmap(self.cylinderStart)
        self.cylLabelStart.setGeometry(793,490,200,100)

        # self.cylinderEnd = QPixmap('end.png')
        # self.cylinder2End = self.pixmap.scaled(280, 150, QtCore.Qt.KeepAspectRatio) # Logo
        # self.cylLabelEnd = QLabel(self.frame)
        # self.cylLabelEnd.setStyleSheet("background-color: transparent;")
        # self.cylLabelEnd.setPixmap(self.cylinderEnd)
        # self.cylLabelEnd.setGeometry(793,470,200,100)

        #routing slots by name
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Annotate Labels and Components

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Vulcan Labs", "Vulcan Labs"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Mode Selection"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Motion Limiting"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Pressure Limiting"))
        self.initLayerHeightUnitCombobox.setItemText(0, _translate("MainWindow", "mm"))
        self.initLayerHeightUnitCombobox.setItemText(1, _translate("MainWindow", "μm"))
        self.label_9.setText(_translate("MainWindow", "Initial Layer"))
        self.label_91.setText(_translate("MainWindow", "Height"))
        self.compactedLayerHeightComboBox.setItemText(0, _translate("MainWindow", "mm"))
        self.compactedLayerHeightComboBox.setItemText(1, _translate("MainWindow", "μm"))
        self.label_10.setText(_translate("MainWindow", "Compacted"))
        self.label_101.setText(_translate("MainWindow", "Layer Height"))
        self.label_11.setText(_translate("MainWindow", "Number"))
        self.label_111.setText(_translate("MainWindow", "Of Layers"))
        self.label_12.setText(_translate("MainWindow", "Target"))
        self.label_121.setText(_translate("MainWindow", "Pressure"))
        self.targetPressureUnitCombobox.setItemText(0, _translate("MainWindow", "kPa"))
        self.targetPressureUnitCombobox.setItemText(1, _translate("MainWindow", "MPa"))
        self.pushButton.setText(_translate("MainWindow", "STOP"))
        self.pushButton_2.setText(_translate("MainWindow", "Home"))
        self.pushButton_8.setText(_translate("MainWindow", "Calibrate"))
        self.tareButton.setText(_translate("MainWindow", "Tare"))
        self.pushButton_5.setText(_translate("MainWindow", "Down"))
        self.pushButton_6.setText(_translate("MainWindow", "Up"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Jogging"))
        self.comboBox_5.setItemText(0, _translate("MainWindow", "1 mm"))
        self.comboBox_5.setItemText(1, _translate("MainWindow", "5 mm"))
        self.comboBox_5.setItemText(2, _translate("MainWindow", "10 mm"))
        self.groupBox_6.setTitle(_translate("MainWindow", ""))
        self.pushButton_3.setText(_translate("MainWindow", "Pause"))
        self.pushButton_4.setText(_translate("MainWindow", "Run"))
        # self.pushButton_7.setText(_translate("MainWindow", "Resume"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("MainWindow", "Control"))
        self.label_21.setText(_translate("MainWindow", "Load Cell Reading:"))
        self.label_tab2_pressure.setText(_translate("MainWindow", "Current Pressure:"))
        self.label_tab2_pressure_units.setText(_translate("MainWindow", " kPa"))
        self.label_tab2_force.setText(_translate("MainWindow", "Current Force:"))
        self.label_tab2_force_units.setText(_translate("MainWindow", " N"))
        self.label_tab2_load_units.setText(_translate("MainWindow", " kg"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "System"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Data"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Communication"))
        self.connectionLabel.setText(_translate("MainWindow", "Connection: "+str(motor.connectionStatus)))
        self.ipLabel.setText(_translate("MainWindow", "System IP: "+self.IpAdd))
        self.deviceIpLabel.setText(_translate("MainWindow", "Connected Device IP:"+str(motor.SERVER_HOST)))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Configuration"))
        self.groupBox.setTitle(_translate("MainWindow", "System State"))
        self.Modelabel.setText(_translate("MainWindow", "Mode: "))
        self.MotorLabel.setText(_translate("MainWindow", "Motor: "))
        self.targetPressureLabel.setText(_translate("MainWindow", "Target Pressure: "))
        self.initLayerHeightLabel.setText(_translate("MainWindow", "Initial Layer Height: "))
        self.layerCountLabel.setText(_translate("MainWindow", "Layer: "))
        self.compactedLayerHeightLabel.setText(_translate("MainWindow", "Compacted Layer Height: "))
        self.currentPressureLabel.setText(_translate("MainWindow", "Current Pressure: "))
        self.currentLayerHeightLabel.setText(_translate("MainWindow", "Current Layer Height: "))
        # self.refreshButton.setText(_translate("MainWindow", "Refresh"))
        self.clearButton.setText(_translate("MainWindow", "Clear"))
        self.exportButton.setText(_translate("MainWindow", "Export"))
        # self.labelMassInput.setText(_translate("MainWindow", "Mass [kg]"))

        # -- ROUTING -- #

        # Calibration Button
        self.pushButton_8.clicked.connect(self.Calibration) #cellInstance.user

        # Tare Button
        self.tareButton.clicked.connect(self.tare) #### CHANGE TO TARE FUNCTION ###

        # Update Mode after selection
        self.comboBox.currentIndexChanged.connect(self.updateMode)
        self.comboBox.currentIndexChanged[int].connect(self.disableWidget)

        # Update desired parameters
        self.targetPressureInput.textChanged.connect(self.updateDesiredParam)
        self.initLayerHeightInput.textChanged.connect(self.updateDesiredParam)
        self.compactedLayerHeightInput.textChanged.connect(self.updateDesiredParam)
        self.layerCountInput.textChanged.connect(self.updateDesiredParam)
        # self.lineEditMassInput.textChanged.connect(self.updateDesiredParam)
        self.comboBox.currentIndexChanged.connect(self.updateDesiredParam)
        self.initLayerHeightUnitCombobox.currentIndexChanged.connect(self.updateDesiredParam)
        self.compactedLayerHeightComboBox.currentIndexChanged.connect(self.updateDesiredParam)
        self.targetPressureUnitCombobox.currentIndexChanged.connect(self.updateDesiredParam)
        self.comboBox_5.currentIndexChanged.connect(self.updateDesiredParam)
        self.targetPressureUnitCombobox.currentIndexChanged.connect(self.updateDesiredParam)

        # System state changes
        self.pushButton_4.clicked.connect(lambda x: self.updateSystemState(2)) #running
        # self.pushButton_4.clicked.connect(lambda x: self.setWorker(self.execute_this_fn)) #running
        self.pushButton_3.clicked.connect(lambda X: self.updateSystemState(3)) #Paused
        # self.pushButton_7.clicked.connect(lambda X: self.updateSystemState(2)) #running
        self.pushButton.clicked.connect(lambda x: self.updateSystemState(4))   #Stopped
        # 0:idle 1:Starting 2:Running 3:Paused 4:Stopped 5:Processing

        self.checkCalibration()
        self.checkMotorConnection()
        self.checkHomed()
        self.updateMode()
        self.disableWidget(self.comboBox.currentIndex())

    def kbLayer(self):
        kb.show()

    def kbCompacted(self):
        kb2.show()

    def kbPressure(self):
        kb3.show()

    def kbLayerCount(self):
        kb4.show()

    def kbMass(self):
        kb5.show()

    def kbWeight(self):
        kb6.show()

    def kbMassNext(self):
        kb7.show()

    def printAbsPos(self):
        # print(f'abs pos: {motor.absolutePosition}')
        self.warningLabel.setText(str(motor.absolutePosition))

    def checkKeyboard(self):
        if kb.okCheck == 1:
            self.initLayerHeightInput.setText(kb.inputString)
            kb.okCheck = 0
        elif kb2.okCheck == 1:
            self.compactedLayerHeightInput.setText(kb2.inputString)
            kb2.okCheck = 0
        elif kb3.okCheck == 1:
            self.targetPressureInput.setText(kb3.inputString)
            kb3.okCheck = 0
        elif kb4.okCheck == 1:
            self.layerCountInput.setText(kb4.inputString)
            kb4.okCheck = 0
        # elif kb5.okCheck == 1:
            # self.lineEditMassInput.setText(kb5.inputString)
            # kb5.okCheck = 0
        elif kb6.okCheck == 1:
            self.dialog.inputWeight.setText(kb6.inputString)
        elif kb7.okCheck == 1:
            self.nL.input.setText(kb7.inputString)

    def extractPiston(self):
        self.msg = QMessageBox()
        self.msg.setStyleSheet("font-size: 16 px;")
        self.msg.setWindowTitle("Extraction Warning")
        self.msg.setText("Sliding plate must be removed before proceeding with extraction. \n\nSelect Ok when plate is removed.")
        self.msg.setIcon(QMessageBox.Question)
        self.msg.setStandardButtons(QMessageBox.Close|QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.buttonClick)

        x = self.msg.exec_()

    def newLayer(self):
        if motor.massInput == True:
            self.nL = newLayer()
            self.nL.show()
            motor.massInput = False
        else:
            pass
            

    def sendMassData(self):
        self.mass = self.nL.input.text()
        motor.mass = self.mass
        motor.massIn = True
        print("0000: ",self.mass)
        motor.motionRun()
        
    def massDialog(self):
        text = QtGui.QInputDialog.getText(self, 'Powder', 'Enter mass of layer:')    
        # QInputDialog. self.kbMmassNext()
        QInputDialog.QLineEdit.setText("87878787")
        # if text[1]:
        #     massOfLayer = text[0]
        #     self.mass = massOfLayer
        #     motor.mass = self.mass

    def buttonClick(self,button):
        print(button,button.text())
        if button.text() == 'OK':
            print("cleaning up")
            motor.cleanUp()
        if button.text() == 'Close':
            print("cancelled")
            self.msg.close()
        else:
            print('nothing matched')

    def mm2cylinder(self,mm):
        cylinderPosition = math.floor(mm*3.66)
        return cylinderPosition

    def updateCylinder(self):
        pos = self.mm2cylinder(motor.absolutePosition)
        # pos = self.mm2cylinder(30)
        self.cylLabelStart.setGeometry(793,520-pos,200,100)
        # self.cylLabelEnd.setGeometry(793,520,200,100)
    
    def checkMotorConnection(self):
        if motor.connectionStatus == 0:
            self.MotorLineEdit.setText("Not Connected")
        else:
            self.MotorLineEdit.setText("Connected")

    def runMotor(self):
        self.updateCylinder()

        if self.modeSelected == 1: #motion limiting
            motor.initLayerHeight = self.initLayerHeight
            motor.compactedLayerHeight = self.compactedLayerHeight
            motor.numberOfLayers = self.numberOfLayers
            motor.mass = self.mass
            motor.modeSelected = self.modeSelected

        elif self.modeSelected == 2: #pressure limiting
            motor.modeSelected = self.modeSelected
            motor.targetPressure = self.targetPressure
            motor.numberOfLayers = self.numberOfLayers
            motor.mass = self.mass

        print(f'mode selected: {motor.modeSelected},ilh: {motor.initLayerHeight}, compaction: {motor.compactedLayerHeight}, targPress: {motor.targetPressure}, #ofLayers: {motor.numberOfLayers}, mass: {motor.mass}')
        motor.run()

    def disableWidget(self,currentIndex):
        print(currentIndex)

        if currentIndex == 0:
            """no mode selected"""
            self.initLayerHeightInput.setEnabled(False)
            self.compactedLayerHeightInput.setEnabled(False)
            self.label_9.setEnabled(False)
            self.label_91.setEnabled(False)
            self.label_10.setEnabled(False)
            self.label_101.setEnabled(False)
            self.label_12.setEnabled(False)
            self.label_121.setEnabled(False)
            self.targetPressureInput.setEnabled(False)
            self.initLayerHeightUnitCombobox.setEnabled(False)
            self.editLayerHeightButton.setEnabled(False)
            self.compactedLayerHeightButton.setEnabled(False)
            self.targetPressureButton.setEnabled(False)
            self.compactedLayerHeightComboBox.setEnabled(False)
            self.targetPressureUnitCombobox.setEnabled(False)
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            # self.pushButton_7.setEnabled(False)
        elif currentIndex == 1:
            """motion widgets enabled, pressure widgets disabled"""
            self.initLayerHeightInput.setEnabled(True)
            self.compactedLayerHeightInput.setEnabled(True)
            self.label_9.setEnabled(True)
            self.label_91.setEnabled(True)
            self.label_10.setEnabled(True)
            self.label_101.setEnabled(True)
            self.label_12.setEnabled(False)
            self.label_121.setEnabled(False)
            self.targetPressureInput.setEnabled(False)
            self.initLayerHeightUnitCombobox.setEnabled(True)
            self.compactedLayerHeightComboBox.setEnabled(True)
            self.targetPressureUnitCombobox.setEnabled(False)
            self.editLayerHeightButton.setEnabled(True)
            self.compactedLayerHeightButton.setEnabled(True)
            self.targetPressureButton.setEnabled(False)
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            # self.pushButton_7.setEnabled(True)
        elif currentIndex == 2:
            '''reverse'''
            self.initLayerHeightInput.setEnabled(False)
            self.compactedLayerHeightInput.setEnabled(False)
            self.label_9.setEnabled(False)
            self.label_91.setEnabled(False)
            self.label_10.setEnabled(False)
            self.label_101.setEnabled(False)
            self.label_12.setEnabled(True)
            self.label_121.setEnabled(True)
            self.targetPressureInput.setEnabled(True)
            self.initLayerHeightUnitCombobox.setEnabled(False)
            self.compactedLayerHeightComboBox.setEnabled(False)
            self.targetPressureUnitCombobox.setEnabled(True)
            self.editLayerHeightButton.setEnabled(False)
            self.compactedLayerHeightButton.setEnabled(False)
            self.targetPressureButton.setEnabled(True)
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            # self.pushButton_7.setEnabled(True)

    def keyboardPopUp(self):
        kb.show()

    def checkHomed(self):
        homed = motor.homed
        # homed = 1
        if homed == 1:
            self.warningLabel.setText("")
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            # self.pushButton_7.setEnabled(True)
        elif homed == 0:
            self.warningLabel.setText("CAUTION: Home Device")
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            # self.pushButton_7.setEnabled(False)

    def tare(self):
        cellInstance.zeroCell()

    def runStartTimer(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.runStartTime = current_time
        print(f'run started at time: {self.runStartTime}')

    def plotState(self,b):
        if b.text() == 'Plot Force':
            if b.isChecked() == True:
                DB.getTable('force',1)
        if b.text() == 'Plot Force':
            if b.isChecked() == False:
                DB.getTable('force',0)
        if b.text() == 'Plot Pressure':
            if b.isChecked() == True:
                DB.getTable('pressure',1)
        if b.text() == 'Plot Pressure':
            if b.isChecked() == False:
                DB.getTable('pressure',0)
        if b.text() == 'Plot Weight':
            if b.isChecked() == True:
                DB.getTable('weight',1)
        if b.text() == 'Plot Weight':
            if b.isChecked() == False:
                DB.getTable('weight',0)

    def updateMode(self):
        mode = self.comboBox.currentIndex()
        if mode == 1:
            self.modeSelected = 1
            self.ModeLineEdit.setText("Motion")
        elif mode == 2:
            self.modeSelected = 2
            self.ModeLineEdit.setText("Pressure")
        else:
            self.modeSelected = 0
            self.ModeLineEdit.setText("  - - - - -")

    def UpdateForceReadingValue(self):
        """Updates the LCD Force Reading Value"""
        # force_reading_raw = random.random()
        force_reading_raw = cellInstance.cell.get_weight_mean(4)    #5 recomended for accuracy
        self.force_reading_raw = force_reading_raw
        if force_reading_raw < 0:
            force_reading_raw = 0
        force_reading_kg = round(force_reading_raw,3)            #(grams to kg)
        self.force_reading_kg = force_reading_kg
        # pressure = MQtt()
        # pressure.publish(force_reading_kg,"force")
        force_reading_N = round(force_reading_kg*9.81,3)
        self.force_reading_N = force_reading_N
        pistonDiameter = 19.05 #mm
        r = pistonDiameter/2 #mm
        r_m = r/1000    # [m]
        Area = math.pi*math.pow(r_m,2)
        pressure_reading = round((force_reading_N/Area)/1000,3)  #Kpa
        self.pressure_reading = pressure_reading

        self.lcdNumber.display(force_reading_kg)
        DB.insert_value('weight', force_reading_kg)
        self.lcdNumber2.display(pressure_reading)
        DB.insert_value('pressure', pressure_reading)
        self.lcdNumber3.display(force_reading_N)
        DB.insert_value('force', force_reading_N)
        self.update()

    def Calibration(self):
        self.dialog = calibrationDialogWindow()
        self.dialog.show()

    def checkCalibration(self):
        if cellInstance.calibrated == 1:
            pass
        else:
            self.calibrationWarn()

    def calibrationWarn(self):
        self.dialog2 = calibrationWarning()
        self.dialog2.raise_()
        self.dialog2.show()

    def UpdateGUI(self):
        self.UpdateForceReadingValue()

    def clearPlot(self):
        self.force_vals = []
        self.pressure_vals = []
        self.weight_vals = []
        self.time_x = []

    def update_plot_data(self):
        self.time_x.append(time.time() - self.StartingTime)   # Add a new value 1 higher than the last.
        self.force_vals.append(self.force_reading_N)
        self.force_vals_fixed = signal.medfilt(self.force_vals,33)
        self.pressure_vals.append(self.pressure_reading)
        self.pressure_vals_fixed = signal.medfilt(self.pressure_vals,33)
        self.weight_vals.append(self.force_reading_kg)
        self.position_vals.append(motor.absolutePosition)
        self.currentPressureLineEdit.setText(str(np.round(self.pressure_reading,2)))

        if self.plotForceCheckbox.isChecked():
            self.forcePlot.setData(self.time_x, self.force_vals_fixed)
        else:
            self.forcePlot.clear()
        if self.plotPressureCheckbox.isChecked():
            self.pressurePlot.setData(self.time_x, self.pressure_vals_fixed)
        else:
            self.pressurePlot.clear()
        if self.plotPositionCheckBox.isChecked():
            self.positionPlot.setData(self.time_x, self.position_vals)
        else:
            self.positionPlot.clear()

    def updateSystemState(self,index):
        self.systemState = int(index)
        indices = {
            0: "Idle",
            1: "Starting",
            2: "Running",
            3: "Paused",
            4: "Stopped",
            5: "Processing",
            6: "Homed"
        }

    def updateDesiredParam(self):
        
        self.initLayerHeightLineEdit.setText(self.initLayerHeightInput.text())
        self.initLayerHeightVal = self.initLayerHeightInput.text()
        self.initLayerHeightUnit = self.initLayerHeightUnitCombobox.currentIndex()
        self.initLayerHeightUnitLabel.setText(self.initLayerHeightUnitCombobox.currentText())
        self.initLayerHeight = [float(self.initLayerHeightVal),self.initLayerHeightUnit]

        self.compactedLayerHeightLineEdit.setText(self.compactedLayerHeightInput.text())
        self.compactedLayerHeightVal = self.compactedLayerHeightInput.text()
        self.compactedLayerHeightUnit = self.compactedLayerHeightComboBox.currentIndex()
        self.compactedLayerHeight = [float(self.compactedLayerHeightVal),self.compactedLayerHeightUnit]
        self.compactedLayerHeightUnitLabel.setText(self.compactedLayerHeightComboBox.currentText())

        self.targetPressureLineEdit.setText(self.targetPressureInput.text())
        self.targetPressureLabelUnit.setText(self.targetPressureUnitCombobox.currentText())
        self.targetPressureVal = self.targetPressureInput.text()
        self.targetPressureUnit = self.targetPressureUnitCombobox.currentIndex()
        self.targetPressure = [float(self.targetPressureVal),self.targetPressureUnit]
        
        self.layerCountLineEdit.setText("  __ / "+str(self.layerCountInput.text()))
        self.numberOfLayers = int(self.layerCountInput.text())
        
        # self.mass = float(self.lineEditMassInput.text())

        if self.compactedLayerHeightUnit == 0:
            runStroke = self.compactedLayerHeight[0]*0.001
            totalStroke = runStroke*self.numberOfLayers
        if self.compactedLayerHeightUnit == 1:
            runStroke = (self.compactedLayerHeight[0]*0.00001)
            totalStroke = runStroke*self.numberOfLayers
        if totalStroke > 0.03:
            self.warningLabel.setText("WARNING: Reached max stroke length. Lower 'Initial Layer Height', 'Compacted Layer Height', or 'Layer Count'.")
            self.pushButton_4.setEnabled(False)
        else:
            self.pushButton_4.setEnabled(True)
            self.warningLabel.setText("")

    def exportData(self):
        d = {'Time':self.time_x,'Force [N]':self.force_vals,'Pressure [kPa]':self.pressure_vals,'Position [mm]':self.position_vals}
        df = pd.DataFrame(d)
        df.to_csv('/media/pi/VULCANLABS/log.csv', index=False)

class newLayer(QWidget):
    def __init__(self):
        super().__init__()
        mainWin.kbMassNext()
        self.resize(300,200)
        self.cancel_button = QPushButton('Cancel')
        # self.next_button = QPushButton('Next')
        self.input = QLineEdit()
        self.submit_button = QPushButton('Submit')
        # self.finish_button = QPushButton('Finish')
        self.dialogText = QLabel('\n\n New Layer Parameters:\n\n\n\n1. Place powder in cylinder\n\n2. Record mass of additional powder below:\n\n')
        # self.warningText = QLabel('\n\nWarning: Continuing will pause the program')
        self.setWindowTitle('Layering')
        self.setStyleSheet('background-color: #fff; color: #202020; font-size: 16px; QPushButton { background-color: #fff }')

        # #Initializes layout
        self.setLayout(QFormLayout())
        self.layout().addRow(self.dialogText)
        self.layout().addRow(self.input)
        buttons = QWidget()
        buttons.setLayout(QHBoxLayout())
        buttons.layout().addWidget(self.cancel_button)
        buttons.layout().addWidget(self.submit_button)
        self.layout().addRow('', buttons)
        # self.layout().addRow('',self.warningText)

        # #Routes front end to back end
        # self.input.setText("8998989898")
        # mainWin.mass = self.input.text()
        # a = self.input.text()
        # b = self.input.value()
        # print("A",a)
        # print("B",b)
        # self.next_button.clicked.connect(self.getInputWindow)
        self.submit_button.clicked.connect(mainWin.sendMassData)
        self.submit_button.clicked.connect(self.close)
        self.cancel_button.clicked.connect(self.close)

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

class WorkerThread(QThread):
    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)

    def run(self):
        time.sleep(3)
        self.emit(SIGNAL('threadDone()'))
 
class loadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300,200)
        self.dialog = QLabel("Running...")

        self.setLayout(QFormLayout())
        self.layout().addRow(self.dialog)

class removePlatePopUp(QWidget):
    def __init__(self):
        super().__init__()
        self.ok_button = QPushButton('Ok')
        self.cancel_button = QPushButton('Cancel')
        self.dialog = QLabel("Remove Sliding Plate before proceeding with extraction.\n\n Select Ok when plate is removed.")
        self.setWindowTitle('WARNING')

        self.setLayout(QFormLayout())
        self.layout().addRow(self.dialog)
        buttons = QWidget()
        buttons.setLayout(QHBoxLayout())
        buttons.layout().addWidget(self.ok_button)
        buttons.layout().addWidget(self.cancel_button)
        self.layout().addRow('', buttons)

        #Routes front end to back end
        self.cancel_button.clicked.connect(self.close)
        self.ok_button.clicked.connect(motor.cleanUp)
        self.ok_button.clicked.connect(self.close)

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
        self.layout().addRow('', buttons)

        #Routes front end to back end
        self.ok_button.clicked.connect(self.close)
        self.cal_button.clicked.connect(Ui_MainWindow.Calibration)

#Class handling calibration pop up boxes
class calibrationDialogWindow(QWidget): # this one
    def __init__(self):
        super().__init__()
        self.resize(300,200)
        self.cancel_button = QPushButton('Cancel')
        self.next_button = QPushButton('Next')
        self.submit_button = QPushButton('Submit')
        self.finish_button = QPushButton('Finish')
        self.dialogText = QLabel('\n\n Calibration requires:\n\n    - Device is at Home Position\n\n    - An object of known weight\n\n    - Top plate removed from machine\n\n\nOnce all conditions are met press next to proceed')
        self.warningText = QLabel('\n\nWarning: Continuing will pause the program')
        self.setWindowTitle('Calibration')
        self.setStyleSheet('background-color: #fff; color: #202020; font-size: 16px; QPushButton { background-color: #fff }')

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
        self.next_button.clicked.connect(mainWin.kbWeight)
        self.cancel_button.clicked.connect(self.close)
            
    def collectingDataWindow(self):
        self.close()
        self.setWindowTitle('Calibration 3')
        for i in reversed(range(self.layout().count())):        #Clears components from first window
            self.layout().itemAt(i).widget().deleteLater()
        self.dialogText = QLabel('Initializing...')
        self.layout().addRow('',self.dialogText)
        self.show()
        while cellInstance.initializing == 1:
            self.dialogText = QLabel('Initializing.')
            time.sleep(1)
            self.dialogText = QLabel('Initializing..')
            time.sleep(1)
            self.dialogText = QLabel('Initializing...')
        self.close()



    #Second window in calibration branch
    def getInputWindow(self):
        for i in reversed(range(self.layout().count())):        #Clears components from first window
            self.layout().itemAt(i).widget().deleteLater()
        self.dialogText = QLabel('Raising...')
        self.warningText = QLabel('Please Wait')
        self.layout().addRow('',self.dialogText)
        self.layout().addRow('',self.warningText)
        self.show()
        time.sleep(0.2)
        motor.cleanUp()
        while motor.topFlag == False:
            self.dialogText.setText("running.")
            time.sleep(1)
            self.dialogText.setText("running..")
            time.sleep(1)
            self.dialogText.setText("running...")
        self.knownGrams = 0
        for i in reversed(range(self.layout().count())):        #Clears components from first window
            self.layout().itemAt(i).widget().deleteLater()
        self.dialogText = QLabel('Place object of known weight on scale and enter weight [kg]: ')
        self.inputWeight = QLineEdit()
        buttons = QWidget()
        buttons.setLayout(QHBoxLayout())
        buttons.layout().addWidget(self.cancel_button)
        buttons.layout().addWidget(self.submit_button)
        self.layout().addRow('',self.dialogText)
        self.layout().addRow('',self.inputWeight)
        self.layout().addRow('',buttons)
        self.show()

        self.inputWeight.textChanged.connect(self.setKnownGrams)
        self.submit_button.clicked.connect(self.sendKnownInput)
        self.cancel_button.clicked.connect(self.close)

    def setKnownGrams(self,lineEdit):
        self.knownGrams = self.inputWeight.text()

    def startCalibration(self):
        cellInstance.userCalibrationPart1()

    #Sends known weight from user to Load cell calibration
    def sendKnownInput(self):
        self.close()
        self.setWindowTitle('Calibration 3')
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().deleteLater()
        print(f'user inputted value: {self.knownGrams}')
        self.dialogText = QLabel('Calibration Complete.')
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
        screen = loadingScreen()
        screen.show()
        while motor.top == False:
            loadingScreen.dialog.setText('loading.')
            time.sleep(1)
            loadingScreen.dialog.setText('loading..')
            time.sleep(1)
            loadingScreen.dialog.setText('loading...')

        self.next_button.clicked.connect(self.getInputWindow)
        self.next_button.clicked.connect(self.startCalibration)
        self.next_button.clicked.connect(self.collectingDataWindow)

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

        print(f'raw_data_mean: {self.reading}, predicted ratio = {self.reading/198}')

        print('getting initial data...')

        self.initializing = 0


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

    def zeroCell(self):
        self.cell.zero()
        self.tare = 1 

        print("Calibration is succesful")

if __name__ == '__main__':
    motor = Motor()
    cellInstance = LoadCell()
    DB = sqlDatabase()
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    kb = VirtualKeyboard()
    kb2 = VirtualKeyboard2()
    kb3 = VirtualKeyboard3()
    kb4 = VirtualKeyboard4()
    kb5 = VirtualKeyboard5()
    kb6 = VirtualKeyboard6()
    kb7 = VirtualKeyboard7()
    mainWin = Ui_MainWindow()
    ld = loadingScreen()
    styleFile=os.path.join(os.path.split(__file__)[0],"styleVulcan.stylesheet")
    styleSheetStr = open(styleFile,"r").read()
    mainWin.setStyleSheet(styleSheetStr)
    mainWin.show()

    fps = 3
    timer = QtCore.QTimer()
    timer.timeout.connect(mainWin.UpdateGUI)
    timer.setInterval(int(1000/fps))
    timer.start()

    sys.exit(app.exec_())
