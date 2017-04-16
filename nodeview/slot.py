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
from uuid import uuid4 as uid
from collections import OrderedDict
from errors import NodeviewConnectionRoleError, NodeviewConnectionLimitError


class Slot(object):

    INPUT = "input"
    OUTPUT = "output"

    def __init__(self, name, role, parent_node):
        self.uid = str(uid())
        self._parent_node = parent_node
        self.name = name
        self.role = role
        self.connected = list()
        self.max_connection = 0

    def connect(self, target_slot, _mirror_connect=False):
        if target_slot.role == self.role:
            raise NodeviewConnectionRoleError(self, target_slot)

        if self.max_connection != 0 and len(self.connected) >= self.max_connection:
            raise NodeviewConnectionLimitError(self)

        if target_slot.max_connection != 0 and len(target_slot.connected) >= target_slot.max_connection:
            raise NodeviewConnectionLimitError(target_slot)

        if target_slot not in self.connected:
            self.connected.append(target_slot)

        if not _mirror_connect:
            target_slot.connect(self, _mirror_connect=True)

    def disconnect(self, target_slot):
        if target_slot in self.connected:
            self.connected.remove(target_slot)
            target_slot.disconnect(self)

    def clear(self):
        connected = list(self.connected)
        for target_slot in connected:
            target_slot.disconnect(self)

    def to_dict(self):
        slot_dict = OrderedDict()
        slot_dict['uid'] = self.uid
        slot_dict['name'] = self.name
        slot_dict['role'] = self.role
        slot_dict['max_connection'] = self.max_connection
        slot_dict['connected_to'] = [slot.uid for slot in self.connected]

        return slot_dict
