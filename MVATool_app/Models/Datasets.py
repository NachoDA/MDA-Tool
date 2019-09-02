from sklearn import preprocessing
import pandas as pd

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

    # Allow comparison between data sets. Used in dict
    def __hash__(self):
        return hash(str(self))

    def get_numeric_data(self, preprocessed=False):
        df = self.data_file.get_dataframe()
        data_rows = self.get_data_rows()
        data_cols = self.get_data_cols()
        numeric_data = df.iloc[data_rows, data_cols]

        if preprocessed:
            numeric_data = self.preprocess_data(numeric_data)

        return numeric_data

    def preprocess_data(self, df):
        scaled = preprocessing.scale(df)
        preprocessed_data = pd.DataFrame(scaled)
        return preprocessed_data

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