import logging

DEFAULT_INPUT_COLOR = (.05, .95, .95)
DEFAULT_OUTPUT_COLOR = (.95, .05, .95)


class AbstractSlot(object):
    def __init__(self, name, color=DEFAULT_INPUT_COLOR, parent_node=None):
        """
        Base class for slot object, slot hold methode for connect and disconnect node
        :param name: slot's name, also visible in node ui
        :param color: slot's color
        :param parent_node: parent node
        """
        # Init Members
        self.parent_node = parent_node
        self.name = name.capitalize()
        self.color = color
        self.position = (0, 0)
        self.connected_slots = list()
        self.connected_edges = list()
        self.connect_data = ''
        #path name of the connect to slot
        self.connect_to = ''
        #path name of this slot
        self.path_name = ''
        #implementation SlotPySide
        self.implementation = None

    def connect(self, slot):
        raise NotImplementedError

    def disconnect(self, slot):
        raise NotImplementedError

class InputSlot(AbstractSlot):
    def connect(self, output_slot):
        """
        connect the output_slot to this input slot
        :param output_slot: output slot
        :return: None
        """
        # Assert Type
        assert isinstance(output_slot, OutputSlot), "Connect Input to output only !"
        #loop breaker
        def sss(node):
            sss.looped = None
            for slot in node.input_slots:
                if len(slot.connected_slots) == 0:
                    continue
                for output_slot in slot.connected_slots:
                    print output_slot.parent_node.name
                    if output_slot.parent_node == self.parent_node:
                        sss.looped = True
                    else:
                        sss.looped = False
                        sss(output_slot.parent_node)

        sss(output_slot.parent_node)
        if sss.looped:
            print 'looped'
            return
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
        """
        Disconnect the output slot to this slot
        :param output_slot:
        :return:
        """
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
        """
        connect the input_slot to this output slot
        :param output_slot: output slot
        :return: None
        """
        print 'out caca'
        # Assert Type
        assert isinstance(input_slot, InputSlot), "Connect Output to input only !"
        #loop breaker
        def sss(node):
            sss.looped = None
            for slot in node.output_slots:
                if len(slot.connected_slots) == 0:
                    continue
                for output_slot in slot.connected_slots:
                    print output_slot.parent_node.name
                    if output_slot.parent_node == self.parent_node:
                        sss.looped = True
                    else:
                        sss.looped = False
                        sss(output_slot.parent_node)

        sss(input_slot.parent_node)
        if sss.looped:
            print 'looped'
            return
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
        """
        Disconnect the input slot to this slot
        :param output_slot:
        :return:
        """
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
