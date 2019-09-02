from GUI.DataSetsSelectorWindow import DataSetsSelectorWindow
from Controllers.Controller import Controller
from Controllers.EditDatasetController import EditDataSetController
from Models.DataFrameModel import DataFrameModel


class DataSetsSelectorController(Controller):

    def __init__(self, data_sets_manager):
        super().__init__()
        self._last_row_selected = 0
        self._data_sets_manager = data_sets_manager
        self._view = DataSetsSelectorWindow()
        self.refresh_data_set()
        self.refresh_list()
        self._view.list_widget.setCurrentRow(0)
        self.make_connections()

    def make_connections(self):
        self._view.list_widget.itemSelectionChanged.connect(self.refresh_last_row_selected)
        self._view.list_widget.itemSelectionChanged.connect(self.refresh_data_set)
        self._view.delete_button.clicked.connect(self.delete_selected)
        self._view.cancel_button.clicked.connect(self.cancel)
        self._view.edit_button.clicked.connect(self.edit_selected)

    def delete_selected(self):
        row_to_delete = self._last_row_selected
        if self._last_row_selected != 0:
            self._last_row_selected = self._last_row_selected - 1
            self._view.list_widget.setCurrentRow(self._last_row_selected)
        self._data_sets_manager.remove_by_index(row_to_delete)
        self.refresh_list()

    def cancel(self):
        self._view.close()

    # TODO: Define behaviour when trying to edit a data set linked with a model
    #  Posibility 1: Can't edit it. Explanation window. Only create a copy and edit that copy
    #  Posibility 2: Warning: data set is linked with 1..., 2..., n... models. Can edit but must ¿remodel?
    def edit_selected(self):
        data_set = self._data_sets_manager.get_by_index(self._last_row_selected)
        self._edit_dataset_controller = EditDataSetController(
            data_set,
            self._data_sets_manager
        )
        self._edit_dataset_controller.connect_to_close(self.refresh_list)

    def refresh_data_set(self):
        print('refresh_data_set: ' + str(self._last_row_selected))
        data_set = self._data_sets_manager.get_by_index(self._last_row_selected)
        dataframe_model = DataFrameModel(data_set.data_file.get_dataframe())
        dataframe_model.set_rows_and_cols_info(data_set.primary_rows, data_set.secondary_rows,
                                               data_set.discarded_rows, data_set.primary_cols,
                                               data_set.secondary_cols, data_set.discarded_cols)
        self._view.refresh_data_set(dataframe_model, data_set.description)

    def refresh_list(self):
        self._view.refresh_list(self._data_sets_manager.all_names_and_data_file())
        self._view.list_widget.setCurrentRow(self._last_row_selected)

    def refresh_last_row_selected(self):
        current_row = self._view.list_widget.currentRow()
        if current_row >= self._view.list_widget.count():
            self._last_row_selected = self._view.list_widget.count() - 1
        elif current_row != -1:
            self._last_row_selected = current_row
        print('self._view.list_widget.currentRow() = ' + str(self._view.list_widget.currentRow()))