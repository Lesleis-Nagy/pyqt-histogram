import typing

from PyQt6.QtWidgets import (
    QWidget,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsEllipseItem,
    QApplication
)

from PyQt6.QtGui import (
    QBrush, QPen
)

from PyQt6 import QtCore

from PyQt6.QtCore import Qt, QPointF, QRectF

from PyQt6 import QtGui

class HistogramGraphicsEllipseItem(QGraphicsEllipseItem):

    def __init__(self, x, y, w, h, parent=None, brush=None, pen=None):
        QGraphicsEllipseItem.__init__(self, x, y, w, h, parent=parent)

        self.grid_size = 10

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

        if brush:
            self.setBrush(brush)
        if pen:
            self.setPen(pen)

    def itemChange(self, change: 'QGraphicsItem.GraphicsItemChange', value: typing.Any) -> typing.Any:
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            new_pos = QPointF(value)

            xx = round(new_pos.x() / self.grid_size) * self.grid_size
            yy = round(new_pos.y() / self.grid_size) * self.grid_size

            return QPointF(xx, yy)
        else:
            return value

class HistogramScene(QGraphicsScene):

    def __init__(self, parent):
        super(HistogramScene, self).__init__(parent=parent)
        self.grid_size = 10

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF) -> None:
        painter.setPen(QPen())

        left = float(int(rect.left()) - (int(rect.left()) % self.grid_size))
        top = float(int(rect.top()) - (int(rect.top()) % self.grid_size))

        points = []
        x = left
        while x < rect.right():
            y = top
            while y < rect.bottom():
                points.append(QPointF(x, y))
                y += self.grid_size
            x += self.grid_size

        pen = QPen(Qt.GlobalColor.blue)
        pen.setCosmetic(True)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawPoints(points)


class Histogram(QGraphicsView):

    def __init__(self, parent):

        super(Histogram, self).__init__(parent=parent)

        self.setScene(HistogramScene(parent=self))

        brush = QBrush(Qt.GlobalColor.red)
        pen = QPen(Qt.GlobalColor.black)
        pen.setCosmetic(True)
        pen.setWidth(3)

        self.rect = QRectF(-300, -300, 600, 600)
        self.setSceneRect(self.rect)

        self.e1 = self.scene().addEllipse(0, 0, 10, 10, brush=brush, pen=pen)
        self.e1.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.e2 = self.scene().addEllipse( 100,  100, 10, 10, brush=brush, pen=pen)
        self.e2.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.e3 = self.scene().addEllipse(-100, -100, 10, 10, brush=brush, pen=pen)
        self.e3.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.e4 = HistogramGraphicsEllipseItem(-50, -50, 10, 10, brush=brush, pen=pen)
        self.scene().addItem(self.e4)

    def fit_view(self):

        self.fitInView(self.rect, Qt.AspectRatioMode.KeepAspectRatio)
        self.setSceneRect(self.rect)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.fit_view()

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        self.fit_view()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        QGraphicsView.mouseMoveEvent(self, event)
        print(self.e1.pos())
