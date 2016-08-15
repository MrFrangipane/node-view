from PySide.QtGui import QGraphicsScene
from node import Node
from edge import Edge
from slots import InputSlot, OutputSlot
from edgepyside import ConnectingEdgePySide, FreeEdgePySide


class NodalScene(QGraphicsScene):

    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.nodes = list()

    def add_node(self, node):
        # Register as parent scene
        node.parent_scene = self
        # Add
        self.addItem(node.implementation)
        self.nodes.append(node)

    def new_edge(self, input_slot, output_slot):
        # New Edge
        new_edge = Edge(output_slot, input_slot, parent_scene=self, implementation_class=EdgePySide)
        # Update Slots
        input_slot.connected_edges.append(new_edge)
        output_slot.connected_edges.append(new_edge)
        # Add
        self.addItem(new_edge.implementation)
        # Update
        new_edge.implementation.update()  # Pyside Call !!
        new_edge.implementation.setZValue(0)  # Pyside Call !!

    def node_changed(self, node):  # Should be optimized !!
        # Each Input
        for input_slot in node.input_slots:
            # Each Edge
            for edge in input_slot.connected_edges:
                # Update
                edge.implementation.update()  # Pyside Call !!

        # Each Output
        for output_slot in node.output_slots:
            # Each Edge
            for edge in output_slot.connected_edges:
                # Update
                edge.implementation.update()  # Pyside Call !!

    def input_slot_pressed(self, input_slot):
        print input_slot

    def output_slot_pressed(self, output_slot):
        print output_slot

    # Load / Save
    def as_document(self):
        # Save Scene
        nodes = list()
        connections = list()

        for node in self.nodes:
            # Node Dict
            node_dict = dict()
            node_dict['name'] = node.name
            node_dict['color'] = node.color
            node_dict['caption'] = node.caption
            node_dict['position'] = node.position
            node_dict['size'] = node.size
            node_dict['is_selected'] = node.is_selected
            node_dict['is_resizable'] = node.is_resizable
            node_dict['input_slots'] = list()
            node_dict['output_slots'] = list()

            # Each Input Slot
            for slot in node.input_slots:
                # Slot Dict
                slot_dict = dict()
                slot_dict['name'] = slot.name
                slot_dict['color'] = slot.color
                # Append
                node_dict['input_slots'].append(slot_dict)

            # Each Output Slot
            for slot in node.output_slots:
                # Slot Dict
                slot_dict = dict()
                slot_dict['name'] = slot.name
                slot_dict['color'] = slot.color
                # Append
                node_dict['output_slots'].append(slot_dict)

                # Each Connected Slot
                for target_slot in slot.connected_slots:
                    # Indexes
                    origin_node_id = self.nodes.index(node)
                    origin_slot_id = node.output_slots.index(slot)

                    target_node_id = self.nodes.index(target_slot.parent_node)
                    target_slot_id = target_slot.parent_node.input_slots.index(target_slot)

                    # Store
                    connections.append({
                        'origin_node_id': origin_node_id,
                        'origin_slot_id': origin_slot_id,
                        'target_node_id': target_node_id,
                        'target_slot_id': target_slot_id
                    })

            # Append
            nodes.append(node_dict)

        # Doc
        document = {
            'nodes': nodes,
            'connections': connections
        }

        # Return
        return document

    def from_document(self, document):
        # Each Node
        for node_dict in document['nodes']:
            # Node
            node = Node(node_dict['name'], node_dict['caption'])

            # Inputs
            input_slots = list()
            for input_dict in node_dict['input_slots']:
                # Input Slot
                slot = InputSlot(input_dict['name'], input_dict['color'])
                # Append
                input_slots.append(slot)
            # Set
            node.set_inputs(input_slots)

            # Outputs
            output_slots = list()
            for output_dict in node_dict['output_slots']:
                # Input Slot
                slot = OutputSlot(output_dict['name'], output_dict['color'])
                # Append
                output_slots.append(slot)
            # Set
            node.set_outputs(output_slots)

            # Position, Size, Color, Resizable
            node.set_position(*node_dict['position'])
            node.set_resizable(node_dict['is_resizable'])
            node.set_size(node_dict['size'][0], node_dict['size'][1])
            node.set_color(node_dict['color'][0], node_dict['color'][1], node_dict['color'][2])

            # Add
            self.add_node(node)

        # Each Connection
        for connection_dict in document['connections']:
            # Connect
            self.nodes[connection_dict['origin_node_id']].output_slots[connection_dict['origin_slot_id']].connect(
                self.nodes[connection_dict['target_node_id']].input_slots[connection_dict['target_slot_id']]
            )
