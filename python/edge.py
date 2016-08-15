from edgepyside import ConnectingEdgePySide  # Temporary, for auto-completion


class Edge(object):
    def __init__(self, origin_slot, target_slot, parent_scene=None, implementation_class=ConnectingEdgePySide):
        # Set Members
        self.origin_slot = origin_slot
        self.target_slot = target_slot
        self.parent_scene = parent_scene
        # Create Delegate
        self.implementation = implementation_class(self)
