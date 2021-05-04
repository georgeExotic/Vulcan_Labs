import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThreadPool, QRunnable, QThread, pyqtSignal, pyqtSlot, QObject, QMutex
from PyQt5.QtGui import QCursor

class WorkerSignals(QObject):
    '''
    Defines signals that can be used from running worker thread
    finished
        No data
    error
        'tuple' (exectpye, value, traceback.format_exec() )
    result
        'object' data returned from processing, anything
    progress
        'int' indicating % progress
    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(float)
    forceReading = pyqtSignal(float)
    topLimit = pyqtSignal(bool)
    homeLimit = pyqtSignal(bool)
    positionReading = pyqtSignal(int)
    saveFile = pyqtSignal(bool)

class Worker(QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handle worker thread setup and signals
    :param callback: The callback function to run on this worker thread with args and kwargs
    :type callback: function
    :param args: Arguments to pass to callback
    :pram kwargs: Keywords to pass to callback
    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.kwargs['progress_callback'] = self.signals.progress
        self.kwargs['forceReading_callback'] = self.signals.forceReading
        self.kwargs['topLimit_callback'] = self.signals.topLimit
        self.kwargs['homeLimit_callback'] = self.signals.homeLimit
        self.kwargs['positionReading_callback'] = self.signals.positionReading
        self.kwargs['saveFile_callback'] = self.signals.saveFile

    @pyqtSlot()
    def run(self):
        '''Inits the function passed in with passed args and kwargs'''
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()