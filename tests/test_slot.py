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
import nodeview.slot
import mock


class TestSlot(TestCase):

    def setUp(self):
        nodeview.slot.uid = mock.uid
        graph = nodeview.Graph("Graph")

        self.node_a = nodeview.Node("Node A", graph, inputs=["input1"])
        self.node_b = nodeview.Node("Node B", graph, outputs=["output1"])
        self.node_c = nodeview.Node(
            name="Node C",
            graph=graph,
            inputs=["input1"],
            outputs=["output1"]
        )

        self.slot_a_in = self.node_a.inputs['input1']
        self.slot_b_out = self.node_b.outputs['output1']
        self.slot_c_in = self.node_c.inputs['input1']
        self.slot_c_out = self.node_c.outputs['output1']

    def tearDown(self):
        mock.uid_counter = 0

    def test_connect_from_in_to_out(self):
        self.slot_b_out.connect(self.slot_a_in)

        self.assertEqual(
            [self.slot_b_out],
            self.node_a.inputs['input1'].connected
        )

        self.assertEqual(
            [self.slot_a_in],
            self.node_b.outputs['output1'].connected
        )

    def test_connect_from_out_to_in(self):
        self.slot_b_out.connect(self.slot_a_in)

        self.assertEqual(
            [self.slot_a_in],
            self.node_b.outputs['output1'].connected
        )

        self.assertEqual(
            [self.slot_b_out],
            self.node_a.inputs['input1'].connected
        )

    def test_connect_from_in_to_in(self):
        self.assertRaises(
            nodeview.errors.NodeviewConnectionRoleError,
            self.slot_a_in.connect,
            self.slot_c_in
        )

    def test_connect_from_out_to_out(self):
        self.assertRaises(
            nodeview.errors.NodeviewConnectionRoleError,
            self.slot_b_out.connect,
            self.slot_c_out
        )

    def test_connect_2_outs_to_1_in(self):
        self.slot_b_out.connect(self.slot_a_in)
        self.slot_c_out.connect(self.slot_a_in)

        self.assertEqual(
            [self.node_b.outputs['output1'], self.node_c.outputs['output1']],
            self.slot_a_in.connected
        )

    def test_disconnect_1(self):
        self.slot_b_out.connect(self.slot_a_in)
        self.slot_a_in.disconnect(self.slot_b_out)

        self.assertEqual(
            list(),
            self.slot_a_in.connected
        )

        self.assertEqual(
            list(),
            self.slot_b_out.connected
        )

    def test_disconnect_2(self):
        self.slot_b_out.connect(self.slot_a_in)
        self.slot_c_out.connect(self.slot_a_in)

        self.slot_a_in.disconnect(self.slot_b_out)

        self.assertEqual(
            [self.slot_c_out],
            self.slot_a_in.connected
        )

        self.assertEqual(
            list(),
            self.slot_b_out.connected
        )

        self.assertEqual(
            [self.slot_a_in],
            self.slot_c_out.connected
        )

    def test_clear_slot_1_to_many(self):
        self.slot_b_out.connect(self.slot_a_in)
        self.slot_c_out.connect(self.slot_a_in)

        self.slot_a_in.clear()

        self.assertEqual(
            list(),
            self.slot_a_in.connected
        )

        self.assertEqual(
            list(),
            self.slot_b_out.connected
        )

        self.assertEqual(
            list(),
            self.slot_c_out.connected
        )

    def test_max_connection(self):
        self.slot_a_in.max_connection = 1
        self.slot_b_out.connect(self.slot_a_in)

        self.assertRaises(
            nodeview.errors.NodeviewConnectionLimitError,
            self.slot_c_out.connect, self.slot_a_in
        )

    def test_to_dict_input(self):
        self.slot_a_in.max_connection = 5
        self.slot_b_out.connect(self.slot_a_in)
        slot_dict = self.slot_a_in.to_dict()

        self.assertEqual(
            {
                "uid": "2",
                "name": "input1",
                "role": "input",
                "max_connection": 5,
                "connected_to": ["4"]
            },
            slot_dict
        )

    def test_to_dict_output(self):
        self.slot_b_out.connect(self.slot_a_in)
        slot_dict = self.slot_b_out.to_dict()

        self.assertEqual(
            {
                "uid": "4",
                "name": "output1",
                "role": "output",
                "max_connection": 0,
                "connected_to": ["2"]
            },
            slot_dict
        )
