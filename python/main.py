import json
import yaml
from view import NodalView
from scene import NodalScene
from node import Node
from slots import InputSlot, OutputSlot


def _node_1(name, caption):
    # Node 1
    new_node = Node(name, caption)
    # Inputs
    new_node.set_inputs([
        InputSlot('diffuse', (.95, .95, .05)),
        InputSlot('reflection', (.95, .95, .05)),
        InputSlot('refraction', (.95, .95, .05)),
        InputSlot('bump'),
        InputSlot('opacity', (.95, .95, .05)),
        InputSlot('displace')
    ])
    # Outputs
    new_node.set_outputs([
        OutputSlot('out')
    ])
    # Return
    return new_node


def _node_2(name, caption):
    # Node 1
    new_node = Node(name, caption)
    # Inputs
    new_node.set_inputs([
        InputSlot('red', (.9, .1, .1)),
        InputSlot('green', (.1, .9, .1)),
        InputSlot('blue', (.1, .1, .9)),
        InputSlot('alpha', (.8, .8, .8))
    ])
    # Outputs
    new_node.set_outputs([
        OutputSlot('chroma'),
        OutputSlot('luma')
    ])
    # Return
    return new_node


def populate(scene):
    node_10 = _node_1("Rocks", "Shader des familles")
    node_10.set_position(-250, -130)
    node_10.set_color(.75, .5, .25)

    node_11 = _node_1("Snow", "Chantale Goyave")
    node_11.set_position(-250, 130)
    node_11.set_color(.5, .5, .95)

    node_20 = _node_2("Convert 1", "Pierre Cadran")
    node_20.set_color(.95, .25, .25)

    node_21 = _node_2("Convert 2", "")
    node_21.set_position(250, 0)

    backdrop = Node("Backdrop", "Range des trucs ici")
    backdrop.set_color(0, 0, 0)
    backdrop.set_resizable(True)
    backdrop.set_position(-300, -200)
    backdrop.set_size(800, 600)

    scene.add_node(backdrop)
    scene.add_node(node_10)
    scene.add_node(node_11)
    scene.add_node(node_20)
    scene.add_node(node_21)

    node_10.output("out").connect(node_11.input('diffuse'))

    node_11.output("out").connect(node_20.input('red'))
    node_11.output("out").connect(node_20.input('green'))
    node_11.output("out").connect(node_20.input('blue'))

    node_11.output("out").connect(node_21.input('red'))
    node_11.output("out").connect(node_21.input('blue'))

    node_20.output("chroma").connect(node_21.input('green'))
    node_20.output("luma").connect(node_21.input('alpha'))


if __name__ == '__main__':
    import edgepyside
    import nodepyside

    global scene

    def _redraw():
        global scene
        for item in scene.items():
            try:
                item.compute_geometry_values()
            except:
                pass
            item.update()

    def _slider_grad_length(value):
        print value
        edgepyside.GRADIENT_LENGTH = value
        _redraw()

    def _slider_slot_size(value):
        print value
        nodepyside.SLOT_RADIUS = value
        _redraw()

    def _slider_row_height(value):
        print value
        nodepyside.ROW_HEIGHT = value
        _redraw()


    def _slider_edge_tangent(value):
        print value
        edgepyside.EDGE_TANGENT = value
        _redraw()

    # Application
    from PySide.QtGui import QApplication, QWidget, QVBoxLayout, QSlider
    from PySide.QtCore import QRect, Qt
    app = QApplication([])

    # Scene
    scene = NodalScene()
    scene.setSceneRect(QRect(-600, -250, 1200, 700))

    # Load
    try:
        with open('./scene.yml') as scene_file:
            document_yml = scene_file.read()
        document = yaml.load(document_yml)
        scene.from_document(document)
    except Exception, e:
        print e.message
        populate(scene)

    # View
    view = NodalView()
    view.setScene(scene)

    # Sliders
    slider_grad_length = QSlider(Qt.Horizontal)
    slider_grad_length.valueChanged.connect(_slider_grad_length)

    slider_slot_size = QSlider(Qt.Horizontal)
    slider_slot_size.valueChanged.connect(_slider_slot_size)

    slider_row_height = QSlider(Qt.Horizontal)
    slider_row_height.valueChanged.connect(_slider_row_height)

    slider_edge_tangent = QSlider(Qt.Horizontal)
    slider_edge_tangent.valueChanged.connect(_slider_edge_tangent)

    # Widget
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.addWidget(view)
    layout.addWidget(slider_grad_length)
    layout.addWidget(slider_slot_size)
    layout.addWidget(slider_row_height)
    layout.addWidget(slider_edge_tangent)

    widget.resize(1920, 1080)
    widget.show()

    # Exec
    app.exec_()

    # Save Scene
    document = scene.as_document()
    document_yml = yaml.dump(document, indent=2)
    with open('./scene.yml', 'w+') as scene_file:
        scene_file.write(document_yml)
