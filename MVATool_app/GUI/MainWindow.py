from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence as QKSec
from GUI.RibbonButton import RibbonButton
from GUI.Icons import get_icon
from GUI.RibbonTextbox import RibbonTextbox
from GUI.RibbonWidget import *
from GUI.View import View
import pyqtgraph as pg

__author__ = 'mamj'

class MainWindow(QMainWindow, View):
    
    on_load_file = pyqtSignal()
    on_new_data_set = pyqtSignal()
    on_edit_data_set = pyqtSignal()
    on_models = pyqtSignal()
    on_create_PCA = pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self, None)
        self.title = 'MVA Tool'
        self.width = 1280
        self.height = 800
        self.window_icon = get_icon('icon')

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.init_UI()

    def init_UI(self):
        self.resize(self.width, self.height)
        self.setWindowTitle(self.title)
        self.setDockNestingEnabled(True)
        self.setWindowIcon(self.window_icon)
        self._main_dock_widget = QDockWidget(self)
        self._main_dock_widget.setObjectName("MainDock")
        self._main_dock_widget.setWindowTitle("Main dock")
        self.addDockWidget(Qt.LeftDockWidgetArea, self._main_dock_widget)
        self.centralWidget()

        # -------------      actions       -----------------
        # Data
        self._load_file_action = self.add_action("Load", "load", "Load file", True, self.on_load_file, QKSec.Open)
        self._new_data_set = self.add_action("New data set", "new-data-set", "New data set", True, self.on_new_data_set, QKSec.Save)
        self._edit_data_set = self.add_action("Edit data set", "edit-data-set", "Edit data set", True, self.on_edit_data_set, QKSec.Copy)
        # Models
        self._models = self.add_action("Models", "models", "View models", True, self.on_models, QKSec.Paste)
        self._create_PCA = self.add_action("Create PCA", "models", "Create PCA", True, self.on_create_PCA, QKSec.Paste)

        self._paste_action = self.add_action("Paste", "paste", "Paste from clipboard", True, self.on_paste, QKSec.Paste)
        self._zoom_action = self.add_action("Zoom", "zoom", "Zoom in on document", True, self.on_zoom)
        self._about_action = self.add_action("About", "about", "About QupyRibbon", True, self.on_about)
        self._license_action = self.add_action("License", "license", "Licence for this software", True, self.on_license)

        # -------------      textboxes       -----------------

        self._text_box1 = RibbonTextbox("Text 1", self.on_text_box1_changed, 80)
        self._text_box2 = RibbonTextbox("Text 2", self.on_text_box1_changed, 80)
        self._text_box3 = RibbonTextbox("Text 3", self.on_text_box1_changed, 80)

        # Ribbon

        self._ribbon = RibbonWidget(self)
        self.addToolBar(self._ribbon)
        self.init_ribbon()

    def add_action(self, caption, icon_name, status_tip, icon_visible, connection, shortcut=None):
        action = QAction(get_icon(icon_name), caption, self)
        action.setStatusTip(status_tip)
        action.triggered.connect(connection)
        action.setIconVisibleInMenu(icon_visible)
        if shortcut is not None:
            action.setShortcuts(shortcut)
        self.addAction(action)
        return action

    def init_ribbon(self):
        home_tab = self._ribbon.add_ribbon_tab("Data")
        file_pane = home_tab.add_ribbon_pane("File")
        file_pane.add_ribbon_widget(RibbonButton(self, self._load_file_action, True))
        edit_panel = home_tab.add_ribbon_pane("Data set")
        edit_panel.add_ribbon_widget(RibbonButton(self, self._new_data_set, True))
        edit_panel.add_ribbon_widget(RibbonButton(self, self._edit_data_set, True))
        # edit_panel.add_ribbon_widget(RibbonButton(self, self._paste_action, True))
        # grid = edit_panel.add_grid_widget(200)
        # grid.addWidget(QLabel("Text box 1"), 1, 1)
        # grid.addWidget(QLabel("Text box 2"), 2, 1)
        # grid.addWidget(QLabel("Text box 3"), 3, 1)
        # grid.addWidget(self._text_box1, 1, 2)
        # grid.addWidget(self._text_box2, 2, 2)
        # grid.addWidget(self._text_box3, 3, 2)

        view_panel = home_tab.add_ribbon_pane("View")
        view_panel.add_ribbon_widget(RibbonButton(self, self._zoom_action, True))
        home_tab.add_spacer()

        models_tab = self._ribbon.add_ribbon_tab("Models")
        manage = models_tab.add_ribbon_pane("Manage")
        manage.add_ribbon_widget(RibbonButton(self, self._models, True))
        latent_variable = models_tab.add_ribbon_pane("Latent variable")
        latent_variable.add_ribbon_widget(RibbonButton(self, self._create_PCA, True))

        about_tab = self._ribbon.add_ribbon_tab("About")
        info_panel = about_tab.add_ribbon_pane("Info")
        info_panel.add_ribbon_widget(RibbonButton(self, self._about_action, True))
        info_panel.add_ribbon_widget(RibbonButton(self, self._license_action, True))

    def closeEvent(self, close_event):
        pass

    #def on_load_file(self):
    #    pass

    def on_save_to_excel(self):
        pass

    def on_save(self):
        pass

    def on_text_box1_changed(self):
        pass

    def on_text_box2_changed(self):
        pass

    def on_text_box3_changed(self):
        pass

    def on_copy(self):
        pass

    def on_paste(self):
        pass

    def on_zoom(self):
        pass

    def on_about(self):
        text = "QupyRibbon\n"
        text += "This program was made by Magnus Jørgensen.\n"
        text += "Copyright © 2016 Magnus Jørgensen"
        QMessageBox().about(self, "About QupyRibbon", text)

    def on_license(self):
        file = open('LICENSE', 'r')
        lic = file.read()
        QMessageBox().information(self, "License", lic)
