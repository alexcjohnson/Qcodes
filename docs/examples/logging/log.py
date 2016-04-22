#!/usr/bin/env python
#-*- coding:utf-8 -*-

from io import StringIO
import logging
import time

from PyQt4 import QtCore, QtGui


class logBuffer(QtCore.QObject):
    bufferMessage = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        QtCore.QObject.__init__(self)

    def write(self, message):
        message = message.strip()
        if message:
            self.bufferMessage.emit(message)


class myWindow(QtGui.QWidget):

    def __init__(self, parent=None):
        super(myWindow, self).__init__(parent)

        self.pushButton = QtGui.QPushButton(self)
        self.pushButton.setText("Send Log Message")
        self.pushButton.clicked.connect(self.on_pushButton_clicked)

        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setText("Hello!")

        self.label = QtGui.QLabel(self)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.pushButton)
        # self.layout.addWidget(self.pushButtonThread)
        self.layout.addWidget(self.label)

        self.logBuffer = logBuffer()
        self.logBuffer.bufferMessage.connect(self.on_logBuffer_bufferMessage)

        logFormatter = logging.Formatter(
            '%(levelname)s: %(module)s - %(message)s')

        logHandler = logging.StreamHandler(self.logBuffer)
        logHandler.setFormatter(logFormatter)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logHandler)

    @QtCore.pyqtSlot(str)
    def on_logBuffer_bufferMessage(self, message):
        message = message.strip()
        self.label.setText(message)

    @QtCore.pyqtSlot()
    def on_pushButton_clicked(self):
        message = self.lineEdit.text()
        self.logger.info(message if message else "No new messages")
        time.sleep(3)

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('myWindow')

    main = myWindow()
    main.show()

    sys.exit(app.exec_())
