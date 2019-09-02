from GUI.GraphWidgets import *
from Controllers.Controller import Controller
from Models.StatModels import *

class AnalyzeController(Controller):

    def __init__(self):
        super().__init__()


class AnalyzeLatentController(AnalyzeController):

    # TODO: Select obs automatically when a new graph is created and has obs selected
    def __init__(self, models_manager, selector_manager,
                 create_selector_tab, delete_selection_tab,
                 active_window):
        super().__init__()
        self._models_manager = models_manager
        self._selector_manager = selector_manager
        self._create_selector_tab = create_selector_tab
        self._delete_selection_tab = delete_selection_tab
        self._active_window = active_window
        self._last_graph_focus = None

    # TODO: Create a specific controller for latent variable models
    # TODO: Create a specific controller for selection behaviour
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
            self._selector_manager.register_new_graph(model.get_data_set(), graph)
        else:
            # TODO: Add alert. Or better: disable button when no latent variable model is selected
            print("This model hasn't score plot!")

    def create_scores_line_graph(self):
        pcx = 0
        model = self._models_manager.get_current_model()
        if isinstance(model, PCAModel):
            scores = model.scores(pcx)
            graph = LinePlot(type=GraphType.score_plot,
                             model_name=model.get_name(),
                             points=scores,
                             num_components=model.get_current_num_component())
            graph.show()
            graph.selector_PC.currentIndexChanged.connect(lambda: self.pc_changed(model, graph))
            self.make_connections_selector(graph)
            self._selector_manager.register_new_graph(model.get_data_set(), graph)
        else:
            # TODO: Add alert. Or better: disable button when no latent variable model is selected
            print("This model hasn't score plot!")

    def create_loading_graph(self):
        pcx, pcy = 0, 1
        model = self._models_manager.get_current_model()
        if isinstance(model, PCAModel):
            loadings = model.loadings(pcx, pcy)
            print('loadings: ' + str(loadings))
            graph = ScatterlotTwoComponents(type=GraphType.loading_plot,
                                            model_name=model.get_name(),
                                            points=loadings,
                                            num_components=model.get_current_num_component())
            graph.set_points_labels(model.get_data_set().var_names())
            graph.show()
            graph.selector_PCX.currentIndexChanged.connect(lambda: self.pc_changed(model, graph))
            graph.selector_PCY.currentIndexChanged.connect(lambda: self.pc_changed(model, graph))
            self.make_connections_selector(graph)
            self._selector_manager.register_new_graph(model.get_data_set(), graph)
        else:
            # TODO: Add alert. Or better: disable button when no latent variable model is selected
            print("This model hasn't score plot!")

    def pc_changed(self, model, graph):
        has_two_components = isinstance(graph, ScatterlotTwoComponents)
        if has_two_components:
            pcx = graph.selector_PCX.currentIndex()
            pcy = graph.selector_PCY.currentIndex()
            if graph.get_type() == GraphType.score_plot:
                points = model.scores2(pcx, pcy)
                graph.update_data(points)
            elif graph.get_type() == GraphType.loading_plot:
                points = model.loadings(pcx, pcy)
                graph.update_data(points)
                graph.update_points_labels()
        else:
            pcy = graph.selector_PC.currentIndex()
            points = model.scores(pcy)
            graph.update_data(points)

    def make_connections_selector(self, graph):
        graph.focus_in_signal.connect(lambda: self.focus_in_selection_graph(graph))
        graph.focus_out_signal.connect(self.focus_out_selection_graph)
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