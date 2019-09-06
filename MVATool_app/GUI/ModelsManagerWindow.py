from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from GUI.View import View
from GUI.Style import get_style
from GUI.GraphWidgets import VarianceExplainedGraph
import pyqtgraph as pg
import numpy as np


class ModelsManagerWindow(View):

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self._window.resize(1100, 800)
        self._window.show()

        self._models_widgets = list()
        self.scroll_area = QScrollArea(parent=self._window)
        self.connect_to_resize(self.resize)
        self.resize()

        self._layer_to_append = QVBoxLayout()

        self._widget_container = QWidget()
        self._widget_container.setLayout(self._layer_to_append)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self._widget_container)

        self._window_layer = QVBoxLayout()
        self._window_layer.addWidget(self._widget_container)

        self.scroll_area.show()
        self._widget_container.show()

    def remove_all_models(self):
        self._models_widgets = list()
        self._layer_to_append = QVBoxLayout()
        self._widget_container.setLayout(self._layer_to_append)

    def add_PCA_model(self, name, data_set_name, variance_ratio):
        widget = PCAManagerWidget(self._window, name, data_set_name, variance_ratio)
        self._models_widgets.append(widget)
        self._layer_to_append.addWidget(widget)
        print(name)
        return widget

    def refresh_widget(self, name, data_set_name, variance_ratio):
        for index, model_widget in enumerate(self._models_widgets):
            if model_widget.name == name:
                # TODO: make refresh works avoiding to restart all the window
                pass
                # widget = PCAManagerWidget(self._window, name, data_set_name, variance_ratio)
                # self._models_widgets[index] = widget
                # self._layer_to_append.removeWidget(name)

                # model_widget.init_UI()
                # model_widget.refresh_widget(variance_ratio)
                # model_widget.repaint()
                # model_widget.update()
                # self._layer_to_append.update()
                # self._window_layer.update()
                # self.scroll_area.show()
                # self.scroll_area.update()
                # self.scroll_area.repaint()
                # self._widget_container.show()
                # self._widget_container.update()
                # self._widget_container.repaint()
                # self._window.show()
                # self._window.update()
                # self._window.repaint()

    def resize(self):
        w = self._window.width()
        h = self._window.height()
        self.scroll_area.resize(w, h)

class PCAManagerWidget(QWidget):

    def __init__(self, parent, name, data_set_name, variance_ratio):
        super().__init__()
        self.setObjectName(name)
        self.name = name
        self._data_set_name = data_set_name
        self.variance_ratio = variance_ratio
        self.setParent(parent)
        self.init_UI()

    def init_UI(self):
        self.setMinimumHeight(400)
        print('------ init_UI')

        layout = QHBoxLayout(self)
        self._inner_layout = QHBoxLayout(self)
        group = QGroupBox(self)
        group.setLayout(self._inner_layout)
        # group.setMinimumHeight(400)
        layout.addWidget(group)
        self.setLayout(layout)

        # Left - Title, labels and buttons
        self.left_layout = QVBoxLayout(self)
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
        name_line.setText(self.name)
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
        self.info_box = QGroupBox('Variance ratio', self)
        self.info_layout = QHBoxLayout(self)
        self._info_label = self.variance_ratio_label()
        self.info_layout.addWidget(self._info_label)
        self.info_box.setLayout(self.info_layout)

        self.left_layout.addWidget(title_label)
        self.left_layout.addWidget(labels_box)
        self.left_layout.addWidget(buttons_box)
        self.left_layout.addWidget(self.info_box)
        self.left_layout.addStretch(1)

        # Right - Graph
        right_layout = QVBoxLayout(self)
        # Graph
        self._plot = self.variance_ratio_plot()

        right_layout.addWidget(self._plot)
        right_layout.addStretch(1)

        self._inner_layout.addLayout(self.left_layout)
        self._inner_layout.addLayout(right_layout)
        self._inner_layout.addStretch(1)

    def variance_ratio_label(self):
        info = ''
        for num, val in enumerate(self.variance_ratio):
            info = info + 'Comp. ' + str(num+1) + ': ' + str(format(val,'.2f')) + '\n'
        # info = str(len(self.variance_ratio))
        info_label = QLabel(self)
        info_label.setText(info)
        return info_label

    def variance_ratio_plot(self):
        graph = VarianceExplainedGraph(self.variance_ratio,
                                       # parent=self,
                                       title='Explained variance ratio per component')
        return graph

    # def refresh_widget(self, variance_ratio):
    #     self.variance_ratio = variance_ratio
    #     print(self.variance_ratio)
    #     self._info_label = self.variance_ratio_label()
    #     print(self._info_label.text())
    #     self._info_label.update()
    #     self._info_label.repaint()
    #     self.info_layout.update()
    #     self.left_layout.update()
    #     self.info_box.update()
    #     self.info_box.repaint()
    #     self._inner_layout.update()
    #     self.update()
    #     self.repaint()
    #
    #     self._plot = self.variance_ratio_plot()
    #     self._plot.update()
    #     self._plot.repaint()
