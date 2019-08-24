from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from GUI.View import View
from GUI.Style import get_style


class DataSetsSelectorWindow(View):

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self._window.resize(1200, 800)
        list_max_width = 300
        table_max_heigh = 600
        description_max_heigh = 120
        self._window.show()

        general_layout = QHBoxLayout(self._window)

        # Left - List layout
        left_layout = QVBoxLayout(self._window)
        self.list_widget = QListWidget(self._window)
        self.list_widget.setMaximumWidth(list_max_width)
        self.list_widget.show()
        left_layout.addWidget(self.list_widget)

        # Right - Table, descriptor and buttons
        right_layout = QVBoxLayout(self._window)
        # Table
        self.table = QTableView(self._window)
        self.table.show()
        # Text area
        self.description_area = QTextEdit(self._window)
        self.description_area.setMaximumHeight(description_max_heigh)
        self.description_area.setReadOnly(True)
        # Below - Buttons
        # Cancel and edit
        self.cancel_button = QPushButton(self._window)
        self.cancel_button.setText('Cancel')
        # TODO: Focus on edit button
        self.edit_button = QPushButton(self._window)
        self.edit_button.setText('Edit data set')
        both_bottons_layout = QHBoxLayout(self._window)
        both_bottons_layout.addWidget(self.cancel_button)
        both_bottons_layout.addWidget(self.edit_button)
        both_bottons_layout.setAlignment(QtCore.Qt.AlignRight)
        # Delete
        # TODO: Add confirmation window
        delete_layout = QHBoxLayout(self._window)
        self.delete_button = QPushButton(self._window)
        self.delete_button.setText('Delete')
        delete_layout.addWidget(self.delete_button)
        delete_layout.setAlignment(QtCore.Qt.AlignLeft)

        below_layout = QHBoxLayout(self._window)
        below_layout.addLayout(delete_layout)
        below_layout.addLayout(both_bottons_layout)

        right_layout.addWidget(self.table)
        right_layout.addWidget(self.description_area)
        right_layout.addLayout(below_layout)

        general_layout.addLayout(left_layout)
        general_layout.addLayout(right_layout)

    def refresh_data_set(self, dataframe_model, description):
        self.table.setModel(dataframe_model)
        self.description_area.setText(description)

    def refresh_list(self, data_set_names):
        self.list_widget.clear()
        self.list_widget.addItems(data_set_names)
        self.list_widget.repaint()

    def close(self):
        self._window.close()