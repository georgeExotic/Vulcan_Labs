import traceback
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QRect, QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThreadPool, QRunnable, QThread


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
    progress = pyqtSignal(int)

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