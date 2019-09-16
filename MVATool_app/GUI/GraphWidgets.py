from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import Qt
from GUI.View import View
from GUI.Style import get_style
from GUI.MVAQWidget import MVAQWidget
import pyqtgraph as pg
import numpy as np
from enum import Enum


# TODO: Study when is useful use function out of classes. Be pythonic
# TODO: Line plots whose x axis is time.
#  - Maybe it can change in days
# TODO: Change size of symbols depending on number of observations
# TODO: Study how optimize complex graphs understanding PyQtGraph
class GraphType(Enum):
    line_plot = 1
    obs_graph = 2
    vars_graph = 3
    scatter = 4
    populations = 5
    correlation = 6
    score_plot = 7
    score_line_plot = 8
    loading_plot = 9
    loading_line_plot = 10
    t2_hotelling = 11
    spe = 12


def interpolate_color(initial_color, end_color, initial, end, num):
    num = num - initial
    num = num / (end-initial)
    min_r = min(initial_color.redF(), end_color.redF())
    max_r = max(initial_color.redF(), end_color.redF())
    r_grades = np.linspace(initial_color.red(), end_color.red(), 255, endpoint=True)
    r = r_grades[int(num*(255-1))]
    g_grades = np.linspace(initial_color.green(), end_color.green(), 255, endpoint=True)
    g = g_grades[int(num*(255-1))]
    b_grades = np.linspace(initial_color.blue(), end_color.blue(), 255, endpoint=True)
    b = b_grades[int(num*(255-1))]
    # return QtGui.QColor(r, g, b)
    return QtGui.QColor(r, g, b)


# TODO: Allow panning with % limits
# TODO: Allow zooming with % limits
class MVAQPlot(MVAQWidget):

    new_selection_point_signal = QtCore.pyqtSignal()
    selection_finished_signal = QtCore.pyqtSignal()
    mouse_press_signal = QtCore.pyqtSignal()

    def __init__(self, parent, title='No title', can_select=False):
        MVAQWidget.__init__(self, parent=parent)
        self.setFocus()
        self._title = title
        self.setWindowTitle(title)
        self._can_select = can_select
        if can_select:
            # object cration
            pass
        self.graphics_layout = pg.GraphicsLayoutWidget(self)
        self._creating_region = False
        self.selection_points = list()
        self.selection_timer = QtCore.QTimer()

    # Mouse
    # TODO: wrap buttons to a manager and take it out from View layer
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # TODO: Signal to use when graphs will be ok designed
            self.mouse_press_signal.emit()
            if self._can_select:
                if self._creating_region:
                    self._creating_region = False
                    self.selection_timer.stop()
                    self.selection_finished_signal.emit()
                else:
                    self._creating_region = True
                    self.selection_points = list()
                    self.selection_timer.start(100)
            print("Press!")

    def center_plot(self, plot):
        # x_max = max(max(abs(xs)), min(abs(xs)))
        # y_max = max(max(abs(ys)), min(abs(ys)))
        children_bounds = plot.getViewBox().childrenBounds()
        print('children_bounds: ' + str(children_bounds))
        x_max = max(abs(children_bounds[0][0]), abs(children_bounds[0][1]))
        y_max = max(abs(children_bounds[1][0]), abs(children_bounds[1][1]))
        x_range = (-x_max, x_max)
        y_range = (-y_max, y_max)
        plot.setRange(xRange=x_range, yRange=y_range, padding=0.1)


class VarianceExplainedGraph(MVAQPlot):

    def __init__(self, variance_ratios, parent=None, title=''):
        MVAQPlot.__init__(self, parent=parent, title=title)
        self._variance_ratios = variance_ratios
        self.init_UI()

    def init_UI(self):
        self.resize(300, 600)
        self._plot = self.graphics_layout.addPlot(title=self._title)
        self.graphics_layout.setMinimumHeight(300)
        self.graphics_layout.setMinimumWidth(600)

        num_components = len(self._variance_ratios)
        x = np.linspace(1, num_components, num_components)
        bar_width = 0.8
        bar_graph = pg.BarGraphItem(x0=x - (bar_width / 2),
                                    x1=x + (bar_width / 2),
                                    width=bar_width,
                                    height=self._variance_ratios,
                                    brush=get_style().palette(2))
        curve_item = pg.PlotCurveItem()
        curve_pen = pg.mkPen(color=get_style().palette(5), width=5,
                             style=QtCore.Qt.DashLine)
        curve_item.setData(x=x, y=self._variance_ratios,
                           pen=curve_pen)
        # TODO: Ajustar el gráfico para que en X vaya de 1 a n

        self._plot.showGrid(x=True, y=True, alpha=0.3)
        self._plot.setMouseEnabled(x=False, y=False)
        self._plot.addItem(bar_graph)
        self._plot.addItem(curve_item)

        layout = QVBoxLayout()
        layout.addWidget(self.graphics_layout)
        self.setLayout(layout)

# TODO: A beautiful example of Pearson Correlation graph
#  https://towardsdatascience.com/handling-missing-values-in-machine-learning-part-2-222154b4b58e
class CorrelationPlot(MVAQPlot):

    def __init__(self, type, data_set_name, data_set_list, parent=None):
        self._type = type
        self._data_set_name = data_set_name
        self._data_set_list = data_set_list
        self._title = 'Correlation plot - ' + data_set_name
        can_select = False

        MVAQPlot.__init__(self, can_select=can_select, parent=parent, title=self._title)

        self.graphics_layout.setContentsMargins(0, 0, 0, 0)
        self._combo_width = 200

        self.graphics_layout.setMinimumHeight(900)
        self.graphics_layout.setMinimumWidth(900)
        self.init_UI()

    def init_UI(self):

        general_layout = QVBoxLayout(self)
        selectors_layout = QHBoxLayout(self)

        # Components - Upper labels
        label_data_set = QLabel()
        label_data_set.setText('Data set: ')
        self.selector_data_set = QComboBox()
        self.selector_data_set.setMinimumWidth(self._combo_width)
        self.selector_data_set.addItems(self._data_set_list)

        # Title and description labels
        label = QLabel()
        label.setText(self._title)
        label.setFont(QtGui.QFont("Arial", 12))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setAlignment(QtCore.Qt.AlignCenter)
        description_label = QLabel()
        description_label.setText("Values range from red (positive correlation) to blue (negative correlation)")
        description_label.setFont(QtGui.QFont("Arial", 8))
        description_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description_label.setAlignment(QtCore.Qt.AlignCenter)

        # Layouts
        selectors_layout.addWidget(label_data_set)
        selectors_layout.addWidget(self.selector_data_set)
        selectors_layout.setAlignment(QtCore.Qt.AlignCenter)

        general_layout.addLayout(selectors_layout)
        general_layout.addItem(QSpacerItem(0, 10))
        general_layout.addWidget(label)
        general_layout.addItem(QSpacerItem(0, 10))
        general_layout.addWidget(description_label)
        general_layout.addItem(QSpacerItem(0, 10))
        general_layout.addWidget(self.graphics_layout)

        self.setLayout(general_layout)

        self.set_children_focus_policy()

    def set_grid(self, correlation_matrix, var_names):
        self.graphics_layout.clear()
        self.graphics_layout.addLabel('')  # Leaves blank (0, 0) position
        for name in var_names:
            self.graphics_layout.addLabel(name)
        self.graphics_layout.nextRow()
        for i_row, row in enumerate(correlation_matrix):
            self.graphics_layout.addLabel(var_names[i_row])
            for corr in row:
                if corr < 0:
                    color = interpolate_color(get_style().palette(5),
                                              QtGui.QColor(255,255,255), -1, 0, corr)
                else:
                    color = interpolate_color(QtGui.QColor(255,255,255),
                                              get_style().palette(6), 0, 1, corr)
                plot = self.graphics_layout.addPlot(axisItems=None)
                plot.hideAxis('left')
                plot.hideAxis('bottom')
                plot.getViewBox().setBackgroundColor(color)
                text = pg.TextItem(str(round(corr, 2)), anchor=(0.5, 0.5), color=(50, 50, 50))
                plot.addItem(text)
            self.graphics_layout.nextRow()

    def get_type(self):
        return self._type

class PopulationsGraph(MVAQPlot):

    def __init__(self, type, data_set_name, data_set_list, parent=None):
        self._type = type
        self._data_set_name = data_set_name
        self._data_set_list = data_set_list
        title = 'Correlation plot - ' + data_set_name
        can_select = True

        MVAQPlot.__init__(self, can_select=can_select, parent=parent, title=title)

        self._scatter_list = list()
        self._histograms_list = list()
        self.graphics_layout.setContentsMargins(0, 0, 0, 0)
        self._combo_width = 200

        self.graphics_layout.setMinimumHeight(1000)
        self.graphics_layout.setMinimumWidth(1000)
        self.init_UI()

    def init_UI(self):
        general_layout = QVBoxLayout(self)
        selectors_layout = QHBoxLayout(self)

        # Components - Upper labels
        label_data_set = QLabel()
        label_data_set.setText('Data set: ')
        self.selector_data_set = QComboBox()
        self.selector_data_set.setMinimumWidth(self._combo_width)
        self.selector_data_set.addItems(self._data_set_list)

        # Layouts
        selectors_layout.addWidget(label_data_set)
        selectors_layout.addWidget(self.selector_data_set)
        selectors_layout.setAlignment(QtCore.Qt.AlignCenter)

        general_layout.addLayout(selectors_layout)
        general_layout.addWidget(self.graphics_layout)

        self.setLayout(general_layout)

        self.set_children_focus_policy()

    def set_data(self, data, var_names):
        self._scatter_list = list()
        self._histograms_list = list()
        self.graphics_layout.clear()
        self.graphics_layout.addLabel('')  # Leaves blank (0, 0) position
        for name in var_names:
            self.graphics_layout.addLabel(name)
        self.graphics_layout.nextRow()
        self._num_points = len(data)
        self._selected = [False] * self._num_points
        data = np.array(data.transpose())
        num_cols = len(data)
        for i_col1 in range(num_cols):
            self.graphics_layout.addLabel(var_names[i_col1])
            for i_col2 in range(num_cols):
                plot = self.graphics_layout.addPlot(axisItems=None)
                plot.showGrid(x=True, y=True, alpha=0.3)
                plot.setMouseEnabled(x=False, y=False)
                if i_col1 == i_col2:
                    y, x = np.histogram(data[i_col1])
                    histogram = pg.PlotDataItem(x, y, stepMode=True)#, fillLevel=0)
                    plot.addItem(histogram)
                    self._histograms_list.append(histogram)
                else:
                    scatter_plot = pg.ScatterPlotItem()
                    plot.addItem(scatter_plot)
                    self._scatter_list.append(scatter_plot)
                    print(str(i_col1) + ', ' + str(i_col2))
                    scatter_plot.setData(x=data[i_col2], y=data[i_col1], size=4)
            self.graphics_layout.nextRow()

        self.repaint_plot()

    def draw_selected(self, selected):
        self._selected = selected
        self.repaint_plot()

    def repaint_plot(self):
        pens = list()
        brushes = list()
        # TODO: Optimize changing only points that has changed
        for i in range(self._num_points):
            pen = pg.mkPen(0.0)
            brush = QtGui.QBrush(get_style().palette(5))
            if self._selected[i]:
                pen = pg.mkPen(width=3, color=(0, 0, 0))

            pens.append(pen)
            brushes.append(brush)

        brush = QtGui.QBrush(get_style().palette(5))
        pen = pg.mkPen(0.0)
        pen_selected = pen = pg.mkPen(width=3, color=(0, 0, 0))

        for scatter in self._scatter_list:
            scatter.setPen(pens)
            scatter.setBrush(brushes)

        for histogram in self._histograms_list:
            histogram.setPen(pen_selected)
            histogram.setBrush(brush)

    def get_selected(self):
        return self._selected

    def get_type(self):
        return self._type


class ObsGraph(MVAQPlot):

    def __init__(self, type, data_set_name, data_set_list, parent=None):
        self._type = type
        if self._type == GraphType.obs_graph:
            self._title = 'Observations plot - ' + data_set_name
        elif self._type == GraphType.vars_graph:
            self._title = 'Variables plot - ' + data_set_name
        self._data_set_list = data_set_list
        can_select = True

        MVAQPlot.__init__(self, can_select=can_select, parent=parent, title=self._title)

        self._curves_list = list()
        self._combo_width = 200

        self.graphics_layout.setMinimumHeight(600)
        self.graphics_layout.setMinimumWidth(1000)
        self.init_UI()

    def init_UI(self):
        general_layout = QVBoxLayout(self)
        selectors_layout = QHBoxLayout(self)

        # Components - Upper labels
        label_data_set = QLabel()
        label_data_set.setText('Data set: ')
        self.selector_data_set = QComboBox()
        self.selector_data_set.setMinimumWidth(self._combo_width)
        self.selector_data_set.addItems(self._data_set_list)

        # Layouts
        selectors_layout.addWidget(label_data_set)
        selectors_layout.addWidget(self.selector_data_set)
        selectors_layout.setAlignment(QtCore.Qt.AlignCenter)

        general_layout.addLayout(selectors_layout)
        general_layout.addWidget(self.graphics_layout)

        self.setLayout(general_layout)

        self.set_children_focus_policy()

    def set_data(self, data, var_names, data_set_name):

        if self._type == GraphType.obs_graph:
            self._title = 'Observations plot - ' + data_set_name
        elif self._type == GraphType.vars_graph:
            self._title = 'Variables plot - ' + data_set_name

        self.graphics_layout.clear()
        self._curves_list = list()
        data = np.array(data)
        num_vars = len(var_names)
        vars_ids = list(range(num_vars))
        self._num_obs = len(data)
        self._selected = [False] * self._num_obs

        # x-axis
        var_dict = dict(enumerate(var_names))
        x_axis = pg.AxisItem(orientation='bottom')
        x_axis.setTicks([var_dict.items()])

        # Plot
        self._plot = self.graphics_layout.addPlot(title=self._title, axisItems={'bottom': x_axis})
        self.graphics_layout.nextRow()
        self._plot_label_obs = self.graphics_layout.addLabel("Observations")

        # set data
        for index, obs in enumerate(data):
            curve_item = pg.PlotCurveItem(x=vars_ids, y=obs)
            self._plot.addItem(curve_item)
            self._curves_list.append(curve_item)

        self.repaint_plot()

    def draw_selected(self, selected):
        self._selected = selected
        self.repaint_plot()

    def repaint_plot(self):
        for index, curve in enumerate(self._curves_list):
            print('repaint_plot: ' + str(curve))
            color = interpolate_color(get_style().palette(5), get_style().palette(6),
                                      0, self._num_obs, index)
            if self._selected[index]:
                pen = pg.mkPen(width=3, color=color)
            else:
                pen = pg.mkPen(width=1, color=color)
            curve.setPen(pen)

    def get_selected(self):
        return self._selected

    def get_type(self):
        return self._type

# TODO: Add a bar with two points to define the visible range
class LinePlot(MVAQPlot):

    def __init__(self, type, model_name, points, num_components, var_names = None, parent=None):
        self._type = type
        self._ys = points
        self._xs = list(range(len(self._ys)))
        self._num_components = num_components

        if type == GraphType.score_line_plot:
            title = 'Score plot - ' + model_name
            can_select = True
        elif type == GraphType.loading_line_plot:
            title = "Loading plot - " + model_name
            can_select = True
        elif type == GraphType.t2_hotelling:
            title = "Hotelling's T2 - " + model_name
            can_select = True
        elif type == GraphType.spe:
            title = 'SPE-X plot - ' + model_name
            can_select = True

        MVAQPlot.__init__(self, can_select=can_select, parent=parent, title=title)

        self._num_xs = len(self._xs)
        self._selected = [False] * self._num_xs

        if var_names is not None:
            var_dict = dict(enumerate(var_names))
            self._x_axis = pg.AxisItem(orientation='bottom')
            self._x_axis.setTicks([var_dict.items()])

        self._roi = None
        self._roi_pen = pg.mkPen(width=2)
        self._roi_pen.setBrush(QtGui.QBrush(get_style().palette(2), QtCore.Qt.SolidPattern))

        # TODO: As normal practice, import QtGui (and others) to make lines shorter
        #Confidence intervals
        if self._type is not GraphType.score_line_plot and self._type is not GraphType.loading_line_plot:
            interval_95_pen = pg.mkPen(width=1, style=QtCore.Qt.DashLine)
            interval_95_pen.setBrush(QtGui.QBrush(get_style().palette(6), QtCore.Qt.SolidPattern))
            self._interval_95_roi = pg.LineSegmentROI([10000, -1000], 10, angle=-45, pen=interval_95_pen)
            interval_99_pen = pg.mkPen(width=1)
            interval_99_pen.setBrush(QtGui.QBrush(get_style().palette(6), QtCore.Qt.SolidPattern))
            self._interval_99_roi = pg.LineSegmentROI([10000, -1000], 10, angle=-45, pen=interval_99_pen)

        self._combo_width = 50
        self._size_points = 12
        self.graphics_layout.setMinimumWidth(900)

        self.init_UI()

    def init_UI(self):
        self.resize(600, 600)
        # TODO: fill with color the drawn area. Maybe with drawPolygon
        self._roi = pg.PolyLineROI([], pen=self._roi_pen)

        general_layout = QVBoxLayout(self)
        selectors_layout = QHBoxLayout(self)

        # Components - Upper labels
        label_PC = QLabel()
        if self._type == GraphType.spe:
            label_PC.setText('From first component to component: ')
        elif self._type == GraphType.t2_hotelling:
            label_PC.setText('From component ')
        else:
            label_PC.setText('Principal Component: ')
        self.selector_PC = QComboBox()
        self.selector_PC.setMinimumWidth(self._combo_width)

        if self._type == GraphType.t2_hotelling:
            label_PC2 = QLabel()
            label_PC2.setText('to component ')
            self.selector_PC2 = QComboBox()
            self.selector_PC2.setMinimumWidth(self._combo_width)
            self.update_components_list(self._num_components)
            self.selector_PC.setCurrentIndex(0)
            self.selector_PC2.setCurrentIndex(self._num_components - 1)
        else:
            self.update_components_list(self._num_components)
            self.selector_PC.setCurrentIndex(self._num_components - 1)

        # Plot
        self._plot_item = pg.PlotDataItem()
        self._scatter_plot = pg.ScatterPlotItem()
        # graphics_layout and items
        self.graphics_layout.setContentsMargins(10, 10, 10, 10)
        if self._type == GraphType.score_line_plot or self._type == GraphType.loading_line_plot:
            self._plot_label_PCY = self.graphics_layout.addLabel('Principal component', angle=-90, col=0, rowspan=2)
        if self._type == GraphType.loading_line_plot:
            self._plot = self.graphics_layout.addPlot(title=self._title, axisItems={'bottom': self._x_axis})
        else:
            self._plot = self.graphics_layout.addPlot(title=self._title)
        self.set_confidence_intervals()
        self.graphics_layout.nextRow()
        self._plot_label_obs = self.graphics_layout.addLabel("Observations")
        self._plot.addItem(self._plot_item)
        self._plot.addItem(self._scatter_plot, size=self._size_points)
        self._plot.addItem(self._roi, ignoreBounds=True)


        self._plot.setWindowTitle(self._title)
        # TODO: Change style to get a Seaborn's like grid
        self._plot.showGrid(x=True, y=True, alpha=0.3)
        self._plot.setMouseEnabled(x=False, y=False)
        # Set data
        # TODO: Axis scale must be the same
        self.update_data(self._ys)
        # self._plot.disableAutoRange()
        # self.center_plot(self._plot)

        # Layouts
        selectors_layout.addWidget(label_PC)
        selectors_layout.addWidget(self.selector_PC)
        if self._type == GraphType.t2_hotelling:
            spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
            selectors_layout.addItem(spacer)
            selectors_layout.addWidget(label_PC2)
            selectors_layout.addWidget(self.selector_PC2)
        selectors_layout.setAlignment(QtCore.Qt.AlignCenter)
        general_layout.addLayout(selectors_layout)
        general_layout.addWidget(self.graphics_layout)

        self.setLayout(general_layout)

        self.set_children_focus_policy()

    # TODO: Call when the components of the model change
    def update_components_list(self, num_components):
        index_cpx = self.selector_PC.currentIndex()
        index_cpx = index_cpx if index_cpx < num_components else num_components - 1
        self.selector_PC.clear()
        names = ['PC ' + str(i + 1) for i in range(num_components)]
        self.selector_PC.addItems(names)
        self.selector_PC.setCurrentIndex(index_cpx)
        if self._type == GraphType.t2_hotelling:
            self.selector_PC2.clear()
            self.selector_PC2.addItems(names)
            self.selector_PC2.setCurrentIndex(index_cpx)

    def update_data(self, ys):
        self._ys = ys
        self._plot_item.setData(y=self._ys)
        self._scatter_plot.setData(x=self._xs, y=self._ys, size=self._size_points)
        self.repaint_plot()

    def update_labels(self):
        index_cpx = self.selector_PC.currentIndex()
        self._plot_label_PCY.setText('PC ' + str(index_cpx + 1))

    def set_confidence_intervals(self):
        if self._type is not GraphType.score_line_plot and self._type is not GraphType.loading_line_plot:
            self._text_95 = pg.TextItem(str('0.95'), anchor=(0.5, 1), color=get_style().palette(6))
            self._text_99 = pg.TextItem(str('0.99'), anchor=(0.5, 1), color=get_style().palette(6))
            self._plot.addItem(self._text_95)
            self._plot.addItem(self._text_99)
            self._plot.addItem(self._interval_95_roi, ignoreBounds=True)
            self._plot.addItem(self._interval_99_roi, ignoreBounds=True)
            if self._type == GraphType.score_line_plot:
                pass
            # self._confidence_intervals = [self._interval_95_roi, self._interval_99_roi]
            # self._confidence_labels = [self._text_95, self._text_99]

    def update_confidence_intervals(self, interval_95, interval_99):
        if self._type is not GraphType.score_line_plot:
            if self._type == GraphType.score_line_plot:
                pass
            else:
                point_95 = QtCore.QPointF(0, interval_95)
                point_99 = QtCore.QPointF(0, interval_99)
                self._text_95.setPos(point_95)
                self._text_99.setPos(point_99)
                self._interval_95_roi.setPos(pos=point_95)
                self._interval_99_roi.setPos(pos=point_99)

    def draw_selected(self, selected):
        self._selected = selected
        self.repaint_plot()

    def repaint_plot(self):
        scatter_pens = list()
        scatter_brushes = list()
        pen = pg.mkPen(0.0)
        # pen = pg.mkPen(color=get_style().palette(5), width=2)
        brush = pg.mkBrush(get_style().palette(5))

        for i in self._xs:
            scatter_pen = pg.mkPen(0.0)
            # scatter_pen = pg.mkPen(color=get_style().palette(5), size=self._size_points)
            scatter_brush = pg.mkBrush(get_style().palette(5))
            if self._selected[i]:
                scatter_pen = pg.mkPen(width=3, color=(0, 0, 0))

            scatter_pens.append(scatter_pen)
            scatter_brushes.append(scatter_brush)

        self._plot_item.setPen(pen)
        self._plot_item.setBrush(brush)
        self._scatter_plot.setPen(scatter_pens)
        self._scatter_plot.setBrush(scatter_brushes)

    def get_points(self):
        points = list()
        for i in self._xs:
            points.append(QtCore.QPointF(i, self._ys[i]))
        return points

    def get_selected(self):
        return self._selected

    def get_item_to_map(self):
        return self._scatter_plot

    def get_type(self):
        return self._type


class ScatterlotTwoComponents(MVAQPlot):

    # TODO: Set a proper name convention. Points are the elements or the positions?
    #  What is a graph and a plot? And more.
    # TODO: Create a generic object to give selection properties
    def __init__(self, type, model_name, points, num_components, parent=None):
        self._type = type
        self._points = points

        # TODO: Obviously, this is not a good solution. There must be separate classes
        #  for each GraphType
        if type == GraphType.score_plot:
            title = 'Score plot - ' + model_name
            can_select = True
        elif type == GraphType.loading_plot:
            title = 'Loading plot - ' + model_name
            can_select = False

        MVAQPlot.__init__(self, can_select=can_select, parent=parent, title=title)

        self._num_points = len(points[0])
        self._selected = [False] * self._num_points

        self._num_components = num_components

        self._roi = None
        self._roi_pen = pg.mkPen(width=2)
        self._roi_pen.setBrush(QtGui.QBrush(get_style().palette(2), QtCore.Qt.SolidPattern))

        # if self._type == GraphType.score_plot:
        #     # Confidence intervals
        #     interval_95_pen = pg.mkPen(width=1, style=QtCore.Qt.DashLine)
        #     interval_95_pen.setBrush(QtGui.QBrush(get_style().palette(6), QtCore.Qt.SolidPattern))
        #     self._interval_95_roi = pg.EllipseROI([0, 0], [1,1], pen=interval_95_pen)
        #     interval_99_pen = pg.mkPen(width=1)
        #     interval_99_pen.setBrush(QtGui.QBrush(get_style().palette(6), QtCore.Qt.SolidPattern))
        #     self._interval_99_roi = pg.EllipseROI([0, 0], [1,1], pen=interval_99_pen)

        self._combo_width = 50
        self._size_points = 12

        self.init_UI()

    def init_UI(self):
        self.resize(600, 600)
        # TODO: fill with color the drawn area. Maybe with drawPolygon
        if self._type == GraphType.score_plot:
            self._roi = pg.PolyLineROI([], pen=self._roi_pen)

        general_layout = QVBoxLayout(self)
        selectors_layout = QHBoxLayout(self)

        # Components - Upper labels
        label_PCX = QLabel()
        label_PCX.setText('Axis X: ')
        self.selector_PCX = QComboBox()
        self.selector_PCX.setMinimumWidth(self._combo_width)
        label_PCY = QLabel()
        label_PCY.setText('Axis Y: ')
        self.selector_PCY = QComboBox()
        self.selector_PCY.setMinimumWidth(self._combo_width)

        self.update_components_list(self._num_components)
        self.selector_PCX.setCurrentIndex(0)
        self.selector_PCY.setCurrentIndex(1)

        # Plot
        self._scatter_plot = pg.ScatterPlotItem()
        # graphics_layout and items
        self.graphics_layout.setContentsMargins(10, 10, 10, 10)
        self._plot_label_PCY = self.graphics_layout.addLabel('Principal component Y', angle=-90, col=0, rowspan=2)
        self._plot = self.graphics_layout.addPlot(title=self._title)
        self.graphics_layout.nextRow()
        self._plot_label_PCX = self.graphics_layout.addLabel("Principal component X")
        self._plot.addItem(self._scatter_plot)
        if self._type == GraphType.score_plot:
            self._plot.addItem(self._roi, ignoreBounds=True)
        self._plot.setWindowTitle(self._title)
        # TODO: Change style to get a Seaborn's like grid
        self._plot.showGrid(x=True, y=True, alpha=0.3)
        self._plot.setMouseEnabled(x=False, y=False)
        # if self._type == GraphType.score_plot:
        #     self.set_confidence_intervals()
        #     self.update_confidence_intervals(1,2)
        # Set data
        # TODO: Axis scale must be the same
        self.update_data(self._points)

        # Layouts
        selectors_layout.addWidget(label_PCX)
        selectors_layout.addWidget(self.selector_PCX)
        spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        selectors_layout.addItem(spacer)
        selectors_layout.addWidget(label_PCY)
        selectors_layout.addWidget(self.selector_PCY)
        selectors_layout.setAlignment(QtCore.Qt.AlignCenter)
        general_layout.addLayout(selectors_layout)
        general_layout.addWidget(self.graphics_layout)

        self.setLayout(general_layout)

        self._plot.disableAutoRange()
        self.center_plot(self._plot)

        self.set_children_focus_policy()

    # TODO: Call when the components of the model change
    def update_components_list(self, num_components):
        index_cpx = self.selector_PCX.currentIndex()
        index_cpy = self.selector_PCY.currentIndex()
        index_cpx = index_cpx if index_cpx < num_components else num_components - 1
        index_cpy = index_cpy if index_cpy < num_components else num_components - 1
        self.selector_PCX.clear()
        self.selector_PCY.clear()
        names = ['PC ' + str(i + 1) for i in range(num_components)]
        self.selector_PCY.addItems(names)
        self.selector_PCX.addItems(names)
        self.selector_PCX.setCurrentIndex(index_cpx)
        self.selector_PCY.setCurrentIndex(index_cpy)

    def update_data(self, points):
        self._points = points
        self._scatter_plot.setData(self._points[0], self._points[1],
                                   size=self._size_points)  # , symbol='t')
        self.repaint_plot()
        self.update_labels()
        # TODO: Any signal to wrapp data changes?
        self.center_plot(self._plot)

    def update_labels(self):
        index_cpx = self.selector_PCX.currentIndex()
        index_cpy = self.selector_PCY.currentIndex()
        self._plot_label_PCX.setText('PC ' + str(index_cpx + 1))
        self._plot_label_PCY.setText('PC ' + str(index_cpy + 1))

    def set_confidence_intervals(self):
        self._text_95 = pg.TextItem(str('0.95'), anchor=(0.5, 1), color=get_style().palette(6))
        self._text_99 = pg.TextItem(str('0.99'), anchor=(0.5, 1), color=get_style().palette(6))
        self._plot.addItem(self._text_95)
        self._plot.addItem(self._text_99)
        self._plot.addItem(self._interval_95_roi, ignoreBounds=True)
        self._plot.addItem(self._interval_99_roi, ignoreBounds=True)

    def update_confidence_intervals(self, interval_95, interval_99):
        center_95 = QtCore.QPointF(-2, 2)
        center_99 = QtCore.QPointF(-2, 2)
        size_95 = QtCore.QPointF(6, 5)
        size_99 = QtCore.QPointF(7, 5.5)
        self._text_95.setPos(center_95)
        self._text_99.setPos(center_99)
        self._interval_95_roi.setPos(center_95)
        self._interval_99_roi.setPos(center_99)
        self._interval_95_roi.setSize(size_95)
        self._interval_99_roi.setSize(size_99)

    def draw_selected(self, selected):
        self._selected = selected
        self.repaint_plot()

    # TODO: Color system by priority layers? First default, after that check x, finally class...
    def repaint_plot(self):
        pens = list()
        brushes = list()
        # TODO: Optimize changing only points that has changed
        for i in range(self._num_points):
            pen = pg.mkPen(0.0)
            brush = QtGui.QBrush(get_style().palette(5))
            if self._selected[i]:
                pen = pg.mkPen(width=3, color=(0, 0, 0))

            pens.append(pen)
            brushes.append(brush)

        self._scatter_plot.setPen(pens)
        self._scatter_plot.setBrush(brushes)

    def get_points(self):
        self._q_points = list()
        for i in range(self._num_points):
            self._q_points.append(QtCore.QPointF(self._points[0][i], self._points[1][i]))
        return self._q_points

    def get_selected(self):
        return self._selected

    def get_item_to_map(self):
        return self._scatter_plot

    # TODO: All this logic must be in another layer
    def set_points_labels(self, texts):
        self._text_items = list()
        print('texts: ' + str(texts))
        if len(texts) != self._num_points:
            print('Number of texts and points must be the same.')
        else:
            for index, text in enumerate(texts):
                text_item = pg.TextItem(str(text), anchor=(0.5, -0.3), color=(0, 0, 0))
                self._plot.addItem(text_item)
                self._text_items.append(text_item)
            self.update_points_labels()

    def update_points_labels(self):
        points = self.get_points()
        for index, text_item in enumerate(self._text_items):
            text_item.setPos(points[index])

    def get_type(self):
        return self._type
