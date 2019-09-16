from Models.Datasets import DataSet
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
from scipy import stats
import math

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
            return self._current_model

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
        self._numeric_data = self._data_set.get_numeric_data(
            preprocessed=True, apply_missing=True)

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
        print(self.get_data_set().var_names())
        self._pca.fit(self._numeric_data)
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

    def loadings2(self, pcx, pcy):
        loadings_pcx = self._pca.components_[pcx, :]
        loadings_pcy = self._pca.components_[pcy, :]
        return loadings_pcx, loadings_pcy

    def loadings(self, pc):
        loadings_pc = self._pca.components_[pc, :]
        return loadings_pc

    def t2_hotelling(self, pc1, pc2):
        # How calculate: https://learnche.org/pid/latent-variable-modelling/principal-component-analysis/hotellings-t2-statistic
        scores = self._pca.transform(self._numeric_data)[:, pc1:pc2+1]
        std = np.apply_along_axis(np.std, 0, scores)
        t_div_std_2 = np.divide(scores, std)**2
        t2 = t_div_std_2.sum(axis=1)
        return list(t2)

    def t2_interval(self, from_pc, to_pc, p_value):
        # How calculate: http://users.stat.umn.edu/~helwig/notes/mvmean-Notes.pdf
        scores = self._pca.transform(self._numeric_data)[:, from_pc:to_pc+1]
        n = len(scores)
        p = to_pc-from_pc+1 #TODO: Check why this +1
        print('p: ' + str(p))
        f = stats.f.ppf(p_value, p, n-p)
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
        # Fuente:(1) https://hrcak.srce.hr/file/117623, http://www.wseas.us/e-library/conferences/2010/Merida/CIMMACS/CIMMACS-20.pdf
        # (2) http://pro-pat.eu/propat01/files/2018/11/statistical-process-control.pdf
        # (3) https://www.sciencedirect.com/science/article/pii/S0026265X14001507
        # (4) Equivale a 1: https://books.google.es/books?id=cPgXg3GIMAsC&pg=PA828&lpg=PA828&dq=pca+q+statistic+is+the+same+as+spe&source=bl&ots=yeCjrBosl3&sig=ACfU3U1s_ZUKbFwcwWg7onBmVM7IeOxr-A&hl=es&sa=X&ved=2ahUKEwjP9JbfgsPkAhWx3eAKHfF9DpkQ6AEwC3oECAkQAQ#v=onepage&q=pca%20q%20statistic%20is%20the%20same%20as%20spe&f=false
        # (5) https://www.sciencedirect.com/science/article/pii/S0959152403000994
        # (6) Apuntes MOD y https://books.google.es/books?id=KyoQWVBAG9MC&pg=PA264&lpg=PA264&dq=UCL(SP+E)+pca&source=bl&ots=3Q8ggxJefQ&sig=ACfU3U1kh64mWjhfVptbhD465VHs3xjubg&hl=es&sa=X&ved=2ahUKEwi6roifhcPkAhUImBQKHW-LAt4Q6AEwAHoECAkQAQ#v=onepage&q=UCL(SP%20E)%20pca&f=false
        # (6.1) Enlace de arriba
        # (7) https://riunet.upv.es/bitstream/handle/10251/109272/45911355_TFG_15360123490954411822475928808580.pdf?sequence=1&isAllowed=y

        # alpha = 1-p_value
        # scores = self._pca.transform(self._numeric_data)[:, :pc+1]
        # scores = self._pca.transform(self._numeric_data)[:, :pc+1]
        # # print('spe: ' + str(spe))
        # n = len(scores)
        # print('n: ' + str(n))
        # g = n-pc
        # print('g: ' + str(g))
        #
        # m = np.mean(spe)
        # print('m: ' + str(m))
        # interval = stats.chi2.ppf(alpha, df=g)

        # chi = stats.f.ppf(alpha, p, n-p)

        print('\n\n\n')

        loadings = self._pca.components_[:pc+1, :]
        print('loadings: ' + str(loadings))
        spe = np.array(self.spe(pc))
        samples = np.array(self._data_set.get_numeric_data(preprocessed=False))

        # TODO: Implement calculating normal distribution:
        #  http://eric.univ-lyon2.fr/~ricco/tanagra/fichiers/en_Tanagra_Calcul_P_Value.pdf
        if p_value == 0.95:
            # c = 1.96
            c = 1.6449
        else:
            # c = 1.96
            c = 2.3263

        k = pc

        fi1 = fi(1, samples, loadings)
        print('fi1: ' + str(fi1))
        fi2 = fi(2, samples, loadings)
        print('fi2: ' + str(fi2))
        fi3 = fi(3, samples, loadings)
        print('fi3: ' + str(fi3))
        h_0 = h0(fi1, fi2, fi3)
        print('h_0: ' + str(h_0))

        # # VERSIÓN 1
        # left = (c * math.sqrt(2*fi2*h_0**2)) / fi1
        # print('left: ' + str(left))
        # right = fi2*h_0*(h_0-1) / fi1**2
        # print('right: ' + str(right))
        # interval = fi1 * (left + 1 + right) ** (1/h_0)
        # print('interval: ' + str(interval))

        # # VERSIÓN 1.1
        # left = (h_0 * c * math.sqrt(2*fi2)) / fi1
        # print('left: ' + str(left))
        # right = fi2*h_0*(h_0-1) / fi1**2
        # print('right: ' + str(right))
        # interval = fi1 * (left + 1 + right) ** (1/h_0)
        # print('interval: ' + str(interval))

        # # VERSIÓN 2
        # left = (h_0 * c * math.sqrt(2 * fi2)) / fi1
        # print('left: ' + str(left))
        # right = fi2 * h_0 * (h_0 - 1) / fi1 ** 2
        # print('right: ' + str(right))
        # interval = fi1 * (left + 1 + right)
        # print('interval: ' + str(interval))

        # # VERSIÓN 3
        # middle = fi2*h_0*((1-h_0)/(fi1**2))
        # print('middle: ' + str(middle))
        # right = math.sqrt(c * (2*fi2*(h_0**2))) / fi1
        # print('right: ' + str(right))
        # interval = fi1 - (1 - middle + right) ** (1/h_0)
        # print('interval: ' + str(interval))

        # VERSIÓN 4 EQUIVALE A 1
        middle = fi2*h_0*((1-h_0)/(fi1**2))
        print('middle: ' + str(middle))
        right = c * (2*fi2*(h_0**2))**(1/2) / fi1
        print('right: ' + str(right))
        interval = fi1 * (1 - middle + right) ** (1/h_0)
        print('interval: ' + str(interval))

        # # VERSIÓN 5
        # left = fi1*c*2*fi2*(h_0**2)*fi1
        # print('left: ' + str(left))
        # right = (fi2*h_0*(h_0-1)*fi1**2) ** (1/h_0)
        # print('right: ' + str(right))
        # interval = (left + 1 + right)
        # print('interval: ' + str(interval))

        # spe_var = np.var(spe)
        # spe_mean = np.mean(spe)
        #
        # g = spe_var / 2*spe_mean #0.000769
        # # print('g: ' + str(g))
        # h = len(samples) - len(loadings)  # grados de libertad
        # # print('h: ' + str(h))

        # # VERSIÓN 6 (X2)
        # interval = g * stats.chi2.ppf(p_value, h)

        # # VERSIÓN 6.1 (X2)
        # h = (2*spe_mean**2) / spe_var
        # interval = g*h*(1-(2/9*h) + c*(2/9*h)**(1/2))**3

        # # VERSIÓN 7
        # n = len(samples)
        # p = pc+1
        # print('p: ' + str(p))
        # samples = np.array(samples)
        # k = samples.shape[1]
        # print('k: ' + str(k))
        # f = stats.f.ppf(p_value, k-p, (n-p-1)*(k-p))
        # print('f: ' + str(f))
        # c = 0.22
        # interval = ((k - p) / c**2) * spe_var * f

        print('\n\n\n')

        return interval

def fi(i, samples, loadings):
    k = loadings.shape[0]
    print(k)
    n = samples.shape[1]
    print(n)
    # eigenval = eigenvalues(samples, loadings)
    eigenval = eigenvalues(samples)
    # print('eigenval: ' + str(eigenval))
    print('len(eigenval): ' + str(len(eigenval)))
    sum = 0
    for j in range(k, n):  # is not k+1 because starts in 0
        print('j: ' + str(j))
        sum += eigenval[j] ** i
    return sum

def h0(fi1, fi2, fi3):
    res = 1 - ((2*fi1*fi3) / (3*fi2**2))
    return res

# # VERSIÓN 5
# def fi(i, samples, loadings):
#     k = loadings.shape[0]
#     print(k)
#     n = samples.shape[1]
#     print(n)
#     # eigenval = eigenvalues(samples, loadings)
#     eigenval = eigenvalues(samples)
#     # print('eigenval: ' + str(eigenval))
#     print('len(eigenval): ' + str(len(eigenval)))
#     sum = 0
#     for j in range(k, n):  # is not k+1 because starts in 0
#         print('j: ' + str(j))
#         sum += eigenval[j] ** i
#     return sum
#
# def h0(fi1, fi2, fi3):
#     res = 1 - (2*fi1*fi3*3*(fi2**2))
#     return res

def eigenvalues(matrix):
    # cov = np.cov(matrix.T)
    # # print('cov: ' + str(cov))
    # w, _ = np.linalg.eig(cov)
    # # print('w: ' + str(w))
    cov = np.cov(StandardScaler().fit_transform(matrix).T)
    # print('cov transformed: ' + str(cov))
    w, _ = np.linalg.eig(cov)
    # print('w: ' + str(w))
    return w

# TODO: Plot Q2-T2. Seen in: http://www.users.abo.fi/khaggblo/MMDA/MMDA6.pdf
# TODO: Boxplot like https://mattsigal.github.io/eqcov_supp/iris-ex.html
# TODO: Correlation per class. Extended: Each graph with different classification options:
#  http://rstudio-pubs-static.s3.amazonaws.com/376329_7bd791576b7240d2b8e6d251d6929aab.html

# def eigenvalues(samples, loadings):
#     n_samples = samples.shape[0]
#     # We center the data and compute the sample covariance matrix.
#     samples -= np.mean(samples, axis=0)
#     cov_matrix = np.dot(samples.T, samples) / n_samples
#     for eigenvector in loadings:
#         print(np.dot(eigenvector.T, np.dot(cov_matrix, eigenvector)))

class PCAModel(LatentVariablesModel):

    def __init__(self, name, data_set, num_components):
        super(PCAModel, self).__init__(name, data_set)
        self._pca = PCA(n_components=0)
        self.show_to_component(num_components)
