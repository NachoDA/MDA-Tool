from GUI.ModelsCreatorWindow import ModelsCreatorWindow
from Controllers.Controller import Controller
from Models.StatModels import *
from enum import Enum


class ModelType(Enum):
    PCA = 1


class ModelsCreatorController(Controller):

    def __init__(self, models_manager, data_sets_manager, model_type):
        super().__init__()
        self._models_manager = models_manager
        self._data_sets_manager = data_sets_manager
        self._view = ModelsCreatorWindow(model_type,
                                         data_sets_manager.all_names_and_data_file(),
                                         self._models_manager.count())
        self._view.select_last_data_set()
        self.make_connections()

    # TODO: Block window to avoid interaction in main window
    def make_connections(self):
        self._view.cancel_button.clicked.connect(self.cancel)
        self._view.create_button.clicked.connect(self.create_model)

    def create_model(self):
        name = self._view.pca_creator.name_box.text()
        index_data_set = self._view.pca_creator.data_set_widget.data_sets_combo.currentIndex()
        data_set = self._data_sets_manager.get_by_index(index_data_set)
        num_components = self._view.pca_creator.components_widget.components_box.value()
        model = self._models_manager.create_PCA(name, data_set, num_components)
        self._view.close()

    def cancel(self):
        self._view.close()
