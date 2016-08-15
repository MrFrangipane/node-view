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
        delta = event.pos() - self._mouse_previous_position
        self._mouse_previous_position = event.pos()
        self.translate(delta.x(), delta.y())
        # Forward
        QGraphicsView.mouseMoveEvent(self, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            # Warn Scene
            self.scene().delete_pressed()
        # Forward
        QGraphicsView.keyPressEvent(self, event)
