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

class GraphType(Enum):
    score_plot = 1
    score_line_plot = 2
    loading_plot = 3

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
        print(children_bounds[0][0])
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
        self._plot = self.graphics_layout.addPlot(title=self._title)
        self.graphics_layout.setMinimumHeight(300)
        self.graphics_layout.setMinimumWidth(600)

        num_components = len(self._variance_ratios)
        x = np.linspace(1, num_components, num_components)
        bar_width = 0.8
        bar_graph = pg.BarGraphItem(x0=x-(bar_width/2),
                                    x1=x+(bar_width/2),
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


class LinePlot(MVAQPlot):

    def __init__(self, type, model_name, points, num_components, parent=None):
        self._type = type
        self._ys = points
        self._xs = list(range(len(self._ys)))
        self._num_components = num_components

        if type == GraphType.score_plot:
            title = 'Score plot - ' + model_name
            can_select = True
        elif type == GraphType.loading_plot:
            title = 'Loading plot - ' + model_name
            can_select = False

        MVAQPlot.__init__(self, can_select=can_select, parent=parent, title=title)

        self._num_xs = len(self._xs)
        self._selected = [False] * self._num_xs

        self._roi = None
        self._roi_pen = pg.mkPen(width=2)
        self._roi_pen.setBrush(QtGui.QBrush(get_style().palette(2), QtCore.Qt.SolidPattern))

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
        label_PC.setText('Principal Component: ')
        self.selector_PC = QComboBox()
        self.selector_PC.setMinimumWidth(self._combo_width)

        self.update_components_list(self._num_components)
        self.selector_PC.setCurrentIndex(0)

        # Plot
        self._plot_item = pg.PlotDataItem()
        self._scatter_plot = pg.ScatterPlotItem()
        # graphics_layout and items
        self.graphics_layout.setContentsMargins(10, 10, 10, 10)
        self._plot_label_PCY = self.graphics_layout.addLabel('Principal component ', angle=-90, col=0, rowspan=2)
        self._plot = self.graphics_layout.addPlot(title=self._title)
        self.graphics_layout.nextRow()
        self._plot_label_obs = self.graphics_layout.addLabel("Observations", col=1, colspan=2)
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
        selectors_layout.setAlignment(QtCore.Qt.AlignCenter)
        general_layout.addLayout(selectors_layout)
        general_layout.addWidget(self.graphics_layout)

        self.setLayout(general_layout)

        self.set_children_focus_policy()

    # TODO: Call when the components of the model change
    def update_components_list(self, num_components):
        index_cpx = self.selector_PC.currentIndex()
        index_cpx = index_cpx if index_cpx < num_components else num_components-1
        self.selector_PC.clear()
        names = ['PC ' + str(i+1) for i in range(num_components)]
        self.selector_PC.addItems(names)
        self.selector_PC.setCurrentIndex(index_cpx)

    def update_data(self, ys):
        self._ys = ys
        self._plot_item.setData(y=self._ys)
        self._scatter_plot.setData(x=self._xs, y=self._ys, size=self._size_points)
        self.repaint_plot()

    def update_labels(self):
        index_cpx = self.selector_PC.currentIndex()
        self._plot_label_PCY.setText('PC '+str(index_cpx+1))

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
        self._num_components = num_components

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

        self._roi = None
        self._roi_pen = pg.mkPen(width=2)
        self._roi_pen.setBrush(QtGui.QBrush(get_style().palette(2), QtCore.Qt.SolidPattern))

        self._combo_width = 50
        self._size_points = 12

        self.init_UI()

    def init_UI(self):
        self.resize(600, 600)
        # TODO: fill with color the drawn area. Maybe with drawPolygon
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
        self._plot_label_PCX = self.graphics_layout.addLabel("Principal component X", col=1, colspan=2)
        self._plot.addItem(self._scatter_plot)
        self._plot.addItem(self._roi, ignoreBounds=True)
        self._plot.setWindowTitle(self._title)
        # TODO: Change style to get a Seaborn's like grid
        self._plot.showGrid(x=True, y=True, alpha=0.3)
        self._plot.setMouseEnabled(x=False, y=False)
        # Set data
        # TODO: Axis scale must be the same
        self.update_data(self._points)
        self._plot.disableAutoRange()
        self.center_plot(self._plot)

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

        self.set_children_focus_policy()

    # TODO: Call when the components of the model change
    def update_components_list(self, num_components):
        index_cpx = self.selector_PCX.currentIndex()
        index_cpy = self.selector_PCY.currentIndex()
        index_cpx = index_cpx if index_cpx < num_components else num_components-1
        index_cpy = index_cpy if index_cpy < num_components else num_components-1
        self.selector_PCX.clear()
        self.selector_PCY.clear()
        names = ['PC ' + str(i+1) for i in range(num_components)]
        self.selector_PCY.addItems(names)
        self.selector_PCX.addItems(names)
        self.selector_PCX.setCurrentIndex(index_cpx)
        self.selector_PCY.setCurrentIndex(index_cpy)

    def update_data(self, points):
        self._points = points
        self._scatter_plot.setData(self._points[0], self._points[1],
                                   size=self._size_points)#, symbol='t')
        self.repaint_plot()
        self.update_labels()
        # TODO: Any signal to wrapp data changes?
        self.center_plot(self._plot)

    def update_labels(self):
        index_cpx = self.selector_PCX.currentIndex()
        index_cpy = self.selector_PCY.currentIndex()
        self._plot_label_PCX.setText('PC '+str(index_cpx+1))
        self._plot_label_PCY.setText('PC '+str(index_cpy+1))

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
        points = list()
        for i in range(self._num_points):
            points.append(QtCore.QPointF(self._points[0][i], self._points[1][i]))
        return points

    def get_selected(self):
        return self._selected

    def get_item_to_map(self):
        return self._scatter_plot

    # TODO: All this logic must be in another layer
    def set_points_labels(self, texts):
        self._text_items = list()
        points = self.get_points()
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