from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence as QKSec, QIcon
from PyQt5.QtWidgets import QFrame
from GUI.RibbonButton import RibbonButton
from GUI.Icons import get_icon
from GUI.RibbonTextbox import RibbonTextbox
from GUI.RibbonWidget import *
from GUI.View import View
import pyqtgraph as pg
from PyQt5.Qt import Qt

__author__ = 'mamj'

class MainWindow(QMainWindow, View):

    # Data
    on_load_file = pyqtSignal()
    on_new_data_set = pyqtSignal()
    on_edit_data_set = pyqtSignal()
    # Models
    on_models = pyqtSignal()
    on_create_PCA = pyqtSignal()
    # Explore
    on_line_plot = pyqtSignal()
    on_obs_plot = pyqtSignal()
    on_vars_plot = pyqtSignal()
    on_scatter = pyqtSignal()
    on_populations = pyqtSignal()
    on_correlation = pyqtSignal()
    # Analyze
    on_variance_explained = pyqtSignal()
    on_scores = pyqtSignal()
    on_line_scores = pyqtSignal()
    on_loadings = pyqtSignal()
    on_t2_hotelling = pyqtSignal()
    on_spe = pyqtSignal()
    # Selection
    on_exclude = pyqtSignal()
    on_include = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        # self.setMouseTracking(True)
        self.setFocusPolicy(Qt.Qt.StrongFocus)

    def __init__(self):
        QMainWindow.__init__(self, None)
        self.title = 'MVA Tool'
        self.width = 1280
        self.height = 800
        self.window_icon = get_icon('icon')
        self.setFocusPolicy(Qt.StrongFocus)

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
        # Explore
        self._line_plot = self.add_action("Line plot", "line_plot", "Line plot", True, self.on_line_plot, QKSec.Paste)
        self._obs_plot = self.add_action("Obs plot", "obs_plot", "Observations plot", True, self.on_obs_plot, QKSec.Paste)
        self._vars_plot = self.add_action("Vars plot", "obs_plot", "Observations plot", True, self.on_vars_plot, QKSec.Paste)
        self._scatter = self.add_action("Scatter", "scatter", "Scatter plot", True, self.on_scatter, QKSec.Paste)
        self._populations = self.add_action("Populations", "populations", "Populations plot", True, self.on_populations, QKSec.Paste)
        self._correlation_plot = self.add_action("Correlation", "correlation", "Plot correlation", True, self.on_correlation, QKSec.Paste)
        # Analyze
        self._variance_plot = self.add_action("Variance exp.", "variance_explained", "Variance explained plot", True, self.on_variance_explained, QKSec.Paste)
        self._scores = self.add_action("Score plot", "scores", "View scores", True, self.on_scores, QKSec.Paste)
        self._line_scores = self.add_action("Line scores", "line_scores", "View scores", True, self.on_line_scores, QKSec.Paste)
        self._loadings = self.add_action("Loadings", "loadings", "View loadings", True, self.on_loadings, QKSec.Paste)
        self._t2_hotelling = self.add_action("Hotelling's T2", "hotelling", "View Hotelling's T2", True, self.on_t2_hotelling, QKSec.Paste)
        self._SPE = self.add_action("SPE-X", "spe", "View SPE-X", True, self.on_spe, QKSec.Paste)
        # Selection
        self._exclude = self.add_action("Exclude", "exclude", "Create data set", True, self.on_exclude, QKSec.Paste)
        self._include = self.add_action("Include", "include", "Create data set", True, self.on_include, QKSec.Paste)

        self._paste_action = self.add_action("Paste", "paste", "Paste from clipboard", True, self.on_paste, QKSec.Paste)
        self._zoom_action = self.add_action("Zoom", "zoom", "Zoom in on document", True, self.on_zoom)
        self._about_action = self.add_action("About", "about", "About QupyRibbon", True, self.on_about)
        self._license_action = self.add_action("License", "license", "Licence for this software", True, self.on_license)

        # -------------      textboxes       -----------------

        self._text_box1 = RibbonTextbox("Text 1", self.on_text_box1_changed, 80)
        self._text_box2 = RibbonTextbox("Text 2", self.on_text_box1_changed, 80)
        self._text_box3 = RibbonTextbox("Text 3", self.on_text_box1_changed, 80)

        # Menu bar
        # Icons
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        layout = QHBoxLayout(self)
        new_project_icon = QtGui.QPixmap("icons/save.png")
        self.new_project_button = QPushButton(self)
        self.new_project_button.setIcon(QIcon(new_project_icon))
        self.new_project_button.setObjectName('FromMenuBar')
        load_icon = QtGui.QPixmap("icons/save.png")
        self.load_button = QPushButton(self)
        self.load_button.setIcon(QIcon(load_icon))
        self.load_button.setObjectName('FromMenuBar')
        save_icon = QtGui.QPixmap("icons/save.png")
        self.save_button = QPushButton(self)
        self.save_button.setIcon(QIcon(save_icon))
        self.save_button.setObjectName('FromMenuBar')
        # Model selector
        label = QLabel(self)
        # TODO: Add a data set selector. By default, selected data set is the data set from the
        #  last selected model. Indicate when a selected data set doesn't correspond to selected model
        label.setText('Selected model: ')
        self.model_selector = QComboBox(self)
        self.model_selector.setMinimumWidth(300)
        layout.addWidget(self.new_project_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.save_button)
        layout.addWidget(spacer)
        layout.addWidget(label)
        layout.addWidget(self.model_selector)
        self.menuBar().setMinimumHeight(45)
        # TODO: reduce margins. That doesn't seems to work
        self.menuBar().setContentsMargins(0, 0, 0, 0)
        self.menuBar().setLayout(layout)
        self.menuBar().setStyleSheet(get_style().get_stylesheet("main"))

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
        # Data
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

        # Explore
        explore_tab = self._ribbon.add_ribbon_tab('Explore')
        # univariate = explore_tab.add_ribbon_pane('Univariate')
        # univariate.add_ribbon_widget(RibbonButton(self, self._line_plot, True))
        multivariate = explore_tab.add_ribbon_pane('Multivariate')
        multivariate.add_ribbon_widget(RibbonButton(self, self._obs_plot, True))
        multivariate.add_ribbon_widget(RibbonButton(self, self._vars_plot, True))
        multivariate.add_ribbon_widget(RibbonButton(self, self._scatter, True))
        multivariate.add_ribbon_widget(RibbonButton(self, self._populations, True))
        multivariate.add_ribbon_widget(RibbonButton(self, self._correlation_plot, True))
        # Models
        models_tab = self._ribbon.add_ribbon_tab("Models")
        manage = models_tab.add_ribbon_pane("Manage")
        manage.add_ribbon_widget(RibbonButton(self, self._models, True))
        latent_variable = models_tab.add_ribbon_pane("Latent variable")
        latent_variable.add_ribbon_widget(RibbonButton(self, self._create_PCA, True))
        # Analyze
        analyze_tab = self._ribbon.add_ribbon_tab('Analyze')
        latent_variable_models = analyze_tab.add_ribbon_pane('Latent variable models')
        latent_variable_models.add_ribbon_widget(RibbonButton(self, self._variance_plot, True))
        latent_variable_models.add_ribbon_widget(RibbonButton(self, self._scores, True))
        latent_variable_models.add_ribbon_widget(RibbonButton(self, self._line_scores, True))
        latent_variable_models.add_ribbon_widget(RibbonButton(self, self._loadings, True))
        latent_variable_models.add_ribbon_widget(RibbonButton(self, self._t2_hotelling, True))
        latent_variable_models.add_ribbon_widget(RibbonButton(self, self._SPE, True))
        # About
        about_tab = self._ribbon.add_ribbon_tab("About")
        info_panel = about_tab.add_ribbon_pane("Info")
        info_panel.add_ribbon_widget(RibbonButton(self, self._about_action, True))
        info_panel.add_ribbon_widget(RibbonButton(self, self._license_action, True))

    # TODO: Build a system to have a context tab (Selection, ...) and not only selection
    # "fixed tabs" and "context tabs"
    def create_selection_tab(self):
        self._selection_tab = self._ribbon.add_ribbon_tab("Selection")
        create_data_set_panel = self._selection_tab.add_ribbon_pane("Create new data set")
        create_data_set_panel.add_ribbon_widget(RibbonButton(self, self._exclude, True))
        create_data_set_panel.add_ribbon_widget(RibbonButton(self, self._include, True))
        # TODO: Create button "add to class". With that, you can assign obs to 1) an existing
        #  classification with a new value or a an existing one; or 2) create a new column
        #  to classify
        self._ribbon.select_ribbon_tab(self._selection_tab)

    def delete_selection_tab(self):
        self._ribbon.remove_ribbon_tab(self._selection_tab)
        self._selection_tab = None

    def select_tab(self, tab):
        self._ribbon.select_ribbon_tab(tab)

    def get_current_tab(self):
        return self._ribbon.get_current_tab()

    # def eventFilter(self, source, event):
    #     if event.type() == QEvent.FocusOut:
    #         print(str(source)+' - Looooooooooooooooost focus')

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