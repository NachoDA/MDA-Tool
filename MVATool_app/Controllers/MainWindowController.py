import sys
import os.path
from PyQt5.QtWidgets import *
from GUI.MainWindow import MainWindow
from Controllers.Controller import Controller
from Controllers.EditDatasetController import EditDataSetController
from Controllers.DataSetsSelectorController import DataSetsSelectorController
from Controllers.ModelsManagerController import ModelsManagerController
from Controllers.ModelsCreatorController import *
from Models.MainWindowModel import MainWindowModel
from Models.Datasets import DataSetsManager
from Models.DataFiles import DataFilesManager
from Models.StatModels import StatModelsManager

class MainWindowController(Controller):

    def __init__(self):
        self._app = QApplication(sys.argv)
        super().__init__()
        self._view = MainWindow()
        self._view.show()
        self._model = MainWindowModel()
        self.make_connections()

        self.data_sets_manager = DataSetsManager()
        self.data_files_manager = DataFilesManager()
        self.models_manager = StatModelsManager()
        self.load_path = 'C:\\Users\\Nacho\\Documents\\MVATool\\Datos'
        self._edit_dataset_controller = None

    def make_connections(self):
        self._view.on_load_file.connect(self.on_load_file)
        self._view.on_new_data_set.connect(self.on_new_data_set)
        self._view.on_edit_data_set.connect(self.on_edit_data_set)
        self._view.on_models.connect(self.on_models)
        self._view.on_create_PCA.connect(self.on_create_PCA)

    def run(self):
        self._view.show()
        return self._app.exec()

    # -------------      signals       -----------------

    def on_load_file(self):
        file_dialog = QFileDialog()
        file_path_to_load, file_type_to_load = file_dialog.getOpenFileName(
            self._view, "Load file", self.load_path, "Excel Files (*.xls);;Excel 2013 Files (*.xlsx);;CSV Files (*.csv)")

        file_loaded = self._model.load_file(file_path_to_load, file_type_to_load)

        if file_loaded is None:
            print("File is empty")
        else:
            data_file_name = os.path.basename(file_path_to_load)
            default_data_set_name = "data set name " + str(self.data_sets_manager.count())
            data_file = self.data_files_manager.create_data(data_file_name, file_loaded)
            data_set = self.data_sets_manager.create(default_data_set_name, data_file, "")
            self._edit_dataset_controller = EditDataSetController(
                data_set,
                self.data_sets_manager
            )

    def on_new_data_set(self):
        pass

    def on_edit_data_set(self):
        if self.data_sets_manager.count() == 0:
            self.error_dialog = QMessageBox()
            self.error_dialog.setIcon(QMessageBox.Warning)
            self.error_dialog.setText('There are not data sets to edit.')
            self.error_dialog.setWindowTitle('Error')
            self.error_dialog.exec_()
            # self.error_dialog = QErrorMessage()
            # self.error_dialog.showMessage('There are not data sets to edit.')
        else:
            self._data_sets_selector_controller = DataSetsSelectorController(self.data_sets_manager)

    def on_models(self):
        self._models_manager_controller = ModelsManagerController(self.models_manager)

    def on_create_PCA(self):
        self._models_creator_controller = ModelsCreatorController(self.models_manager,
                                                                  self.data_sets_manager,
                                                                  ModelType.PCA)