from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class InputState:
    LOWER = 0
    CAPITAL = 1

class KeyButton(QPushButton):
    sigKeyButtonClicked = pyqtSignal(object)

    def __init__(self, key):
        super(KeyButton, self).__init__()

        self._key = key
        self._activeSize = QSize(50,50)
        self.clicked.connect(self.emitKey)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.sigKeyButtonClicked.emit(self._key)

    def emitKey(self):
        self.sigKeyButtonClicked.emit(self._key)

    def enterEvent(self, event):
        self.setFixedSize(self._activeSize)

    def leaveEvent(self, event):
        self.setFixedSize(self.sizeHint())

    def sizeHint(self):
        return QSize(40, 40)
        sigInputString = pyqtSignal(object)
        sigKeyButtonClicked = pyqtSignal(object)

class VirtualKeyboard(QWidget):
    sigInputString = pyqtSignal(object)
    sigKeyButtonClicked = pyqtSignal()

    def __init__(self):
        super(VirtualKeyboard, self).__init__()

        self.globalLayout = QVBoxLayout(self)
        self.keysLayout = QGridLayout()
        self.buttonLayout = QHBoxLayout()
        self.enterFlag = 0
        self.okCheck = 0

        self.keyListByLines = [
                    ['1', '2', '3'], #, 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                    ['4', '5', '6'], #, 'f', 'g', 'h', 'j', 'k', 'l', 'm'],
                    ['7', '8', '9'], #, 'v', 'b', 'n', '_', '.', '/', ' '],
                    [' ', '0', '.']
                ]
        self.inputString = ""
        self.state = InputState.LOWER

        self.stateButton = QPushButton()
        self.stateButton.setText('Maj.')
        self.backButton = QPushButton()
        self.backButton.setText('<-')
        self.okButton = QPushButton()
        self.okButton.setText('OK')
        self.cancelButton = QPushButton()
        self.cancelButton.setText("Cancel")

        self.inputLine = QLineEdit()


        for lineIndex, line in enumerate(self.keyListByLines):
            for keyIndex, key in enumerate(line):
                buttonName = "keyButton" + key.capitalize()
                self.__setattr__(buttonName, KeyButton(key))
                self.keysLayout.addWidget(self.getButtonByKey(key), self.keyListByLines.index(line), line.index(key))
                self.getButtonByKey(key).setText(key)
                self.getButtonByKey(key).sigKeyButtonClicked.connect(self.addInputByKey)
                self.keysLayout.setColumnMinimumWidth(keyIndex, 50)
            self.keysLayout.setRowMinimumHeight(lineIndex, 50)

        self.stateButton.clicked.connect(self.switchState)
        self.backButton.clicked.connect(self.backspace)
        self.okButton.clicked.connect(self.emitInputString)
        self.okButton.clicked.connect(self.emit2Gui)
        self.okButton.clicked.connect(self.close) 
        self.cancelButton.clicked.connect(self.emitCancel)


        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.stateButton)
        self.buttonLayout.addWidget(self.okButton)

        self.globalLayout.addWidget(self.inputLine)
        self.globalLayout.addLayout(self.keysLayout)

        self.globalLayout.addLayout(self.buttonLayout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        
    def emit2Gui(self):
        self.okCheck = 1
        

    def getButtonByKey(self, key):
        return getattr(self, "keyButton" + key.capitalize())

    def getLineForButtonByKey(self, key):
        return [key in keyList for keyList in self.keyListByLines].index(True)

    def switchState(self):
        self.state = not self.state

    def addInputByKey(self, key):
        self.inputString += (key.lower(), key.capitalize())[self.state]
        self.inputLine.setText(self.inputString)
        # mainWin.currentlineEdit.setText(self.inputString)

    def backspace(self):
        self.inputLine.backspace()
        # mainWin.currentlineEdit = self.inputString[:-1]
        self.inputString = self.inputString[:-1]
        self.sigInputString.emit("")

    def emitInputString(self):
        self.enterFlag = 1
        self.sigInputString.emit(self.inputString)
        self.enterFlag = 0

    def emitCancel(self):
        self.sigInputString.emit()

    def sizeHint(self):
        return QSize(480,272)

### number 2 ###

class VirtualKeyboard2(QWidget):
    sigInputString = pyqtSignal(object)
    sigKeyButtonClicked = pyqtSignal()

    def __init__(self):
        super(VirtualKeyboard2, self).__init__()

        self.globalLayout = QVBoxLayout(self)
        self.keysLayout = QGridLayout()
        self.buttonLayout = QHBoxLayout()
        self.okCheck = 0

        self.keyListByLines = [
                    ['1', '2', '3'], #, 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                    ['4', '5', '6'], #, 'f', 'g', 'h', 'j', 'k', 'l', 'm'],
                    ['7', '8', '9'], #, 'v', 'b', 'n', '_', '.', '/', ' '],
                    [' ', '0', '.']
                ]
        self.inputString = ""
        self.state = InputState.LOWER

        self.stateButton = QPushButton()
        self.stateButton.setText('Maj.')
        self.backButton = QPushButton()
        self.backButton.setText('<-')
        self.okButton = QPushButton()
        self.okButton.setText('OK')
        self.cancelButton = QPushButton()
        self.cancelButton.setText("Cancel")

        self.inputLine = QLineEdit()


        for lineIndex, line in enumerate(self.keyListByLines):
            for keyIndex, key in enumerate(line):
                buttonName = "keyButton" + key.capitalize()
                self.__setattr__(buttonName, KeyButton(key))
                self.keysLayout.addWidget(self.getButtonByKey(key), self.keyListByLines.index(line), line.index(key))
                self.getButtonByKey(key).setText(key)
                self.getButtonByKey(key).sigKeyButtonClicked.connect(self.addInputByKey)
                self.keysLayout.setColumnMinimumWidth(keyIndex, 50)
            self.keysLayout.setRowMinimumHeight(lineIndex, 50)

        self.stateButton.clicked.connect(self.switchState)
        self.backButton.clicked.connect(self.backspace)
        self.okButton.clicked.connect(self.emitInputString)
        self.okButton.clicked.connect(self.emit2Gui)
        self.okButton.clicked.connect(self.close) 
        self.cancelButton.clicked.connect(self.emitCancel)


        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.stateButton)
        self.buttonLayout.addWidget(self.okButton)

        self.globalLayout.addWidget(self.inputLine)
        self.globalLayout.addLayout(self.keysLayout)

        self.globalLayout.addLayout(self.buttonLayout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        
    def emit2Gui(self):
        self.okCheck = 1
        

    def getButtonByKey(self, key):
        return getattr(self, "keyButton" + key.capitalize())

    def getLineForButtonByKey(self, key):
        return [key in keyList for keyList in self.keyListByLines].index(True)

    def switchState(self):
        self.state = not self.state

    def addInputByKey(self, key):
        self.inputString += (key.lower(), key.capitalize())[self.state]
        self.inputLine.setText(self.inputString)
        # mainWin.currentlineEdit.setText(self.inputString)

    def backspace(self):
        self.inputLine.backspace()
        # mainWin.currentlineEdit = self.inputString[:-1]
        self.inputString = self.inputString[:-1]
        self.sigInputString.emit("")

    def emitInputString(self):
        self.sigInputString.emit(self.inputString)

    def emitCancel(self):
        self.sigInputString.emit()

    def sizeHint(self):
        return QSize(480,272)

### number 3 ###

class VirtualKeyboard3(QWidget):
    sigInputString = pyqtSignal(object)
    sigKeyButtonClicked = pyqtSignal()

    def __init__(self):
        super(VirtualKeyboard3, self).__init__()

        self.globalLayout = QVBoxLayout(self)
        self.keysLayout = QGridLayout()
        self.buttonLayout = QHBoxLayout()
        self.okCheck = 0

        self.keyListByLines = [
                    ['1', '2', '3'], #, 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                    ['4', '5', '6'], #, 'f', 'g', 'h', 'j', 'k', 'l', 'm'],
                    ['7', '8', '9'], #, 'v', 'b', 'n', '_', '.', '/', ' '],
                    [' ', '0', '.']
                ]
        self.inputString = ""
        self.state = InputState.LOWER

        self.stateButton = QPushButton()
        self.stateButton.setText('Maj.')
        self.backButton = QPushButton()
        self.backButton.setText('<-')
        self.okButton = QPushButton()
        self.okButton.setText('OK')
        self.cancelButton = QPushButton()
        self.cancelButton.setText("Cancel")

        self.inputLine = QLineEdit()


        for lineIndex, line in enumerate(self.keyListByLines):
            for keyIndex, key in enumerate(line):
                buttonName = "keyButton" + key.capitalize()
                self.__setattr__(buttonName, KeyButton(key))
                self.keysLayout.addWidget(self.getButtonByKey(key), self.keyListByLines.index(line), line.index(key))
                self.getButtonByKey(key).setText(key)
                self.getButtonByKey(key).sigKeyButtonClicked.connect(self.addInputByKey)
                self.keysLayout.setColumnMinimumWidth(keyIndex, 50)
            self.keysLayout.setRowMinimumHeight(lineIndex, 50)

        self.stateButton.clicked.connect(self.switchState)
        self.backButton.clicked.connect(self.backspace)
        self.okButton.clicked.connect(self.emitInputString)
        self.okButton.clicked.connect(self.emit2Gui)
        self.okButton.clicked.connect(self.close)
        self.cancelButton.clicked.connect(self.emitCancel)


        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.stateButton)
        self.buttonLayout.addWidget(self.okButton)

        self.globalLayout.addWidget(self.inputLine)
        self.globalLayout.addLayout(self.keysLayout)

        self.globalLayout.addLayout(self.buttonLayout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        
    def emit2Gui(self):
        self.okCheck = 1
        

    def getButtonByKey(self, key):
        return getattr(self, "keyButton" + key.capitalize())

    def getLineForButtonByKey(self, key):
        return [key in keyList for keyList in self.keyListByLines].index(True)

    def switchState(self):
        self.state = not self.state

    def addInputByKey(self, key):
        self.inputString += (key.lower(), key.capitalize())[self.state]
        self.inputLine.setText(self.inputString)
        # mainWin.currentlineEdit.setText(self.inputString)

    def backspace(self):
        self.inputLine.backspace()
        # mainWin.currentlineEdit = self.inputString[:-1]
        self.inputString = self.inputString[:-1]
        self.sigInputString.emit("")

    def emitInputString(self):
        self.sigInputString.emit(self.inputString)

    def emitCancel(self):
        self.sigInputString.emit()

    def sizeHint(self):
        return QSize(480,272)

### number 4 ###

class VirtualKeyboard4(QWidget):
    sigInputString = pyqtSignal(object)
    sigKeyButtonClicked = pyqtSignal()

    def __init__(self):
        super(VirtualKeyboard4, self).__init__()

        self.globalLayout = QVBoxLayout(self)
        self.keysLayout = QGridLayout()
        self.buttonLayout = QHBoxLayout()
        self.okCheck = 0

        self.keyListByLines = [
                    ['1', '2', '3'], #, 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                    ['4', '5', '6'], #, 'f', 'g', 'h', 'j', 'k', 'l', 'm'],
                    ['7', '8', '9'], #, 'v', 'b', 'n', '_', '.', '/', ' '],
                    [' ', '0', '.']
                ]
        self.inputString = ""
        self.state = InputState.LOWER

        self.stateButton = QPushButton()
        self.stateButton.setText('Maj.')
        self.backButton = QPushButton()
        self.backButton.setText('<-')
        self.okButton = QPushButton()
        self.okButton.setText('OK')
        self.cancelButton = QPushButton()
        self.cancelButton.setText("Cancel")

        self.inputLine = QLineEdit()


        for lineIndex, line in enumerate(self.keyListByLines):
            for keyIndex, key in enumerate(line):
                buttonName = "keyButton" + key.capitalize()
                self.__setattr__(buttonName, KeyButton(key))
                self.keysLayout.addWidget(self.getButtonByKey(key), self.keyListByLines.index(line), line.index(key))
                self.getButtonByKey(key).setText(key)
                self.getButtonByKey(key).sigKeyButtonClicked.connect(self.addInputByKey)
                self.keysLayout.setColumnMinimumWidth(keyIndex, 50)
            self.keysLayout.setRowMinimumHeight(lineIndex, 50)

        self.stateButton.clicked.connect(self.switchState)
        self.backButton.clicked.connect(self.backspace)
        self.okButton.clicked.connect(self.emitInputString)
        self.okButton.clicked.connect(self.emit2Gui)
        self.okButton.clicked.connect(self.close)
        self.cancelButton.clicked.connect(self.emitCancel)


        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.stateButton)
        self.buttonLayout.addWidget(self.okButton)

        self.globalLayout.addWidget(self.inputLine)
        self.globalLayout.addLayout(self.keysLayout)

        self.globalLayout.addLayout(self.buttonLayout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        
    def emit2Gui(self):
        self.okCheck = 1 

    def getButtonByKey(self, key):
        return getattr(self, "keyButton" + key.capitalize())

    def getLineForButtonByKey(self, key):
        return [key in keyList for keyList in self.keyListByLines].index(True)

    def switchState(self):
        self.state = not self.state

    def addInputByKey(self, key):
        self.inputString += (key.lower(), key.capitalize())[self.state]
        self.inputLine.setText(self.inputString)
        # mainWin.currentlineEdit.setText(self.inputString)

    def backspace(self):
        self.inputLine.backspace()
        # mainWin.currentlineEdit = self.inputString[:-1]
        self.inputString = self.inputString[:-1]
        self.sigInputString.emit("")

    def emitInputString(self):
        self.sigInputString.emit(self.inputString)

    def emitCancel(self):
        self.sigInputString.emit()

    def sizeHint(self):
        return QSize(480,272)

### number 5 ###

class VirtualKeyboard5(QWidget):
    sigInputString = pyqtSignal(object)
    sigKeyButtonClicked = pyqtSignal()

    def __init__(self):
        super(VirtualKeyboard5, self).__init__()

        self.globalLayout = QVBoxLayout(self)
        self.keysLayout = QGridLayout()
        self.buttonLayout = QHBoxLayout()
        self.setWindowTitle("Keyboard")
        self.resize(300,300)
        # self.center()
        self.okCheck = 0

        self.keyListByLines = [
                    ['1', '2', '3'], #, 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                    ['4', '5', '6'], #, 'f', 'g', 'h', 'j', 'k', 'l', 'm'],
                    ['7', '8', '9'], #, 'v', 'b', 'n', '_', '.', '/', ' '],
                    ['', '0', '.']
                ]
        self.inputString = ""
        self.state = InputState.LOWER

        self.stateButton = QPushButton()
        self.stateButton.setText('Maj.')
        self.backButton = QPushButton()
        self.backButton.setText('<-')
        self.okButton = QPushButton()
        self.okButton.setText('OK')
        self.cancelButton = QPushButton()
        self.cancelButton.setText("Cancel")

        self.inputLine = QLineEdit()


        for lineIndex, line in enumerate(self.keyListByLines):
            for keyIndex, key in enumerate(line):
                buttonName = "keyButton" + key.capitalize()
                self.__setattr__(buttonName, KeyButton(key))
                self.keysLayout.addWidget(self.getButtonByKey(key), self.keyListByLines.index(line), line.index(key))
                self.getButtonByKey(key).setText(key)
                self.getButtonByKey(key).sigKeyButtonClicked.connect(self.addInputByKey)
                self.keysLayout.setColumnMinimumWidth(keyIndex, 50)
            self.keysLayout.setRowMinimumHeight(lineIndex, 50)

        self.stateButton.clicked.connect(self.switchState)
        self.backButton.clicked.connect(self.backspace)
        self.okButton.clicked.connect(self.emitInputString)
        self.okButton.clicked.connect(self.emit2Gui) 
        self.okButton.clicked.connect(self.close)
        self.cancelButton.clicked.connect(self.emitCancel)


        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.stateButton)
        self.buttonLayout.addWidget(self.okButton)

        self.globalLayout.addWidget(self.inputLine)
        self.globalLayout.addLayout(self.keysLayout)

        self.globalLayout.addLayout(self.buttonLayout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        
    def emit2Gui(self):
        print("ok")
        self.okCheck = 1

    def getButtonByKey(self, key):
        return getattr(self, "keyButton" + key.capitalize())

    def getLineForButtonByKey(self, key):
        return [key in keyList for keyList in self.keyListByLines].index(True)

    def switchState(self):
        self.state = not self.state

    def addInputByKey(self, key):
        self.inputString += (key.lower(), key.capitalize())[self.state]
        self.inputLine.setText(self.inputString)
        # mainWin.currentlineEdit.setText(self.inputString)

    def backspace(self):
        self.inputLine.backspace()
        # mainWin.currentlineEdit = self.inputString[:-1]
        self.inputString = self.inputString[:-1]
        self.sigInputString.emit("")

    def emitInputString(self):
        self.sigInputString.emit(self.inputString)

    def emitCancel(self):
        self.sigInputString.emit()

    def sizeHint(self):
        return QSize(480,272)

### number 6 ###
class VirtualKeyboard6(QWidget):
    sigInputString = pyqtSignal(object)
    sigKeyButtonClicked = pyqtSignal()

    def __init__(self):
        super(VirtualKeyboard6, self).__init__()

        self.globalLayout = QVBoxLayout(self)
        self.keysLayout = QGridLayout()
        self.buttonLayout = QHBoxLayout()
        self.setWindowTitle("Keyboard")
        self.resize(300,300)
        # self.center()
        self.okCheck = 0

        self.keyListByLines = [
                    ['1', '2', '3'], #, 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                    ['4', '5', '6'], #, 'f', 'g', 'h', 'j', 'k', 'l', 'm'],
                    ['7', '8', '9'], #, 'v', 'b', 'n', '_', '.', '/', ' '],
                    ['', '0', '.']
                ]
        self.inputString = ""
        self.state = InputState.LOWER

        self.stateButton = QPushButton()
        self.stateButton.setText('Maj.')
        self.backButton = QPushButton()
        self.backButton.setText('<-')
        self.okButton = QPushButton()
        self.okButton.setText('OK')
        self.cancelButton = QPushButton()
        self.cancelButton.setText("Cancel")

        self.inputLine = QLineEdit()


        for lineIndex, line in enumerate(self.keyListByLines):
            for keyIndex, key in enumerate(line):
                buttonName = "keyButton" + key.capitalize()
                self.__setattr__(buttonName, KeyButton(key))
                self.keysLayout.addWidget(self.getButtonByKey(key), self.keyListByLines.index(line), line.index(key))
                self.getButtonByKey(key).setText(key)
                self.getButtonByKey(key).sigKeyButtonClicked.connect(self.addInputByKey)
                self.keysLayout.setColumnMinimumWidth(keyIndex, 50)
            self.keysLayout.setRowMinimumHeight(lineIndex, 50)

        self.stateButton.clicked.connect(self.switchState)
        self.backButton.clicked.connect(self.backspace)
        self.okButton.clicked.connect(self.emitInputString)
        self.okButton.clicked.connect(self.emit2Gui) 
        self.okButton.clicked.connect(self.close)
        self.cancelButton.clicked.connect(self.emitCancel)


        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.stateButton)
        self.buttonLayout.addWidget(self.okButton)

        self.globalLayout.addWidget(self.inputLine)
        self.globalLayout.addLayout(self.keysLayout)

        self.globalLayout.addLayout(self.buttonLayout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        
    def emit2Gui(self):
        print("ok")
        self.okCheck = 1

    def getButtonByKey(self, key):
        return getattr(self, "keyButton" + key.capitalize())

    def getLineForButtonByKey(self, key):
        return [key in keyList for keyList in self.keyListByLines].index(True)

    def switchState(self):
        self.state = not self.state

    def addInputByKey(self, key):
        self.inputString += (key.lower(), key.capitalize())[self.state]
        self.inputLine.setText(self.inputString)
        # mainWin.currentlineEdit.setText(self.inputString)

    def backspace(self):
        self.inputLine.backspace()
        # mainWin.currentlineEdit = self.inputString[:-1]
        self.inputString = self.inputString[:-1]
        self.sigInputString.emit("")

    def emitInputString(self):
        self.sigInputString.emit(self.inputString)

    def emitCancel(self):
        self.sigInputString.emit()

    def sizeHint(self):
        return QSize(480,272)

### number 7 ###
class VirtualKeyboard7(QWidget):
    sigInputString = pyqtSignal(object)
    sigKeyButtonClicked = pyqtSignal()

    def __init__(self):
        super(VirtualKeyboard7, self).__init__()

        self.globalLayout = QVBoxLayout(self)
        self.keysLayout = QGridLayout()
        self.buttonLayout = QHBoxLayout()
        self.setWindowTitle("Keyboard")
        self.resize(300,300)
        # self.center()
        self.okCheck = 0

        self.keyListByLines = [
                    ['1', '2', '3'], #, 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                    ['4', '5', '6'], #, 'f', 'g', 'h', 'j', 'k', 'l', 'm'],
                    ['7', '8', '9'], #, 'v', 'b', 'n', '_', '.', '/', ' '],
                    ['', '0', '.']
                ]
        self.inputString = ""
        self.state = InputState.LOWER

        self.stateButton = QPushButton()
        self.stateButton.setText('Maj.')
        self.backButton = QPushButton()
        self.backButton.setText('<-')
        self.okButton = QPushButton()
        self.okButton.setText('OK')
        self.cancelButton = QPushButton()
        self.cancelButton.setText("Cancel")

        self.inputLine = QLineEdit()


        for lineIndex, line in enumerate(self.keyListByLines):
            for keyIndex, key in enumerate(line):
                buttonName = "keyButton" + key.capitalize()
                self.__setattr__(buttonName, KeyButton(key))
                self.keysLayout.addWidget(self.getButtonByKey(key), self.keyListByLines.index(line), line.index(key))
                self.getButtonByKey(key).setText(key)
                self.getButtonByKey(key).sigKeyButtonClicked.connect(self.addInputByKey)
                self.keysLayout.setColumnMinimumWidth(keyIndex, 50)
            self.keysLayout.setRowMinimumHeight(lineIndex, 50)

        self.stateButton.clicked.connect(self.switchState)
        self.backButton.clicked.connect(self.backspace)
        self.okButton.clicked.connect(self.emitInputString)
        self.okButton.clicked.connect(self.emit2Gui) 
        self.okButton.clicked.connect(self.close)
        self.cancelButton.clicked.connect(self.emitCancel)


        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.stateButton)
        self.buttonLayout.addWidget(self.okButton)

        self.globalLayout.addWidget(self.inputLine)
        self.globalLayout.addLayout(self.keysLayout)

        self.globalLayout.addLayout(self.buttonLayout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        
    def emit2Gui(self):
        print("ok")
        self.okCheck = 1

    def getButtonByKey(self, key):
        return getattr(self, "keyButton" + key.capitalize())

    def getLineForButtonByKey(self, key):
        return [key in keyList for keyList in self.keyListByLines].index(True)

    def switchState(self):
        self.state = not self.state

    def addInputByKey(self, key):
        self.inputString += (key.lower(), key.capitalize())[self.state]
        self.inputLine.setText(self.inputString)
        # mainWin.currentlineEdit.setText(self.inputString)

    def backspace(self):
        self.inputLine.backspace()
        # mainWin.currentlineEdit = self.inputString[:-1]
        self.inputString = self.inputString[:-1]
        self.sigInputString.emit("")

    def emitInputString(self):
        self.sigInputString.emit(self.inputString)

    def emitCancel(self):
        self.sigInputString.emit()

    def sizeHint(self):
        return QSize(480,272)


class Test(QWidget):
    def __init__(self):
        super(Test, self).__init__()

        self.b1 = KeyButton("1")
        self.b2 = KeyButton("2")
        self.b3 = KeyButton("3")
        self.b4 = KeyButton("4")

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.b1,0,0)
        self.layout.addWidget(self.b2,0,1)
        self.layout.addWidget(self.b3,1,0)
        self.layout.addWidget(self.b4,1,1)

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    win = VirtualKeyboard()
    win.show()
    app.exec_()