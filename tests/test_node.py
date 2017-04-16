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
from unittest import TestCase
from collections import OrderedDict
import nodeview


class TestNode(TestCase):

    def setUp(self):
        self.graph = nodeview.Graph()

    def test_create_node_no_params(self):
        node = nodeview.Node("Node")

        self.assertEqual("Node", node.name)
        self.assertEqual(list(), self.graph.nodes)
        self.assertEqual(dict(), node.inputs)
        self.assertEqual(dict(), node.outputs)
        self.assertEqual(dict(), node.attributes)

    def test_create_node_in_graph(self):
        node = nodeview.Node("Node", graph=self.graph)

        self.assertEqual(
            [node],
            self.graph.nodes
        )

    def test_create_node_inputs(self):
        node = nodeview.Node(
            name="Node",
            inputs=['input 1', 'input 2']
        )

        self.assertEqual(2, len(node.inputs))
        self.assertEqual(['input 1', 'input 2'], node.inputs.keys())

        slot = node.inputs['input 1']
        self.assertIsInstance(slot, nodeview.Slot)
        self.assertEqual("input 1", slot.name)
        self.assertEqual(nodeview.Slot.INPUT, slot.role)
        self.assertEqual(node, slot._parent_node)

    def test_create_node_outputs(self):
        node = nodeview.Node(
            name="Node",
            outputs=['output 1', 'output 2']
        )

        self.assertEqual(2, len(node.outputs))
        self.assertEqual(['output 1', 'output 2'], node.outputs.keys())

        slot = node.outputs['output 1']
        self.assertIsInstance(slot, nodeview.Slot)
        self.assertEqual("output 1", slot.name)
        self.assertEqual(nodeview.Slot.OUTPUT, slot.role)
        self.assertEqual(node, slot._parent_node)

    def test_create_node_attributes(self):
        attributes = OrderedDict()
        attributes['name'] = "Node One"
        attributes['caption'] = "The One and only"

        node = nodeview.Node(name="Node", attributes=attributes)

        self.assertEqual(['name', 'caption'], node.attribute_names())
        self.assertEqual("Node One", node['name'])
        self.assertEqual("The One and only", node.get('caption'))

        self.assertRaises(
            nodeview.errors.NodeviewAttributeError,
            node.__getitem__, 'missing-attribute'
        )

        self.assertEqual(
            "default-value",
            node.get('missing-attribute', "default-value")
        )
