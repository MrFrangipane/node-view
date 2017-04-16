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
from slot import Slot
from errors import NodeviewAttributeError


class Node(object):

    def __init__(self, name, graph=None, inputs=None, outputs=None, attributes=None):
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
            raise NodeviewAttributeError(self, item)

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
        return self.attributes.keys()

    def get(self, item, default=None):
        try:
            return self[item]
        except NodeviewAttributeError:
            return default
