from GUI.EditDatasetWindow import *
from Controllers.Controller import Controller
from Models.DataFrameModel import DataFrameModel
from Models.Datasets import ScaleType, MissingStrategy
import pandas as pd


class EditDataSetController(Controller):

    def __init__(self, data_set, data_sets_manager):
        super().__init__()
        self._dataframe_model = DataFrameModel(data_set.data_file.get_dataframe())
        self._dataframe_model.set_rows_and_cols_info(data_set.primary_rows, data_set.secondary_rows,
                                                     data_set.discarded_rows, data_set.primary_cols,
                                                     data_set.secondary_cols, data_set.discarded_cols)
        self._data_set = data_set
        self.data_sets_manager = data_sets_manager
        self._view = EditDatasetWindow(self._dataframe_model, data_set.name,
                                       data_set.description, data_set.var_names())
        self.init_scale_widget()
        self._view.save_button.setFocus()
        self.make_connections()

    def make_connections(self):
        # TODO: When closing window with cross, data set must not be created
        # TODO: Change access to signals from View. Call _window must be avoided
        # self._view._window.close_signal.connect(self.close)
        self._view.tab_widget.currentChanged.connect(self.tab_changed)
        # DATA SET TABLE WIDGET
        # rows
        self._view.table_widget.primary_row_button.clicked.connect(self.add_primary_rows)
        self._view.table_widget.secondary_row_button.clicked.connect(self.add_secondary_rows)
        # cols
        self._view.table_widget.primary_col_button.clicked.connect(self.add_primary_cols)
        self._view.table_widget.secondary_col_button.clicked.connect(self.add_secondary_cols)
        # rows and cols
        self._view.table_widget.discard_both_button.clicked.connect(self.add_discard)
        self._view.table_widget.data_both_button.clicked.connect(self.add_data)
        # below buttons
        self._view.cancel_button.clicked.connect(self.close)
        self._view.save_button.clicked.connect(self.save)
        # SCALE WIDGET
        self._view.scale_widget.set_group_button.clicked.connect(self.on_group_button_clicked)

    def tab_changed(self):
        current_widget = self._view.tab_widget.currentWidget()
        print(current_widget)
        if isinstance(current_widget, ScaleWidget):
            self.init_scale_widget()

    def init_scale_widget(self):
        # This logic shouldn't be here
        var_names = self._data_set.var_names()
        scales = self._data_set.get_rows_scale_group()
        if scales is None:
            scales = [0] * len(var_names)
            scale_per_group = [ScaleType.unitary]
            num_groups = 1
        else:
            scale_per_group = self._data_set.get_scale_per_group()
            num_groups = len(scale_per_group)
        self._view.scale_widget.set_list_scales(scale_per_group)
        self._view.scale_widget.refresh_combo_box(num_groups=num_groups)
        self.set_scale_df(var_names, scales)

    def set_scale_df(self, var_names, blocks):
        data = {'Variables': var_names,
                'Block group': blocks}
        df = pd.DataFrame(data)
        df_model = DataFrameModel(df)
        self._view.scale_widget.set(df_model)

    def on_group_button_clicked(self):
        # TODO: Color cells by scale group
        indexes = self._view.scale_widget.table.selectionModel().selectedIndexes()
        index_combo = self._view.scale_widget.groups_combo_box.currentIndex()
        blocks = self._view.scale_widget.scales_list.copy()
        for index in indexes:
            blocks[index.row()] = index_combo

        need_new_group = len(indexes) != 0 and \
                         index_combo == self._view.scale_widget.num_groups
        if need_new_group:
            self.add_scale_group()

        var_names = self._data_set.var_names()
        self.set_scale_df(var_names, blocks)

    def add_scale_group(self):
        # TODO: Logic variables must be in logic layer... Makes no sense read it from
        #  View each time
        scale_per_group = self._view.scale_widget.scale_per_group + [ScaleType.unitary]
        self._view.scale_widget.refresh_combo_box(len(scale_per_group))
        self._view.scale_widget.set_list_scales(scale_per_group)


    # def scale_combo_box_changed(self):


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
        indexes = self._view.table_widget.table.selectionModel().selectedRows()
        if len(indexes) > 1:
            # TODO: Add warning window
            print('Primary row must be unique!')
        if len(indexes) > 0:
            first_index = indexes[0]
            self._data_set.add_primary_rows(first_index)
            self.refresh_marked_rows()

    def add_secondary_rows(self):
        indexes = self._view.table_widget.table.selectionModel().selectedRows()
        self._data_set.add_secondary_rows(indexes)
        self.refresh_marked_rows()

    def add_discard_rows(self, indexes=None):
        if indexes is None:
            indexes = self._view.table_widget.table.selectionModel().selectedRows()
        self._data_set.add_discard_rows(indexes)
        self.refresh_marked_rows()

    # TODO: Change this int functions in a more elegant way
    def add_discard_rows_int(self, indexes=None):
        if indexes is None:
            indexes = self._view.table_widget.table.selectionModel().selectedRows()
        self._data_set.add_discard_rows_int(indexes)
        self.refresh_marked_rows()

    def add_data_rows(self):
        indexes = self._view.table_widget.table.selectionModel().selectedRows()
        self._data_set.add_data_rows(indexes)
        self.refresh_marked_rows()

    def refresh_marked_rows(self):
        self._view.table_widget.table.model().primary_rows = self._data_set.primary_rows
        self._view.table_widget.table.model().secondary_rows = self._data_set.secondary_rows
        self._view.table_widget.table.model().discarded_rows = self._data_set.discarded_rows

    # COLS
    def add_primary_cols(self):
        indexes = self._view.table_widget.table.selectionModel().selectedColumns()
        if len(indexes) > 1:
            # TODO: Add warning window
            print('Primary collumn must be unique!')
        if len(indexes) > 0:
            first_index = indexes[0]
            self._data_set.add_primary_cols(first_index)
            self.refresh_marked_cols()

    def add_secondary_cols(self):
        indexes = self._view.table_widget.table.selectionModel().selectedColumns()
        self._data_set.add_secondary_cols(indexes)
        self.refresh_marked_cols()

    def add_discard_cols(self):
        indexes = self._view.table_widget.table.selectionModel().selectedColumns()
        self._data_set.add_discard_cols(indexes)
        self.refresh_marked_cols()

    def add_data_cols(self):
        indexes = self._view.table_widget.table.selectionModel().selectedColumns()
        self._data_set.add_data_cols(indexes)
        self.refresh_marked_cols()

    def refresh_marked_cols(self):
        self._view.table_widget.table.model().primary_cols = self._data_set.primary_cols
        self._view.table_widget.table.model().secondary_cols = self._data_set.secondary_cols
        self._view.table_widget.table.model().discarded_cols = self._data_set.discarded_cols
        # TODO: Change the way to deal with this. Is not elegant. Use events or something similar
        self.init_scale_widget()

    # CLOSE and SAVE
    # TODO: Check in close and save that data is numeric
    def close(self):
        self.data_sets_manager.remove(self._data_set.name)
        self._view.close()

    def save(self):
        self._data_set.name = self._view.table_widget.name_box.text()
        self._data_set.description = self._view.table_widget.description_area.toPlainText()
        scale_per_group = [ScaleType(scale_type.currentIndex())
                           for scale_type in self._view.scale_widget.combo_boxes]
        self._data_set.set_scales(self._view.scale_widget.scales_list, scale_per_group)
        # strategy = int(self._view.missing_widget.buttons_group.checkedId())
        # print('strategy: ' + str(strategy))
        # if strategy != -1:
        #     self._data_set.set_missing_strategy(MissingStrategy(strategy))
        self._view.close()
