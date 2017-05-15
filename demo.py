import sys
from PySide.QtGui import QApplication
from nodeview import Graph
from nodeview import widgets


if __name__ == '__main__':
    app = QApplication(sys.argv)

    view = widgets.View()
    view.set_scene_size(1200, 700)
    view.resize(1280, 720)

    graph = Graph("Demo Graph")

    view.add_node(widgets.Node(
        "Demo Node",
        graph,
        ["Input A", "Input B", "Input C"],
        ["Output"]
    ))

    view.add_node(widgets.Node(
        "Demo Node 2",
        graph,
        ["Input"],
        ["Output 1", "Output 2"]
    ))

    view.show()

    app.exec_()
