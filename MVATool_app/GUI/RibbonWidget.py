from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from GUI.RibbonTab import RibbonTab
from GUI import gui_scale
from GUI.Style import get_style

__author__ = 'magnus'


class RibbonWidget(QToolBar):
    def __init__(self, parent):
        QToolBar.__init__(self, parent)
        self.setStyleSheet(get_style().get_stylesheet("ribbon"))
        self.setObjectName("ribbonWidget")
        self.setWindowTitle("Ribbon")
        self._ribbon_widget = QTabWidget(self)
        self._ribbon_widget.setMaximumHeight(120*gui_scale())
        self._ribbon_widget.setMinimumHeight(110*gui_scale())
        self.setMovable(False)
        self.addWidget(self._ribbon_widget)

    def add_ribbon_tab(self, name):
        ribbon_tab = RibbonTab(self, name)
        ribbon_tab.setObjectName("tab_" + name)
        self._ribbon_widget.addTab(ribbon_tab, name)
        return ribbon_tab

    def remove_ribbon_tab(self, tab):
        index = self._ribbon_widget.indexOf(tab)
        self._ribbon_widget.removeTab(index)

    def select_ribbon_tab(self, tab):
        index = self._ribbon_widget.indexOf(tab)
        self._ribbon_widget.setCurrentIndex(index)

    def get_current_tab(self):
        return self._ribbon_widget.currentWidget()

    def add_ribbon_combo_box(self, models_names):
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        layout = QHBoxLayout(self)
        label = QLabel(self)
        label.setText('Selected model aaaaaaaa: ')
        combo_box = QComboBox(self)
        combo_box.addItems(models_names)
        # layout.addWidget(label)
        # layout.addWidget(spacer)
        # layout.addWidget(combo_box)

        # self.addWidget(spacer)
        # self.addWidget(label)
        # self.addWidget(combo_box)
        self.addAction('aaaa')
        self.setLayout(layout)
        return layout

    def set_active(self, name):
        self.setCurrentWidget(self.findChild("tab_" + name))