import logging
from collections import OrderedDict
from PySide.QtGui import *
from PySide.QtCore import *
from node import Node
from edge import Edge
from slots import InputSlot, OutputSlot
from edgepyside import ConnectingEdgePySide, FreeEdgePySide
from nodepyside import NodePySide


class NodalScene(QGraphicsScene):
    def __init__(self, parent=None):
        """
        holder for manage graphicsitem, node, slot, backdrop...
        :param parent:
        """
        QGraphicsScene.__init__(self, parent)
        #attributes
        #nodes listes
        self.nodes = list()
        #edges listes
        self.edges = dict()
        #slot handler
        self._source_slot = None
        #drawing edge bool for visibility or not
        self._is_drawing_edge = False
        #free edge object (drawing edge)
        self._drawing_edge = FreeEdgePySide()
        self._drawing_edge.setVisible(False)
        self._drawing_edge.setZValue(len(self.items()))
        self.addItem(self._drawing_edge)
        #mouse pos handler
        self._mouse_previous_position = QPoint(0, 0)



    def add_node(self, node):
        """
        Add a node to th scene
        :param node: node as Node object
        :type node: Node
        :return: None
        """
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
        """
        Create a new edge connection between two slots.
        :param input_slot: input slot
        :type input_slot: InputSlot
        :param output_slot: output slot to connect
        :type output_slot: OutputSlot
        :return: Edge
        """
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
        #Return edge object
        return new_edge

    def delete_edge(self, input_slot, output_slot):
        """
        rdelete an edge between two slots
        :param input_slot: input slot
        :type input_slot: InputSlot
        :param output_slot: output slot to connect
        :type output_slot: OutputSlot
        :return: None
        """
        # Find Edge
        edge = self.edges[output_slot][input_slot]
        # Remove Key
        self.edges[output_slot].pop(input_slot)
        # Remove from Scene
        self.removeItem(edge.implementation)

    def node_changed(self, node):  # Should be optimized !!
        """
        Update all edges of nodes in scene
        :param node: edge's node to update
        :return: None
        """
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
        """
        start to draw an freeedge with drag
        :param input_slot: the input slot clicked
        :return: None
        """
        # If not Drawing
        if not self._is_drawing_edge:
            # Store Slot
            self._source_slot = input_slot
            # Enter Drawing
            self._enter_drawing_edge()

    def output_slot_pressed(self, output_slot):
        """
        start to draw an freeedge with drag
        :param output_slot: the output slot clicked
        :return: None
        """
        # If not Drawing
        if not self._is_drawing_edge:
            # Store Slot
            self._source_slot = output_slot
            # Enter Drawing
            self._enter_drawing_edge()

    def delete_pressed(self):
        """
        def call by del keys for  delete selected edges
        :return: None
        """
        # Each Item
        edges = [item for item in self.selectedItems() if isinstance(item, ConnectingEdgePySide)]
        for edge in edges:
            # Disconnect
            self.del_edge(edge)

    def del_edge(self, edge):
        """
        delete edges
        :param edge: Edge
        :return: None
        """
        # Disconnect
        origin_slot = edge.edge.origin_slot
        target_slot = edge.edge.target_slot
        origin_slot.disconnect(target_slot)

    # Edge Drawing
    def _enter_drawing_edge(self):
        """
        initialise the free drawing edge, set pos and pass visibility
        :return: None
        """
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
        """
        disabled the free drawing edge, by pass visibility False
        :return:
        """
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
        #Each Connection
        for connection_dict in document['connections']:
            # Connect
            source_node = self.nodes[connection_dict['origin_node_id']]
            target_node = self.nodes[connection_dict['target_node_id']]
            source_slot = source_node.output_slots[connection_dict['origin_slot_id']]
            target_slot = target_node.input_slots[connection_dict['target_slot_id']]
            source_slot.connect(target_slot)

    def _select_arbo_top_in(self, nodepyside):
        """
        recursive def from input for select all branche and put it on front
        :param nodepyside: Selected node
        :type nodepyside: NodePySide
        :return: None
        """
        try:
            for slot in nodepyside.node.input_slots:
                for input_slot in slot.connected_slots:
                    input_slot.parent_node.implementation.setZValue(len(self.items()))
                    self._select_arbo_top_in(input_slot.parent_node.implementation)
        except RuntimeError:
            print 'Loop...'
            return

    def _select_arbo_top_out(self, nodepyside):
        """
        recursive def from output for select all branche and put it on front
        :param nodepyside: Selected node
        :type nodepyside: NodePySide
        :return: None
        """
        try:
            for slot in nodepyside.node.output_slots:
                for output_slot in slot.connected_slots:
                    output_slot.parent_node.implementation.setZValue(len(self.items()))
                    self._select_arbo_top_out(output_slot.parent_node.implementation)
        except RuntimeError:
            print 'Loop...'
            return
    #PySide
    # Events
    def dragLeaveEvent(self, event):
        super(NodalScene, self).dragLeaveEvent(event)
        #leave free edge when drop or drag out
        self._leave_drawing_edge()

    def dropEvent(self, event):
        super(NodalScene, self).dropEvent(event)
        #leave free edge when drop or drag out
        self._leave_drawing_edge()

    def dragMoveEvent(self, event):
        super(NodalScene, self).dragMoveEvent(event)
        #create the free drawing edge
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

    def mousePressEvent(self, event):
        super(NodalScene, self).mousePressEvent(event)
        ##ZValue gestion
        #init all zvalue
        for item in self.items():
            if isinstance(item, NodePySide):
                item.setZValue(1)
        #on top all selected node
        item_at = self.itemAt(event.scenePos())
        if isinstance(item_at, NodePySide):
            item_at.setZValue(len(self.items())+1)
            self._select_arbo_top_in(item_at)
            self._select_arbo_top_out(item_at)
