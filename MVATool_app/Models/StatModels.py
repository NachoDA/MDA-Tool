from Models.Datasets import DataSet
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


class StatModelsManager():

    def __init__(self):
        self._stat_models = list()
        self._current_model = None

    def create_PCA(self, name, data_set, num_components):
        PCA_model = PCAModel(name, data_set, num_components)
        self._stat_models.append(PCA_model)
        return PCA_model

    def count(self):
        return len(self._stat_models)

    def get_models(self):
        return self._stat_models

    def set_current_model(self, model):
        self._current_model = model

    def get_current_model(self):
        if self._current_model is None:
            # TODO: Alert window
            if len(self._stat_models) == 0:
                print('There are not models created.')
            else:
                self._current_model = self._stat_models[0]
        else:
            return  self._current_model

    def all_names(self):
        return [x.name for x in self._stat_models]

class StatModel():

    def __init__(self, name, data_set):
        self.name = name
        self._data_set = data_set
        self._numeric_data = self._data_set.get_numeric_data()

    def get_data_set_name(self):
        return self._data_set.name

class LatentVariablesModel(StatModel):

    def __init__(self, name, data_set):
        super(LatentVariablesModel, self).__init__(name, data_set)
        self._calculated_components = 0
        self._current_num_component = 0

    def show_to_component(self, number):
        if number > self._calculated_components:
            self.calculate_components(number)
        else:
            self._current_num_component = number

    # TODO: Condiciones para no calcular:
    #       1. Num_vars > num_components
    def calculate_components(self, number):
        self._pca = PCA(n_components=number)
        self._calculated_components = number
        data = StandardScaler().fit_transform(self._numeric_data)
        self._pca.fit_transform(data)

    def get_current_num_component(self):
        return self._current_num_component

    def explained_variance_ratio(self):
        return self._pca.explained_variance_ratio_[:self._calculated_components]


class PCAModel(LatentVariablesModel):

    def __init__(self, name, data_set, num_components):
        super(PCAModel, self).__init__(name, data_set)
        self._pca = PCA(n_components=0)
        self.show_to_component(num_components)
