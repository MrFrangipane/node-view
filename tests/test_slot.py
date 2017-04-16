from unittest import TestCase
import nodeview


class TestSlot(TestCase):

    def setUp(self):
        self.node_a = nodeview.Node("Node A", inputs=["input1"])
        self.node_b = nodeview.Node("Node B", outputs=["output1"])
        self.node_c = nodeview.Node("Node C", outputs=["output1"])

        self.slot_a = self.node_a.inputs['input1']
        self.slot_b = self.node_b.outputs['output1']
        self.slot_c = self.node_c.outputs['output1']

    def test_connect_from_in_to_out(self):
        self.slot_a.connect(self.slot_b)

        self.assertEqual(
            [self.slot_b],
            self.node_a.inputs['input1'].connected
        )

        self.assertEqual(
            [self.slot_a],
            self.node_b.outputs['output1'].connected
        )

    def test_connect_from_out_to_in(self):
        self.slot_b.connect(self.slot_a)

        self.assertEqual(
            [self.slot_a],
            self.node_b.outputs['output1'].connected
        )

        self.assertEqual(
            [self.slot_b],
            self.node_a.inputs['input1'].connected
        )

    def test_connect_from_in_to_in(self):
        node_a = nodeview.Node("Node A", inputs=['input1'])
        node_b = nodeview.Node("Node B", inputs=['input1'])

        self.assertRaises(
            nodeview.errors.NodeviewConnectionError,
            node_a.inputs['input1'].connect,
            node_b.inputs['input1']
        )

    def test_connect_from_out_to_out(self):
        node_a = nodeview.Node("Node A", outputs=['output1'])
        node_b = nodeview.Node("Node B", outputs=['output1'])

        self.assertRaises(
            nodeview.errors.NodeviewConnectionError,
            node_a.outputs['output1'].connect,
            node_b.outputs['output1']
        )

    def test_connect_2_outs_to_1_in(self):
        node_a1 = nodeview.Node("Node A1", outputs=['output1'])
        node_a2 = nodeview.Node("Node A2", outputs=['output1'])
        node_b = nodeview.Node("Node B", inputs=['input1'])

        a1_slot = node_a1.outputs['output1']
        a2_slot = node_a2.outputs['output1']
        b_slot = node_b.inputs['input1']

        a1_slot.connect(b_slot)
        a2_slot.connect(b_slot)

        self.assertEqual(
            [a1_slot, a2_slot],
            b_slot.connected
        )

    def test_disconnect(self):
        node_a = nodeview.Node("Node A", inputs=["input1"])
        node_b1 = nodeview.Node("Node B1", outputs=["output1"])
        node_b2 = nodeview.Node("Node B2", outputs=["output1"])

        node_a.inputs['input1'].connect(node_b1.outputs['output1'])
        node_a.inputs['input1'].connect(node_b2.outputs['output1'])

        node_a.inputs['input1'].disconnect(node_b1.outputs['output1'])

        self.assertEqual(
            list(),
            node_a.inputs['input1'].connected
        )

        self.assertEqual(
            list(),
            node_b1.outputs['output1'].connected
        )

        self.assertEqual(
            node_a.inputs['input1'],
            node_b2.outputs['output1'].connected
        )

    def test_clear_slot_1_to_many(self):
        node_a1 = nodeview.Node("Node A1", outputs=['output1'])
        node_a2 = nodeview.Node("Node A2", outputs=['output1'])
        node_b = nodeview.Node("Node B", inputs=['input1'])

        a1_slot = node_a1.outputs['output1']
        a2_slot = node_a2.outputs['output1']
        b_slot = node_b.inputs['input1']

        a1_slot.connect(b_slot)
        a2_slot.connect(b_slot)

        a1_slot.clear()

        self.assertEqual(
            list(),
            a1_slot.connected
        )

        self.assertEqual(
            [a2_slot],
            b_slot.connected
        )

        self.assertEqual(
            [b_slot],
            a2_slot.connected
        )

    def test_clear_slot_many_to_1(self):
        node_a1 = nodeview.Node("Node A1", outputs=['output1'])
        node_a2 = nodeview.Node("Node A2", outputs=['output1'])
        node_b = nodeview.Node("Node B", inputs=['input1'])

        a1_slot = node_a1.outputs['output1']
        a2_slot = node_a2.outputs['output1']
        b_slot = node_b.inputs['input1']

        a1_slot.connect(b_slot)
        a2_slot.connect(b_slot)

        b_slot.clear()

        self.assertEqual(
            list(),
            a1_slot.connected
        )

        self.assertEqual(
            list(),
            b_slot.connected
        )

        self.assertEqual(
            list(),
            a2_slot.connected
        )
