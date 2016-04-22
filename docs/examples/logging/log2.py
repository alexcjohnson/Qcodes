from PyQt4 import QtCore, QtGui
import sys
import time

import logging
logger = logging.getLogger('qcodes')
logger.debug('logmodule message')
# ------------------------------------------------------------------------------


class QtSigHandler(logging.Handler):

    def __init__(self, sigEmitter):
        super(QtSigHandler, self).__init__()
        self.sigEmitter = sigEmitter

    def emit(self, logRecord):
        message = str(logRecord.getMessage())
        self.sigEmitter.emit(QtCore.SIGNAL("logMsg(QString)"), message)

# ------------------------------------------------------------------------------


class Window(QtGui.QWidget):

    def __init__(self):
        super(Window, self).__init__()

        # Layout
        self.textBox = QtGui.QTextBrowser()
        self.button = QtGui.QPushButton()
        vertLayout = QtGui.QVBoxLayout()
        vertLayout.addWidget(self.textBox)
        vertLayout.addWidget(self.button)
        self.setLayout(vertLayout)

        # Connect button
        self.button.clicked.connect(self.buttonPressed)

        # Thread
        self.bee = Worker(self.someProcess, ())
        self.bee.finished.connect(self.restoreUi)
        self.bee.terminated.connect(self.restoreUi)

        # Console handler
        dummyEmitter = QtCore.QObject()
        self.connect(dummyEmitter, QtCore.SIGNAL("logMsg(QString)"), self.msg)

        logger = logging.getLogger()

        # This is what levels get generated
        # logger.setLevel(logging.DEBUG)
        # for h in logger.handlers:
        #     logger.removeHandler(h)

        consoleHandler = QtSigHandler(dummyEmitter)
        consoleHandler.setLevel(logging.INFO)
        if consoleHandler not in logger.handlers:
            logger.addHandler(consoleHandler)

    def msg(self, *args):
        self.textBox.append(*args)
        # print(*args)

    def buttonPressed(self):
        # self.button.setEnabled(False)
        self.bee.start()

    def someProcess(self):
        logger.error("starting")
        for i in range(10):
            logger.error("line%d" % i)
            time.sleep(0.1)

    def restoreUi(self):
        self.button.setEnabled(True)

# ------------------------------------------------------------------------------


class Worker(QtCore.QThread):

    def __init__(self, func, args):
        super(Worker, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
