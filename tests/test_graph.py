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
import nodeview
import nodeview.graph
import nodeview.node
import nodeview.slot
import mock


GRAPH_DICT = {
    "name": "Graph",
    "nodes": [
        {
            "uid": "1",
            "name": "Node A",
            "inputs": {
                "in": {
                    "uid": "2",
                    "name": "in",
                    "role": "input",
                    "attributes": {},
                    "max_connection": 0,
                    "connected_to": ["4", "6"]
                }
            },
            "outputs": {},
            "attributes": {}
        },
        {
            "uid": "3",
            "name": "Node B",
            "inputs": {},
            "outputs": {
                "out": {
                    "uid": "4",
                    "name": "out",
                    "role": "output",
                    "attributes": {},
                    "max_connection": 0,
                    "connected_to": ["2"]
                }
            },
            "attributes": {}
        },
        {
            "uid": "5",
            "name": "Node C",
            "inputs": {},
            "outputs": {
                "out": {
                    "uid": "6",
                    "name": "out",
                    "role": "output",
                    "attributes": {},
                    "max_connection": 0,
                    "connected_to": ["2"]
                }
            },
            "attributes": {}
        }
    ]
}


class TestGraph(TestCase):

    def setUp(self):
        nodeview.graph.uid = mock.uid
        nodeview.node.uid = mock.uid
        nodeview.slot.uid = mock.uid

        self.graph = nodeview.Graph('Graph')

        self.node_a = nodeview.Node('Node A', self.graph, inputs=['in'])
        self.node_b = nodeview.Node('Node B', self.graph, outputs=['out'])
        self.node_c = nodeview.Node('Node C', self.graph, outputs=['out'])

        self.node_b.outputs['out'].connect(self.node_a.inputs['in'])
        self.node_c.outputs['out'].connect(self.node_a.inputs['in'])

    def tearDown(self):
        mock.uid_counter = 0

    def test_to_dict(self):
        graph_dict = self.graph.to_dict()

        self.assertEqual(
            GRAPH_DICT,
            graph_dict
        )

    def test_from_dict(self):
        graph = nodeview.Graph.from_dict(GRAPH_DICT)
        # import json
        # print json.dumps(graph.to_dict(), indent=4)

        self.assertEqual(
            GRAPH_DICT,
            graph.to_dict()
        )
