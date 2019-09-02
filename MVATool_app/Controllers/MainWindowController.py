import sys
import os.path
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from GUI.MainWindow import MainWindow
from Controllers.Controller import Controller
from Controllers.EditDatasetController import EditDataSetController
from Controllers.DataSetsSelectorController import DataSetsSelectorController
from Controllers.ModelsManagerController import ModelsManagerController
from Controllers.ModelsCreatorController import *
from Controllers.AnalyzeController import *
from Models.MainWindowModel import MainWindowModel
from Models.Datasets import DataSetsManager
from Models.DataFiles import DataFilesManager
from Models.StatModels import StatModelsManager
from Models.SelectorManager import SelectorManager
import copy


class MainWindowController(Controller):

    # TODO: When main window is closed, application should close
    # TODO: Implement error management
    def __init__(self):
        self._app = QApplication(sys.argv)
        super().__init__()
        self._view = MainWindow()
        self._view.show()
        self._model = MainWindowModel()
        self.make_connections()

        self.data_sets_manager = DataSetsManager()
        self.data_files_manager = DataFilesManager()
        self.models_manager = StatModelsManager(self.set_current_model,
                                                self.fill_models_to_selector)
        self.selector_manager = SelectorManager()

        self._exists_selection_tab = False
        self._last_fixed_tab = None
        self.load_path = 'C:\\Users\\Nacho\\Documents\\MVATool\\Datos'
        self._edit_dataset_controller = None
        # TODO: Organize that in a good way. Too many callbacks... that smells bad
        self._analyze_latent_controller =\
            AnalyzeLatentController(self.models_manager, self.selector_manager,
                                    self.create_selection_tab,
                                    self.delete_selection_tab,
                                    lambda: self._app.activeWindow())
        self.fill_models_to_selector()

    def make_connections(self):
        # Menu bar
        self._view.model_selector.currentTextChanged.connect(self.combo_box_selector_changed)
        # Data
        self._view.on_load_file.connect(self.on_load_file)
        self._view.on_new_data_set.connect(self.on_new_data_set)
        self._view.on_edit_data_set.connect(self.on_edit_data_set)
        # Models
        self._view.on_models.connect(self.on_models)
        self._view.on_create_PCA.connect(self.on_create_PCA)
        # Analyze
        self._view.on_scores.connect(self.on_scores)
        self._view.on_line_scores.connect(self.on_line_scores)
        self._view.on_loadings.connect(self.on_loadings)
        # Selector
        self._view.on_exclude.connect(self.on_exclude)
        self._view.on_include.connect(self.on_include)

    def run(self):
        self._view.show()
        return self._app.exec()

    def set_current_model(self):
        index = self.models_manager.get_current_model_index()
        self._view.model_selector.setCurrentIndex(index)

    def fill_models_to_selector(self):
        if self.models_manager.count() == 0:
            self._view.model_selector.addItem('No models created')
        else:
            self._view.model_selector.clear()
            self._view.model_selector.addItems(self.models_manager.all_names_and_data_sets())

    def create_selection_tab(self):
        if not self._exists_selection_tab:
            self._last_fixed_tab = self._view.get_current_tab()
            self._view.create_selection_tab()
            self._exists_selection_tab = True

    def delete_selection_tab(self):
        if self._exists_selection_tab:
            self._view.delete_selection_tab()
            self._view.select_tab(self._last_fixed_tab)
            self._exists_selection_tab = False

    # -------------      signals       -----------------

    def combo_box_selector_changed(self):
        if self.models_manager.count() > 0:
            index_model = self._view.model_selector.currentIndex()
            model = self.models_manager.get_by_index(index_model)
            self.models_manager.set_current_model(model)
        # else occours when the empty model text is set

    # Data
    def on_load_file(self):
        file_dialog = QFileDialog()
        file_path_to_load, file_type_to_load = file_dialog.getOpenFileName(
            self._view, "Load file", self.load_path, "Excel Files (*.xls);;Excel 2013 Files (*.xlsx);;CSV Files (*.csv)")

        file_loaded = self._model.load_file(file_path_to_load, file_type_to_load)

        if file_loaded is None:
            print("File is empty")
        else:
            # TODO: Store in PC selected path as path to use next time
            data_file_name = os.path.basename(file_path_to_load)
            # TODO: Move this behaviour to data_sets_manager
            default_data_set_name = "data set name " + str(self.data_sets_manager.count())
            data_file = self.data_files_manager.create_data(data_file_name, file_loaded)
            data_set = self.data_sets_manager.create(default_data_set_name, data_file, "")
            self._edit_dataset_controller = EditDataSetController(
                data_set,
                self.data_sets_manager
            )

    def on_new_data_set(self):
        self._view.delete_selection_tab()
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

    # Models
    def on_models(self):
        self._models_manager_controller = ModelsManagerController(self.models_manager)

    def on_create_PCA(self):
        self._models_creator_controller = ModelsCreatorController(self.models_manager,
                                                                  self.data_sets_manager,
                                                                  ModelType.PCA)
    # Analyze
    def on_scores(self):
        self._analyze_latent_controller.create_scores_graph()

    def on_line_scores(self):
        self._analyze_latent_controller.create_scores_line_graph()

    def on_loadings(self):
        self._analyze_latent_controller.create_loading_graph()

    # Selection
    def on_exclude(self):
        self.exclude_or_include(is_exclude=True)

    def on_include(self):
        self.exclude_or_include(is_exclude=False)

    def exclude_or_include(self, is_exclude):
        print('on_exclude')
        graph = self._analyze_latent_controller.get_last_graph()
        data_set = self.selector_manager.get_data_set(graph)

        # TODO: Move this behaviour to data_sets_manager
        new_data_set = copy.deepcopy(data_set)
        name = "data set name " + str(self.data_sets_manager.count())
        self.data_sets_manager.add(new_data_set, name)

        observations = graph.get_selected()
        if is_exclude:
            selected_observations = [i for i in range(len(observations)) if observations[i]]
        else:
            selected_observations = [i for i in range(len(observations)) if not observations[i]]
        indexes = new_data_set.map_numeric_to_global(selected_observations)

        self._edit_dataset_controller = EditDataSetController(new_data_set, self.data_sets_manager)
        self._edit_dataset_controller.add_discard_rows_int(indexes)
