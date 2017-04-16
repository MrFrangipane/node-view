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
import nodeview.node
import nodeview.slot
import mock


class TestNode(TestCase):

    def setUp(self):
        nodeview.node.uid = mock.uid
        nodeview.slot.uid = mock.uid

        self.graph = nodeview.Graph("Graph")

    def tearDown(self):
        mock.uid_counter = 0

    def test_create_node_no_params(self):
        node = nodeview.Node("Node", self.graph)

        self.assertEqual("Node", node.name)
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
            graph=self.graph,
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
            graph=self.graph,
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

        node = nodeview.Node(
            name="Node",
            graph=self.graph,
            attributes=attributes
        )

        self.assertEqual(['name', 'caption'], node.attribute_names())
        self.assertEqual("Node One", node['name'])
        self.assertEqual("The One and only", node.get('caption'))

        self.assertRaises(
            nodeview.errors.NodeviewNodeAttributeError,
            node.__getitem__, 'missing-attribute'
        )

        self.assertEqual(
            "default-value",
            node.get('missing-attribute', "default-value")
        )

    def test_to_dict(self):
        attributes = OrderedDict()
        attributes['attr1'] = 'value1'
        attributes['attr2'] = 2.0
        node = nodeview.Node(
            name="Node",
            graph=self.graph,
            inputs=['in1', 'in2'],
            outputs=['out1', 'out2'],
            attributes=attributes
        )
        node.inputs['in1'].max_connection = 1

        node_dict = node.to_dict()

        self.assertEqual(
            {
                "uid": "1",
                "name": "Node",
                "inputs": {
                    "in1": {
                        "uid": "2",
                        "name": "in1",
                        "role": "input",
                        "max_connection": 1,
                        "connected_to": []
                    },
                    "in2": {
                        "uid": "3",
                        "name": "in2",
                        "role": "input",
                        "max_connection": 0,
                        "connected_to": []
                    }
                },
                "outputs": {
                    "out1": {
                        "uid": "4",
                        "name": "out1",
                        "role": "output",
                        "max_connection": 0,
                        "connected_to": []
                    },
                    "out2": {
                        "uid": "5",
                        "name": "out2",
                        "role": "output",
                        "max_connection": 0,
                        "connected_to": []
                    }
                },
                "attributes": {
                    "attr1": "value1",
                    "attr2": 2.0
                }
            },
            node_dict
        )
