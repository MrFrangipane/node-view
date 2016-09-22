import logging

from nodeview import persistance
from scene import NodalScene
from view import NodalView

if __name__ == '__main__':
    # Log to INFO
    logging.getLogger().setLevel(logging.INFO)

    # Application
    from PySide.QtGui import QApplication
    from PySide.QtCore import QRect
    app = QApplication([])

    # Scene
    scene = NodalScene()
    scene.setSceneRect(QRect(-600, -250, 1200, 700))

    # Load
    document = persistance.document_from_file('../scenes/scene.yml')
    scene.from_document(document)

    # View
    view = NodalView()
    view.setScene(scene)
    view.resize(1280, 720)
    view.show()

    # Exec
    app.exec_()

    # Save Scene
    document = scene.as_document()
    persistance.document_to_file(document, '../scenes/scene.yml')
