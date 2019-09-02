from GUI.ModelsManagerWindow import ModelsManagerWindow
from Controllers.Controller import Controller
from Models.StatModels import *


class ModelsManagerController(Controller):

    def __init__(self, models_manager):
        super().__init__()
        self._models_manager = models_manager
        self._view = ModelsManagerWindow()
        self.make_connections()
        self.add_all_models()

    # TODO: Block window to avoid interaction in main window
    def make_connections(self):
        pass
        # self._view.cancel_button.clicked.connect(self.cancel)
        # self._view.create_button.clicked.connect(self.create_model)

    def add_model(self, model):
        if isinstance(model, PCAModel):
            widget_model = self._view.add_PCA_model(model.get_name(),
                                                    model.get_data_set_name(),
                                                    model.explained_variance_ratio())
            widget_model.add_button.clicked.connect(lambda: self.add_component(model.get_name()))
            widget_model.remove_button.clicked.connect(lambda: self.remove_component(model.get_name()))

    def add_component(self, model_name):
        print(model_name)
        model = self._models_manager.get(model_name)
        model.add_component()
        self.remove_all_models()
        self.add_all_models()
        # self._view.refresh_widget(model_name,
        #                           model.get_data_set_name(),
        #                           model.explained_variance_ratio())

    def remove_component(self, model_name):
        print(model_name)
        model = self._models_manager.get(model_name)
        model.remove_component()
        self.remove_all_models()
        self.add_all_models()
        # self._view.refresh_widget(model_name,
        #                           model.get_data_set_name(),
        #                           model.explained_variance_ratio())

    def remove_all_models(self):
        self._view.init_UI()
        # self._view.remove_all_models()

    def add_all_models(self):
        for model in self._models_manager.get_models():
            print('Num stats models: ' + str(len(self._models_manager.get_models())))
            self.add_model(model)