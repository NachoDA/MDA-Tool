from GUI.GraphWidgets import *
from Controllers.Controller import Controller
from Models.StatModels import *


# TODO: Reorganice. Plot must be build in model layer
class Plot():

    def __init__(self, can_select):

        if can_select:
            self._plot_selection = PlotSelection()


class PlotSelection():

    _creating_region = False

    def __init__(self):
        self.selection_timer = QtCore.QTimer()

        self.make_connections()

    def make_connections(self):
        pass