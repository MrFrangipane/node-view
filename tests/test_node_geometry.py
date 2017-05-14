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
from nodeview.geometry import Rectangle


class TestNodeGeometry(TestCase):

    def setUp(self):
        self.node = nodeview.Node(
            name="Node",
            graph=nodeview.Graph("Graph"),
            inputs=["1", "2", "3"],
            outputs=["a", "b"]
        )

    def test_init_bounding_rectangle(self):
        self.assertEqual(
            Rectangle(0, 0, 130, 135),
            self.node.geometry.bounding_rect
        )

    def test_init_header_rectangle(self):
        self.assertEqual(
            Rectangle(5, 5, 120, 50),
            self.node.geometry.header_rect
        )

    def test_init_main_rectangle(self):
        self.assertEqual(
            Rectangle(5, 55, 120, 75),
            self.node.geometry.main_rect
        )

    def test_init_input_slot_rectangles(self):
        self.assertEqual(
            [
                Rectangle(5, 62, 10, 10),
                Rectangle(5, 87, 10, 10),
                Rectangle(5, 112, 10, 10)
            ],
            self.node.geometry.input_slot_rects
        )

    def test_init_input_label_rectangles(self):
        self.assertEqual(
            [
                Rectangle(15, 55, 50, 25),
                Rectangle(15, 80, 50, 25),
                Rectangle(15, 105, 50, 25)
            ],
            self.node.geometry.input_label_rects
        )

    def test_init_output_slot_rectangles(self):
        self.assertEqual(
            [
                Rectangle(115, 62, 10, 10),
                Rectangle(115, 87, 10, 10)
            ],
            self.node.geometry.output_slot_rects
        )

    def test_init_output_label_rectangles(self):
        self.assertEqual(
            [
                Rectangle(65, 55, 50, 25),
                Rectangle(65, 80, 50, 25)
            ],
            self.node.geometry.output_label_rects
        )
