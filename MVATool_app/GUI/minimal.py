from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import pyqtgraph as pg
import sys

class MVAQPlot(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.resize(600,600)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self._graphics_layout = pg.GraphicsLayoutWidget(self)
        layout = QHBoxLayout()
        layout.addWidget(self._graphics_layout)
        self.setLayout(layout)

        self._scores = ([1, 1.5, 3, 5, 5], [1, 1.5, 3.4, 4, 2])

        self._roi = pg.PolyLineROI([], pen=(5))
        self._scatter_plot = pg.ScatterPlotItem()
        self._scatter_plot.setData(self._scores[0], self._scores[1])
        plot = self._graphics_layout.addPlot()
        plot.addItem(self._scatter_plot)
        plot.addItem(self._roi)

        self._selection_timer = QtCore.QTimer()
        self._selection_timer.timeout.connect(self.update_selection)

        self._creating_region = False
        self._last_point = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self._creating_region:
                self._creating_region = False
                self._selection_timer.stop()
                roi_shape = self._roi.mapToItem(self._scatter_plot, self._roi.shape())
                self._points = list()
                for i in range(len(self._scores[0])):
                    self._points.append(QtCore.QPoint(self._scores[0][i], self._scores[1][i]))
                selected = [roi_shape.contains(pt) for pt in self._points]
                print('Selected points: ' + str(selected))
                self._roi.clearPoints()
            else:
                self._creating_region = True
                self._selection_points = list()
                self._selection_timer.start(1000)

    def update_selection(self):
        if self._roi is not None:
            point = QtCore.QPoint(self._graphics_layout.lastMousePos[0],
                                  self._graphics_layout.lastMousePos[1])
            self._selection_points.append(point)
            region = QtGui.QPolygon(self._selection_points)
            mapped_point = self._scatter_plot.mapFromDevice(region)
            self._roi.setPoints(mapped_point)

    def focusInEvent(self, event):
        print('In focus')

    def focusOutEvent(self, event):
        print('Looooooooooooooooost focus')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QMainWindow()
    view.show()
    widget = MVAQPlot()
    widget.show()
    sys.exit(app.exec_())