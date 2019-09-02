from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from GUI.View import View


class ModelsCreatorWindow(View):

    def __init__(self, model_type, data_sets_names, number_models):
        super().__init__()
        self._model_type = model_type
        self._data_sets_names = data_sets_names
        self._number_models = number_models
        self.init_UI()

    def init_UI(self):
        self._window.resize(300, 300)
        self._window.show()
        layout = QVBoxLayout(self._window)

        tab_widget = QTabWidget(self._window)
        self.pca_creator = PCACreatorWidget(self._data_sets_names, self._number_models)
        tab_widget.addTab(self.pca_creator, 'PCA')
        tab_widget.show()

        # Below buttons
        self.cancel_button = QPushButton(self._window)
        self.cancel_button.setText('Cancel')
        # TODO: Focus on save_button
        self.create_button = QPushButton(self._window)
        self.create_button.setText('Create')
        below_layout = QHBoxLayout(self._window)
        below_layout.addWidget(self.cancel_button)
        below_layout.addWidget(self.create_button)
        below_layout.setAlignment(QtCore.Qt.AlignRight)

        layout.addWidget(tab_widget)
        layout.addLayout(below_layout)

    # TODO: Adapt this to generic cases
    def select_last_data_set(self):
        combo = self.pca_creator.data_set_widget.data_sets_combo
        last_index_combo = combo.count()
        combo.setCurrentIndex(last_index_combo-1)

    def close(self):
        self._window.close()


class SetDataSetWidget(QWidget):

    def __init__(self, data_sets_names):
        super().__init__()
        self._data_sets_names = data_sets_names
        self.init_UI()

    def init_UI(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Set data set group
        data_set_group = QGroupBox('Set data set', self)
        data_sets_layout = QVBoxLayout(self)
        self.data_sets_combo = QComboBox(self)
        self.data_sets_combo.addItems(self._data_sets_names)
        data_sets_buttons_layout = QHBoxLayout(self)
        # TODO: Implementar la funcionalidad de los botones
        # self.new_data_set_button = QPushButton(self)
        # self.new_data_set_button.setText('New data set...')
        # self.from_data_set_button = QPushButton(self)
        # self.from_data_set_button.setText('New from selected...')
        # data_sets_buttons_layout.addWidget(self.new_data_set_button)
        # data_sets_buttons_layout.addWidget(self.from_data_set_button)
        data_sets_layout.addWidget(self.data_sets_combo)
        data_sets_layout.addLayout(data_sets_buttons_layout)
        data_set_group.setLayout(data_sets_layout)

        layout.addWidget(data_set_group)


class ComponentsWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        components_group = QGroupBox('Components', self)
        components_layout = QHBoxLayout(self)
        name_box = QLabel(self)
        name_box.setText('Number of components:')
        self.components_box = QSpinBox(self)
        self.components_box.setValue(3)
        components_layout.addWidget(name_box)
        components_layout.addWidget(self.components_box)
        components_group.setLayout(components_layout)

        layout.addWidget(components_group)

class PCACreatorWidget(QWidget):

    def __init__(self, data_sets_names, number_models):
        super().__init__()
        self.data_sets_names = data_sets_names
        self._number_models = number_models
        self.init_UI()

    def init_UI(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        text_max_width = 200
        # Model name
        self.name_box = QLineEdit(self)
        self.name_box.setMaximumWidth(text_max_width)
        self.name_box.setText('Model name ' + str(self._number_models))

        layout.addWidget(self.name_box)
        self.data_set_widget = SetDataSetWidget(self.data_sets_names)
        self.components_widget = ComponentsWidget()
        layout.addWidget(self.data_set_widget)
        layout.addWidget(self.components_widget)
        layout.addStretch(1)