#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################

import math
import time
import timeit
import random
import sys
import os
import pickle
import socket
# import RPi.GPIO as GPIO #import I/O interface
# from hx711 import HX711 #import HX711 class
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import (QSizePolicy,
        QWidget, QFrame)
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLayout, 
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QStatusBar, QTabWidget, QLCDNumber, QTableWidget, QTableWidgetItem, QTableView, QMainWindow, QMessageBox)

# Main window containing all GUI components
class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupGlobalVars()
        self.setupUi()

    def setupGlobalVars(self):
        self.modeSelected = 0                                   # 0:motion 1:pressure
        self.connectionState = 0                                # 0:No Connection 1:Connection Secure
        self.IpAdd = socket.gethostbyname(socket.gethostname())
        self.systemState = 0                                    # 0:idle 1:Starting 2:Running 3:Paused 4:Stopped 5:Processing
        self.systemCalibrated = 0                               # 0: no 1: calibrated
        # self.elapsedTime = time.perf_counter()

        self.desPos = 0
        self.desPress = 0
        self.curPos = 0
        self.curPress = 0

    def setupUi(self):

        # -- INITIALIZATION -- #

        #Initializes window and parameters
        MainWindow = self
        MainWindow.setObjectName("Vulcan Labs")
        MainWindow.resize(1024, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(9, 9, 1024, 600))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")

        #Initializes tab layout
        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1004, 420))
        self.tabWidget.setObjectName("tabWidget")

        # TAB 1 #

        #Inits box area on left
        self.widget = QWidget()
        self.widget.setObjectName("widget")
        self.groupBox_2 = QGroupBox(self.widget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 20, 300, 360)) # positioning and sizing
        self.groupBox_2.setObjectName("groupBox_2")

        #Inits Mode select dropdown component
        self.comboBox = QComboBox(self.groupBox_2)
        self.comboBox.setGeometry(QtCore.QRect(20, 40, 200, 30)) # positioning and sizing
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        #Inits Logo
        self.pixmap = QPixmap('VulcanLabsLogo.png')
        self.pixmap2 = self.pixmap.scaled(260, 200, QtCore.Qt.KeepAspectRatio) # Logo
        self.labelLogo = QLabel(self.groupBox_2)
        self.labelLogo.setPixmap(self.pixmap2)
        self.labelLogo.setGeometry(20,80,300,300)

        #Inits window icon as logo
        self.setWindowIcon(QtGui.QIcon('3DPrinterLogo.png')) # Logo as Icon
        # self.setStyleSheet("background-color: rgb(255, 255, 255)") #Sets background color of GUI

        #Inits Parameter Group Box
        self.groupBox_3 = QGroupBox(self.widget)
        self.groupBox_3.setGeometry(QtCore.QRect(350, 20, 300, 360)) # positioning and sizing
        self.groupBox_3.setObjectName("groupBox_3")

        #Inits initial layer height input
        self.lineEdit = QLineEdit(self.groupBox_3)
        self.lineEdit.setGeometry(QtCore.QRect(160, 40, 60, 30)) # pos and size
        self.lineEdit.setObjectName("lineEdit")

        #Inits initial layer height unit select
        self.comboBox_2 = QComboBox(self.groupBox_3)
        self.comboBox_2.setGeometry(QtCore.QRect(230, 40, 60, 30)) # pos and size
        self.comboBox_2.setAutoFillBackground(False)
        self.comboBox_2.setEditable(False)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")

        #Inits initial layer height label
        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setGeometry(QtCore.QRect(20, 40, 130, 20)) # pos and size
        self.label_9.setObjectName("label_9")

        #Inits final layer height unit select
        self.comboBox_3 = QComboBox(self.groupBox_3)
        self.comboBox_3.setGeometry(QtCore.QRect(230, 100, 60, 30)) # pos and size
        self.comboBox_3.setAutoFillBackground(False)
        self.comboBox_3.setEditable(False)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")

        #Inits final layer height input
        self.lineEdit_2 = QLineEdit(self.groupBox_3)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 100, 60, 30)) # pos and size
        self.lineEdit_2.setObjectName("lineEdit_2")

        #Inits final layer label
        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setGeometry(QtCore.QRect(20, 100, 150, 20)) # pos and size
        self.label_10.setObjectName("label_10")

        #Inits number of layers label
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setGeometry(QtCore.QRect(20, 150, 150, 20)) # pos and size
        self.label_11.setObjectName("label_11")

        #Inits number of layers input
        self.lineEdit_3 = QLineEdit(self.groupBox_3)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 150, 60, 30)) # pos and size
        self.lineEdit_3.setObjectName("lineEdit_3")

        #Inits desired pressure label
        self.label_12 = QLabel(self.groupBox_3)
        self.label_12.setGeometry(QtCore.QRect(20, 200, 150, 20)) # pos and size
        self.label_12.setObjectName("label_12")

        #Inits desired pressure input
        self.lineEdit_4 = QLineEdit(self.groupBox_3)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 200, 60, 30)) # pos and size
        self.lineEdit_4.setObjectName("lineEdit_4")

        #Inits desired pressure unit select
        self.comboBox_6 = QComboBox(self.groupBox_3)
        self.comboBox_6.setGeometry(QtCore.QRect(230, 200, 60, 30)) # pos and size
        self.comboBox_6.setAutoFillBackground(False)
        self.comboBox_6.setEditable(False)
        self.comboBox_6.setObjectName("comboBox_6")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")

        #Inits STOP button
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(700, 110, 260, 60)) # pos and size
        self.pushButton.setFont(QFont('Arial', 14))#, QFont.Bold)) #adjust font
        self.pushButton.setObjectName("pushButton")

        #Inits Home button
        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(700, 280, 140, 30)) # pos and size
        self.pushButton_2.setObjectName("pushButton_2")

        #Inits Down button
        self.pushButton_5 = QPushButton(self.widget)
        self.pushButton_5.setGeometry(QtCore.QRect(700, 320, 140, 30)) # pos and size
        self.pushButton_5.setObjectName("pushButton_5")

        #Inits Up button
        self.pushButton_6 = QPushButton(self.widget)
        self.pushButton_6.setGeometry(QtCore.QRect(700, 240, 140, 30)) # pos and size
        self.pushButton_6.setObjectName("pushButton_6")

        #Inits Jogging box area
        self.groupBox_4 = QGroupBox(self.widget)
        self.groupBox_4.setGeometry(QtCore.QRect(680, 200, 300, 180)) # pos and size
        self.groupBox_4.setObjectName("groupBox_4")

        #Inits jog step size select
        self.comboBox_5 = QComboBox(self.groupBox_4)
        self.comboBox_5.setGeometry(QtCore.QRect(200, 120, 80, 30)) # pos and size
        self.comboBox_5.setAutoFillBackground(False)
        self.comboBox_5.setEditable(False)
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")

        #Inits program group box area
        self.groupBox_6 = QGroupBox(self.widget)
        self.groupBox_6.setGeometry(QtCore.QRect(680, 20, 300, 180)) # pos and size
        self.groupBox_6.setObjectName("groupBox_6")

        #Inits pause button
        self.pushButton_3 = QPushButton(self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(790, 60, 80, 40)) # pos and size
        self.pushButton_3.setObjectName("pushButton_3")

        #Inits run button
        self.pushButton_4 = QPushButton(self.widget)
        self.pushButton_4.setGeometry(QtCore.QRect(700, 60, 80, 40)) # pos and size
        self.pushButton_4.setObjectName("pushButton_4")

        #Inits resume button
        self.pushButton_7 = QPushButton(self.widget)
        self.pushButton_7.setGeometry(QtCore.QRect(880, 60, 80, 40)) # pos and size
        self.pushButton_7.setObjectName("pushButton_7")

        # raise_() brings components to front layer
        self.groupBox_6.raise_()
        self.groupBox_4.raise_()
        self.groupBox_2.raise_()
        self.groupBox_3.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_5.raise_()
        self.pushButton_6.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.pushButton_7.raise_()

        # TAB 2 #

        #Inits tab 2
        self.tabWidget.addTab(self.widget, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
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
        self.label_tab2_force.setFont(QFont('Arial', 18))
        self.label_tab2_force_units = QLabel(self.tab_2)
        self.label_tab2_force_units.setGeometry(QtCore.QRect(550, 170, 300, 51))
        self.label_tab2_force_units.setFont(QFont('Arial', 18))
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
        self.label_21.setFont(QFont('Arial', 18))
        self.label_21.setObjectName("label_21")

        #Inits pressure reading label
        self.label_tab2_pressure = QLabel(self.tab_2)
        self.label_tab2_pressure.setGeometry(QtCore.QRect(20, 270, 300, 51)) # pos and size
        self.label_tab2_pressure.setFont(font)
        self.label_tab2_pressure.setObjectName("label_tab2_pressure")

        #Inits pressure reading units label
        self.label_tab2_pressure_units = QLabel(self.tab_2)
        self.label_tab2_pressure_units.setGeometry(QtCore.QRect(550, 270, 300, 51)) # pos and size
        self.label_tab2_pressure_units.setFont(font)
        self.label_tab2_pressure_units.setObjectName("label_tab2_pressure_units")

        #Inits load cell reading units label
        self.label_tab2_load_units = QLabel(self.tab_2)
        self.label_tab2_load_units.setGeometry(QtCore.QRect(550, 70, 300, 51)) # pos and size
        self.label_tab2_load_units.setObjectName("label_tab2_load_units")
        self.label_tab2_load_units.setFont(QFont('Arial', 18))

        #Inits calibration button
        self.pushButton_8 = QPushButton(self.tab_2)
        self.pushButton_8.setGeometry(QtCore.QRect(700, 280, 140, 30)) # pos and size
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.raise_() # brings to front

        # TAB 3 #

        #Init tab 3
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")

        #Init data table area
        self.widget_2 = QWidget(self.tab_3)
        self.widget_2.setGeometry(QtCore.QRect(9, 9, 994, 500)) # pos and size
        self.widget_2.setObjectName("widget_2")

        #Init data table
        self.tableWidget = QTableWidget(self.widget_2)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 944, 340)) # pos and size
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)  # col count
        self.tableWidget.setRowCount(9)     # row count

        #Init sample table items
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)

        # TAB 4 #

        #Init tab 4
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")

        #Init communication box area
        self.groupBox_7 = QGroupBox(self.tab_4)
        self.groupBox_7.setGeometry(QtCore.QRect(10, 30, 400, 300)) # pos and size
        self.groupBox_7.setObjectName("groupBox_7")

        #Init connection label
        self.label_15 = QLabel(self.groupBox_7)
        self.label_15.setGeometry(QtCore.QRect(10, 30, 200, 20)) # pos and size
        self.label_15.setObjectName("label_15")

        #Init IP label
        self.label_16 = QLabel(self.groupBox_7)
        self.label_16.setGeometry(QtCore.QRect(10, 60, 200, 20)) # pos and size
        self.label_16.setObjectName("label_16")

        #Init Connection IP label
        self.label_17 = QLabel(self.groupBox_7)
        self.label_17.setGeometry(QtCore.QRect(10, 90, 200, 21)) # pos and size
        self.label_17.setObjectName("label_17")

        #Init system group box area
        self.groupBox_9 = QGroupBox(self.tab_4)
        self.groupBox_9.setGeometry(QtCore.QRect(440, 30, 401, 300)) # pos and size
        self.groupBox_9.setObjectName("groupBox_9")

        #Init system time label
        self.label_18 = QLabel(self.groupBox_9)
        self.label_18.setGeometry(QtCore.QRect(10, 30, 200, 20)) # pos and size
        self.label_18.setObjectName("label_18")

        #Init system date label
        self.label_19 = QLabel(self.groupBox_9)
        self.label_19.setGeometry(QtCore.QRect(10, 60, 200, 20)) # pos and size
        self.label_19.setObjectName("label_19")

        #Init system runtime label
        self.label_20 = QLabel(self.groupBox_9)
        self.label_20.setGeometry(QtCore.QRect(10, 90, 200, 20)) # pos and size
        self.label_20.setObjectName("label_20")

        # BOTTOM TAB #

        #Init Bottom Area frame
        self.tabWidget.addTab(self.tab_4, "")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 440, 1004, 261)) # pos and size
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        #Init bottom box area
        self.groupBox = QGroupBox(self.frame_2)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 1004, 300)) # pos and size
        self.groupBox.setObjectName("groupBox")

        #Init table layout
        self.tableView = QTableView(self.groupBox)
        self.tableView.setGeometry(QtCore.QRect(10, 30, 980, 90)) # pos and size
        self.tableView.setObjectName("tableView")

        #Init connected label
        self.label = QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 40, 150, 20)) # pos and size
        self.label.setObjectName("label")

        #Init system status label
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 150, 20)) # pos and size
        self.label_2.setObjectName("label_2")

        #Init mode label
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(200, 40, 150, 20)) # pos and size
        self.label_3.setObjectName("label_3")
        self.label_3_modeFeedback = QLabel(self.groupBox)
        self.label_3_modeFeedback.setGeometry(QtCore.QRect(250, 40, 150, 20))
        self.label_3_modeFeedback.setObjectName("label_3_modeFeedback")

        #Init error label
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(200, 70, 150, 20)) # pos and size
        self.label_4.setObjectName("label_4")

        #Init desired position label
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(480, 40, 200, 20)) # pos and size
        self.label_5.setObjectName("label_5")

        #Init desired pressure label
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(480, 70, 200, 20)) # pos and size
        self.label_6.setObjectName("label_6")

        #Init current pressure label
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(680, 70, 200, 20)) # pos and size
        self.label_7.setObjectName("label_7")

        #Init desired position label
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(680, 40, 200, 20)) # pos and size
        self.label_8.setObjectName("label_8")

        #center main window with status bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # self.pixmap = QPixmap('VulcanLabsLogo.png')
        # self.labelLogo = QLabel(self)
        # self.labelLogo.setPixmap(self.pixmap)
        # self.labelLogo.setGeometry(30,30,100,100)
        
        #run class fnc to annotate labels properly
        self.retranslateUi(MainWindow)

        #set default index of GUI to tab 0
        self.tabWidget.setCurrentIndex(0)

        #routing slots by name
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Annotate Labels and Components

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Vulcan Labs", "Vulcan Labs"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Mode Select"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Motion Limiting"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Pressure Limiting"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Parameter Input"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "mm"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "μm"))
        self.label_9.setText(_translate("MainWindow", "Initial Layer Height"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "mm"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "μm"))
        self.label_10.setText(_translate("MainWindow", "Final Layer Height"))
        self.label_11.setText(_translate("MainWindow", "Number of Layers"))
        self.label_12.setText(_translate("MainWindow", "Target Pressure"))
        self.comboBox_6.setItemText(0, _translate("MainWindow", "kPa"))
        self.comboBox_6.setItemText(1, _translate("MainWindow", "MPa"))
        self.pushButton.setText(_translate("MainWindow", "STOP"))
        self.pushButton_2.setText(_translate("MainWindow", "Home"))
        self.pushButton_8.setText(_translate("MainWindow", "Calibrate"))
        self.pushButton_5.setText(_translate("MainWindow", "Down"))
        self.pushButton_6.setText(_translate("MainWindow", "Up"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Jogging"))
        self.comboBox_5.setItemText(0, _translate("MainWindow", "1 mm"))
        self.comboBox_5.setItemText(1, _translate("MainWindow", "10 mm"))
        self.comboBox_5.setItemText(2, _translate("MainWindow", "50 mm"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Program"))
        self.pushButton_3.setText(_translate("MainWindow", "Pause"))
        self.pushButton_4.setText(_translate("MainWindow", "Run"))
        self.pushButton_7.setText(_translate("MainWindow", "Resume"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("MainWindow", "Control"))
        self.label_21.setText(_translate("MainWindow", "Load Cell Reading:"))
        self.label_tab2_pressure.setText(_translate("MainWindow", "Current Pressure:"))
        self.label_tab2_pressure_units.setText(_translate("MainWindow", " kPa"))
        self.label_tab2_force.setText(_translate("MainWindow", "Current Force:"))
        self.label_tab2_force_units.setText(_translate("MainWindow", " N"))
        self.label_tab2_load_units.setText(_translate("MainWindow", " kg"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "System"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Log 3"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Log 2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Log 4"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "Log 8"))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "Log 6"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Col 1"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Col 2"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Col 3"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Col 4"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Col 5"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Data"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Communication"))
        self.label_15.setText(_translate("MainWindow", "Connection:"))
        self.label_16.setText(_translate("MainWindow", "System IP: "+self.IpAdd))
        self.label_17.setText(_translate("MainWindow", "Connected Device IP:"))
        self.groupBox_9.setTitle(_translate("MainWindow", "General"))
        self.label_18.setText(_translate("MainWindow", "System Time:"))
        self.label_19.setText(_translate("MainWindow", "System Date:"))
        self.label_20.setText(_translate("MainWindow", "System Runtime:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Configuration"))
        self.groupBox.setTitle(_translate("MainWindow", "System State"))
        self.label.setText(_translate("MainWindow", "State: " + str(self.systemState)))
        self.label_2.setText(_translate("MainWindow", "System Status: "+ str(self.systemState)))
        self.label_3.setText(_translate("MainWindow", "Mode: "))
        self.label_3_modeFeedback.setText(_translate("MainWindow", "Motion Limiting"))
        self.label_4.setText(_translate("MainWindow", "Error: "+str(self.systemState)))
        self.label_5.setText(_translate("MainWindow", "Desired Position: "+str(self.desPos)))
        self.label_6.setText(_translate("MainWindow", "Desired Pressure: "+str(self.desPress)))
        self.label_7.setText(_translate("MainWindow", "Current Pressure: "+str(self.curPress)))
        self.label_8.setText(_translate("MainWindow", "Current Position: "+str(self.curPos)))

        # -- ROUTING -- #

        # Calibration Button
        self.pushButton_8.clicked.connect(self.Calibration)

        # Update Mode after selection
        self.comboBox.currentIndexChanged.connect(self.updateMode)

        # System state changes
        self.pushButton_4.clicked.connect(lambda x: self.updateSystemState(2)) #running
        self.pushButton_3.clicked.connect(lambda X: self.updateSystemState(3)) #Paused
        self.pushButton_7.clicked.connect(lambda X: self.updateSystemState(2)) #running
        self.pushButton.clicked.connect(lambda x: self.updateSystemState(4))   #Stopped
        # 0:idle 1:Starting 2:Running 3:Paused 4:Stopped 5:Processing


    def updateMode(self):
        mode = self.comboBox.currentText()
        print(mode)
        if mode == "Motion Limiting":
            self.modeSelected = 0
            self.label_3_modeFeedback.setText("Motion Limiting")
        else:
            self.modeSelected = 1
            self.label_3_modeFeedback.setText("Pressure Limiting")


    def UpdateForceReadingValue(self):
        """Updates the LCD Force Reading Value"""
        force_reading_raw = random.random()
        # force_reading_raw = cellInstance.cell.get_weight_mean(3)    #5 recomended for accuracy 
        force_reading_kg = round(force_reading_raw/1000,3)            #(grams to kg)
        force_reading_N = round(force_reading_kg*9.81,3)
        pistonDiameter = 20 #mm
        r = pistonDiameter/2 #mm
        r_m = r/1000    # [m]
        Area = math.pi*math.pow(r_m,2)
        pressure_reading = round((force_reading_N/Area)/1000,3)  #Kpa
        
        self.lcdNumber.display(force_reading_kg)
        self.lcdNumber2.display(pressure_reading)
        self.lcdNumber3.display(force_reading_N)
        self.update()

    def Calibration(self):
        self.dialog = calibrationDialogWindow()
        self.dialog.show()

    def UpdateGUI(self):
        self.UpdateForceReadingValue()

    def updateSystemState(self,index):
        self.systemState = int(index)
        indices = {
            0: "Idle",
            1: "Starting",
            2: "Running",
            3: "Paused",
            4: "Stopped",
            5: "Processing"
        }
        self.label.setText("State: "+ str(indices[self.systemState]))
        print(index)

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
        self.cancel_button.clicked.connect(self.close)

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

    #Sends known weight from user to Load cell calibration
    def sendKnownInput(self):
        self.close()
        self.setWindowTitle('Calibration 3')
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().deleteLater()
        print(f'user inputted value: {self.knownGrams}')
        # LoadCell.userCalibration(self.knownGrams)
        # while LoadCell.calibrated == 0:
        #     self.dialogText = QLabel('Calibrating...')
        self.dialogText = QLabel('System calibrated')
        buttons = QWidget()
        buttons.setLayout(QHBoxLayout())
        buttons.layout().addWidget(self.finish_button)
        self.layout().addRow('',self.dialogText)
        self.layout().addRow('',buttons)
        self.show()

        self.finish_button.clicked.connect(self.close)


class LoadCell():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  #set GPIO pind mode to BCM
        self.pd_sckPin=20
        self.dout_pin=21
        cell = HX711(self.dout_pin,self.pd_sckPin)
        self.recorded_configFile_name = 'swap_file.swp'
        self.calibrated = 0


        if os.path.isfile(self.recorded_configFile_name):
            with open(self.recorded_configFile_name,'rb') as swap_file:
                self.cell = pickle.load(swap_file)
                self.calibrated = 1
        else:
            self.calibrated = 0
            print("Please calibrate") # -- Send message to GUI
            

    def userCalibration(self, knownGrams):
        cell = self.cell
        #send the user calibration message
        err = cell.zero()
        if err:
            raise ValueError('Tare is unsuccessful.')

        input('Put known weight on the scale and then press Enter') # -- Send message to user; accept value from user (known weight)
        reading = cell.get_data_mean()
        if reading:
            # print('Mean value from HX711 subtracted by offset:', reading)
            # known_weight_grams = input(
                # 'Write how many grams it was and press Enter: ')
            known_weight_grams = knownGrams
            try:
                value = float(known_weight_grams)
                print(value, 'grams')
            except ValueError:
                print('Expected integer or float and I have got:',
                      known_weight_grams)

            ratio = reading / value  # calculate the ratio for channel A and gain 128
            cell.set_scale_ratio(ratio)  # set ratio for current channel
            print('Ratio is set.')
        else:
            raise ValueError(
                'Cannot calculate mean value. Try debug mode. Variable reading:',
                reading)
                    
        print('Saving the HX711 state to swap file on persistant memory')
        with open(calibrationFile, 'wb') as File:
            pickle.dump(cell, File)
            File.flush()
            os.fsync(File.fileno())
            # you have to flush, fsynch and close the file all the time.
            # This will write the file to the drive. It is slow but safe.
        print("tare is succesful")
        self.calibrated = 1




                
if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainWin = Ui_MainWindow()
    # cellInstance = LoadCell()
    mainWin.show()

    fps = 3
    timer = QtCore.QTimer()
    timer.timeout.connect(mainWin.UpdateGUI)
    timer.setInterval(int(1000/fps))
    timer.start()

    sys.exit(app.exec_())
