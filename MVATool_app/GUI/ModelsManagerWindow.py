from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from GUI.View import View
from GUI.Style import get_style
import pyqtgraph as pg
import numpy as np


class ModelsManagerWindow(View):

    def __init__(self):
        super().__init__()
        self.models_widgets = list()
        self.init_UI()

    def init_UI(self):
        self._window.resize(1100, 800)
        self._window.show()

        self.scroll_area = QScrollArea(parent=self._window)
        self.connect_to_resize(self.resize)
        self.resize()

        self._layer_to_append = QVBoxLayout()

        widget_container = QWidget()
        widget_container.setLayout(self._layer_to_append)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(widget_container)

        window_layer = QVBoxLayout()
        window_layer.addWidget(widget_container)

        self.scroll_area.show()
        widget_container.show()

    def add_PCA_model(self, name, data_set_name, variance_ratio):
        widget = PCAManagerWidget(self._window, name, data_set_name, variance_ratio)
        self._layer_to_append.addWidget(widget)
        print(name)
        return widget

    def resize(self):
        w = self._window.width()
        h = self._window.height()
        self.scroll_area.resize(w, h)

class PCAManagerWidget(QWidget):

    def __init__(self, parent, name, data_set_name, variance_ratio):
        super().__init__()
        self._name = name
        self._data_set_name = data_set_name
        self._variance_ratio = variance_ratio
        self.setParent(parent)
        self.init_UI()

    def init_UI(self):
        self.setMinimumHeight(400)

        layout = QHBoxLayout(self)
        self._inner_layout = QHBoxLayout(self)
        group = QGroupBox(self)
        group.setLayout(self._inner_layout)
        # group.setMinimumHeight(400)
        layout.addWidget(group)
        self.setLayout(layout)

        # Left - Title, labels and buttons
        left_layout = QVBoxLayout(self)
        # Title
        title_label = QLabel(self)
        title_label.setText('PCA')
        title_font = QtGui.QFont("SansSerif", 14, QtGui.QFont.Bold)
        title_label.setFont(title_font)
        # title_label.setMinimumWidth(left_column_size)

        # Labels and QLineEdit
        labels_box = QGroupBox('Basic information', self)
        basic_info_layout = QHBoxLayout(self)
        labels_layout = QVBoxLayout(self)
        name_label = QLabel(self)
        name_label.setText('Model name: ')
        data_set_name_label = QLabel(self)
        data_set_name_label.setText('Data set name: ')
        labels_layout.addWidget(name_label)
        labels_layout.addWidget(data_set_name_label)
        lines_layout = QVBoxLayout(self)
        name_line = QLineEdit(self)
        name_line.setText(self._name)
        name_line.setReadOnly(True)
        data_set_line = QLineEdit(self)
        data_set_line.setText(self._data_set_name)
        data_set_line.setReadOnly(True)
        lines_layout.addWidget(name_line)
        lines_layout.addWidget(data_set_line)
        basic_info_layout.addLayout(labels_layout)
        basic_info_layout.addLayout(lines_layout)
        labels_box.setLayout(basic_info_layout)
        # Buttons
        buttons_box = QGroupBox('Components', self)
        buttons_layout = QHBoxLayout(self)
        self.add_button = QPushButton(self)
        self.add_button.setText('Add')
        self.remove_button = QPushButton(self)
        self.remove_button.setText('Remove')
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.remove_button)
        buttons_box.setLayout(buttons_layout)
        # Components info
        info_box = QGroupBox('Variance ratio', self)
        info_layout = QHBoxLayout(self)
        info = ''
        for num, val in enumerate(self._variance_ratio):
            info = info + 'Comp. ' + str(num+1) + ': ' + str(format(val,'.2f')) + '\n'
        info_label = QLabel(self)
        info_label.setText(info)
        info_layout.addWidget(info_label)
        info_box.setLayout(info_layout)

        left_layout.addWidget(title_label)
        left_layout.addWidget(labels_box)
        left_layout.addWidget(buttons_box)
        left_layout.addWidget(info_box)
        left_layout.addStretch(1)

        # Right - Graph
        right_layout = QVBoxLayout(self)
        # Graph
        graph = pg.PlotWidget(title='% variance explained per component')
        graph.setMaximumHeight(400)
        num_components = len(self._variance_ratio)
        graph.setMouseEnabled(x=False, y=False)
        x = np.linspace(1, num_components, num_components)
        bar_width = 0.8
        bar_graph = pg.BarGraphItem(x0=x,
                                    width=bar_width,
                                    height=self._variance_ratio,
                                    brush=get_style().palette(2))
        curve_item = pg.PlotCurveItem()
        curve_pen = pg.mkPen(color=get_style().palette(5), width=5,
                             style=QtCore.Qt.DashLine)
        curve_item.setData(x=x+(bar_width/2), y=self._variance_ratio,
                           pen=curve_pen)
        graph.showGrid(x=True, y=True, alpha=0.3)
        graph.addItem(bar_graph)
        graph.addItem(curve_item)

        right_layout.addWidget(graph)
        right_layout.addStretch(1)

        self._inner_layout.addLayout(left_layout)
        self._inner_layout.addLayout(right_layout)
        self._inner_layout.addStretch(1)
