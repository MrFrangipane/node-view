from PySide.QtGui import *
from PySide.QtCore import *
from slotspyside import *

WIDTH = 200
HEADER_HEIGHT = 40
ROW_HEIGHT = 25

BACKGROUND_COLOR = (.22, .22, .22, 1)
FRAME_COLOR = (0, 0, 0)

SHADOW_COLOR = (1, 1, 1, .1)
SHADOW_RADIUS = 15

HANDLE_RADIUS = 7
HANDLE_COLOR = (1, 1, 1)

NAME_FONT = QFont()
NAME_FONT.setBold(True)
CAPTION_FONT = QFont()
CAPTION_FONT.setItalic(True)
CAPTION_OPACITY = .75
TEXT_COLOR = (1, 1, 1)
TEXT_PADDING = 4

HANDLE_NONE = 0
HANDLE_TOP_LEFT = 1
HANDLE_TOP_MIDDLE = 2
HANDLE_TOP_RIGHT = 3
HANDLE_MID_LEFT = 4
HANDLE_MID_RIGHT = 5
HANDLE_BOTTOM_LEFT = 6
HANDLE_BOTTOM_MIDDLE = 7
HANDLE_BOTTOM_RIGHT = 8

SLOT_RADIUS = 10
SLOT_COLOR_HOVERED = TEXT_COLOR
SLOT_FONT = QFont()
SLOT_OFFSET = 10


def _color(values):
    """
    Convert rgb value to hex color
    :param values: color as (r, g, b)
    :type values: tuple
    :return: QColor
    """
    return QColor.fromRgbF(*values)


class NodePySide(QGraphicsItem):  # Move all geometry computations in upper class (or dedicated geometry class ?)

    def __init__(self, node, parent=None):
        """
        NodeUI of node object, handle all graphicsItem and SlotsUI SlotPySide
        :param node: the node object
        :type node: Node
        :param parent: parent item or widget
        """
        # Super
        QGraphicsItem.__init__(self, parent)
        # Flags
        self.setFlags(
            QGraphicsItem.ItemIsFocusable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)
        # Init Shadow Effect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setColor(QColor.fromRgbF(*SHADOW_COLOR))
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setBlurRadius(SHADOW_RADIUS)
        self.setGraphicsEffect(self.shadow)
        self.shadow.setEnabled(True)
        # Members
        self.node = node
        self._rect = QRect(0, 0, 0, 0)
        self._min_width = 0
        self._min_height = 0
        # Mouse
        self._is_mouse_over = False
        self._is_mouse_pressed = True
        self._previous_mouse_position = QPoint(0, 0)
        # Handles
        self._handle_rects = dict()
        self._handle_pressed = HANDLE_NONE
        # Compute Geometry Values
        self.compute_geometry_values()

    def add_output_slots(self):
        """
        Add SlotPySide to this NodePySide fom output_slots's node
        :return: None
        """
        rect_labels = QRect(
            0,
            HEADER_HEIGHT,
            self._rect.width(),
            ROW_HEIGHT
        )

        for output_index, output in enumerate(self.node.output_slots):
            #Adjust rect
            rect_labels.moveTop(HEADER_HEIGHT + 10 + output_index * ROW_HEIGHT)
            #creation of OutPutSlotPySide and position it
            output_ui = OutputSlotPySide(rect_labels.x(), rect_labels.y(), slot=output)
            output_ui.input_rect.setWidth(self._rect.width() - SLOT_OFFSET)
            output_ui.dot.setPos(self._rect.width() - 4, 0)
            output_ui.slot.dot_pos = (self.scenePos().x() + self._rect.width() - 4 , rect_labels.y() + self.scenePos().y())
            #parent to NodePyside
            output_ui.setParentItem(self)
            #passe OutputPyside to slot
            output.implementation = output_ui


    def add_input_slots(self):
        """
        Add SlotPySide to this NodePySide fom input_slots's node
        :return: None
        """
        rect_labels = QRect(
            0,
            HEADER_HEIGHT,
            self._rect.width(),
            ROW_HEIGHT
        )
        for input_index, input in enumerate(self.node.input_slots):
            #Adjust rect
            rect_labels.moveTop(HEADER_HEIGHT + 10 + input_index * ROW_HEIGHT)
            #creation of InputSlotPySide and position it
            input_ui = InputSlotPySide(rect_labels.x(), rect_labels.y(), slot=input)
            input_ui.input_rect.setX(SLOT_OFFSET + SLOT_RADIUS)
            #parent to NodePyside
            input_ui.setParentItem(self)
            #passe InputPyside to slot
            input.implementation = input_ui


    def compute_geometry_values(self):
        """
        Compute geometry values, like a redraw
        :return: None
        """
        # Min Values
        self._min_width = WIDTH
        self._min_height = (
            HANDLE_RADIUS +
            HEADER_HEIGHT +
            max(len(self.node.input_slots), len(self.node.output_slots)) * ROW_HEIGHT +
            TEXT_PADDING
        )

        # Update Values
        width = max(self._min_width, self.node.size[0])
        height = max(self._min_height, self.node.size[1])
        self.node.size = (width, height)
        self._compute_rect()
        self._compute_handle_rects()

    def update_pos(self):
        """
        update position of NodePySides and SlotPySides
        :return:
        """
        self.setPos(self.node.position[0], self.node.position[1])
        #Update pos pour slots
        for input in self.node.input_slots:
            input.implementation.update_pos()
        for output in self.node.output_slots:
            output.implementation.update_pos()

    def _compute_rect(self):
        """
        Compute rect
        :return: None
        """
        self._rect = QRect(0, 0, self.node.size[0], self.node.size[1]).adjusted(
            HANDLE_RADIUS / 2.0,
            HANDLE_RADIUS / 2.0,
            -HANDLE_RADIUS,
            -HANDLE_RADIUS
        )

    def _compute_handle_rects(self):
        """
        Compute handle rect for background
        :return:
        """
        # If Resizable
        if self.node.is_resizable:
            # Compute
            rect_tl = QRect(0, 0, HANDLE_RADIUS, HANDLE_RADIUS)
            rect_tm = QRect(self._rect.width() / 2, 0, HANDLE_RADIUS, HANDLE_RADIUS)
            rect_tr = QRect(self._rect.width(), 0, HANDLE_RADIUS, HANDLE_RADIUS)
            rect_ml = QRect(0, self._rect.height() / 2, HANDLE_RADIUS, HANDLE_RADIUS)
            rect_mr = QRect(self._rect.width(), self._rect.height() / 2, HANDLE_RADIUS, HANDLE_RADIUS)
            rect_bl = QRect(0, self._rect.height(), HANDLE_RADIUS, HANDLE_RADIUS)
            rect_bm = QRect(self._rect.width() / 2, self._rect.height(), HANDLE_RADIUS, HANDLE_RADIUS)
            rect_br = QRect(self._rect.width(), self._rect.height(), HANDLE_RADIUS, HANDLE_RADIUS)

            # Update Members
            self._handle_rects = {
                HANDLE_TOP_LEFT: rect_tl,
                HANDLE_TOP_MIDDLE: rect_tm,
                HANDLE_TOP_RIGHT: rect_tr,
                HANDLE_MID_LEFT: rect_ml,
                HANDLE_MID_RIGHT: rect_mr,
                HANDLE_BOTTOM_LEFT: rect_bl,
                HANDLE_BOTTOM_MIDDLE: rect_bm,
                HANDLE_BOTTOM_RIGHT: rect_br
            }

        # Else, no
        else:
            self._handle_rects = dict()

    # PySide
    def boundingRect(self):
        # Return
        return QRect(0, 0, self.node.size[0], self.node.size[1])

    def paint(self, painter, option, widget):
        # Rects
        rect_header = QRect(
            HANDLE_RADIUS / 2.0,
            HANDLE_RADIUS / 2.0,
            self._rect.width(),
            HEADER_HEIGHT - HANDLE_RADIUS
        )
        rect_labels = QRect(
            0,
            HEADER_HEIGHT,
            self._rect.width(),
            ROW_HEIGHT
        )
        # Node Background
        painter.setPen(Qt.NoPen)
        painter.setBrush(_color(BACKGROUND_COLOR).darker(110))
        path = QPainterPath()
        path.addRoundedRect(self._rect, 10, 10)
        painter.drawPath(path)
        # Header Background
        path_head = QPainterPath()
        painter.setBrush(_color(self.node.color))
        painter.setPen(Qt.NoPen)
        path_head.addRoundedRect(rect_header, 10, 10)
        painter.drawPath(path_head)
        rect_header.setY(rect_header.y()+10)
        painter.drawRect(rect_header)
        rect_header.setY(rect_header.y()-10)
        rect_header.setX(rect_header.x()+4)
        #draw line
        if not self.node.is_resizable:
            line_rect = QRect(rect_header.x()-4, rect_header.y() + 32, rect_header.width()+4, 2)
            painter.setBrush(_color(self.node.color).lighter(130))
            painter.drawRect(line_rect)
            line_rect = QRect(rect_header.x()-4, rect_header.y() + 34, rect_header.width()+4, 4)
            painter.setBrush(_color(BACKGROUND_COLOR).darker(150))
            painter.drawRect(line_rect)

        # Frame
        painter.setBrush(Qt.NoBrush)
        if self.isSelected():
            painter.setPen(_color(HANDLE_COLOR))
            path = QPainterPath()
            path.addRoundedRect(self._rect, 10, 10)
            painter.drawPath(path)
        # Header Text
        painter.setFont(NAME_FONT)
        painter.setPen(_color(TEXT_COLOR))
        painter.drawText(
            rect_header.adjusted(TEXT_PADDING, TEXT_PADDING, -TEXT_PADDING, -TEXT_PADDING),
            Qt.AlignLeft | Qt.AlignVCenter,
            self.node.name + "\n"
        )
        painter.setOpacity(CAPTION_OPACITY)
        painter.setFont(CAPTION_FONT)
        painter.drawText(
            rect_header.adjusted(TEXT_PADDING, TEXT_PADDING, -TEXT_PADDING, -TEXT_PADDING),
            Qt.AlignLeft | Qt.AlignVCenter,
            "\n" + self.node.caption
        )
        painter.setOpacity(1)

    def mousePressEvent(self, event):
        # Update Members
        self._previous_mouse_position = event.scenePos()
        self._is_mouse_pressed = True
        # If mouse on handle
        self._handle_pressed = HANDLE_NONE
        for handle_enum, handle_rect in self._handle_rects.items():
            # If Pressed
            if handle_rect.contains(int(event.pos().x()), int(event.pos().y())):
                self._handle_pressed = handle_enum
                break
        # Forward
        QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        # Update Member
        self._is_mouse_pressed = False
        # Forward
        QGraphicsItem.mouseReleaseEvent(self, event)

    def mouseMoveEvent(self, event):
        # If None
        if self._handle_pressed is HANDLE_NONE:
            super(NodePySide, self).mouseMoveEvent(event)
            # Forward
            #QGraphicsItem.mouseMoveEvent(self, event)
            # Exit
            #return
            return

    def hoverEnterEvent(self, event):
        super(NodePySide, self).hoverEnterEvent(event)
        # Set Member
        self._is_mouse_over = True

    def hoverLeaveEvent(self, event):
        super(NodePySide, self).hoverLeaveEvent(event)
        # Reset Members
        self._is_mouse_over = False
        # Ask Redraw
        self.prepareGeometryChange()

    def itemChange(self, change, value):
        # If Moved
        if self.scene() and change in [QGraphicsItem.ItemPositionChange, QGraphicsItem.ItemPositionHasChanged]:
            #Update Node's ans Slots's position
            self.node.position = (self.pos().x(), self.pos().y())
            #update pos attribute in slots
            for input in self.node.input_slots:
                input.implementation.update_pos()
            for output in self.node.output_slots:
                output.implementation.update_pos()
            # Warn Scene
            self.scene().node_changed(self.node)
        # If Selected
        elif self.scene() and change in [QGraphicsItem.ItemSelectedChange, QGraphicsItem.ItemSelectedHasChanged]:
            # Update Node's Member
            self.node.is_selected = self.isSelected()
            # Warn Scene
            self.scene().node_changed(self.node)
            # Shadow Effect
            self.shadow.setColor(QColor.fromRgbF(*SHADOW_COLOR))
        # Forward
        return QGraphicsItem.itemChange(self, change, value)

#Wip
class BackDropPySide(NodePySide):
    def __init__(self, node, parent=None):
        super(BackDropPySide, self).__init__(node, parent=None)
        self.back_rect = self.mapToScene(self.boundingRect())

    def paint(self, painter, option, widget):
        # Rects
        rect_header = QRect(
            HANDLE_RADIUS / 2.0,
            HANDLE_RADIUS / 2.0,
            self._rect.width(),
            HEADER_HEIGHT - HANDLE_RADIUS
        )
        rect_labels = QRect(
            0,
            HEADER_HEIGHT,
            self._rect.width(),
            ROW_HEIGHT
        )
        painter.setPen(Qt.NoPen)
        painter.setBrush(_color(BACKGROUND_COLOR))
        painter.drawRect(self._rect)
        painter.setBrush(_color(self.node.color))
        painter.drawRect(rect_header)
        # Header Text
        painter.setFont(NAME_FONT)
        painter.setPen(_color(TEXT_COLOR))
        painter.drawText(
            rect_header.adjusted(TEXT_PADDING, TEXT_PADDING, -TEXT_PADDING, -TEXT_PADDING),
            Qt.AlignLeft | Qt.AlignVCenter,
            self.node.name + "\n"
        )
        painter.setOpacity(CAPTION_OPACITY)
        painter.setFont(CAPTION_FONT)
        painter.drawText(
            rect_header.adjusted(TEXT_PADDING, TEXT_PADDING, -TEXT_PADDING, -TEXT_PADDING),
            Qt.AlignLeft | Qt.AlignVCenter,
            "\n" + self.node.caption
        )
        painter.setOpacity(1)
        # # Handles
        if self._is_mouse_over:
            painter.setBrush(_color(HANDLE_COLOR))
            painter.setPen(Qt.NoPen)
            for handle_rect in self._handle_rects.values():
                painter.drawEllipse(handle_rect)


    def mousePressEvent(self, event):
        super(BackDropPySide, self).mousePressEvent(event)
        #fix zvalue background
        self.setZValue(0)
        self.back_rect = self.mapToScene(self.boundingRect())

    def mouseMoveEvent(self, event):
        # Compute Deltas
        delta_x = event.scenePos().x() - self._previous_mouse_position.x()
        delta_y = event.scenePos().y() - self._previous_mouse_position.y()
        # Update Mouse Position
        self._previous_mouse_position.setX(self._previous_mouse_position.x() + delta_x)
        self._previous_mouse_position.setY(self._previous_mouse_position.y() + delta_y)
        # Copy Size Values
        new_width = self.node.size[0]
        new_height = self.node.size[1]
        # Should move
        is_moving_x = False
        is_moving_y = False
        # Prepare
        self.prepareGeometryChange()
        # if pressed
        if self._handle_pressed is HANDLE_TOP_LEFT:
            # Resize
            new_width -= delta_x
            new_height -= delta_y
            # Should Move
            is_moving_x = True
            is_moving_y = True
        elif self._handle_pressed is HANDLE_TOP_MIDDLE:
            # Resize
            new_height -= delta_y
            # Should Move on Y only
            is_moving_y = True
        elif self._handle_pressed is HANDLE_TOP_RIGHT:
            # Resize
            new_width += delta_x
            new_height -= delta_y
            # Should Move on Y only
            is_moving_y = True
        elif self._handle_pressed is HANDLE_MID_LEFT:
            # Resize
            new_width -= delta_x
            # Should Move on X only
            is_moving_x = True
        elif self._handle_pressed is HANDLE_MID_RIGHT:
            # Resize
            new_width += delta_x
        elif self._handle_pressed is HANDLE_BOTTOM_LEFT:
            # Resize
            new_width -= delta_x
            new_height += delta_y
            # Should Move on X only
            is_moving_x = True
        elif self._handle_pressed is HANDLE_BOTTOM_MIDDLE:
            # Resize
            new_height += delta_y
        elif self._handle_pressed is HANDLE_BOTTOM_RIGHT:
            # Resize
            new_width += delta_x
            new_height += delta_y
        # Cancel if too small X
        if new_width < self._min_width:
            # Delta
            delta_x = 0
            # New Width
            new_width = self.node.size[0]
        # Cancel if too small Y
        if new_height < self._min_height:
            # Delta
            delta_y = 0
            # New Width
            new_height = self.node.size[1]
        # Resize
        self.node.size = (new_width, new_height)
        # If Should move
        if is_moving_x:
            self.moveBy(delta_x, 0)
        if is_moving_y:
            self.moveBy(0, delta_y)
        # Compute New Geometry
        self.compute_geometry_values()