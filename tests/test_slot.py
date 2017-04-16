from unittest import TestCase
import nodeview


class TestSlot(TestCase):

    def setUp(self):
        self.node_a = nodeview.Node("Node A", inputs=["input1"])
        self.node_b = nodeview.Node("Node B", outputs=["output1"])
        self.node_c = nodeview.Node(
            name="Node C",
            inputs=["input1"],
            outputs=["output1"]
        )

        self.slot_a_in = self.node_a.inputs['input1']
        self.slot_b_out = self.node_b.outputs['output1']
        self.slot_c_in = self.node_c.inputs['input1']
        self.slot_c_out = self.node_c.outputs['output1']

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
            nodeview.errors.NodeviewConnectionError,
            self.slot_a_in.connect,
            self.slot_c_in
        )

    def test_connect_from_out_to_out(self):
        self.assertRaises(
            nodeview.errors.NodeviewConnectionError,
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
