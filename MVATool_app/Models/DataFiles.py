
import pandas as pd

class DataFilesManager():

    def __init__(self):
        self._data_files = list()

    def create_data(self, name, df):
        data_file = DataFile(name, df)
        self._data_files.append(data_file)
        return data_file

    def get_dataset(self, name):
        for data_file in self._data_files:
            if data_file.name == name:
                return data_file

    def count(self):
        return len(self._data_files)

class DataFile():

    def __init__(self, name, df):
        self._name = name
        self._df = df

    def get_name(self):
        return self._name

    def get_dataframe(self):
        return self._df

    def get_num_cols(self):
        return len(self._df.columns)

    def get_num_rows(self):
        return len(self._df)