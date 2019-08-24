from PyQt5 import QtCore, QtGui
from Models.Model import Model
import pandas as pd

class DataFrameItemModel(QtCore.QAbstractItemModel):

    def __init__(self, parent=None):
        return super().__init__(parent=parent)