from PyQt5.QtGui import *

__author__ = 'magnus'

icons_instance = None


def get_icon(name):
    global icons_instance
    if not icons_instance:
        icons_instance = Icons()
    return icons_instance.icon(name)


class Icons(object):
    def __init__(self):
        self._icons = {}
        self.make_icon("folder", "icons/folder.png")
        self.make_icon("open", "icons/folder.png")
        self.make_icon("save", "icons/save.png")
        self.make_icon("icon", "icons/icon.png")
        self.make_icon("exit", "icons/exit.png")
        self.make_icon("paste", "icons/paste.png")
        self.make_icon("zoom", "icons/zoom.png")
        self.make_icon("copy", "icons/copy.png")
        self.make_icon("about", "icons/about.png")
        self.make_icon("license", "icons/license.png")
        self.make_icon("default", "icons/folder.png")
        # Menu bar
        self.make_icon("save", "icons/save.png")
        self.make_icon("load_project", "icons/load_project.png")
        # Data
        self.make_icon("new-data-set", "icons/new-data-set.png")
        self.make_icon("edit-data-set", "icons/edit-data-set.png")
        # Exploratory
        self.make_icon("obs_plot", "icons/obs_plot.png")
        self.make_icon("vars_plot", "icons/vars_plot.png")
        self.make_icon("populations", "icons/populations.png")
        self.make_icon("correlation", "icons/correlation.png")
        # Models
        self.make_icon("models", "icons/models.png")
        # Analyze
        self.make_icon("variance_explained", "icons/variance_explained.png")
        self.make_icon("scores", "icons/scores.png")
        self.make_icon("line_scores", "icons/line_scores.png")
        self.make_icon("loadings", "icons/loadings.png")
        self.make_icon("line_loadings", "icons/line_loadings.png")
        self.make_icon("hotelling", "icons/hotelling.png")
        self.make_icon("spe", "icons/spe.png")
        # Selector
        self.make_icon("exclude", "icons/exclude.png")
        self.make_icon("include", "icons/include.png")

    def make_icon(self, name, path):
        icon = QIcon()
        icon.addPixmap(QPixmap(path), QIcon.Normal, QIcon.Off)
        self._icons[name] = icon

    def icon(self, name):
        icon = self._icons["default"]
        try:
            icon = self._icons[name]
        except KeyError:
            print("icon " + name + " not found")
        return icon
