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


class TestGraphics(TestCase):

    def setUp(self):
        self.node = nodeview.Node(
            name="Node",
            graph=nodeview.Graph("Graph"),
            inputs=["1", "2"],
            outputs=["a", "b"]
        )

    def test_node(self):
        node = nodeview.GraphicNode(self.node)
        node.update()

        self.assertEqual(
            150,
            node.width
        )

        self.assertEqual(
            60,
            node.height
        )
