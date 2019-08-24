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
        self._scroll_area = QScrollArea(self._window)
        self._scroll_area.setAutoFillBackground(True)
        # self._scroll_area.setWidgetResizable(True)
        # self._scroll_area.setFixedHeight(1100)
        # self._scroll_area.setFixedWidth(800)
        self._scroll_area.setMinimumWidth(1100)
        self._scroll_area.setMinimumHeight(800)
        # Primera versión
        self._widget_container = QWidget(self._window)
        # self._widget_container.setLayout(self.models_layout)
        # self._scroll_area.setWidget(self._widget_container)
        self.models_layout = QVBoxLayout(self._widget_container)
        #self.models_layout.addStretch(1)
        self._scroll_area.setLayout(self.models_layout)
        self._general_layout = QVBoxLayout()
        self.models_layout.addLayout(self._general_layout)
        # self._scroll_area.setWidget(self._widget_container)
        # self._widget_container.show()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self._scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._scroll_area.show()

    def add_PCA_model(self, name, data_set_name, variance_ratio):
        widget = PCAManagerWidget(name, data_set_name, variance_ratio)
        #self.models_layout.addWidget(widget)
        self.models_layout.addWidget(widget)
        # layer = widget.get_layer()
        # self.models_layout.addLayout(layer)
        # self._widget_container.repaint()
        return widget


class PCAManagerWidget(QWidget):

    def __init__(self, name, data_set_name, variance_ratio):
        super().__init__()
        self._name = name
        self._data_set_name = data_set_name
        self._variance_ratio = variance_ratio
        self.init_UI()

    def init_UI(self):
        #self.setMinimumHeight(400)
        # self.resize(700, 500)
        # self.resize(self.sizeHint())
        # left_column_size = 400
        # right_column_size = 600

        self.setMinimumHeight(600)

        layout = QHBoxLayout(self)
        self._inner_layout = QHBoxLayout(self)
        group = QGroupBox(self)
        group.setLayout(self._inner_layout)
        group.setMinimumHeight(600)
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

        left_layout.addWidget(title_label)
        left_layout.addWidget(labels_box)
        left_layout.addWidget(buttons_box)
        #left_layout.addStretch(1)

        # Right - Graph
        right_layout = QVBoxLayout(self)
        # Title
        graph_title_label = QLabel(self)
        graph_title_label.setText('% variance explained per component')
        # Graph
        graph = pg.PlotWidget(title='% variance explained per component')
        num_components = len(self._variance_ratio)
        x = np.linspace(1, num_components, num_components)
        bar_graph = pg.BarGraphItem(x=x,
                                    y1=self._variance_ratio,
                                    width=0.6,
                                    brush=get_style().palette(1))
        graph.addItem(bar_graph)

        right_layout.addWidget(graph_title_label)
        right_layout.addWidget(graph)
        #right_layout.addStretch(1)

        self._inner_layout.addLayout(left_layout)
        self._inner_layout.addLayout(right_layout)
        #self._inner_layout.addStretch(1)

    def get_layer(self):
        return self._inner_layout

# class ModelManagerWidget(QWidget):
#
#     def __init__(self):
#         pass
#
# class LatentManagerWidget(ModelManagerWidget):
#
#     def __init__(self):
#         pass
