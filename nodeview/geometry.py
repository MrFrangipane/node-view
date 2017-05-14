

class Rectangle(object):
    """
    Basic implementation of Rectangle, with equity based on member values
    """
    def __init__(self, x=0, y=0, width=0, height=0):
        """
        Create a new Rectangle
        :param x: Position on x axis
        :param y: Position on y axis
        :param width: Width
        :param height: Height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Rectangle({x}, {y}, {width}, {height})".format(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
        )


class NodeGeometry(object):
    """
    Handles computation of rectangles for drawing
    - `bounding_rect`
    - `header_rect`
    - `main_rect`
    - `input_slot_rects`
    - `input_label_rects`
    - `output_slot_rects`
    - `output_label_rects`
    """

    FIXED_WIDTH = 220
    ROW_HEIGHT = 30
    MAIN_PADDING = 8
    SLOT_RADIUS = 15

    def __init__(self):
        self.node = None
        self.bounding_rect = Rectangle()
        self.header_rect = Rectangle()
        self.main_rect = Rectangle()
        self.input_slot_rects = list()
        self.input_label_rects = list()
        self.output_slot_rects = list()
        self.output_label_rects = list()

    def set_node(self, node):
        """
        Gives a Node to compute values from
        :param node: Node
        :return: None
        """
        self.node = node

    def compute(self):
        """
        Updates rectangles 
        :return: 
        """
        self.input_slot_rects = list()
        self.input_label_rects = list()
        self.output_slot_rects = list()
        self.output_label_rects = list()

        row_count = max(
            len(self.node.inputs),
            len(self.node.outputs)
        )

        slot_padding = (self.ROW_HEIGHT - self.SLOT_RADIUS) / 2
        label_width = (self.FIXED_WIDTH - (2 * self.SLOT_RADIUS)) / 2

        self.bounding_rect.width = self.FIXED_WIDTH + 2 * self.MAIN_PADDING
        self.bounding_rect.height = \
            self.MAIN_PADDING + \
            self.ROW_HEIGHT + \
            self.ROW_HEIGHT + \
            (self.ROW_HEIGHT * row_count) + \
            self.MAIN_PADDING

        self.header_rect.x = self.MAIN_PADDING
        self.header_rect.y = self.MAIN_PADDING
        self.header_rect.width = self.FIXED_WIDTH
        self.header_rect.height = self.ROW_HEIGHT * 2

        self.main_rect.x = self.header_rect.x
        self.main_rect.y = self.header_rect.y + self.header_rect.height
        self.main_rect.width = self.FIXED_WIDTH
        self.main_rect.height = self.ROW_HEIGHT * row_count

        for row_index, input in enumerate(self.node.inputs):
            slot_rect = Rectangle(
                self.main_rect.x,
                self.main_rect.y + self.ROW_HEIGHT * row_index + slot_padding,
                self.SLOT_RADIUS,
                self.SLOT_RADIUS
            )
            label_rect = Rectangle(
                self.main_rect.x + self.SLOT_RADIUS,
                self.main_rect.y + self.ROW_HEIGHT * row_index,
                label_width,
                self.ROW_HEIGHT
            )

            self.input_slot_rects.append(slot_rect)
            self.input_label_rects.append(label_rect)

        for row_index, input in enumerate(self.node.outputs):
            slot_rect = Rectangle(
                self.main_rect.x + self.SLOT_RADIUS + (2 * label_width),
                self.main_rect.y + self.ROW_HEIGHT * row_index + slot_padding,
                self.SLOT_RADIUS,
                self.SLOT_RADIUS
            )
            label_rect = Rectangle(
                self.main_rect.x + self.SLOT_RADIUS + label_width,
                self.main_rect.y + self.ROW_HEIGHT * row_index,
                label_width,
                self.ROW_HEIGHT
            )

            self.output_slot_rects.append(slot_rect)
            self.output_label_rects.append(label_rect)
