from PySide.QtGui import *
from PySide.QtCore import *


class NodalView(QGraphicsView):

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QColor(70, 70, 70))
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(Qt.IntersectsItemShape)
        self._mouse_previous_position = QPoint(0, 0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            # Store mouse pos
            self._mouse_previous_position = event.pos()
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        # Forward
        QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.RubberBandDrag)
        # Forward
        QGraphicsView.mouseReleaseEvent(self, event)

    def mouseMoveEvent(self, event):
        super(NodalView, self).mouseMoveEvent(event)
        delta = event.pos() - self._mouse_previous_position
        self._mouse_previous_position = event.pos()
        self.translate(delta.x(), delta.y())
        #Auto fit scene to bounding rect items
        self.rect = self.scene().itemsBoundingRect()
        self.rect.setWidth(self.rect.width()+100)
        self.rect.setX(self.rect.x()-100)
        self.rect.setHeight(self.rect.height()+100)
        self.rect.setY(self.rect.y()-100)
        self.scene().setSceneRect(self.rect)
        # Forward
        QGraphicsView.mouseMoveEvent(self, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            # Warn Scene
            self.scene().delete_pressed()
        if event.key() == Qt.Key_Alt:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        if event.key() == Qt.Key_F:
            self.scene().focusItem()
        # Forward
        QGraphicsView.keyPressEvent(self, event)

    def keyReleaseEvent(self, event):
        super(NodalView, self).keyReleaseEvent(event)
        if event.key() == Qt.Key_Alt:
            self.setDragMode(QGraphicsView.RubberBandDrag)

    def fitView(self):
        self.fitInView(self.scene().itemsBoundingRect(), Qt.KeepAspectRatio)

