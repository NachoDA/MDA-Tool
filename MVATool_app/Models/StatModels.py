from Models.Datasets import DataSet
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
from scipy import stats

# TODO: Create a model class of Points (¿Or observations?) with
#  value, color...
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

    def scores_interval(self, pc1):
        scores = self.scores(pc1)

    def scores_interval_elipse(self, pcx, pcy):
        scores = self.scores2(pcx, pcy)
        # interval = np.apply_along_axis(np.var, 1, scores)

        # m = np.apply_along_axis(np.mean, 0, scores)
        # print('m: ' + str(m))
        # sigma = np.apply_along_axis(np.std, 0, scores)
        # print('sigma: ' + str(sigma))
        # interval = sigma / np.sqrt(n) * stats.t.ppf(alpha/2, n-1)
        # interval = (interval).sum(axis=1)

        interval = 1

        return interval

    def loadings(self, pcx, pcy):
        loadings_pcx = self._pca.components_[pcx, :]
        loadings_pcy = self._pca.components_[pcy, :]
        return loadings_pcx, loadings_pcy

    def t2_hotelling(self, pc1, pc2):
        # How calculate: https://learnche.org/pid/latent-variable-modelling/principal-component-analysis/hotellings-t2-statistic
        scores = self._pca.transform(self._numeric_data)[:, pc1:pc2+1]
        std = np.apply_along_axis(np.std, 0, scores)
        t_div_std_2 = np.divide(scores, std)**2
        t2 = t_div_std_2.sum(axis=1)
        return list(t2)

    def t2_interval(self, from_pc, to_pc, alpha):
        # How calculate: http://users.stat.umn.edu/~helwig/notes/mvmean-Notes.pdf
        scores = self._pca.transform(self._numeric_data)[:, from_pc:to_pc+1]
        n = len(scores)
        p = to_pc-from_pc+1 #TODO: Check why this +1
        print('p: ' + str(p))
        f = stats.f.ppf(alpha, p, n-p)
        print('f: ' + str(f))
        t2_interval = ((n-1)*p/(n-p))*f
        return t2_interval

    def spe(self, pc):
        scores = self._pca.transform(self._numeric_data)[:, :pc+1]
        loadings = self._pca.components_[:pc+1, :]
        tp = scores @ loadings
        e = self._numeric_data - tp
        spe = (e**2).sum(axis=1)
        return list(spe)

    def spe_interval(self, pc, p_value):
        alpha = 1-p_value
        scores = self._pca.transform(self._numeric_data)[:, :pc+1]
        spe = np.array(self.spe(pc))
        scores = self._pca.transform(self._numeric_data)[:, :pc+1]
        # print('spe: ' + str(spe))
        n = len(scores)
        print('n: ' + str(n))
        g = n-pc
        print('g: ' + str(g))
        # interval = g * stats.chi2.ppf(alpha, spe)
        # print('len(interval): ' + str(len(interval)))

        # print('n: ' + str(n))
        # m = np.apply_along_axis(np.mean, 0, scores)
        # print('m: ' + str(m))
        # sigma = np.apply_along_axis(np.std, 0, scores)
        # print('sigma: ' + str(sigma))
        # interval = sigma / np.sqrt(n) * stats.t.ppf(alpha/2, n-1)
        # interval = (interval).sum(axis=1)

        # std = np.apply_along_axis(np.std, 0, scores)
        # std = sum(std)
        # std = np.std(scores)
        # print('std: ' + str(std))
        m = np.mean(spe)
        print('m: ' + str(m))
        interval = stats.chi2.ppf(alpha, df=g)

        # chi = stats.f.ppf(alpha, p, n-p)

        return interval


class PCAModel(LatentVariablesModel):

    def __init__(self, name, data_set, num_components):
        super(PCAModel, self).__init__(name, data_set)
        self._pca = PCA(n_components=0)
        self.show_to_component(num_components)
