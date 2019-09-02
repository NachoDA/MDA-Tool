from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget
from PyQt5 import Qt


class MVAQWidget(QWidget):

    close_signal = pyqtSignal()
    resize_signal = pyqtSignal()
    focus_in_signal = pyqtSignal()
    focus_out_signal = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        # self.setMouseTracking(True)
        self.setFocusPolicy(Qt.Qt.StrongFocus)

    def closeEvent(self, event):
        self.close_signal.emit()
        print('Close event!')

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resize_signal.emit()

    def focusInEvent(self, event):
        print('--> focusInEvent' + str(self))
        self._focus_event = event
        self.focus_in_signal.emit()

    def focusOutEvent(self, event):
        print('<-- focusOutEvent' + str(self))
        self.focus_out_signal.emit()

    def set_children_focus_policy(self):
        for child in self.findChildren(QWidget):
            child.setFocusPolicy(Qt.Qt.TabFocus)