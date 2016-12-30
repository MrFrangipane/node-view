import copy
from nodepyside import NodePySide  # Temporary, for auto-completion

DEFAULT_NODE_COLOR = (.25, .75, .25)


class Node(object):

    def __init__(self, name, caption, parent_scene=None, implementation_class=NodePySide):
        # Init Members
        self.name = name
        self.caption = caption
        self.color = DEFAULT_NODE_COLOR
        self.is_resizable = False
        self.input_slots = list()
        self.output_slots = list()
        self.position = (0, 0)
        self.size = (0, 0)
        self.is_selected = False
        self.zvalue = 2
        self.edges = []
        self.parent_scene = parent_scene  # PySide Related !!
        # Create Delegate
        self.implementation = implementation_class(self)
        self.implementation.setZValue(self.zvalue)

    # Setters
    def set_inputs(self, inputs):
        # Update Member with fresh copies of inputs
        self.input_slots = copy.deepcopy(inputs)
        # Register as parent Node
        for input_ in self.input_slots:
            input_.parent_node = self
        # Update Delegate
        self.implementation.compute_geometry_values()
        self.implementation.add_input_slots()


    def set_outputs(self, outputs):
        # Update Member with  fresh copies of outputs
        self.output_slots = copy.deepcopy(outputs)
        # Register as parent Node
        for output in self.output_slots:
            output.parent_node = self
        self.implementation.compute_geometry_values()
        self.implementation.add_output_slots()

    def set_zvalue(self, z):
        #
        self.zvalue = z
        self.implementation.setZValue(self.zvalue)

    def set_position(self, x, y):
        # Update Member
        self.position = (x, y)
        # Update Delegate
        self.implementation.update_pos()

    def set_size(self, width, height):
        # If Resizable
        if self.is_resizable:
            # Update Member
            self.size = (width, height)
            # Update Delegate
            self.implementation.width = width
            self.implementation.height = height
            self.implementation.compute_geometry_values()

    def set_color(self, *color_tuple):
        # Update Member
        self.color = color_tuple
        # Update Delegate
        self.implementation.compute_geometry_values()

    def set_resizable(self, is_resizable):
        # Update Member
        self.is_resizable = is_resizable
        # Update Delegate
        self.implementation.compute_geometry_values()

    # Getters
    def input(self, input_name):
        return [input_ for input_ in self.input_slots if input_.name.lower() == input_name.lower()][0]

    def output(self, output_name):
        return [output for output in self.output_slots if output.name.lower() == output_name.lower()][0]

    # Signals
    def input_connected(self, output_slot, input_slot):
        # Warn Scene
        try:
            self.parent_scene.new_edge(output_slot, input_slot)
        # Raise if no scene
        except AttributeError:
            raise RuntimeError("Node must be added to a Scene before changing its connections")

    def output_connected(self, output_slot, input_slot):
        # Warn Scene
        try:
            pass
        # Raise if no scene
        except AttributeError:
            raise RuntimeError("Node must be added to a Scene before changing its connections")
        self.parent_scene.new_edge(output_slot, input_slot)

    def input_disconnected(self, output_slot, input_slot):
        # Warn Scene
        try:
            self.parent_scene.delete_edge(output_slot, input_slot)
        # Raise if no scene
        except AttributeError:
            raise RuntimeError("Node must be added to a Scene before changing its connections")

    def output_disconnected(self, output_slot, input_slot):
        # Warn Scene
        try:
            self.parent_scene.delete_edge(output_slot, input_slot)
        # Raise if no scene
        except AttributeError:
            raise RuntimeError("Node must be added to a Scene before changing its connections")
