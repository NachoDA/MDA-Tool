import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtGui
from Models.Model import Model 

class EditDatasetModel(Model):

    def __init__(self):
        self.current_data = None
        return super().__init__()