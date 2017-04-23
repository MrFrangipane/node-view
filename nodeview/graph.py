"""
Nodeview. A PySide nodal view
    Copyright (C) 2017  Valentin Moriceau - moriceau.v@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from collections import OrderedDict
from node import Node


class Graph(object):
    """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna 
    aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
    """

    def __init__(self, name):
        """
        Create a new graph
        :param name: Valid string 
        """
        self.name = name
        self.nodes = list()

    def add_node(self, node):
        """
        Add a valid Node to the graph
        :param node: Valid Node
        :return: None
        """
        self.nodes.append(node)

    def to_dict(self):
        """
        Represents Graph to a serializable dict
        :return: dict
        """
        graph_dict = OrderedDict()
        graph_dict['name'] = self.name
        graph_dict['nodes'] = [node.to_dict() for node in self.nodes]

        return graph_dict

    @staticmethod
    def from_dict(graph_dict):
        """
        Recreates Graph from dict 
        :return: Graph
        """
        graph = Graph(graph_dict['name'])
        input_slots = dict()
        output_slots = dict()


        for node_dict in graph_dict['nodes']:
            input_names = node_dict['inputs'].keys()
            output_names = node_dict['outputs'].keys()

            node = Node(
                name=node_dict['name'],
                graph=graph,
                inputs=input_names,
                outputs=output_names,
                attributes=node_dict['attributes']
            )

            node.uid = node_dict['uid']

            for slot_name, slot in node.inputs.items():
                slot_dict = node_dict['inputs'][slot_name]
                slot.uid = slot_dict['uid']
                slot.max_connection = slot_dict['max_connection']
                slot.attributes = slot_dict['attributes']

                input_slots[slot.uid] = slot

            for slot_name, slot in node.outputs.items():
                slot_dict = node_dict['outputs'][slot_name]
                slot.uid = slot_dict['uid']
                slot.max_connection = slot_dict['max_connection']
                slot.attributes = slot_dict['attributes']

                slot.connected_to = slot_dict['connected_to']

                output_slots[slot.uid] = slot

        for output_slot_uid, output_slot in output_slots.items():
            for input_slot_uid in output_slot.connected_to:
                input_slot = input_slots[input_slot_uid]
                output_slot.connect(input_slot)

            del(output_slot.connected_to)

        return graph
