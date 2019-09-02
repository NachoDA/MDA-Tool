from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from GUI.View import View
from GUI.Style import get_style
from GUI.MVAQWidget import MVAQWidget


class EditDatasetWindow(View):

    # TODO: Add option to add a observations ID column and fill it automatically (1, 2...)
    # TODO: Add option to add a variable ID row and fill it automatically (Var1, Var2...)
    def __init__(self, dataframe_model, dataset_name, description):
        super().__init__()
        self._dataframe_model = dataframe_model
        self._dataset_name = dataset_name
        self._description = description
        self.init_UI()
        #TODO: Manejo básico de datos faltantes:
        # ... df = df.dropna() (columnas o las observaciones)
        # ... o media

    def init_UI(self):
        self._window.resize(1200, 800)
        text_max_width = 200
        self._window.setStyleSheet(get_style().get_stylesheet('editDataset'))
        self._window.show()

        general_layout = QVBoxLayout(self._window)
        central_layout = QHBoxLayout(self._window)

        # Left - Name and buttons
        # Name
        name_layout = QHBoxLayout(self._window)
        self.name_box = QLineEdit(self._window)
        self.name_box.setMaximumWidth(text_max_width)
        self.name_box.setText(self._dataset_name)
        name_layout.addWidget(self.name_box)
        # Buttons
        row_group_buttons = QGroupBox('Set rows', self._window)
        row_group_layout = QVBoxLayout(self._window)
        self.primary_row_button = QPushButton(row_group_buttons)
        self.primary_row_button.setText('Primary ID')
        self.primary_row_button.setObjectName('PrimaryRow')
        self.secondary_row_button = QPushButton(row_group_buttons)
        self.secondary_row_button.setText('Secondary IDs')
        self.secondary_row_button.setObjectName('SecondaryRow')
        row_group_layout.addWidget(self.primary_row_button)
        row_group_layout.addWidget(self.secondary_row_button)
        row_group_buttons.setLayout(row_group_layout)

        col_group_buttons = QGroupBox('Set columns', self._window)
        col_group_layout = QVBoxLayout(self._window)
        self.primary_col_button = QPushButton(col_group_buttons)
        self.primary_col_button.setText('Primary ID')
        self.primary_col_button.setObjectName('PrimaryCol')
        self.secondary_col_button = QPushButton(col_group_buttons)
        self.secondary_col_button.setText('Secondary IDs')
        self.secondary_col_button.setObjectName('SecondaryCol')
        col_group_layout.addWidget(self.primary_col_button)
        col_group_layout.addWidget(self.secondary_col_button)
        col_group_buttons.setLayout(col_group_layout)

        both_group_buttons = QGroupBox('Set rows and columns', self._window)
        both_group_layout = QVBoxLayout(self._window)
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
        self.description_area = QTextEdit(self._window)
        self.description_area.setMaximumWidth(text_max_width)
        self.description_area.setPlaceholderText('Write a description (optional)')
        self.description_area.setPlainText(self._description)

        buttons_layout = QVBoxLayout(self._window)
        buttons_layout.addItem(name_layout)
        buttons_layout.addWidget(row_group_buttons)
        buttons_layout.addWidget(col_group_buttons)
        buttons_layout.addWidget(both_group_buttons)
        buttons_layout.addWidget(self.description_area)
        buttons_layout.addStretch(1)

        # Right - Table
        self.table = QTableView(self._window)
        self.table.show()
        self.table.setModel(self._dataframe_model)

        # Below - Buttons
        self.cancel_button = QPushButton(self._window)
        self.cancel_button.setText('Cancel')
        # TODO: Focus on save_button
        self.save_button = QPushButton(self._window)
        self.save_button.setText('Save data set')
        below_layout = QHBoxLayout(self._window)
        below_layout.addWidget(self.cancel_button)
        below_layout.addWidget(self.save_button)
        below_layout.setAlignment(QtCore.Qt.AlignRight)

        # Final layout compositions
        central_layout.addLayout(buttons_layout)
        central_layout.addWidget(self.table)
        general_layout.addLayout(central_layout)
        general_layout.addLayout(below_layout)

    def get_data_set_name(self):
        return self.name_box.text()

    def close(self):
        self._window.close()
