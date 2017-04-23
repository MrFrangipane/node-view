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
    """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna 
    aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
    
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint 
    occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """

    INPUT = "input"
    OUTPUT = "output"

    def __init__(self, name, role, parent_node, attributes=None):
        """
        Constructor
        :param name: Valid string 
        :param role: Slot.INPUT or Slot.OUTPUT
        :param parent_node: Valid Node to be associated to
        :param attributes: **Serializable** user attributes
        """
        self.uid = str(uid())
        self._parent_node = parent_node
        self.name = name
        self.role = role
        self.attributes = OrderedDict()
        self.max_connection = 0
        self.connected = list()

        if attributes is not None:
            self.attributes = attributes

    def connect(self, target_slot, _mirror_connect=False):
        """
        Connect blah to bleh
        :param target_slot: Slot
        :param _mirror_connect: do not use
        :return: None
        """
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
        """
        Disconnect blah from bleh
        :param target_slot: a valid Slot
        :return: None
        """
        if target_slot in self.connected:
            self.connected.remove(target_slot)
            target_slot.disconnect(self)

    def clear(self):
        """
        Disconnect **all** slots
        :return: None
        """
        connected = list(self.connected)
        for target_slot in connected:
            target_slot.disconnect(self)

    def to_dict(self):
        """
        Represents Slot to a serializable dict
        :return: dict
        """
        slot_dict = OrderedDict()
        slot_dict['uid'] = self.uid
        slot_dict['name'] = self.name
        slot_dict['role'] = self.role
        slot_dict['attributes'] = self.attributes
        slot_dict['max_connection'] = self.max_connection
        slot_dict['connected_to'] = [slot.uid for slot in self.connected]

        return slot_dict
