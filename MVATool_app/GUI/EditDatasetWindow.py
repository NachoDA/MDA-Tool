from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from GUI.View import View
from GUI.Style import get_style
from Models.Datasets import MissingStrategy


class EditDatasetWindow(View):

    _dataframe_model = None
    _dataset_name = 'dataset_name'
    _description = 'description'

    # TODO: Add option to add a observations ID column and fill it automatically (1, 2...)
    # TODO: Add option to add a variable ID row and fill it automatically (Var1, Var2...)
    def __init__(self, dataframe_model, dataset_name, description, var_names):
        super().__init__()
        self._dataframe_model = dataframe_model
        self._dataset_name = dataset_name
        self._description = description
        self._var_names = var_names
        self.init_UI()
        #TODO: Manejo básico de datos faltantes:
        # ... df = df.dropna() (columnas o las observaciones)
        # ... o media

    def init_UI(self):
        self._window.resize(1200, 800)
        self._window.setStyleSheet(get_style().get_stylesheet('editDataset'))
        self._window.show()

        general_layout = QVBoxLayout(self._window)
        self.tab_widget = QTabWidget(self._window)
        self.table_widget = DatasetTableWidget(self._dataframe_model, self._dataset_name,
                                               self._description)
        self.tab_widget.addTab(self.table_widget, 'Table data')
        self.observations_widget = ObservationsWidget()
        # self.tab_widget.addTab(self.observations_widget, 'Observations')
        self.scale_widget = ScaleWidget(self._var_names)
        self.tab_widget.addTab(self.scale_widget, 'Scale')
        # self.missing_widget = MissingWidget()
        # self.tab_widget.addTab(self.missing_widget, 'Missing')
        self.tab_widget.show()

        # Below - Buttons
        self.cancel_button = QPushButton()
        self.cancel_button.setText('Cancel')
        # TODO: Focus on save_button
        self.save_button = QPushButton()
        self.save_button.setText('Save data set')
        below_layout = QHBoxLayout()
        below_layout.addWidget(self.cancel_button)
        below_layout.addWidget(self.save_button)
        below_layout.setAlignment(QtCore.Qt.AlignRight)

        general_layout.addWidget(self.tab_widget)
        general_layout.addLayout(below_layout)

    def get_data_set_name(self):
        return self.name_box.text()

    def close(self):
        self._window.close()


class ScaleWidget(QWidget):

    def __init__(self, var_names):
        super().__init__()
        self.scales_list = [0] * len(var_names)
        self.scale_per_group = list()
        self.combo_boxes = list()
        self.init_UI()

    def init_UI(self):
        general_layout = QHBoxLayout()
        self.setLayout(general_layout)

        self.table = QTableView()
        self.table.show()

        options_layout = QVBoxLayout()
        # Set groups
        set_group_layout = QHBoxLayout()
        label_set = QLabel()
        label_set.setText('Set group to selected: ')
        self.groups_combo_box = QComboBox()
        self.groups_combo_box.setMinimumWidth(100)
        self.set_group_button = QPushButton()
        self.set_group_button.setText('Set')
        set_group_layout.addWidget(label_set)
        set_group_layout.addWidget(self.groups_combo_box)
        set_group_layout.addWidget(self.set_group_button)
        # Scales
        scales_group = QGroupBox('Scales')
        self._scales_layout = QVBoxLayout()
        scales_group.setLayout(self._scales_layout)

        # Final layout compositions
        options_layout.addLayout(set_group_layout)
        options_layout.addWidget(scales_group)
        general_layout.addWidget(self.table)
        general_layout.addLayout(options_layout)

    # TODO: Rename all vars and funcs. It's a mess
    def set(self, df_model):
        self.table.setModel(df_model)
        self.scales_list = df_model.select(cols=-1).values

    def refresh_combo_box(self, num_groups):
        self.num_groups = num_groups
        self.groups_combo_box.clear()
        groups_list = ['Group ' + str(i) for i in range(num_groups+1)]
        self.groups_combo_box.addItems(groups_list)

    def set_list_scales(self, scale_per_group):
        self.scale_per_group = scale_per_group
        self.combo_boxes = list()
        # Clear layout
        for i in reversed(range(self._scales_layout.count())):
            widget = self._scales_layout.takeAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        for i, scale_type in enumerate(self.scale_per_group):
            layout = QHBoxLayout()
            label_set = QLabel()
            label_set.setText('Group ' + str(i))
            groups_combo_box = QComboBox()
            groups_combo_box.addItem('UV: 1/std')
            groups_combo_box.addItem('pareto: 1 / (std * (m^(1/4))')
            groups_combo_box.addItem('equal weigh: 1 / (std * (m^(1/2))')
            groups_combo_box.setCurrentIndex(int(scale_type))
            layout.addWidget(label_set)
            layout.addWidget(groups_combo_box)
            self.combo_boxes.append(groups_combo_box)
            self._scales_layout.addLayout(layout)

        self._scales_layout.addStretch()


class MissingWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        general_layout = QVBoxLayout()
        self.setLayout(general_layout)

        group_box = QGroupBox('Set strategy')
        layout = QVBoxLayout()
        self.buttons_group = QButtonGroup()
        mean_button = QRadioButton('Mean')
        mean_button.setChecked(True)
        self.buttons_group.addButton(mean_button, int(MissingStrategy.mean))
        # discard_row_button = QRadioButton('Discard row')
        # self.buttons_group.addButton(discard_row_button, int(MissingStrategy.discard_row))
        # discard_column_button = QRadioButton('Discard column')
        # self.buttons_group.addButton(discard_column_button, int(MissingStrategy.discard_column))
        knn_imputation_button = QRadioButton('KNN imputation')
        self.buttons_group.addButton(knn_imputation_button, int(MissingStrategy.knn_imputation))

        layout.addWidget(mean_button)
        # layout.addWidget(discard_row_button)
        # layout.addWidget(discard_column_button)
        layout.addWidget(knn_imputation_button)
        layout.addStretch()
        group_box.setLayout(layout)

        general_layout.addWidget(group_box)


class ObservationsWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        general_layout = QVBoxLayout()
        self.setLayout(general_layout)

        # Final layout compositions
        # central_layout.addLayout(buttons_layout)
        # central_layout.addWidget(self.table)
        # general_layout.addLayout(central_layout)
        # general_layout.addLayout(below_layout)


class DatasetTableWidget(QWidget):

    def __init__(self, dataframe_model, dataset_name, description):
        super().__init__()
        self._dataframe_model = dataframe_model
        self._dataset_name = dataset_name
        self._description = description
        self.init_UI()

    def init_UI(self):
        general_layout = QVBoxLayout()
        self.setLayout(general_layout)
        central_layout = QHBoxLayout()
        text_max_width = 200

        # Left - Name and buttons
        # Name
        name_layout = QHBoxLayout()
        self.name_box = QLineEdit()
        self.name_box.setMaximumWidth(text_max_width)
        self.name_box.setText(self._dataset_name)
        name_layout.addWidget(self.name_box)
        # Buttons
        row_group_buttons = QGroupBox('Set rows')
        row_group_layout = QVBoxLayout()
        self.primary_row_button = QPushButton(row_group_buttons)
        self.primary_row_button.setText('Primary ID')
        self.primary_row_button.setObjectName('PrimaryRow')
        self.secondary_row_button = QPushButton(row_group_buttons)
        self.secondary_row_button.setText('Secondary IDs')
        self.secondary_row_button.setObjectName('SecondaryRow')
        row_group_layout.addWidget(self.primary_row_button)
        row_group_layout.addWidget(self.secondary_row_button)
        row_group_buttons.setLayout(row_group_layout)

        col_group_buttons = QGroupBox('Set columns')
        col_group_layout = QVBoxLayout()
        self.primary_col_button = QPushButton(col_group_buttons)
        self.primary_col_button.setText('Primary ID')
        self.primary_col_button.setObjectName('PrimaryCol')
        self.secondary_col_button = QPushButton(col_group_buttons)
        self.secondary_col_button.setText('Secondary IDs')
        self.secondary_col_button.setObjectName('SecondaryCol')
        col_group_layout.addWidget(self.primary_col_button)
        col_group_layout.addWidget(self.secondary_col_button)
        col_group_buttons.setLayout(col_group_layout)

        both_group_buttons = QGroupBox('Set rows and columns')
        both_group_layout = QVBoxLayout()
        self.discard_both_button = QPushButton(both_group_buttons)
        self.discard_both_button.setText('Discard')
        self.discard_both_button.setObjectName('Discard')
        self.data_both_button = QPushButton(both_group_buttons)
        self.data_both_button.setText('Data')
        self.data_both_button.setObjectName('Data')
        both_group_layout.addWidget(self.discard_both_button)
        both_group_layout.addWidget(self.data_both_button)
        both_group_buttons.setLayout(both_group_layout)

        # Text area
        self.description_area = QTextEdit()
        self.description_area.setMaximumWidth(text_max_width)
        self.description_area.setPlaceholderText('Write a description (optional)')
        self.description_area.setPlainText(self._description)

        buttons_layout = QVBoxLayout()
        buttons_layout.addItem(name_layout)
        buttons_layout.addWidget(row_group_buttons)
        buttons_layout.addWidget(col_group_buttons)
        buttons_layout.addWidget(both_group_buttons)
        buttons_layout.addWidget(self.description_area)
        buttons_layout.addStretch(1)

        # Right - Table
        self.table = QTableView()
        self.table.show()
        self.table.setModel(self._dataframe_model)

        # Final layout compositions
        central_layout.addLayout(buttons_layout)
        central_layout.addWidget(self.table)
        general_layout.addLayout(central_layout)
