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
from uuid import uuid4 as uid
from collections import OrderedDict
from slot import Slot
from errors import NodeviewNodeAttributeError


class Node(object):
    """
    Class holding data solts bmofjze zelze ze zefze zef ze
    
    f zef zofzefizfoizefze fzefijzef z zef z
    
    ef zefzef zfzef zfeghty nj uj-j rgd trh 
    
    ergerg e
    
    ```python
    example = Node()
    example.connect(a, b)
    ```
    """

    def __init__(self, name, graph, inputs=None, outputs=None, attributes=None):
        """
        Constructor
        :param name: Valid string 
        :param graph: Parent Graph
        :param inputs: List of input names
        :param outputs: List of output names
        :param attributes: **Serializable** user attributes (OrderedDict recomanded)
        """
        self.uid = str(uid())
        self.name = name
        self.graph = graph
        self.inputs = OrderedDict()
        self.outputs = OrderedDict()
        self.attributes = OrderedDict()

        if self.graph is not None:
            self.graph.add_node(self)

        if inputs is not None:
            self._init_inputs(inputs)

        if outputs is not None:
            self._init_outputs(outputs)

        if attributes is not None:
            self.attributes = attributes

    def __getitem__(self, item):
        try:
            return self.attributes[item]
        except KeyError:
            raise NodeviewNodeAttributeError(self, item)

    def _init_inputs(self, input_names):
        for input_name in input_names:
            slot = Slot(
                name=input_name,
                role=Slot.INPUT,
                parent_node=self
            )
            self.inputs[input_name] = slot

    def _init_outputs(self, output_names):
        for output_name in output_names:
            slot = Slot(
                name=output_name,
                role=Slot.OUTPUT,
                parent_node=self
            )
            self.outputs[output_name] = slot

    def attribute_names(self):
        """
        List attributes names
        :return: List of strings
        """
        return self.attributes.keys()

    def get(self, item, default=None):
        """
        Similar to dict.get()
        :param item: Name of the attribute 
        :param default: Default value if attribute missing
        :return: Value
        """
        try:
            return self[item]
        except NodeviewNodeAttributeError:
            return default

    def to_dict(self):
        """
        Represents Node to a serializable dict
        :return: dict
        """
        node_dict = OrderedDict()
        node_dict['uid'] = self.uid
        node_dict['name'] = self.name

        inputs = OrderedDict()
        for input_name, input_slot in self.inputs.items():
            inputs[input_name] = input_slot.to_dict()
        node_dict['inputs'] = inputs

        outputs = OrderedDict()
        for output_name, output_slot in self.outputs.items():
            outputs[output_name] = output_slot.to_dict()
        node_dict['outputs'] = outputs

        node_dict['attributes'] = self.attributes

        return node_dict
