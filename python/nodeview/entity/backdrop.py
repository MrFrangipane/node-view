import entity


class Backdrop(entity.Entity):
    def __init__(self, name, caption="", color=(0, 0, 0), position=(0, 0), size=(10, 10)):
        # Attributes
        self.name = name
        self.caption = caption
        self.color = color
        self.position = position
        self.size = size
