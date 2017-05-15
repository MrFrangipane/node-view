from PySide.QtGui import QGraphicsScene


class Scene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
