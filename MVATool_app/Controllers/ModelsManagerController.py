from GUI.ModelsManagerWindow import ModelsManagerWindow
from Controllers.Controller import Controller
from Models.StatModels import *


class ModelsManagerController(Controller):

    def __init__(self, models_manager):
        super().__init__()
        self._models_manager = models_manager
        self._view = ModelsManagerWindow()
        for model in self._models_manager.get_models():
            print('Num stats models: ' + str(len(self._models_manager.get_models())))
            self.add_model(model)
        self.make_connections()

    # TODO: Block window to avoid interaction in main window
    def make_connections(self):
        pass
        # self._view.cancel_button.clicked.connect(self.cancel)
        # self._view.create_button.clicked.connect(self.create_model)

    def add_model(self, model):
        if isinstance(model, PCAModel):
            model = self._view.add_PCA_model(model.name,
                                             model.get_data_set_name(),
                                             model.explained_variance_ratio())
            # model.add_button.clicked.connect(self.add_component)
            # model.remove_button.clicked.connect(self.remove_component)

    def add_component(self):
        pass
        # index = self._view.models_layout.add_PCA_model

    def remove_component(self):
        pass