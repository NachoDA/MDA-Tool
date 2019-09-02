from Models.Datasets import DataSet
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


class StatModelsManager():

    def __init__(self, set_current_model_selector, list_models_changed):
        self._stat_models = list()
        self._current_model = None
        self._set_current_model_selector = set_current_model_selector
        self._list_models_changed = list_models_changed

    def create_PCA(self, name, data_set, num_components):
        PCA_model = PCAModel(name, data_set, num_components)
        self._stat_models.append(PCA_model)
        self.new_model_created(PCA_model)
        return PCA_model

    def new_model_created(self, new_model):
        self._list_models_changed()
        self.set_current_model(new_model)

    def get(self, name):
        for model in self._stat_models:
            if model.get_name() == name:
                return model

    def get_by_index(self, index):
        return self._stat_models[index]

    def count(self):
        return len(self._stat_models)

    def get_models(self):
        return self._stat_models

    def set_current_model(self, model):
        self._current_model = model
        self._set_current_model_selector()

    def get_current_model(self):
        if self._current_model is None:
            # TODO: Alert window
            if len(self._stat_models) == 0:
                print('There are not models created.')
            else:
                self._current_model = self._stat_models[0]
        else:
            return  self._current_model

    def get_current_model_index(self):
        return self._stat_models.index(self.get_current_model())

    def exists(self, name):
        return self.get(name) is not None

    def all_names(self):
        return [x.get_name() for x in self._stat_models]

    def all_names_and_data_sets(self):
        return [x.get_name_and_data_set() for x in self._stat_models]

class StatModel():

    def __init__(self, name, data_set):
        self._name = name
        self._data_set = data_set
        self._numeric_data = self._data_set.get_numeric_data(preprocessed=True)

    # Allow comparison between data sets. Used in dict
    def __hash__(self):
        return hash(str(self))

    def get_data_set_name(self):
        return self._data_set.name

    def num_rows(self):
        return len(self._numeric_data.index)

    def num_columns(self):
        return len(self._numeric_data.columns)

    def get_name(self):
        return self._name

    def get_name_and_data_set(self):
        return self._name + ' : ' + self.get_data_set_name()

    def get_data_set(self):
        return self._data_set


class LatentVariablesModel(StatModel):

    def __init__(self, name, data_set):
        super(LatentVariablesModel, self).__init__(name, data_set)
        self._calculated_components = 0
        self._current_num_component = 0
        print("str(self): " + str(self))

    def show_to_component(self, number):
        if number == 0:
            # TODO: Can't do it message
            print("Can't set components to 0.")
        elif number > self.num_columns():
            # TODO: Can't do it message
            print("Can't calculate more components than variables.")
        else:
            self._current_num_component = number
            if number > self._calculated_components:
                self.calculate_components(number)

    # TODO: ¿Trasladar aquí las condiciones de no cálculo de las componentes?
    #       También añadir más.
    def calculate_components(self, number):
        self._pca = PCA(n_components=number)
        self._calculated_components = number
        # data = StandardScaler().fit_transform(self._numeric_data)
        self._pca.fit_transform(self._numeric_data)
        self._pca.score(self._numeric_data)

    def add_component(self):
        self.show_to_component(self._current_num_component+1)

    def remove_component(self):
        self.show_to_component(self._current_num_component-1)

    def get_current_num_component(self):
        return self._current_num_component

    def explained_variance_ratio(self):
        return self._pca.explained_variance_ratio_[:self._current_num_component]

    def scores(self, pc):
        scores = self._pca.transform(self._numeric_data)[:, pc]
        return scores

    def scores2(self, pcx, pcy):
        scores_pcx = self._pca.transform(self._numeric_data)[:, pcx]
        scores_pcy = self._pca.transform(self._numeric_data)[:, pcy]
        return scores_pcx, scores_pcy

    def loadings(self, pcx, pcy):
        print('self._pca.components_: ' + str(self._pca.components_))
        loadings_pcx = self._pca.components_[pcx, :]
        loadings_pcy = self._pca.components_[pcy, :]
        return loadings_pcx, loadings_pcy

class PCAModel(LatentVariablesModel):

    def __init__(self, name, data_set, num_components):
        super(PCAModel, self).__init__(name, data_set)
        self._pca = PCA(n_components=0)
        self.show_to_component(num_components)
