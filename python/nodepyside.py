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
    return QColor.fromRgbF(*values)


class NodePySide(QGraphicsItem):  # Move all geometry computations in upper class (or dedicated geometry class ?)

    def __init__(self, node, parent=None):
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

        # Slots
        self._slot_input_rects = dict()
        self._slot_output_rects = dict()
        self._slot_input_hovered = ""
        self._slot_output_hovered = ""

        # Compute Geometry Values
        self.compute_geometry_values()

    def add_output_slots(self):
        rect_labels = QRect(
            0,
            HEADER_HEIGHT,
            self._rect.width(),
            ROW_HEIGHT
        )
        print self.node.name
        for s in self.node.input_slots:
            print 'slot : ' + s.name

        for output_index, output in enumerate(self.node.output_slots):
            rect_labels.moveTop(HEADER_HEIGHT + 10 + output_index * ROW_HEIGHT)
            output_ui = OutputSlotPySide(rect_labels.x(), rect_labels.y(), slot=output)
            output_ui.input_rect.setWidth(self._rect.width() - SLOT_OFFSET)
            output_ui.dot.setPos(self._rect.width() - 4, 0)
            output_ui.slot.dot_pos = (self.scenePos().x() + self._rect.width() - 4 , rect_labels.y() + self.scenePos().y())
            output_ui.setParentItem(self)
            output.implementation = output_ui


    def add_input_slots(self):
        rect_labels = QRect(
            0,
            HEADER_HEIGHT,
            self._rect.width(),
            ROW_HEIGHT
        )
        print self.node.name
        for s in self.node.input_slots:
            print 'slot : ' + s.name
        for input_index, input in enumerate(self.node.input_slots):
            rect_labels.moveTop(HEADER_HEIGHT + 10 + input_index * ROW_HEIGHT)
            input_ui = InputSlotPySide(rect_labels.x(), rect_labels.y(), slot=input)
            input_ui.input_rect.setX(SLOT_OFFSET + SLOT_RADIUS)
            input_ui.setParentItem(self)
            input.implementation = input_ui

    # for output_index, output in enumerate(self.node.output_slots):
    #     # Move Rect Label
    #     rect_labels.moveTop(HEADER_HEIGHT + output_index * ROW_HEIGHT)
    #     # Draw Text
    #     painter.drawText(
    #         rect_labels.adjusted(TEXT_PADDING, TEXT_PADDING, TEXT_PADDING - SLOT_RADIUS, -TEXT_PADDING),
    #         Qt.AlignRight | Qt.AlignVCenter,
    #         output.name
    #     )


    def compute_geometry_values(self):
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
        #self._compute_handle_rects()
        #self._compute_input_rects()
        #self._compute_output_rects()


    def update_pos(self):
        self.setPos(self.node.position[0], self.node.position[1])
        # Update pos pour slots #
        for input in self.node.input_slots:
            input.implementation.update_pos()
        for output in self.node.output_slots:
            output.implementation.update_pos()

    def _compute_rect(self):
        self._rect = QRect(0, 0, self.node.size[0], self.node.size[1]).adjusted(
            HANDLE_RADIUS / 2.0,
            HANDLE_RADIUS / 2.0,
            -HANDLE_RADIUS,
            -HANDLE_RADIUS
        )

    # def _compute_handle_rects(self):
    #     # If Resizable
    #     if self.node.is_resizable:
    #         # Compute
    #         rect_tl = QRect(0, 0, HANDLE_RADIUS, HANDLE_RADIUS)
    #         rect_tm = QRect(self._rect.width() / 2, 0, HANDLE_RADIUS, HANDLE_RADIUS)
    #         rect_tr = QRect(self._rect.width(), 0, HANDLE_RADIUS, HANDLE_RADIUS)
    #         rect_ml = QRect(0, self._rect.height() / 2, HANDLE_RADIUS, HANDLE_RADIUS)
    #         rect_mr = QRect(self._rect.width(), self._rect.height() / 2, HANDLE_RADIUS, HANDLE_RADIUS)
    #         rect_bl = QRect(0, self._rect.height(), HANDLE_RADIUS, HANDLE_RADIUS)
    #         rect_bm = QRect(self._rect.width() / 2, self._rect.height(), HANDLE_RADIUS, HANDLE_RADIUS)
    #         rect_br = QRect(self._rect.width(), self._rect.height(), HANDLE_RADIUS, HANDLE_RADIUS)
    #
    #         # Update Members
    #         self._handle_rects = {
    #             HANDLE_TOP_LEFT: rect_tl,
    #             HANDLE_TOP_MIDDLE: rect_tm,
    #             HANDLE_TOP_RIGHT: rect_tr,
    #             HANDLE_MID_LEFT: rect_ml,
    #             HANDLE_MID_RIGHT: rect_mr,
    #             HANDLE_BOTTOM_LEFT: rect_bl,
    #             HANDLE_BOTTOM_MIDDLE: rect_bm,
    #             HANDLE_BOTTOM_RIGHT: rect_br
    #         }
    #
    #     # Else, no
    #     else:
    #         self._handle_rects = dict()

    # def _compute_input_rects(self):
    #     # Init
    #     self._slot_input_rects = dict()
    #     # Each Input
    #     for input_index, input_slot in enumerate(self.node.input_slots):
    #         # New Rect
    #         input_rect = QRect(
    #             0,
    #             (HEADER_HEIGHT + ROW_HEIGHT * .5) - (SLOT_RADIUS / 2) + (input_index * ROW_HEIGHT),
    #             SLOT_RADIUS,
    #             SLOT_RADIUS
    #         )
    #         # Set Member
    #         self._slot_input_rects[input_slot] = input_rect
    #         # Set Slot Member
    #         input_slot.position = (  # This is why we need a dedicated geometry class :)
    #             input_rect.x() + SLOT_RADIUS * .5,
    #             input_rect.y() + SLOT_RADIUS * .5,
    #         )

    # def _compute_output_rects(self):
    #     # Init
    #     self._slot_output_rects = dict()
    #     # Each Input
    #     for output_index, output_slot in enumerate(self.node.output_slots):
    #         # New Rect
    #         output_rect = QRect(
    #             self._rect.width() + HANDLE_RADIUS - SLOT_RADIUS,
    #             (HEADER_HEIGHT + ROW_HEIGHT * .5) - (SLOT_RADIUS / 2) + (output_index * ROW_HEIGHT),
    #             SLOT_RADIUS,
    #             SLOT_RADIUS
    #         )
    #         # Set Member
    #         self._slot_output_rects[output_slot] = output_rect
    #         # Set Slot Member
    #         output_slot.position = (  # This is why we need a dedicated geometry class :)
    #             output_rect.x() + SLOT_RADIUS * .5,
    #             output_rect.y() + SLOT_RADIUS * .5,
    #         )

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
        if self.node.is_resizable:
            painter.setBrush(_color(BACKGROUND_COLOR))
        else:
            painter.setBrush(_color(BACKGROUND_COLOR).darker(110))
        painter.drawRect(self._rect)

        # Header Background
        painter.setBrush(_color(self.node.color))
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect_header)

        # Frame
        painter.setBrush(Qt.NoBrush)
        if self.isSelected():
            painter.setPen(_color(HANDLE_COLOR))
            painter.drawRect(self._rect)

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

        # # Input Labels
        # painter.setFont(SLOT_FONT)
        # painter.setPen(_color(TEXT_COLOR))
        # for input_index, input in enumerate(self.node.input_slots):
        #     # Move Rect Label
        #     rect_labels.moveTop(HEADER_HEIGHT + input_index * ROW_HEIGHT)
        #     # Draw Text
        #     painter.drawText(
        #         rect_labels.adjusted(TEXT_PADDING + SLOT_RADIUS, TEXT_PADDING, -TEXT_PADDING, -TEXT_PADDING),
        #         Qt.AlignLeft | Qt.AlignVCenter,
        #         input.name
        #     )

        # Outputs Labels
        # painter.setFont(SLOT_FONT)
        # painter.setPen(_color(TEXT_COLOR))
        # for output_index, output in enumerate(self.node.output_slots):
        #     # Move Rect Label
        #     rect_labels.moveTop(HEADER_HEIGHT + output_index * ROW_HEIGHT)
        #     # Draw Text
        #     painter.drawText(
        #         rect_labels.adjusted(TEXT_PADDING, TEXT_PADDING, TEXT_PADDING - SLOT_RADIUS, -TEXT_PADDING),
        #         Qt.AlignRight | Qt.AlignVCenter,
        #         output.name
        #     )

        # # Input Slots
        # painter.setPen(_color(FRAME_COLOR))
        # # Each Input Slot
        # for input_, slot_rect in self._slot_input_rects.items():
        #     # Brush
        #     painter.setBrush(_color(input_.color))
        #     # If Hovered
        #     if self._slot_input_hovered == input_:
        #         painter.setBrush(_color(SLOT_COLOR_HOVERED))
        #     painter.drawEllipse(slot_rect)

        # # Output Slots
        # painter.setPen(_color(FRAME_COLOR))
        # # Each Input Slot
        # for output, slot_rect in self._slot_output_rects.items():
        #     # Brush
        #     painter.setBrush(_color(output.color))
        #     # If Hovered
        #     if self._slot_output_hovered == output:
        #         painter.setBrush(_color(SLOT_COLOR_HOVERED))
        #     painter.drawEllipse(slot_rect)

        # # Handles
        # if self._is_mouse_over:
        #     painter.setBrush(_color(HANDLE_COLOR))
        #     painter.setPen(Qt.NoPen)
        #     for handle_rect in self._handle_rects.values():
        #         painter.drawEllipse(handle_rect)

    # def mousePressEvent(self, event):
    #     # Update Members
    #     self._previous_mouse_position = event.scenePos()
    #     self._is_mouse_pressed = True
    #
    #     # If mouse on handle
    #     self._handle_pressed = HANDLE_NONE
    #     for handle_enum, handle_rect in self._handle_rects.items():
    #         # If Pressed
    #         if handle_rect.contains(int(event.pos().x()), int(event.pos().y())):
    #             self._handle_pressed = handle_enum
    #             break
    #
    #     # If mouse on input slot
    #     if self._slot_input_hovered:
    #         self.scene().input_slot_pressed(self._slot_input_hovered)
    #
    #     # If mouse on output slot
    #     if self._slot_output_hovered:
    #         self.scene().output_slot_pressed(self._slot_output_hovered)
    #
    #     # Forward
    #     QGraphicsItem.mousePressEvent(self, event)
    #
    # def mouseReleaseEvent(self, event):
    #     # Update Member
    #     self._is_mouse_pressed = False
    #     # Forward
    #     QGraphicsItem.mouseReleaseEvent(self, event)

    # def mouseMoveEvent(self, event):
    #     # If None
    #     if self._handle_pressed is HANDLE_NONE and not self._slot_input_hovered and not self._slot_output_hovered:
    #         # Forward
    #         QGraphicsItem.mouseMoveEvent(self, event)
    #         # Exit
    #         return
    #
    #     # Prepare
    #     self.prepareGeometryChange()
    #
    #     # Compute Deltas
    #     delta_x = event.scenePos().x() - self._previous_mouse_position.x()
    #     delta_y = event.scenePos().y() - self._previous_mouse_position.y()
    #     # Copy Size Values
    #     new_width = self.node.size[0]
    #     new_height = self.node.size[1]
    #     # Should move
    #     is_moving_x = False
    #     is_moving_y = False
    #
    #     if self._handle_pressed is HANDLE_TOP_LEFT:
    #         # Resize
    #         new_width -= delta_x
    #         new_height -= delta_y
    #         # Should Move
    #         is_moving_x = True
    #         is_moving_y = True
    #
    #     elif self._handle_pressed is HANDLE_TOP_MIDDLE:
    #         # Resize
    #         new_height -= delta_y
    #         # Should Move on Y only
    #         is_moving_y = True
    #
    #     elif self._handle_pressed is HANDLE_TOP_RIGHT:
    #         # Resize
    #         new_width += delta_x
    #         new_height -= delta_y
    #         # Should Move on Y only
    #         is_moving_y = True
    #
    #     elif self._handle_pressed is HANDLE_MID_LEFT:
    #         # Resize
    #         new_width -= delta_x
    #         # Should Move on X only
    #         is_moving_x = True
    #
    #     elif self._handle_pressed is HANDLE_MID_RIGHT:
    #         # Resize
    #         new_width += delta_x
    #
    #     elif self._handle_pressed is HANDLE_BOTTOM_LEFT:
    #         # Resize
    #         new_width -= delta_x
    #         new_height += delta_y
    #         # Should Move on X only
    #         is_moving_x = True
    #
    #     elif self._handle_pressed is HANDLE_BOTTOM_MIDDLE:
    #         # Resize
    #         new_height += delta_y
    #
    #     elif self._handle_pressed is HANDLE_BOTTOM_RIGHT:
    #         # Resize
    #         new_width += delta_x
    #         new_height += delta_y
    #
    #     # Cancel if too small X
    #     if new_width < self._min_width:
    #         # Delta
    #         delta_x = 0
    #         # New Width
    #         new_width = self.node.size[0]
    #
    #     # Cancel if too small Y
    #     if new_height < self._min_height:
    #         # Delta
    #         delta_y = 0
    #         # New Width
    #         new_height = self.node.size[1]
    #
    #     # Resize
    #     self.node.size = (new_width, new_height)
    #
    #     # If Should move
    #     if is_moving_x:
    #         self.moveBy(delta_x, 0)
    #
    #     if is_moving_y:
    #         self.moveBy(0, delta_y)
    #
    #     # Update Mouse Position
    #     self._previous_mouse_position.setX(self._previous_mouse_position.x() + delta_x)
    #     self._previous_mouse_position.setY(self._previous_mouse_position.y() + delta_y)
    #     # Compute New Geometry
    #     self.compute_geometry_values()

    # def hoverEnterEvent(self, event):
    #     # Set Member
    #     self._is_mouse_over = True
    #
    # def hoverLeaveEvent(self, event):
    #     # Reset Members
    #     self._is_mouse_over = False
    #     self._slot_input_hovered = ""
    #     self._slot_output_hovered = ""
    #     # Ask Redraw
    #     self.prepareGeometryChange()

    # def hoverMoveEvent(self, event):
    #     # If Over input
    #     is_over_input = False
    #     is_over_output = False
    #
    #     # Each input slot
    #     for slot, slot_rect in self._slot_input_rects.items():
    #         # If Mouse Hovers
    #         if slot_rect.contains(int(event.pos().x()), int(event.pos().y())):
    #             # If different
    #             if self._slot_input_hovered != slot:
    #                 # Update Member
    #                 self._slot_input_hovered = slot
    #                 # Ask Redraw
    #                 self.prepareGeometryChange()
    #             # Set
    #             is_over_input = True
    #
    #     # Each output slot
    #     for slot, slot_rect in self._slot_output_rects.items():
    #         # If Mouse Hovers
    #         if slot_rect.contains(int(event.pos().x()), int(event.pos().y())):
    #             # If different
    #             if self._slot_output_hovered != slot:
    #                 # Update Member
    #                 self._slot_output_hovered = slot
    #                 # Ask Redraw
    #                 self.prepareGeometryChange()
    #             # Set
    #             is_over_output = True
    #
    #     # Reset Members
    #     if not is_over_input:
    #         self._slot_input_hovered = ""
    #
    #     if not is_over_output:
    #         self._slot_output_hovered = ""
    #
    #     # Ask Redraw
    #     self.prepareGeometryChange()
    # def update_pos(self):
    #     #
    #     for input in self.node.input_slots:
    #         input.implementation.update_pos()

    def itemChange(self, change, value):
        # If Moved
        if self.scene() and change in [QGraphicsItem.ItemPositionChange, QGraphicsItem.ItemPositionHasChanged]:
            # Update Node's position
            self.node.position = (self.pos().x(), self.pos().y())
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
