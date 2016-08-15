from PySide.QtGui import *
from PySide.QtCore import *


class NodalView(QGraphicsView):

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QColor(70, 70, 70))
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(Qt.ContainsItemBoundingRect)
