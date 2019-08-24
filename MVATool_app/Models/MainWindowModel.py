import numpy as np
import pandas as pd
from Models.Model import Model 

class MainWindowModel(Model):

    def __init__(self):
        self.current_data = None
        return super().__init__()

    def load_file(self, file_name, file_type):

        file_loaded = None

        if '.xls' in file_type or '.xlsx' in file_type:
            file_loaded = pd.read_excel(file_name, header=None, index_col=None)
            print(file_loaded)

        return file_loaded
