from GUI.EditDatasetWindow import EditDatasetWindow
from Controllers.Controller import Controller
from Models.DataFrameModel import DataFrameModel


class EditDataSetController(Controller):

    def __init__(self, data_set, data_sets_manager):
        super().__init__()
        self._dataframe_model = DataFrameModel(data_set.data_file.get_dataframe())
        self._dataframe_model.set_rows_and_cols_info(data_set.primary_rows, data_set.secondary_rows,
                                                     data_set.discarded_rows, data_set.primary_cols,
                                                     data_set.secondary_cols, data_set.discarded_cols)
        self._data_set = data_set
        self.data_sets_manager = data_sets_manager
        self._view = EditDatasetWindow(self._dataframe_model, data_set.name, data_set.description)
        self._view.save_button.setFocus()
        self.make_connections()

    def make_connections(self):
        # TODO: When closing window with cross, data set must not be created
        # TODO: Change access to signals from View. Call _window must be avoided
        # self._view._window.close_signal.connect(self.close)
        # rows
        self._view.primary_row_button.clicked.connect(self.add_primary_rows)
        self._view.secondary_row_button.clicked.connect(self.add_secondary_rows)
        # cols
        self._view.primary_col_button.clicked.connect(self.add_primary_cols)
        self._view.secondary_col_button.clicked.connect(self.add_secondary_cols)
        # rows and cols
        self._view.discard_both_button.clicked.connect(self.add_discard)
        self._view.data_both_button.clicked.connect(self.add_data)
        # below buttons
        self._view.cancel_button.clicked.connect(self.close)
        self._view.save_button.clicked.connect(self.save)

    def get_current_data_set_name(self):
        return self._data_set.name

    # --- Manage signals ---#
    def add_discard(self):
        self.add_discard_rows()
        self.add_discard_cols()

    def add_data(self):
        self.add_data_rows()
        self.add_data_cols()

    # TODO: Changes must be reflected when are done, not only when another click is done
    # ROWS
    def add_primary_rows(self):
        indexes = self._view.table.selectionModel().selectedRows()
        if len(indexes) > 1:
            # TODO: Add warning window
            print('Primary row must be unique!')
        if len(indexes) > 0:
            first_index = indexes[0]
            self._data_set.add_primary_rows(first_index)
            self.refresh_marked_rows()

    def add_secondary_rows(self):
        indexes = self._view.table.selectionModel().selectedRows()
        self._data_set.add_secondary_rows(indexes)
        self.refresh_marked_rows()

    def add_discard_rows(self, indexes=None):
        if indexes is None:
            indexes = self._view.table.selectionModel().selectedRows()
        self._data_set.add_discard_rows(indexes)
        self.refresh_marked_rows()

    # TODO: Change this int functions in a more ellegant way
    def add_discard_rows_int(self, indexes=None):
        if indexes is None:
            indexes = self._view.table.selectionModel().selectedRows()
        self._data_set.add_discard_rows_int(indexes)
        self.refresh_marked_rows()

    def add_data_rows(self):
        indexes = self._view.table.selectionModel().selectedRows()
        self._data_set.add_data_rows(indexes)
        self.refresh_marked_rows()

    def refresh_marked_rows(self):
        self._view.table.model().primary_rows = self._data_set.primary_rows
        self._view.table.model().secondary_rows = self._data_set.secondary_rows
        self._view.table.model().discarded_rows = self._data_set.discarded_rows

    # COLS
    def add_primary_cols(self):
        indexes = self._view.table.selectionModel().selectedColumns()
        if len(indexes) > 1:
            # TODO: Add warning window
            print('Primary collumn must be unique!')
        if len(indexes) > 0:
            first_index = indexes[0]
            self._data_set.add_primary_cols(first_index)
            self.refresh_marked_cols()

    def add_secondary_cols(self):
        indexes = self._view.table.selectionModel().selectedColumns()
        self._data_set.add_secondary_cols(indexes)
        self.refresh_marked_cols()

    def add_discard_cols(self):
        indexes = self._view.table.selectionModel().selectedColumns()
        self._data_set.add_discard_cols(indexes)
        self.refresh_marked_cols()

    def add_data_cols(self):
        indexes = self._view.table.selectionModel().selectedColumns()
        self._data_set.add_data_cols(indexes)
        self.refresh_marked_cols()

    def refresh_marked_cols(self):
        self._view.table.model().primary_cols = self._data_set.primary_cols
        self._view.table.model().secondary_cols = self._data_set.secondary_cols
        self._view.table.model().discarded_cols = self._data_set.discarded_cols

    # CLOSE and SAVE
    # TODO: Check in close and save that data is numeric
    def close(self):
        self.data_sets_manager.remove(self._data_set.name)
        self._view.close()

    def save(self):
        self._data_set.name = self._view.name_box.text()
        self._data_set.description = self._view.description_area.toPlainText()
        self._view.close()
