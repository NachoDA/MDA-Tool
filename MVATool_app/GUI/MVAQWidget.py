from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget


class MVAQWidget(QWidget):

    close_signal = pyqtSignal()
    resize_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

    def closeEvent(self, event):
        self.close_signal.emit()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resize_signal.emit()