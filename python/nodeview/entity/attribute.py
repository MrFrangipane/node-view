import entity


class Attribute(entity.Entity):

    def __init__(self, name, value=None, is_private=True, is_editable=False):
        # Attributes
        self.name = name
        self.value = value
        self.is_private = is_private
        self.is_editable = is_editable
