import logging
from collections import OrderedDict
from PySide.QtGui import QGraphicsScene
from PySide.QtCore import QPoint
from node import Node
from edge import Edge
from slots import InputSlot, OutputSlot
from edgepyside import ConnectingEdgePySide, FreeEdgePySide


class NodalScene(QGraphicsScene):

    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.nodes = list()
        self.edges = dict()

        self._source_slot = None

        self._is_drawing_edge = False

        self._drawing_edge = FreeEdgePySide()
        self._drawing_edge.setVisible(False)
        self._drawing_edge.setZValue(len(self.items()))
        self.addItem(self._drawing_edge)

        self._mouse_previous_position = QPoint(0, 0)

    def add_node(self, node):
        # Register as parent scene
        node.parent_scene = self
        # Add
        self.addItem(node.implementation)
        self.nodes.append(node)
        # Log
        logging.info("Adding Node '{node_name}' to Scene at {node_position}".format(
            node_name=node.name,
            node_caption=node.caption,
            node_position=node.position
        ))

    def new_edge(self, input_slot, output_slot):
        # New Edge
        new_edge = Edge(output_slot, input_slot, parent_scene=self, implementation_class=ConnectingEdgePySide)
        # Update Slots
        input_slot.connected_edges.append(new_edge)
        output_slot.connected_edges.append(new_edge)
        # Add
        self.addItem(new_edge.implementation)
        if output_slot not in self.edges.keys():
            self.edges[output_slot] = {input_slot: new_edge}
        else:
            self.edges[output_slot][input_slot] = new_edge
        # Updat
        new_edge.implementation.setZValue(0)  # Pyside Call !!
        new_edge.implementation.update()  # Pyside Call !!

    def delete_edge(self, input_slot, output_slot):
        # Find Edge
        edge = self.edges[output_slot][input_slot]
        # Remove Key
        self.edges[output_slot].pop(input_slot)
        # Remove from Scene
        self.removeItem(edge.implementation)

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
        # If not Drawing
        if not self._is_drawing_edge:
            # Store Slot
            self._source_slot = input_slot
            # Enter Drawing
            self._enter_drawing_edge()

        # If Drawing
        else:
            # If Source is output
            if isinstance(self._source_slot, OutputSlot):
                # Connect
                self._source_slot.connect(input_slot)
            # Stop Drawing
            self._leave_drawing_edge()

    def output_slot_pressed(self, output_slot):
        # If not Drawing
        if not self._is_drawing_edge:
            # Store Slot
            self._source_slot = output_slot
            # Enter Drawing
            self._enter_drawing_edge()

            # If Drawing
        else:
            # If Source is output
            if isinstance(self._source_slot, InputSlot):
                # Connect
                output_slot.connect(self._source_slot)
            # Stop Drawing
            self._leave_drawing_edge()

    def delete_pressed(self):
        # Each Item
        edges = [item for item in self.selectedItems() if isinstance(item, ConnectingEdgePySide)]
        for edge in edges:
            # Disconnect
            origin_slot = edge.edge.origin_slot
            target_slot = edge.edge.target_slot
            origin_slot.disconnect(target_slot)

    # Edge Drawing
    def _enter_drawing_edge(self):
        # Init Rectangle
        self._drawing_edge.set_rectangle(
            (self._mouse_previous_position.x(), self._mouse_previous_position.y()),
            (self._mouse_previous_position.x(), self._mouse_previous_position.y())
        )
        # Show Drawing Edge
        self._drawing_edge.setZValue(len(self.items()))
        self._drawing_edge.setVisible(True)
        # Set member
        self._is_drawing_edge = True

    def _leave_drawing_edge(self):
        # Hide Drawing Edge
        self._drawing_edge.setVisible(False)
        # Set member
        self._is_drawing_edge = False

    # Load / Save
    def as_document(self):
        # Save Scene
        nodes = list()
        connections = list()

        for node in self.nodes:
            # Node Dict
            node_dict = OrderedDict()
            node_dict['name'] = node.name
            node_dict['caption'] = node.caption
            node_dict['color'] = node.color
            node_dict['position'] = node.position
            node_dict['size'] = node.size
            node_dict['is_selected'] = node.is_selected
            node_dict['is_resizable'] = node.is_resizable
            node_dict['input_slots'] = list()
            node_dict['output_slots'] = list()

            # Each Input Slot
            for slot in node.input_slots:
                # Slot Dict
                slot_dict = OrderedDict()
                slot_dict['name'] = slot.name
                slot_dict['color'] = slot.color
                # Append
                node_dict['input_slots'].append(slot_dict)

            # Each Output Slot
            for slot in node.output_slots:
                # Slot Dict
                slot_dict = OrderedDict()
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
        z = 2
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

            # Position, Size, Color, Resizable, zvalue
            node.set_position(*node_dict['position'])
            node.set_resizable(node_dict['is_resizable'])
            node.set_size(node_dict['size'][0], node_dict['size'][1])
            node.set_color(node_dict['color'][0], node_dict['color'][1], node_dict['color'][2])
            # Add
            self.add_node(node)
        # Each Connection
        # for connection_dict in document['connections']:
        #     # Connect
        #     source_node = self.nodes[connection_dict['origin_node_id']]
        #     target_node = self.nodes[connection_dict['target_node_id']]
        #     source_slot = source_node.output_slots[connection_dict['origin_slot_id']]
        #     target_slot = target_node.input_slots[connection_dict['target_slot_id']]
        #     source_slot.connect(target_slot)

    # Events
    def mousePressEvent(self, event):
        # Store mouse pos
        self._mouse_previous_position = event.scenePos()
        for item in self.items():
            item.setZValue(0)
        # Forward
        QGraphicsScene.mousePressEvent(self, event)

    def dragLeaveEvent(self, event):
        super(NodalScene, self).dragLeaveEvent(event)
        self.scene()._drawing_edge.set_rectangle(self.dot_pos, (event.scenePos().x(), event.scenePos().y()))

    def dropEvent(self, event):
        super(NodalScene, self).dropEvent(event)
        self._leave_drawing_edge()

    def dragMoveEvent(self, event):
        super(NodalScene, self).dragMoveEvent(event)
        if self._is_drawing_edge:
            # If input to output
            if isinstance(self._source_slot, OutputSlot):
                origin = (event.scenePos().x(), event.scenePos().y())
                target = (self._mouse_previous_position.x(), self._mouse_previous_position.y())
            # Output to input
            else:
                origin = (self._mouse_previous_position.x(), self._mouse_previous_position.y())
                target = (event.scenePos().x(), event.scenePos().y())
        self._drawing_edge.set_rectangle(origin, target)