from PyQt5 import QtCore

class SelectorManager():

    close_signal = QtCore.pyqtSignal()

    def __init__(self):
        data_sets_with_selections = list()
        self._data_sets = dict()

    def register_new_graph(self, data_set, graph):
        # data_sets = self._data_sets[data_set]
        if data_set not in self._data_sets:
            self._data_sets[data_set] = list()
        self._data_sets[data_set].append(graph)

    # TODO: Communication between model and view layers must be avoided
    #  Probably, this can be achieved by creating a graph in the model layer?
    #  And more: probably this kind of alerts must be done with events
    def new_selection(self, graph, selected):
        data_set = self.get_data_set(graph)
        for graph in self._data_sets[data_set]:
            graph.draw_selected(selected)

    def detele_graph(self, graph):
        print('Delete graph!')
        data_set = self.get_data_set(graph)
        self._data_sets[data_set].remove(graph)

    def get_data_set(self, graph):
        for data_set in self._data_sets:
            if graph in self._data_sets[data_set]:
                return data_set
