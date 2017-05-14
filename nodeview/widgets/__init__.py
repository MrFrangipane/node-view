from PySide.QtCore import QRect
from PySide.QtGui import QLabel, QPainter
from nodeview.node import Node


class PyNode(QLabel, Node):

    def __init__(self, name, graph, inputs=None, outputs=None, parent=None):
        self.node = Node(name, graph, inputs, outputs)
        QLabel.__init__(self, parent=parent)
        self.setFixedSize(
            self.node.geometry.bounding_rect.width,
            self.node.geometry.bounding_rect.height
        )

    def _paint_header(self, painter, rectangle):
        painter.drawRect(QRect(rectangle.x, rectangle.y, rectangle.width, rectangle.height))

    def _paint_main(self, painter, rectangle):
        painter.drawRect(QRect(rectangle.x, rectangle.y, rectangle.width, rectangle.height))

    def _paint_slot(self, painter, rectangle, slot):
        painter.drawRect(QRect(rectangle.x, rectangle.y, rectangle.width, rectangle.height))

    def _paint_label(self, painter, rectangle, slot, is_input):
        painter.drawRect(QRect(rectangle.x, rectangle.y, rectangle.width, rectangle.height))

    def _paint(self, painter):
        self._paint_header(painter, self.node.geometry.header_rect)

        self._paint_main(painter, self.node.geometry.main_rect)

        for index, input_ in enumerate(self.node.inputs):
            rectangle = self.node.geometry.input_slot_rects[index]
            self._paint_slot(painter, rectangle, input_)

            rectangle = self.node.geometry.input_label_rects[index]
            self._paint_label(painter, rectangle, input_, is_input=True)

        for index, output in enumerate(self.node.outputs):
            rectangle = self.node.geometry.output_slot_rects[index]
            self._paint_slot(painter, rectangle, output)

            rectangle = self.node.geometry.output_label_rects[index]
            self._paint_label(painter, rectangle, output, is_input=False)

    def paintEvent(self, event):
        QLabel.paintEvent(self, event)
        painter = QPainter()
        painter.begin(self)
        self._paint(painter)
        painter.end()


if __name__ == '__main__':
    import sys
    from PySide.QtGui import QApplication
    from nodeview.graph import Graph

    app = QApplication(sys.argv)

    pynode = PyNode(
        "PyNode Demo",
        Graph("Graph"),
        ['Input A', 'Input B', 'Input C'],
        ['Output']
    )
    pynode.show()

    app.exec_()
