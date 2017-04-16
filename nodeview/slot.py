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
from errors import NodeviewConnectionError


class Slot(object):

    INPUT = "input"
    OUTPUT = "output"

    def __init__(self, name, role, parent_node):
        self._parent_node = parent_node
        self.name = name
        self.role = role
        self.connected = list()

    def connect(self, target_slot, _mirror_connect=False):
        if target_slot.role == self.role:
            raise NodeviewConnectionError(self, target_slot)

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
