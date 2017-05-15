from PySide.QtGui import QGraphicsView, QPainter, QColor
from PySide.QtCore import Qt, QRect
from scene import Scene


class View(QGraphicsView):

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QColor(70, 70, 70))
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(Qt.IntersectsItemShape)

        self.scene = Scene()
        self.setScene(self.scene)

    def set_scene_size(self, width, height):
        self.scene.setSceneRect(QRect(
            -width / 2,
            -height / 2,
            width,
            height
        ))

    def add_node(self, node):
        self.scene.addItem(node)
