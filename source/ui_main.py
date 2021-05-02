# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog

class ui_main(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 600))
        MainWindow.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Top_Bar = QtWidgets.QFrame(self.centralwidget)
        self.Top_Bar.setMaximumSize(QtCore.QSize(16777215, 40))
        self.Top_Bar.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.Top_Bar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Top_Bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Top_Bar.setObjectName("Top_Bar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Top_Bar)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_toggle = QtWidgets.QFrame(self.Top_Bar)
        self.frame_toggle.setMaximumSize(QtCore.QSize(70, 40))
        self.frame_toggle.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.frame_toggle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_toggle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_toggle.setObjectName("frame_toggle")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_toggle)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Btn_Toggle = QtWidgets.QPushButton(self.frame_toggle)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_Toggle.sizePolicy().hasHeightForWidth())
        self.Btn_Toggle.setSizePolicy(sizePolicy)
        self.Btn_Toggle.setStyleSheet("color: rgb(255, 255, 255);\n"
"border: 0px solid; font: bold 12px \"arial black\";")
        self.Btn_Toggle.setObjectName("Btn_Toggle")
        self.verticalLayout_2.addWidget(self.Btn_Toggle)
        self.horizontalLayout.addWidget(self.frame_toggle)
        self.frame_top = QtWidgets.QFrame(self.Top_Bar)
        self.frame_top.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top.setObjectName("frame_top")
        self.horizontalLayout.addWidget(self.frame_top)
        self.verticalLayout.addWidget(self.Top_Bar)
        self.Content = QtWidgets.QFrame(self.centralwidget)
        self.Content.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Content.setObjectName("Content")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.Content)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_left_menu = QtWidgets.QFrame(self.Content)
        self.frame_left_menu.setMinimumSize(QtCore.QSize(70, 0))
        self.frame_left_menu.setMaximumSize(QtCore.QSize(70, 16777215))
        self.frame_left_menu.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.frame_left_menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_left_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_left_menu.setObjectName("frame_left_menu")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_left_menu)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_top_menus = QtWidgets.QFrame(self.frame_left_menu)
        self.frame_top_menus.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_top_menus.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_menus.setObjectName("frame_top_menus")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_top_menus)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.btn_page_1 = QtWidgets.QPushButton(self.frame_top_menus)
        self.btn_page_1.setMinimumSize(QtCore.QSize(0, 60))
        self.btn_page_1.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"    font: bold 16px \"Arial Black\";\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_page_1.setObjectName("btn_page_1")
        self.verticalLayout_4.addWidget(self.btn_page_1)
        self.btn_page_2 = QtWidgets.QPushButton(self.frame_top_menus)
        self.btn_page_2.setMinimumSize(QtCore.QSize(0, 60))
        self.btn_page_2.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"    font: bold 16px \"Arial Black\";\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_page_2.setObjectName("btn_page_2")
        self.verticalLayout_4.addWidget(self.btn_page_2)
        self.btn_page_3 = QtWidgets.QPushButton(self.frame_top_menus)
        self.btn_page_3.setMinimumSize(QtCore.QSize(0, 60))
        self.btn_page_3.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"    font: bold 16px \"Arial Black\";\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_page_3.setObjectName("btn_page_3")
        self.verticalLayout_4.addWidget(self.btn_page_3)
        self.verticalLayout_3.addWidget(self.frame_top_menus, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_2.addWidget(self.frame_left_menu)
        self.frame_pages = QtWidgets.QFrame(self.Content)
        self.frame_pages.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_pages.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_pages.setObjectName("frame_pages")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_pages)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_pages)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.page_1)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.loadReading_label = QtWidgets.QLabel(self.page_1)
        self.loadReading_label.setStyleSheet("color: #fff; margin: 20; font: 18px \"arial black\"")
        self.loadReading_label.setObjectName("loadReading_label")
        self.gridLayout.addWidget(self.loadReading_label, 4, 6, 1, 1)
        self.jogDown_button = QtWidgets.QPushButton(self.page_1)
        self.jogDown_button.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.jogDown_button.setFont(font)
        self.jogDown_button.setStyleSheet("*{border: 4px solid \'#333\'; border-radius: 10px; font: bold 18px \"Arial Black\"; color: \'white\'; padding: 5px 5px; margin: 0px 0px; background: #555} *:hover{background: \'#369\';}")
        self.jogDown_button.setObjectName("jogDown_button")
        self.gridLayout.addWidget(self.jogDown_button, 5, 0, 1, 1)
        self.motorStatus_static_label = QtWidgets.QLabel(self.page_1)
        self.motorStatus_static_label.setStyleSheet("color: #fff; margin: 20; font: 18px \"arial black\"")
        self.motorStatus_static_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.motorStatus_static_label.setObjectName("motorStatus_static_label")
        self.gridLayout.addWidget(self.motorStatus_static_label, 0, 3, 1, 1)
        self.loadStatus_static_label = QtWidgets.QLabel(self.page_1)
        self.loadStatus_static_label.setStyleSheet("color: #fff; margin: 20; font: 18px \"arial black\"")
        self.loadStatus_static_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.loadStatus_static_label.setObjectName("loadStatus_static_label")
        self.gridLayout.addWidget(self.loadStatus_static_label, 2, 3, 1, 1)
        self.loadReading_static_label = QtWidgets.QLabel(self.page_1)
        self.loadReading_static_label.setStyleSheet("color: #fff; margin: 20; font: 18px \"arial black\"")
        self.loadReading_static_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.loadReading_static_label.setObjectName("loadReading_static_label")
        self.gridLayout.addWidget(self.loadReading_static_label, 4, 3, 1, 1)
        self.position_static_label = QtWidgets.QLabel(self.page_1)
        self.position_static_label.setStyleSheet("color: #fff; margin: 20; font: 18px \"arial black\"")
        self.position_static_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.position_static_label.setObjectName("position_static_label")
        self.gridLayout.addWidget(self.position_static_label, 5, 3, 1, 1)
        self.positionReading_label = QtWidgets.QLabel(self.page_1)
        self.positionReading_label.setStyleSheet("color: #fff; margin: 20; font: 18px \"arial black\"")
        self.positionReading_label.setObjectName("positionReading_label")
        self.gridLayout.addWidget(self.positionReading_label, 5, 6, 1, 1)
        self.loadStatus_label = QtWidgets.QLabel(self.page_1)
        self.loadStatus_label.setStyleSheet("color: #fff; margin: 20; font: 18px \"arial black\"")
        self.loadStatus_label.setObjectName("loadStatus_label")
        self.gridLayout.addWidget(self.loadStatus_label, 2, 6, 1, 1)
        self.connectLoad_button = QtWidgets.QPushButton(self.page_1)
        self.connectLoad_button.setMinimumSize(QtCore.QSize(0, 60))
        self.connectLoad_button.setStyleSheet("*{border: 4px solid \'#333\'; border-radius: 10px; font: bold 18px \"Arial Black\"; color: \'white\'; padding: 5px 5px; margin: 0px 0px; background: #555} *:hover{background: \'#369\';}")
        self.connectLoad_button.setObjectName("connectLoad_button")
        self.gridLayout.addWidget(self.connectLoad_button, 2, 0, 1, 1)
        self.home_button_page1 = QtWidgets.QPushButton(self.page_1)
        self.home_button_page1.setMinimumSize(QtCore.QSize(0, 60))
        self.home_button_page1.setStyleSheet("*{border: 4px solid \'#333\'; border-radius: 10px; font: bold 18px \"Arial Black\"; color: \'white\'; padding: 5px 5px; margin: 0px 0px; background: #555} *:hover{background: \'#369\';}")
        self.home_button_page1.setObjectName("home_button_page1")
        self.gridLayout.addWidget(self.home_button_page1, 3, 0, 1, 1)
        self.jogdown_lineedit = QtWidgets.QLineEdit(self.page_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jogdown_lineedit.sizePolicy().hasHeightForWidth())
        self.jogdown_lineedit.setSizePolicy(sizePolicy)
        self.jogdown_lineedit.setMaximumSize(QtCore.QSize(100, 50))
        self.jogdown_lineedit.setStyleSheet("QLineEdit {border: 2px solid \'#ccc\'; border-radius: 5px; font-size: 18px; color: #fff; margin-left: 20;} QLineEdit:read-only {border: 2px solid \'#333\'; border-radius: 5px; font-size: 18px; color: #777; margin-left: 20;}")
        self.jogdown_lineedit.setObjectName("jogdown_lineedit")
        self.gridLayout.addWidget(self.jogdown_lineedit, 5, 2, 1, 1)
        self.jogup_lineEdit = QtWidgets.QLineEdit(self.page_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jogup_lineEdit.sizePolicy().hasHeightForWidth())
        self.jogup_lineEdit.setSizePolicy(sizePolicy)
        self.jogup_lineEdit.setMinimumSize(QtCore.QSize(0, 50))
        self.jogup_lineEdit.setMaximumSize(QtCore.QSize(100, 50))
        self.jogup_lineEdit.setStyleSheet("QLineEdit {border: 2px solid \'#ccc\'; border-radius: 5px; font-size: 18px; color: #fff; margin-left: 20;} QLineEdit:read-only {border: 2px solid \'#333\'; border-radius: 5px; font-size: 18px; color: #777; margin-left: 20;}")
        self.jogup_lineEdit.setText("")
        self.jogup_lineEdit.setObjectName("jogup_lineEdit")
        self.gridLayout.addWidget(self.jogup_lineEdit, 4, 2, 1, 1)
        self.connectMotor_button = QtWidgets.QPushButton(self.page_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connectMotor_button.sizePolicy().hasHeightForWidth())
        self.connectMotor_button.setSizePolicy(sizePolicy)
        self.connectMotor_button.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.connectMotor_button.setFont(font)
        self.connectMotor_button.setStyleSheet("*{border: 4px solid \'#333\'; border-radius: 10px; font: bold 18px \"Arial Black\"; color: \'white\'; padding: 5px 5px; margin: 0px 0px; background: #555} *:hover{background: \'#369\';}")
        self.connectMotor_button.setObjectName("connectMotor_button")
        self.gridLayout.addWidget(self.connectMotor_button, 0, 0, 1, 1)
        self.jogUp_button = QtWidgets.QPushButton(self.page_1)
        self.jogUp_button.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.jogUp_button.setFont(font)
        self.jogUp_button.setStyleSheet("*{border: 4px solid \'#333\'; border-radius: 10px; font: bold 18px \"Arial Black\"; color: \'white\'; padding: 5px 5px; margin: 0px 0px; background: #555} *:hover{background: \'#369\';}")
        self.jogUp_button.setObjectName("jogUp_button")
        self.gridLayout.addWidget(self.jogUp_button, 4, 0, 1, 1)
        self.motorStatus_label = QtWidgets.QLabel(self.page_1)
        self.motorStatus_label.setStyleSheet("color: #fff; margin: 20; font: 18px \"arial black\"")
        self.motorStatus_label.setObjectName("motorStatus_label")
        self.gridLayout.addWidget(self.motorStatus_label, 0, 6, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 4, 1, 1)
        self.stopButton_page1 = QtWidgets.QPushButton(self.page_1)
        self.stopButton_page1.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.stopButton_page1.setFont(font)
        self.stopButton_page1.setStyleSheet("*{border: 4px solid \'#222\'; border-radius: 10px; font: bold 18px \"Arial Black\"; color: \'white\'; padding: 5px 5px; margin: 0px 0px; background: #555} *:hover{background: \'#369\';}")
        self.stopButton_page1.setObjectName("stopButton_page1")
        self.gridLayout.addWidget(self.stopButton_page1, 6, 0, 1, 1)
        self.jogup_comboBox = QtWidgets.QComboBox(self.page_1)
        self.jogup_comboBox.setMaximumSize(QtCore.QSize(16777215, 50))
        self.jogup_comboBox.setAccessibleDescription("")
        self.jogup_comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.jogup_comboBox.setAutoFillBackground(False)
        self.jogup_comboBox.addItem('  100 um')
        self.jogup_comboBox.addItem('  500 um')
        self.jogup_comboBox.addItem('  1 mm')
        self.jogup_comboBox.addItem('  5 mm')
        self.jogup_comboBox.addItem('  10 mm')
        self.jogup_comboBox.addItem('  custom')
        self.jogup_comboBox.setView( QtWidgets.QListView())
        self.jogup_comboBox.setStyleSheet("QListView {font: bold 16px #fff;} QListView::item:selected {background-color: #369;} QListView::item {color: #fff; background-color: #333; height: 50px;} QComboBox {color: #fff; font: bold 16px; margin-left: 20px;}")
        self.jogup_comboBox.setObjectName("jogup_comboBox")
        self.jogup_comboBox.currentIndexChanged.connect(self.check_jogup_custom)
        self.gridLayout.addWidget(self.jogup_comboBox, 4, 1, 1, 1)
        self.jogdown_comboBox = QtWidgets.QComboBox(self.page_1)
        self.jogdown_comboBox.setMaximumSize(QtCore.QSize(200, 50))
        self.jogdown_comboBox.setAutoFillBackground(False)
        self.jogdown_comboBox.addItem('  100 um')
        self.jogdown_comboBox.addItem('  500 um')
        self.jogdown_comboBox.addItem('  1 mm')
        self.jogdown_comboBox.addItem('  5 mm')
        self.jogdown_comboBox.addItem('  10 mm')
        self.jogdown_comboBox.addItem('  custom')
        self.jogdown_comboBox.setView( QtWidgets.QListView())
        self.jogdown_comboBox.setStyleSheet("QListView {font: bold 16px #fff;} QListView::item:selected {background-color: #369;} QListView::item {color: #fff; background-color: #333; height: 50px;} QComboBox {color: #fff; font: bold 16px; margin-left: 20px;}")
        self.jogdown_comboBox.setObjectName("jogdown_comboBox")
        self.jogdown_comboBox.currentIndexChanged.connect(self.check_jogdown_custom)
        self.gridLayout.addWidget(self.jogdown_comboBox, 5, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.page_1)
        self.label_7.setStyleSheet("color: #fff; margin: 20; font-size: 16px")
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 3, 1, 1)
        self.flagStatus_static_label = QtWidgets.QLabel(self.page_1)
        self.flagStatus_static_label.setStyleSheet("color: #fff; margin: 20; font: 18px \"arial black\"")
        self.flagStatus_static_label.setObjectName("flagStatus_static_label")
        self.gridLayout.addWidget(self.flagStatus_static_label, 6, 3, 1, 1)
        self.flag_reading_label = QtWidgets.QLabel(self.page_1)
        self.flag_reading_label.setStyleSheet("color: #fff; margin: 20; font: 18px \"arial black\"")
        self.flag_reading_label.setObjectName("flag_reading_label")
        self.gridLayout.addWidget(self.flag_reading_label, 6, 6, 1, 1)
        self.verticalLayout_7.addLayout(self.gridLayout)
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.layerCount_label = QtWidgets.QLabel(self.page_2)
        self.layerCount_label.setStyleSheet("color: #fff; margin: 20; font: 20px \"arial black\"")
        self.layerCount_label.setObjectName("layerCount_label")
        self.gridLayout_2.addWidget(self.layerCount_label, 3, 0, 1, 1)
        self.layerAfter_lineedit = QtWidgets.QLineEdit(self.page_2)
        self.layerAfter_lineedit.setMinimumSize(QtCore.QSize(0, 50))
        self.layerAfter_lineedit.setStyleSheet("border: 2px solid \'#ccc\'; border-radius: 5px; font-size: 18px; color: #fff; margin: 0 20")
        self.layerAfter_lineedit.setObjectName("layerAfter_lineedit")
        self.gridLayout_2.addWidget(self.layerAfter_lineedit, 1, 1, 1, 1)
        self.layerBefore_label = QtWidgets.QLabel(self.page_2)
        self.layerBefore_label.setStyleSheet("color: #fff; margin: 20; font: 20px \"arial black\"")
        self.layerBefore_label.setTextFormat(QtCore.Qt.AutoText)
        self.layerBefore_label.setWordWrap(True)
        self.layerBefore_label.setObjectName("layerBefore_label")
        self.gridLayout_2.addWidget(self.layerBefore_label, 0, 0, 1, 1)
        self.layerCount_lineedit = QtWidgets.QLineEdit(self.page_2)
        self.layerCount_lineedit.setMinimumSize(QtCore.QSize(0, 50))
        self.layerCount_lineedit.setStyleSheet("border: 2px solid \'#ccc\'; border-radius: 5px; font-size: 18px; color: #fff; margin: 0 20")
        self.layerCount_lineedit.setText("")
        self.layerCount_lineedit.setObjectName("layerCount_lineedit")
        self.gridLayout_2.addWidget(self.layerCount_lineedit, 3, 1, 1, 1)
        self.layerBefore_lineedit = QtWidgets.QLineEdit(self.page_2)
        self.layerBefore_lineedit.setMinimumSize(QtCore.QSize(0, 50))
        self.layerBefore_lineedit.setStyleSheet("border: 2px solid \'#ccc\'; border-radius: 5px; font-size: 18px; color: #fff; margin: 0 20")
        self.layerBefore_lineedit.setObjectName("layerBefore_lineedit")
        self.gridLayout_2.addWidget(self.layerBefore_lineedit, 0, 1, 1, 1)
        self.layerAfter_label = QtWidgets.QLabel(self.page_2)
        self.layerAfter_label.setStyleSheet("color: #fff; margin: 20; font: 20px \"arial black\"")
        self.layerAfter_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.layerAfter_label.setWordWrap(True)
        self.layerAfter_label.setObjectName("layerAfter_label")
        self.gridLayout_2.addWidget(self.layerAfter_label, 1, 0, 1, 1)
        self.sampleProgramButton = QtWidgets.QPushButton(self.page_2)
        self.sampleProgramButton.setMinimumSize(QtCore.QSize(0, 60))
        self.sampleProgramButton.setStyleSheet("*{border: 4px solid \'#333\'; border-radius: 10px; font: bold 18px \"Arial Black\"; color: \'white\'; padding: 5px 5px; margin: 0px 0px; background: #555} *:hover{background: \'#369\';}")
        self.sampleProgramButton.setObjectName("sampleProgramButton")
        self.gridLayout_2.addWidget(self.sampleProgramButton, 6, 4, 1, 1)
        self.layerBeforeUnit_label = QtWidgets.QLabel(self.page_2)
        self.layerBeforeUnit_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.layerBeforeUnit_label.setStyleSheet("color: #fff; margin-left: 20; font: 18px \"arial black\"")
        self.layerBeforeUnit_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layerBeforeUnit_label.setObjectName("layerBeforeUnit_label")
        self.gridLayout_2.addWidget(self.layerBeforeUnit_label, 0, 2, 1, 1)
        self.layerAfterUnit_label = QtWidgets.QLabel(self.page_2)
        self.layerAfterUnit_label.setStyleSheet("color: #fff; margin-left: 20; font: 18px \"arial black\"")
        self.layerAfterUnit_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.layerAfterUnit_label.setObjectName("layerAfterUnit_label")
        self.gridLayout_2.addWidget(self.layerAfterUnit_label, 1, 2, 1, 1)
        self.exportDataButton = QtWidgets.QPushButton(self.page_2)
        self.exportDataButton.setMinimumSize(QtCore.QSize(0, 60))
        self.exportDataButton.setStyleSheet("*{border: 4px solid \'#333\'; border-radius: 10px; font: bold 18px \"Arial Black\"; color: \'white\'; padding: 5px 5px; margin: 0px 0px; background: #555} *:hover{background: \'#369\';}")
        self.exportDataButton.setObjectName("exportDataButton")
        self.gridLayout_2.addWidget(self.exportDataButton, 6, 1, 1, 1)
        self.layerBefore_comboBox = QtWidgets.QComboBox(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layerBefore_comboBox.sizePolicy().hasHeightForWidth())
        self.layerBefore_comboBox.setSizePolicy(sizePolicy)
        self.layerBefore_comboBox.setMinimumSize(QtCore.QSize(0, 50))
        self.layerBefore_comboBox.setMaximumSize(QtCore.QSize(130, 50))
        self.layerBefore_comboBox.addItem('    mm')
        self.layerBefore_comboBox.addItem('    um')
        self.layerBefore_comboBox.setView(QtWidgets.QListView())
        self.layerBefore_comboBox.setStyleSheet("QListView {font: bold 18px #fff;} QListView::item {height: 40px; color: #FFF; background-color: #333; font: bold 16px #fff; } QListView::item:selected {color: #FFF; background-color: #369}} QComboBox {border: 2px solid #ccc; border-radius: 7px; background-color: #333; margin-left: 20; margin-bottom: 10; font: bold 16px; color: #fff} QComboBox::drop-down { width: 30px; height: 35px;} QComboBox::item {color: #FFF; background-color: #333; font: bold 16px #fff;}")
        self.layerBefore_comboBox.setObjectName("layerBefore_comboBox")
        self.layerBefore_comboBox.setAutoFillBackground(False)
        self.gridLayout_2.addWidget(self.layerBefore_comboBox, 0, 4, 1, 1)
        self.layerAfter_comboBox = QtWidgets.QComboBox(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layerAfter_comboBox.sizePolicy().hasHeightForWidth())
        self.layerAfter_comboBox.setSizePolicy(sizePolicy)
        self.layerAfter_comboBox.setMaximumSize(QtCore.QSize(130, 50))
        self.layerAfter_comboBox.addItem('    mm')
        self.layerAfter_comboBox.addItem('    um')
        self.layerAfter_comboBox.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.layerAfter_comboBox.setView(QtWidgets.QListView())
        self.layerAfter_comboBox.setStyleSheet("QListView {font: bold 18px #fff;} QListView::item {height: 40px; color: #FFF; background-color: #333; font: bold 16px #fff; } QListView::item:selected {color: #FFF; background-color: #369}} QComboBox {border: 2px solid #ccc; border-radius: 7px; background-color: #333; margin-left: 20; margin-bottom: 10; font: bold 16px; color: #fff} QComboBox::drop-down { width: 30px; height: 35px;} QComboBox::item {color: #FFF; background-color: #333; font: bold 16px #fff;}")
        self.layerAfter_comboBox.setObjectName("layerAfter_comboBox")
        self.gridLayout_2.addWidget(self.layerAfter_comboBox, 1, 4, 1, 1)
        self.startDataButton = QtWidgets.QPushButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startDataButton.sizePolicy().hasHeightForWidth())
        self.startDataButton.setSizePolicy(sizePolicy)
        self.startDataButton.setMinimumSize(QtCore.QSize(0, 60))
        self.startDataButton.setMaximumSize(QtCore.QSize(350, 16777215))
        self.startDataButton.setStyleSheet("*{border: 4px solid \'#333\'; border-radius: 10px; font: bold 18px \"Arial Black\"; color: \'white\'; padding: 0px 0px; margin-left: 30; background: #555} *:hover{background: \'#369\';}")
        self.startDataButton.setObjectName("startDataButton")
        self.gridLayout_2.addWidget(self.startDataButton, 4, 0, 1, 1)
        self.stopButton_page2 = QtWidgets.QPushButton(self.page_2)
        self.stopButton_page2.setMinimumSize(QtCore.QSize(0, 60))
        self.stopButton_page2.setStyleSheet("*{border: 4px solid \'#333\'; border-radius: 10px; font: bold 18px \"Arial Black\"; color: \'white\'; padding: 5px 5px; margin: 0px 0px; background: #555} *:hover{background: \'#369\';}")
        self.stopButton_page2.setObjectName("stopButton_page2")
        self.gridLayout_2.addWidget(self.stopButton_page2, 4, 4, 1, 1)
        self.runButton_page2 = QtWidgets.QPushButton(self.page_2)
        self.runButton_page2.setMinimumSize(QtCore.QSize(0, 60))
        self.runButton_page2.setStyleSheet("*{border: 4px solid \'#333\'; border-radius: 10px; font: bold 18px \"Arial Black\"; color: \'white\'; padding: 5px 5px; margin: 0px 0px; background: #555} *:hover{background: \'#369\';}")
        self.runButton_page2.setObjectName("runButton_page2")
        self.gridLayout_2.addWidget(self.runButton_page2, 3, 4, 1, 1)
        self.stopDataButton = QtWidgets.QPushButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stopDataButton.sizePolicy().hasHeightForWidth())
        self.stopDataButton.setSizePolicy(sizePolicy)
        self.stopDataButton.setMinimumSize(QtCore.QSize(0, 60))
        self.stopDataButton.setMaximumSize(QtCore.QSize(350, 16777215))
        self.stopDataButton.setStyleSheet("*{border: 4px solid \'#333\'; border-radius: 10px; font: bold 18px \"Arial Black\"; color: \'white\'; padding: 0px 0px; margin-left: 30; background: #555} *:hover{background: \'#369\';}")
        self.stopDataButton.setObjectName("stopDataButton")
        self.gridLayout_2.addWidget(self.stopDataButton, 6, 0, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_2)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label = QtWidgets.QLabel(self.page_3)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #FFF;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_8.addWidget(self.label)
        self.stackedWidget.addWidget(self.page_3)
        self.verticalLayout_5.addWidget(self.stackedWidget)
        self.horizontalLayout_2.addWidget(self.frame_pages)
        self.verticalLayout.addWidget(self.Content)
        MainWindow.setCentralWidget(self.centralwidget)

        self.btn_page_1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btn_page_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btn_page_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Btn_Toggle.setText(_translate("MainWindow", "VULCAN"))
        self.btn_page_1.setText(_translate("MainWindow", "HOME"))
        self.btn_page_2.setText(_translate("MainWindow", "RUN"))
        self.btn_page_3.setText(_translate("MainWindow", "DATA"))
        self.loadReading_label.setText(_translate("MainWindow", "--"))
        self.jogDown_button.setText(_translate("MainWindow", "Jog Down"))
        self.motorStatus_static_label.setText(_translate("MainWindow", "MOTOR: "))
        self.loadStatus_static_label.setText(_translate("MainWindow", "LOAD CELL:"))
        self.loadReading_static_label.setText(_translate("MainWindow", "FORCE READING:"))
        self.position_static_label.setText(_translate("MainWindow", "POSITION READING: "))
        self.positionReading_label.setText(_translate("MainWindow", "--"))
        self.loadStatus_label.setText(_translate("MainWindow", "Not Connected"))
        self.connectLoad_button.setText(_translate("MainWindow", "Connect LoadCell"))
        self.home_button_page1.setText(_translate("MainWindow", "Home Piston"))
        self.connectMotor_button.setText(_translate("MainWindow", "Connect Motor"))
        self.jogUp_button.setText(_translate("MainWindow", "Jog Up"))
        self.motorStatus_label.setText(_translate("MainWindow", "Not Connected"))
        self.stopButton_page1.setText(_translate("MainWindow", "Stop"))
        self.flagStatus_static_label.setText(_translate("MainWindow", "TOP FLAG/HOME FLAG:"))
        self.flag_reading_label.setText(_translate("MainWindow", "- / -"))
        self.layerCount_label.setText(_translate("MainWindow", "Enter number of total layers: "))
        self.layerBefore_label.setText(_translate("MainWindow", "Enter height of layer before compaction: "))
        self.layerAfter_label.setText(_translate("MainWindow", "Enter height of layer after compaction: "))
        self.sampleProgramButton.setText(_translate("MainWindow", "SAMPLE PROGRAM"))
        self.layerBeforeUnit_label.setText(_translate("MainWindow", "Unit:"))
        self.layerAfterUnit_label.setText(_translate("MainWindow", "Unit: "))
        self.exportDataButton.setText(_translate("MainWindow", "EXPORT DATA"))
        self.startDataButton.setText(_translate("MainWindow", "START DATA COLLECTION"))
        self.stopButton_page2.setText(_translate("MainWindow", "STOP"))
        self.runButton_page2.setText(_translate("MainWindow", "RUN"))
        self.stopDataButton.setText(_translate("MainWindow", "STOP DATA COLLECTION"))
        self.label.setText(_translate("MainWindow", "PAGE 3"))

    def check_jogdown_custom(self):
        if(self.jogdown_comboBox.currentIndex() == 5):
            self.jogdown_lineedit.setReadOnly(False)
        else:
            self.jogdown_lineedit.setReadOnly(True)

    def check_jogup_custom(self):
        if(self.jogup_comboBox.currentIndex() == 5):
            self.jogup_lineEdit.setReadOnly(False)
        else:
            self.jogup_lineEdit.setReadOnly(True)

    def launchPowderPopup(self):
        self.PowderDialogWindow = QDialog()
        powderPopUp = Ui_powderDialog()
        powderPopUp.setupUi(self.PowderDialogWindow)
        self.PowderDialogWindow.show()
        self.PowderDialogWindow.exec_()

class Ui_powderDialog(object):
    def setupUi(self, PowderDialog):
        PowderDialog.setObjectName("PowderDialog")
        PowderDialog.resize(630, 237)
        # PowderDialog.setMinimumSize(QtCore.QSize(630, 237))
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        # PowderDialog.setSizePolicy(sizePolicy)
        PowderDialog.setMaximumSize(QtCore.QSize(630, 16777215))
        PowderDialog.setStyleSheet("background: rgb(195,195,195);")
        self.verticalLayoutWidget = QtWidgets.QWidget(PowderDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(29, 19, 570, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setStyleSheet("color: #333; margin: 20; font: 20px \"arial black\"")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setStyleSheet("QDialogButtonBox:QPushButton {color: '#F00';}")
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(PowderDialog)
        self.buttonBox.accepted.connect(PowderDialog.accept)
        self.buttonBox.rejected.connect(PowderDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PowderDialog)

    def retranslateUi(self, PowderDialog):
        _translate = QtCore.QCoreApplication.translate
        PowderDialog.setWindowTitle(_translate("PowderDialog", "PowderDialog"))
        self.label.setText(_translate("PowderDialog", "Run has been paused to allow powder to be inserted. Once powder is in place select \'Ok\' to resume the run."))-