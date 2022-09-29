import logging
import typing

from PyQt6.QtWidgets import (
    QWidget,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsEllipseItem,
    QApplication,
    QMenu,
)

from PyQt6.QtGui import (
    QBrush, QPen, QFont
)

from PyQt6 import QtCore

from PyQt6.QtCore import Qt, QPointF, QRectF, QPoint

from PyQt6 import QtGui


class HistogramEllipseItem(QGraphicsEllipseItem):

    def __init__(self, x, y, w, h, parent=None, brush=None, pen=None):
        QGraphicsEllipseItem.__init__(self, x, y, w, h, parent=parent)

        self.grid_size = w

        self.setFlag(
            # QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
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

            xx = round(new_pos.x() / (2*self.grid_size)) * 2*self.grid_size
            yy = round(new_pos.y() / self.grid_size) * self.grid_size

            return QPointF(xx, yy)
        else:
            return value


class HistogramScene(QGraphicsScene):

    def __init__(self, parent, grid_size=10, bottom_values=[]):
        super(HistogramScene, self).__init__(parent=parent)
        self.grid_size = grid_size
        self.bottom_values = bottom_values

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF) -> None:
        painter.setPen(QPen())

        left = float(int(rect.left()) - (int(rect.left()) % self.grid_size))
        top = float(int(rect.top()) - (int(rect.top()) % self.grid_size))
        right = float(int(rect.right()) - (int(rect.right()) % self.grid_size))
        bottom = float(int(rect.bottom()) - (int(rect.bottom()) % self.grid_size))

        logging.debug(f"left: {left}, top: {top}, right: {right}, bottom: {bottom}")

        points = []
        x = left
        while x <= right:
            y = top
            while y <= bottom:
                points.append(QPointF(x, y))
                y += self.grid_size
            x += self.grid_size

        pen = QPen(Qt.GlobalColor.blue)
        pen.setCosmetic(True)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawPoints(points)

        txt_item_font = QFont("Arial", 14)

        painter.setFont(txt_item_font)
        index = 0
        for value in self.bottom_values:

            # txt_item_background = self.scene().addRect(0, 0, 10, 10, pen=bkg_pen, brush=bkg_brush)
            # txt_item_background.setPos(10, 10)
            painter.drawText(QPointF(self.grid_size*2 + index*2*self.grid_size, bottom - self.grid_size), str(value))
            #txt_item = self.addText(str(value), font=txt_item_font)
            #txt_item.setPos(index * 60, 60)

            index += 1



class HistogramView(QGraphicsView):

    def __init__(self, parent):

        super(HistogramView, self).__init__(parent=parent)

        self.grid_size = 30
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setScene(HistogramScene(parent=self, grid_size=self.grid_size, bottom_values=[10, 20, 300, 400, 500, 600]))

        brush = QBrush(Qt.GlobalColor.red)
        pen = QPen(Qt.GlobalColor.black)
        pen.setCosmetic(True)
        pen.setWidth(3)

        self.rect = QRectF(0, 0, 600, 600)
        self.setSceneRect(self.rect)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        logging.debug(f"Scene: {self.scene().sceneRect().x()}")

        self.e1 = HistogramEllipseItem(0, 0, self.grid_size, self.grid_size, brush=brush, pen=pen)
        self.e1.setPos(50, 50)
        self.scene().addItem(self.e1)

        self.e2 = HistogramEllipseItem(0, 0, self.grid_size, self.grid_size, brush=brush, pen=pen)
        self.e2.setPos(100, 100)
        self.scene().addItem(self.e2)

        self.e3 = HistogramEllipseItem(0, 0, self.grid_size, self.grid_size, brush=brush, pen=pen)
        self.e3.setPos(150, 150)
        self.scene().addItem(self.e3)

        self.e4 = HistogramEllipseItem(0, 0, self.grid_size, self.grid_size, brush=brush, pen=pen)
        self.e4.setPos(200, 200)
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
        logging.debug(f"e1.pos() = {self.e1.pos().toPoint()}")
        logging.debug(f"e2.pos() = {self.e2.pos().toPoint()}")
        logging.debug(f"e3.pos() = {self.e3.pos().toPoint()}")
        logging.debug(f"e4.pos() = {self.e4.pos().toPoint()}")
        logging.debug("")

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:

        context_menu = QMenu(parent=self)

        act_add_point = context_menu.addAction("add point")
        act_add_point.triggered.connect(self.ctx_menu_act_add_point)

        act_remove_point = context_menu.addAction("remove point")
        act_remove_point.triggered.connect(self.ctx_menu_act_remove_point)

        context_menu.addSeparator()

        act_exit = context_menu.addAction("exit")
        act_exit.triggered.connect(self.ctx_menu_exit)

        context_menu.exec(event.globalPos())

    def ctx_menu_act_add_point(self):
        print("Add point clicked")

    def ctx_menu_act_remove_point(self):
        print("remove point clicked")

    def ctx_menu_exit(self):
        pass

    def set_horizontal_values(self, values):

        pass
