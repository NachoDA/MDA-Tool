from PyQt5 import QtGui

__author__ = 'magnus'

style_instance = None

def get_style():
    global style_instance
    if not style_instance:
        style_instance = Style()
    return style_instance

class Style(object):
    def __init__(self):
        self._stylesheets = {}
        self.make_stylesheet("main", "stylesheets/main.css")
        self.make_stylesheet("ribbon", "stylesheets/ribbon.css")
        self.make_stylesheet("ribbonPane", "stylesheets/ribbonPane.css")
        self.make_stylesheet("ribbonButton", "stylesheets/ribbonButton.css")
        self.make_stylesheet("ribbonSmallButton", "stylesheets/ribbonSmallButton.css")

        # Cells
        self.make_stylesheet("editDataset", "stylesheets/Cells/editDataset.css")

    def make_stylesheet(self, name, path):
        with open(path) as data_file:
            stylesheet = data_file.read()

        self._stylesheets[name] = stylesheet

    def get_stylesheet(self, name):
        stylesheet = ""
        try:
            stylesheet = self._stylesheets[name]
        except KeyError:
            print("stylesheet " + name + " not found")
        return stylesheet
    
    # -------------      colors       -----------------
    def color_primary_row(self):
        return QtGui.QColor('#fdcb6e')

    def color_secondary_row(self):
        return QtGui.QColor('#ffeaa7')

    def color_primary_col(self):
        return QtGui.QColor('#00cec9')

    def color_secondary_col(self):
        return QtGui.QColor('#81ecec')

    def color_discarded(self):
        return QtGui.QColor('#b2bec3')

    def color_data(self):
        return QtGui.QColor('ffffff')

    def palette(self, order):
        if order == 1:
            return QtGui.QColor('#81ecec')
        elif order == 2:
            return QtGui.QColor('#fdcb6e')
        elif order == 3:
            return QtGui.QColor('#55efc4')
        elif order == 4:
            return QtGui.QColor('#fab1a0')
        elif order == 5:
            return QtGui.QColor('#74b9ff')
        elif order == 6:
            return QtGui.QColor('#ff7675')
        elif order == 7:
            return QtGui.QColor('#a29bfe')
