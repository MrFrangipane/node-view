import logging

DEFAULT_INPUT_COLOR = (.05, .95, .95)
DEFAULT_OUTPUT_COLOR = (.95, .05, .95)


class AbstractSlot(object):

    def __init__(self, name, color=DEFAULT_INPUT_COLOR, parent_node=None):
        # Init Members
        self.parent_node = parent_node
        self.name = name.capitalize()
        self.color = color
        self.position = (0, 0)
        self.connected_slots = list()
        self.connected_edges = list()
        self.dot_pos = []
        self.connect_data = ''

        self.connect_to = ''
        self.path_name = ''

        self.implementation = None

    def connect(self, slot):
        raise NotImplementedError

    def disconnect(self, slot):
        raise NotImplementedError


class InputSlot(AbstractSlot):

    def connect(self, output_slot):
        # Assert Type
        assert isinstance(output_slot, OutputSlot), "Connect Input to output only !"
        # If already connected
        if output_slot in self.connected_slots:
            return
        # Update Members
        self.connected_slots.append(output_slot)
        output_slot.connected_slots.append(self)
        # Warn Parent Nodes
        self.parent_node.input_connected(output_slot, self)
        # Log
        logging.info('Connecting {source_node}.{source_slot} ---> {target_node}.{target_slot}'.format(
            source_node=output_slot.parent_node.name,
            source_slot=output_slot.name,
            target_node=self.parent_node.name,
            target_slot=self.name
        ))

    def disconnect(self, output_slot):
        # If present
        if output_slot in self.connected_slots:
            # Update Members
            self.connected_slots.remove(output_slot)
            output_slot.connected_slots.remove(self)
            # Warn Parent Node
            self.parent_node.input_disconnected(output_slot, self)
        # Log
        logging.info('Disconnecting {source_node}.{source_slot} -X-> {target_node}.{target_slot}'.format(
            source_node=output_slot.parent_node.name,
            source_slot=output_slot.name,
            target_node=self.parent_node.name,
            target_slot=self.name
        ))


class OutputSlot(AbstractSlot):

    def connect(self, input_slot):
        # Assert Type
        assert isinstance(input_slot, InputSlot), "Connect Output to input only !"
        # If already connected
        if input_slot in self.connected_slots:
            return
        # Update Members
        self.connected_slots.append(input_slot)
        input_slot.connected_slots.append(self)
        # Warn Parent Nodes
        self.parent_node.output_connected(self, input_slot)
        # Log
        logging.info('Connecting {source_node}.{source_slot} ---> {target_node}.{target_slot}'.format(
            source_node=self.parent_node.name,
            source_slot=self.name,
            target_node=input_slot.parent_node.name,
            target_slot=input_slot.name
        ))

    def disconnect(self, input_slot):
        # If present
        if input_slot in self.connected_slots:
            # Update Members
            self.connected_slots.remove(input_slot)
            input_slot.connected_slots.remove(self)
            # Warn Parent Node
            self.parent_node.input_disconnected(self, input_slot)
        # Log
        logging.info('Disconnecting {source_node}.{source_slot} -X-> {target_node}.{target_slot}'.format(
            source_node=self.parent_node.name,
            source_slot=self.name,
            target_node=input_slot.parent_node.name,
            target_slot=input_slot.name
        ))
