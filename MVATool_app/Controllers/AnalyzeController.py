from GUI.GraphWidgets import *
from Controllers.Controller import Controller
from Models.StatModels import *

class GraphController(Controller):

    def __init__(self, selector_manager, create_selector_tab, delete_selection_tab):
        super().__init__()
        self._selector_manager = selector_manager
        self._create_selector_tab = create_selector_tab
        self._delete_selection_tab = delete_selection_tab
        self._graphs = list()  # Just to avoid the destruction by the garbage collector

    def make_connections_focus(self, graph):
        graph.focus_in_signal.connect(lambda: self.focus_in_selection_graph(graph))
        graph.focus_out_signal.connect(self.focus_out_selection_graph)

    def make_connections_selector(self, graph):
        graph.selection_finished_signal.connect(lambda: self.make_selection(graph))
        graph.selection_timer.timeout.connect(lambda: self.update_selection(graph))
        graph.close_signal.connect(lambda: self._selector_manager.detele_graph(graph))

    def update_selection(self, graph):
        x = graph.graphics_layout.lastMousePos[0]
        y = graph.graphics_layout.lastMousePos[1]
        if not(x is None or y is None):
            point = QtCore.QPointF(x, y)
            graph.selection_points.append(point)
            if graph._roi is not None:
                polygon = QtGui.QPolygonF(graph.selection_points)
                mapped_point = graph.get_item_to_map().mapFromDevice(polygon)
                graph._roi.setPoints(mapped_point)

    def focus_in_selection_graph(self, graph):
        self._last_graph_focus = graph
        if True in graph.get_selected():
            self._create_selector_tab()
        else:
            self._delete_selection_tab()

    def focus_out_selection_graph(self):
        if not isinstance(self._active_window(), QMainWindow):
            self._delete_selection_tab()

    def make_selection(self, graph):
        roi_shape = graph._roi.mapToItem(graph.get_item_to_map(), graph._roi.shape())
        selected = [roi_shape.contains(pt) for pt in graph.get_points()]
        graph._roi.clearPoints()
        if True in selected:
            self._create_selector_tab()
        else:
            self._delete_selection_tab()
        self._selector_manager.new_selection(graph, selected)

    def get_last_graph(self):
        return self._last_graph_focus


class ExploreController(GraphController):

    # TODO: Select obs automatically when a new graph is created and has obs selected
    def __init__(self, data_sets_manager, selector_manager,
                 create_selector_tab, delete_selection_tab,
                 active_window):
        super().__init__(selector_manager, create_selector_tab, delete_selection_tab)
        self._data_sets_manager = data_sets_manager
        self._create_selector_tab = create_selector_tab
        self._active_window = active_window
        self._last_graph_focus = None

    def create_obs_graph(self):
        data_set_count = self._data_sets_manager.count()
        if data_set_count > 0:
            last_data_set = data_set_count - 1
            data_set = self._data_sets_manager.get_by_index(last_data_set)
            data_set_list = self._data_sets_manager.all_names()
            graph = ObsGraph(GraphType.obs_graph, data_set.name, data_set_list)
            data = data_set.get_numeric_data(preprocessed=False)
            var_names = data_set.var_names()
            graph.set_data(data, var_names, data_set.name)
            graph.show()
            self._graphs.append(graph)
            graph.selector_data_set.currentIndexChanged.connect(lambda: self.selector_changed(graph))
            self.make_connections_focus(graph)
            self._selector_manager.register_new_graph(data_set, graph)

    def create_vars_graph(self):
        data_set_count = self._data_sets_manager.count()
        if data_set_count > 0:
            last_data_set = data_set_count - 1
            data_set = self._data_sets_manager.get_by_index(last_data_set)
            data_set_list = self._data_sets_manager.all_names()
            graph = ObsGraph(GraphType.vars_graph, data_set.name, data_set_list)
            data = data_set.get_numeric_data(preprocessed=False)
            num_obs = len(data)
            data = data.transpose()
            var_names = list(range(num_obs))
            graph.set_data(data, var_names, data_set.name)
            graph.show()
            self._graphs.append(graph)
            graph.selector_data_set.currentIndexChanged.connect(lambda: self.selector_changed(graph))

    def create_population_graph(self):
        data_set_count = self._data_sets_manager.count()
        if data_set_count > 0:
            last_data_set = data_set_count - 1
            data_set = self._data_sets_manager.get_by_index(last_data_set)
            data_set_list = self._data_sets_manager.all_names()
            graph = PopulationsGraph(GraphType.populations, data_set.name, data_set_list)
            data = data_set.get_numeric_data(preprocessed=False)
            var_names = data_set.var_names()
            graph.set_data(data, var_names)
            graph.show()
            self._graphs.append(graph)
            graph.selector_data_set.currentIndexChanged.connect(lambda: self.selector_changed(graph))
            self.make_connections_focus(graph)
            self._selector_manager.register_new_graph(data_set, graph)

    def create_correlation_graph(self):
        print('create_correlation_graph')
        print('self._data_sets_manager.count(): ' + str(self._data_sets_manager.count()))
        data_set_count = self._data_sets_manager.count()
        if data_set_count > 0:
            last_data_set = data_set_count - 1
            data_set = self._data_sets_manager.get_by_index(last_data_set)
            var_names = data_set.var_names()
            data_set_list = self._data_sets_manager.all_names()
            graph = CorrelationPlot(GraphType.correlation, data_set.name, data_set_list)
            graph.set_grid(data_set.correlation_matrix(), var_names)
            graph.show()
            self._graphs.append(graph)
            graph.selector_data_set.currentIndexChanged.connect(lambda: self.selector_changed(graph))

    def selector_changed(self, graph):
        if graph.get_type() == GraphType.obs_graph:
            index = graph.selector_data_set.currentIndex()
            data_set = self._data_sets_manager.get_by_index(index)
            data = data_set.get_numeric_data(preprocessed=False)
            var_names = data_set.var_names()
            graph.set_data(data, var_names, data_set.name)
            self._selector_manager.detele_graph(graph)
            self._selector_manager.register_new_graph(data_set, graph)
        elif graph.get_type() == GraphType.vars_graph:
            index = graph.selector_data_set.currentIndex()
            data_set = self._data_sets_manager.get_by_index(index)
            data = data_set.get_numeric_data(preprocessed=False)
            num_obs = len(data)
            data = data.transpose()
            var_names = list(range(num_obs))
            graph.set_data(data, var_names, data_set.name)
        elif graph.get_type() == GraphType.populations:
            index = graph.selector_data_set.currentIndex()
            data_set = self._data_sets_manager.get_by_index(index)
            data = data_set.get_numeric_data(preprocessed=False)
            var_names = data_set.var_names()
            graph.set_data(data, var_names)
            self._selector_manager.detele_graph(graph)
            self._selector_manager.register_new_graph(data_set, graph)
        elif graph.get_type() == GraphType.correlation:
            index = graph.selector_data_set.currentIndex()
            data_set = self._data_sets_manager.get_by_index(index)
            corr = data_set.correlation_matrix()
            var_names = data_set.var_names()
            graph.set_grid(corr, var_names)

    def set_data_sets_manager(self, data_sets_manager):
        self.data_sets_manager = data_sets_manager

class AnalyzeLatentController(GraphController):

    # TODO: Select obs automatically when a new graph is created and has obs selected
    def __init__(self, models_manager, selector_manager,
                 create_selector_tab, delete_selection_tab,
                 active_window):
        super().__init__(selector_manager, create_selector_tab, delete_selection_tab)
        self._models_manager = models_manager
        self._selector_manager = selector_manager
        self._create_selector_tab = create_selector_tab
        self._delete_selection_tab = delete_selection_tab
        self._active_window = active_window
        self._last_graph_focus = None

    # TODO: Create a specific controller for latent variable models
    # TODO: Create a specific controller for selection behaviour
    def variance_explained_graph(self):
        model = self._models_manager.get_current_model()
        if isinstance(model, PCAModel):
            variance_ratios = model.explained_variance_ratio()
            graph = VarianceExplainedGraph(variance_ratios, title='Explained variance ratio per component')
            graph.show()
            self._graphs.append(graph)

    def create_scores_graph(self):
        pcx, pcy = 0, 1
        model = self._models_manager.get_current_model()
        if isinstance(model, PCAModel):
            scores = model.scores2(pcx, pcy)
            graph = ScatterlotTwoComponents(type=GraphType.score_plot,
                                            model_name=model.get_name(),
                                            points=scores,
                                            num_components=model.get_current_num_component())
            graph.show()
            graph.selector_PCX.currentIndexChanged.connect(lambda: self.pc_changed(model, graph))
            graph.selector_PCY.currentIndexChanged.connect(lambda: self.pc_changed(model, graph))
            self.make_connections_selector(graph)
            self.make_connections_focus(graph)
            self._selector_manager.register_new_graph(model.get_data_set(), graph)
            interval = model.scores_interval_elipse(pcx, pcy)
            print('interval: ' + str(interval))
        else:
            # TODO: Add alert. Or better: disable button when no latent variable model is selected
            print("This model hasn't score plot!")

    def create_scores_line_graph(self):
        pcx = 0
        model = self._models_manager.get_current_model()
        if isinstance(model, PCAModel):
            scores = model.scores(pcx)
            graph = LinePlot(type=GraphType.score_line_plot,
                             model_name=model.get_name(),
                             points=scores,
                             num_components=model.get_current_num_component())
            graph.show()
            graph.selector_PC.currentIndexChanged.connect(lambda: self.pc_changed(model, graph))
            self.make_connections_selector(graph)
            self.make_connections_focus(graph)
            self._selector_manager.register_new_graph(model.get_data_set(), graph)
        else:
            # TODO: Add alert. Or better: disable button when no latent variable model is selected
            print("This model hasn't score plot!")

    def create_loading_graph(self):
        pcx, pcy = 0, 1
        model = self._models_manager.get_current_model()
        if isinstance(model, PCAModel):
            loadings = model.loadings2(pcx, pcy)
            graph = ScatterlotTwoComponents(type=GraphType.loading_plot,
                                            model_name=model.get_name(),
                                            points=loadings,
                                            num_components=model.get_current_num_component())
            graph.set_points_labels(model.get_data_set().var_names())
            self._graphs.append(graph)
            graph.show()
            graph.selector_PCX.currentIndexChanged.connect(lambda: self.pc_changed(model, graph))
            graph.selector_PCY.currentIndexChanged.connect(lambda: self.pc_changed(model, graph))
        else:
            # TODO: Add alert. Or better: disable button when no latent variable model is selected
            print("This model hasn't score plot!")

    def create_line_loading_graph(self):
        pc = 0
        model = self._models_manager.get_current_model()
        if isinstance(model, PCAModel):
            loadings = model.loadings(pc)
            graph = LinePlot(type=GraphType.loading_line_plot,
                             model_name=model.get_name(),
                             points=loadings,
                             num_components=model.get_current_num_component(),
                             var_names=model.get_data_set().var_names())
            self._graphs.append(graph)
            graph.show()
            graph.selector_PC.currentIndexChanged.connect(lambda: self.pc_changed(model, graph))
        else:
            # TODO: Add alert. Or better: disable button when no latent variable model is selected
            print("This model hasn't score plot!")

    def create_t2_hotelling_graph(self):
        model = self._models_manager.get_current_model()
        pc1 = 0
        pc2 = model.get_current_num_component()-1
        if isinstance(model, PCAModel):
            t2 = model.t2_hotelling(pc1, pc2)
            graph = LinePlot(type=GraphType.t2_hotelling,
                             model_name=model.get_name(),
                             points=t2,
                             num_components=model.get_current_num_component())
            graph.show()
            graph.selector_PC.currentIndexChanged.connect(lambda: self.pc_changed(model, graph))
            graph.selector_PC2.currentIndexChanged.connect(lambda: self.pc_changed(model, graph))
            self.make_connections_selector(graph)
            self.make_connections_focus(graph)
            self._selector_manager.register_new_graph(model.get_data_set(), graph)
            interval_95 = model.t2_interval(pc1, pc2, 0.95)
            interval_99 = model.t2_interval(pc1, pc2, 0.99)
            graph.update_confidence_intervals(interval_95, interval_99)
        else:
            # TODO: Add alert. Or better: disable button when no latent variable model is selected
            print("This model hasn't score plot!")

    def create_spe_graph(self):
        model = self._models_manager.get_current_model()
        # pc = model.get_current_num_component()-1
        pc = model.get_current_num_component()
        pc = 2
        if isinstance(model, PCAModel):
            spe = model.spe(pc)
            graph = LinePlot(type=GraphType.spe,
                             model_name=model.get_name(),
                             points=spe,
                             num_components=model.get_current_num_component())
            graph.show()
            graph.selector_PC.currentIndexChanged.connect(lambda: self.pc_changed(model, graph))
            self.make_connections_selector(graph)
            self.make_connections_focus(graph)
            self._selector_manager.register_new_graph(model.get_data_set(), graph)
            spe_95 = model.spe_interval(pc, 0.95)
            print('spe_95: ' + str(spe_95))
            spe_99 = model.spe_interval(pc, 0.99)
            print('spe_99: ' + str(spe_99))
            graph.update_confidence_intervals(spe_95, spe_99)
        else:
            # TODO: Add alert. Or better: disable button when no latent variable model is selected
            print("This model hasn't score plot!")


    def pc_changed(self, model, graph):
        if graph.get_type() == GraphType.score_plot:
            pcx = graph.selector_PCX.currentIndex()
            pcy = graph.selector_PCY.currentIndex()
            points = model.scores2(pcx, pcy)
            graph.update_data(points)
        elif graph.get_type() == GraphType.score_line_plot:
            pcy = graph.selector_PC.currentIndex()
            points = model.scores(pcy)
            graph.update_data(points)
        elif graph.get_type() == GraphType.loading_plot:
            pcx = graph.selector_PCX.currentIndex()
            pcy = graph.selector_PCY.currentIndex()
            points = model.loadings2(pcx, pcy)
            graph.update_data(points)
            graph.update_points_labels()
        elif graph.get_type() == GraphType.loading_line_plot:
            pc = graph.selector_PC.currentIndex()
            points = model.loadings(pc)
            graph.update_data(points)
        elif graph.get_type() == GraphType.t2_hotelling:
            pc1 = graph.selector_PC.currentIndex()
            pc2 = graph.selector_PC2.currentIndex()
            # TODO: This constraint is artificial. Must be changed
            if pc1 < pc2:
                points = model.t2_hotelling(pc1, pc2)
                graph.update_data(points)
                interval_95 = model.t2_interval(pc1, pc2, 0.95)
                interval_99 = model.t2_interval(pc1, pc2, 0.99)
                graph.update_confidence_intervals(interval_95, interval_99)
        elif graph.get_type() == GraphType.spe:
            pc = graph.selector_PC.currentIndex()
            points = model.spe(pc)
            graph.update_data(points)
            spe_95 = model.spe_interval(pc, 0.95)
            print('spe_95: ' + str(spe_95))
            spe_99 = model.spe_interval(pc, 0.99)
            print('spe_99: ' + str(spe_99))
            graph.update_confidence_intervals(spe_95, spe_99)

