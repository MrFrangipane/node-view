import math
from operator import add
from PySide.QtGui import *
from PySide.QtCore import *


EDGE_WIDTH = 2
EDGE_COLOR = (0, 0, 0)
EDGE_COLOR_SELECTED = (1, 1, 1)
EDGE_TANGENT = 30
EDGE_OVERSCAN = 20
SHADOW_COLOR = (0, 0, 0, 0.3)
SHADOW_COLOR_SELECTED = (1, 1, 1, .8)
GRADIENT_LENGTH = 25


class EdgeGeometry(object):

    def __init__(self):
        # Init Members
        self.pos_x = 0
        self.pos_y = 0

        self.origin_x = 0
        self.origin_y = 0
        self.origin_tangent_x = 0
        self.origin_tangent_y = 0

        self.target_x = 0
        self.target_y = 0
        self.target_tangent_x = 0
        self.target_tangent_y = 0

        self.bounding_rect = (0, 0, 0, 0)

        self.length = 0

    def update_geometry(self, origin_position, target_position):
        # Compute Position
        x = min(origin_position[0], target_position[0])
        y = min(origin_position[1], target_position[1])

        # Compute Rectangle size
        width = origin_position[0] - target_position[0]
        height = origin_position[1] - target_position[1]

        # New Position
        self.pos_x = x - EDGE_OVERSCAN
        self.pos_y = y - EDGE_OVERSCAN

        # Bounding Rect
        self.bounding_rect = (
            0,
            0,
            abs(width) + 2.0 * (EDGE_OVERSCAN + EDGE_WIDTH),
            abs(height) + 2.0 * (EDGE_OVERSCAN + EDGE_WIDTH)
        )


        # If Width > 0
        if width > 0:
            self.origin_x = EDGE_OVERSCAN
            self.origin_tangent_x = EDGE_OVERSCAN + EDGE_TANGENT
            self.target_x = EDGE_OVERSCAN + width
            self.target_tangent_x = EDGE_OVERSCAN + width - EDGE_TANGENT
        # If Width <= 0
        else:
            self.origin_x = EDGE_OVERSCAN - width
            self.origin_tangent_x = EDGE_OVERSCAN - width + EDGE_TANGENT
            self.target_x = EDGE_OVERSCAN
            self.target_tangent_x = EDGE_OVERSCAN - EDGE_TANGENT

        # If Height > 0
        if height > 0:
            self.origin_y = EDGE_OVERSCAN
            self.target_y = EDGE_OVERSCAN + height
            # If Width <= 0
        else:
            self.origin_y = EDGE_OVERSCAN - height
            self.target_y = EDGE_OVERSCAN

        # Length
        self.length = math.sqrt(width * width + height * height)


def paint_edge(painter, edge_geometry, origin_color, edge_color, target_color):
    # Create Path
    path = QPainterPath()
    path.moveTo(edge_geometry.origin_x, edge_geometry.origin_y)
    path.cubicTo(
        edge_geometry.origin_tangent_x,
        edge_geometry.origin_y,
        edge_geometry.target_tangent_x,
        edge_geometry.target_y,
        edge_geometry.target_x,
        edge_geometry.target_y
    )

    # Prepare Gradient
    gradient = QLinearGradient(
        edge_geometry.origin_x,
        edge_geometry.origin_y,
        edge_geometry.target_x,
        edge_geometry.target_y
    )
    bias = min(GRADIENT_LENGTH / max(.001, edge_geometry.length), .5)

    # Set Colors
    gradient.setColorAt(0, target_color)
    gradient.setColorAt(1, origin_color)

    gradient.setColorAt(bias, edge_color)
    gradient.setColorAt(1 - bias, edge_color)

    # Draw Path
    painter.setBrush(Qt.NoBrush)
    painter.setPen(QPen(QBrush(gradient), EDGE_WIDTH, Qt.SolidLine, Qt.RoundCap))
    painter.drawPath(path)


class ConnectingEdgePySide(QGraphicsItem):

    def __init__(self, edge, parent=None):
        # Super
        QGraphicsItem.__init__(self, parent)
        # Flags
        self.setFlags(
            QGraphicsItem.ItemIsFocusable |
            QGraphicsItem.ItemIsSelectable
        )

        # Shadow
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setColor(QColor.fromRgbF(*SHADOW_COLOR))
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setBlurRadius(5)
        self.setGraphicsEffect(self.shadow)
        self.shadow.setEnabled(True)

        # Members
        self.edge = edge
        self._edge_geometry = EdgeGeometry()

    def _compute_geometry(self):
        # Get Objects
        origin_slot = self.edge.origin_slot
        target_slot = self.edge.target_slot
        origin_node = origin_slot.parent_node
        target_node = target_slot.parent_node

        # Get Slots Scene positions
        origin_position = origin_slot.implementation.dot.dot_pos
        target_position = target_slot.implementation.dot.dot_pos
        #zvalue for edge node
        origin_node.edges.append(self)
        self.setZValue(origin_node.implementation.zValue()-1)

        # Compute Position
        self._edge_geometry.update_geometry(origin_position, target_position)

    # PySide
    def boundingRect(self):
        # Return
        return QRect(*self._edge_geometry.bounding_rect)

    def paint(self, painter, option, widget):
        # Compute Geometry
        self._compute_geometry()

        # Selected
        if self.edge.origin_slot.parent_node.is_selected \
                or self.edge.target_slot.parent_node.is_selected \
                or self.isSelected():
            # Shadow Color
            self.shadow.setColor(QColor.fromRgbF(*SHADOW_COLOR_SELECTED))
            # Slot Colors
            origin_color = QColor.fromRgbF(*self.edge.origin_slot.color).lighter()
            edge_color = QColor.fromRgbF(*EDGE_COLOR_SELECTED)
            target_color = QColor.fromRgbF(*self.edge.target_slot.color).lighter()
            #set zvalue same has nodepyside
            self.setZValue(self.edge.origin_slot.parent_node.implementation.zValue()-1)
        # Not Selected
        else:
            # Shadow Color
            self.shadow.setColor(QColor.fromRgbF(*SHADOW_COLOR))
            # Slot Colors
            origin_color =  QColor.fromRgbF(*self.edge.origin_slot.color).darker()
            edge_color = QColor.fromRgbF(*EDGE_COLOR)
            target_color = QColor.fromRgbF(*self.edge.target_slot.color).darker()

        # Draw Edge
        paint_edge(painter, self._edge_geometry, origin_color, edge_color, target_color)

    def update(self):
        # Compute Geometry
        self._compute_geometry()
        # Move
        self.setPos(self._edge_geometry.pos_x, self._edge_geometry.pos_y)
        # Forward
        QGraphicsItem.update(self)

    def shape(self):  # A revoir, faire un path qui fait 'tout le tour'
        # Create Path
        path = QPainterPath()
        path.moveTo(self._edge_geometry.origin_x, self._edge_geometry.origin_y)
        path.cubicTo(
            self._edge_geometry.origin_tangent_x,
            self._edge_geometry.origin_y,
            self._edge_geometry.target_tangent_x,
            self._edge_geometry.target_y,
            self._edge_geometry.target_x,
            self._edge_geometry.target_y
        )
        return path

class FreeEdgePySide(QGraphicsItem):

    def __init__(self, parent=None):
        # Super
        QGraphicsItem.__init__(self, parent)

        # Shadow
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setColor(QColor.fromRgbF(*SHADOW_COLOR_SELECTED))
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setBlurRadius(5)
        self.setGraphicsEffect(self.shadow)
        self.shadow.setEnabled(True)

        # Members
        self._edge_geometry = EdgeGeometry()

    def set_rectangle(self, origin_position, target_position):
        # Update Geometry
        self._edge_geometry.update_geometry(origin_position, target_position)
        # Update
        self.update()

    # PySide
    def boundingRect(self):
        # Return
        return QRect(*self._edge_geometry.bounding_rect)

    def paint(self, painter, option, widget):
        # Colors
        origin_color = edge_color = target_color = QColor.fromRgbF(*EDGE_COLOR_SELECTED)
        # Draw Edge
        paint_edge(painter, self._edge_geometry, origin_color, edge_color, target_color)

    def update(self):
        # Move
        self.setPos(self._edge_geometry.pos_x, self._edge_geometry.pos_y)
        # Forward
        QGraphicsItem.update(self)
