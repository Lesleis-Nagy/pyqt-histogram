from pyqt_histogram.gui.mainwin.MainWindowRoot import Ui_MainWindowRoot

from PyQt6.QtWidgets import (
    QMainWindow,
    QGraphicsScene
)

from pyqt_histogram.gui.histogram import Histogram

class MainWindow(QMainWindow, Ui_MainWindowRoot):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        Ui_MainWindowRoot.__init__(self)

        self.setupUi(self)

        #self.histogram_scene = QGraphicsScene()
        #self.histogram_graphics.setScene(self.histogram_scene)
        #self.histogram = Histogram(self.histogram_scene)

        print(self.histogram.geometry().size())
