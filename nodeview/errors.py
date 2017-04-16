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


class NodeviewAttributeError(Exception):

    def __init__(self, node, attribute):
        Exception.__init__(self,
            "Node '{node}' has no attribute '{attribute}'".format(
                node=node.name,
                attribute=attribute
            )
        )


class NodeviewConnectionError(Exception):

    def __init__(self, source_slot, target_slot):
        Exception.__init__(self,
            "Can't connect two slots with same role ('{role}'). '{node_a}'.'{slot_a}' -> '{node_b}'.'{slot_b}'".format(
                role=source_slot.role,
                node_a=source_slot._parent_node.name,
                slot_a=source_slot.name,
                node_b=target_slot._parent_node.name,
                slot_b=target_slot.name
            )
        )
