from sklearn import preprocessing
import pandas as pd
import numpy as np
from enum import IntEnum


def count_frequency(my_list):
    freq = {}
    for item in my_list:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1
    return freq

class ScaleType(IntEnum):
    unitary = 0
    pareto = 1
    equal_weigh = 2

class MissingStrategy(IntEnum):
    mean = 1
    discard_row = 2
    discard_column = 3
    knn_imputation = 4

class DataSetsManager():

    def __init__(self):
        self._data_sets = list()

    def create(self, name, data_file, description):
        data_set = DataSet(name, data_file, description)
        self._data_sets.append(data_set)
        return data_set

    def add(self, data_set, name):
        data_set.name = name
        self._data_sets.append(data_set)
        return data_set

    def get(self, name):
        for data_set in self._data_sets:
            if data_set.name == name:
                return data_set

    def get_by_index(self, index):
        return self._data_sets[index]

    def remove(self, name):
        if self.exists(name):
            self._data_sets.remove(self.get(name))

    def remove_by_index(self, index):
        # print('remove_by_index: ' + str(index))
        del self._data_sets[index]

    def count(self):
        return len(self._data_sets)

    def change_name(self, old_name, new_name):
        if self.exits(new_name):
            print('This name already exists')
        else:
            data_set = self.get(old_name)
            data_set.name = new_name

    def exists(self, name):
        return self.get(name) is not None

    def all_names(self):
        return [x.name for x in self._data_sets]

    def all_names_and_data_file(self):
        return [x.get_name_and_data_file() for x in self._data_sets]

# TODO: All dataframe operations must be done in DataFiles as a wrap
# TODO: How to manage datafiles additional data created by user? New class named
#  dataExtension that wraps data files? Maybe each change of this type is a decorator?
# TODO: Design "memory" for calculations if there have been no changes. For data set,
#  for models... Example: correlation calculation.
class DataSet():

    def __init__(self, name, data_file, description):
        self.name = name
        self.data_file = data_file
        self.description = description

        self.primary_rows = list()
        self.secondary_rows = list()
        self.discarded_rows = list()
        self.primary_cols = list()
        self.secondary_cols = list()
        self.discarded_cols = list()

        self._rows_scale_group = None
        self._scale_per_group = None
        self._missing_strategy = MissingStrategy.mean

    # Allow comparison between data sets. Used in dict
    def __hash__(self):
        return hash(str(self))

    def get_numeric_data(self, preprocessed=False, apply_missing=False):
        df = self.data_file.get_dataframe()

        data_rows = self.get_data_rows()
        data_cols = self.get_data_cols()
        numeric_data = df.iloc[data_rows, data_cols]

        # if apply_missing:
        #     numeric_data = self.apply_missing(numeric_data)

        numeric_data = numeric_data.astype(float)

        if preprocessed:
            numeric_data = self.preprocess_data(numeric_data)

        return numeric_data.astype(float)

    # TODO: Study pass these by reference to optimize it
    def preprocess_data(self, df):
        data = df.values
        data = self.center_data(data)
        data = self.scale(data, self._rows_scale_group, self._scale_per_group)
        preprocessed_data = pd.DataFrame(data)
        return preprocessed_data

    def apply_missing(self, df):
        matrix = df.values
        func = None
        if self._missing_strategy == MissingStrategy.mean:
            func = lambda x, y: x+y
            print('mean')
        for i_col in range(matrix.shape[1]):
            # non_numeric = df.loc[~df.iloc[:, i_col].astype(str).str.isdigit()]
            non_numeric = df.iloc[:, i_col].astype(str).str.isdecimal()
            print('non_numeric ' + str(i_col) + ':\n' + str(non_numeric))

        df = pd.DataFrame(matrix)
        return df

    def center_data(self, matrix):
        m = np.mean(matrix, axis=0)
        centered_matrix = matrix - m
        return centered_matrix

    def scale(self, matrix, rows_scale_group, scale_per_group):
        freq = count_frequency(rows_scale_group)
        for i_col, scale_group in enumerate(rows_scale_group):
            scale_type = ScaleType(scale_per_group[scale_group])
            if scale_type == ScaleType.unitary:
                # scale_factor = np.std(matrix[i_col], axis=0)
                scale_factor = np.std(matrix[:, i_col])
            elif scale_type == ScaleType.pareto:
                m = freq[scale_group]
                std = np.std(matrix[:, i_col])
                scale_factor = std * (m ** (1/4))
            elif scale_type == ScaleType.equal_weigh:
                m = freq[scale_group]
                std = np.std(matrix[:, i_col])
                scale_factor = std * (m ** (1/2))
            else:
                print('Scale type not valid')
            matrix[:, i_col] = matrix[:, i_col] / scale_factor
        matrix[np.isnan(matrix)] = 0
        return matrix

    def get_name_and_data_file(self):
        return self.name + ' : ' + self.data_file.get_name()

    def difference_list(self, minuend, subtracting=list()):
        minuend[:] = list(set(minuend) - set(subtracting))

    def refresh_data_set_state(self, new_list, original_list,
                           substract_list1, substract_list2):
        # print('new_list: ' + str(new_list))
        # print('original_list: ' + str(original_list))
        original_list[:] = list(set(original_list + new_list))
        self.difference_list(substract_list1, new_list)
        self.difference_list(substract_list2, new_list)

    def get_data_rows(self):
        df = self.data_file.get_dataframe()
        all_rows = list(range(self.data_file.get_num_rows()))
        rows_to_remove = self.primary_rows + self.secondary_rows + self.discarded_rows
        data_rows = list(set(all_rows) - set(rows_to_remove))
        return data_rows

    def get_data_cols(self):
        df = self.data_file.get_dataframe()
        all_cols = list(range(self.data_file.get_num_cols()))
        cols_to_remove = self.primary_cols + self.secondary_cols + self.discarded_cols
        data_cols = list(set(all_cols) - set(cols_to_remove))
        return data_cols

    # Get all the column, not only ids
    def get_secondary_cols(self):
        df = self.data_file.get_dataframe()
        return df.iloc[:, self.secondary_cols]

    # ROWS
    def add_primary_rows(self, index):  # =QtCore.Qt. .QtModelIndex()):
        self.primary_rows = list()
        new_primary_row = [index.row()]
        self.refresh_data_set_state(new_primary_row, self.primary_rows,
                             self.secondary_rows, self.discarded_rows)

    def add_secondary_rows(self, indexes):
        new_secondary_rows = [x.row() for x in sorted(indexes)]
        self.refresh_data_set_state(new_secondary_rows, self.secondary_rows,
                             self.primary_rows, self.discarded_rows)

    def add_discard_rows(self, indexes):
        new_discarded_rows = [x.row() for x in sorted(indexes)]
        self.refresh_data_set_state(new_discarded_rows, self.discarded_rows,
                             self.primary_rows, self.secondary_rows)

    # TODO: Change this int functions in a more ellegant way
    def add_discard_rows_int(self, indexes):
        new_discarded_rows = [x for x in sorted(indexes)]
        self.refresh_data_set_state(new_discarded_rows, self.discarded_rows,
                             self.primary_rows, self.secondary_rows)

    def add_data_rows(self, indexes):
        new_data_rows = [x.row() for x in sorted(indexes)]
        self.difference_list(self.primary_rows, new_data_rows)
        self.difference_list(self.secondary_rows, new_data_rows)
        self.difference_list(self.discarded_rows, new_data_rows)

    # COLS
    def add_primary_cols(self, index):
        self.primary_cols = list()
        new_primary_col = [index.column()]
        self.refresh_data_set_state(new_primary_col, self.primary_cols,
                             self.secondary_cols, self.discarded_cols)

    def add_secondary_cols(self, indexes):
        new_secondary_cols = [x.column() for x in sorted(indexes)]
        self.refresh_data_set_state(new_secondary_cols, self.secondary_cols,
                             self.primary_cols, self.discarded_cols)

    def add_discard_cols(self, indexes):
        new_discarded_cols = [x.column() for x in sorted(indexes)]
        self.refresh_data_set_state(new_discarded_cols, self.discarded_cols,
                             self.primary_cols, self.secondary_cols)

    def add_data_cols(self, indexes):
        new_data_cols = [x.column() for x in sorted(indexes)]
        self.difference_list(self.primary_cols, new_data_cols)
        self.difference_list(self.secondary_cols, new_data_cols)
        self.difference_list(self.discarded_cols, new_data_cols)

    # TODO: Change all the "indixes" per "indices"
    # Map numeric row indixes to global data set
    def map_numeric_to_global(self, numeric_indixes):
        data_rows = self.get_data_rows()
        # TODO: Error message
        if len(numeric_indixes) > len(data_rows):
            print('There are more selected observations than observations.')
        global_rows = [data_rows[i] for i in numeric_indixes]
        # print('\ndata_rows: ' + str(data_rows))
        # print('\nnumeric_indixes: ' + str(numeric_indixes))
        return global_rows

    def var_names(self):
        df = self.data_file.get_dataframe()
        if len(self.primary_rows) == 1:
            row_index = self.primary_rows
            row = df.iloc[row_index, :].values[0]
            print('row')
        else:
            all_cols = list(range(self.data_file.get_num_cols()))
            row = ['Var'+str(i) for i in all_cols]
        var_names = [row[i] for i in self.get_data_cols()]
        return var_names

    # TODO: Long time consumer algorithms calculate in background and allow continue
    #  ¿New class? With a threshold of estimated time. If grater than threshold,
    #  show option if whant to calculate in background
    def correlation_matrix(self):
        df = self.get_numeric_data(preprocessed=False)
        print(df.corr().values)
        return df.corr().values

    def set_scales(self, rows_scale_group, scale_per_group):
        if len(rows_scale_group) == len(self.var_names()):
            self._rows_scale_group = rows_scale_group
            self._scale_per_group = scale_per_group
        else:
            # TODO: Error message
            print('There are different number of scales and variables')

    def set_missing_strategy(self, missing_strategy):
        self._missing_strategy = missing_strategy

    def get_rows_scale_group(self):
        return self._rows_scale_group

    def get_scale_per_group(self):
        return self._scale_per_group
