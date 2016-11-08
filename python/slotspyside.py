from PySide.QtGui import *
from PySide.QtCore import *

from slots import *

WIDTH = 200
HEADER_HEIGHT = 40
ROW_HEIGHT = 25

BACKGROUND_COLOR = (.22, .22, .22, 1)
FRAME_SLOT_COLOR = (0, 0, 0)
BRUSH_INPUTSLOT_COLOR = (1, 0.5, 1)
BRUSH_OUTPUTSLOT_COLOR = (0.5, 1, 1)

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
TEXT_DOT_PADDING = 12

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
def _color(values):
    return QColor.fromRgbF(*values)

slot = InputSlot('lalislot')


class SlotDotPySide(QGraphicsItem, QGraphicsLayoutItem):
    def __init__(self,x=0 ,y=0, parent=None):
        super(SlotDotPySide, self).__init__()

        input_rect = QRect(x, y, SLOT_RADIUS, SLOT_RADIUS)

        self.tmp_dict = {'slot':input_rect}
        self._slot_input_hovered = False

        self.setAcceptDrops(True)
        self.setAcceptHoverEvents(True)

        self.color_pen = FRAME_SLOT_COLOR
        self.color_brush = (0,0,0)

    def boundingRect(self):
        return self.tmp_dict['slot']

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            event.ignore()
            return

    def mouseMoveEvent(self, event):
        if QLineF(QPointF(event.screenPos()), QPointF(
                event.buttonDownScreenPos(Qt.LeftButton))).length() < QApplication.startDragDistance():
            return
        drag = QDrag(event.widget())
        mime = QMimeData()
        drag.setMimeData(mime)
        mime.setText(self.tmp_dict.keys()[0])
        drag.exec_()

    def dragEnterEvent(self, event):
        event.setAccepted(True)

    def dropEvent(self, event):
        print "dropped"

    def hoverMoveEvent(self, event):
        self._slot_input_hovered = True
        self.prepareGeometryChange()

    def hoverLeaveEvent(self, event):
        self._slot_input_hovered = False
        self.prepareGeometryChange()

    def paint(self, painter, option, widget):
        painter.setPen(_color(self.color_pen))
        painter.setBrush(_color(self.color_brush))
        if self._slot_input_hovered:
            painter.setBrush(_color((1, 1, 1)))
        painter.drawEllipse(self.tmp_dict['slot'])

class SlotPySide(QGraphicsItem):
    def __init__(self, x, y, slot=AbstractSlot):
        super(SlotPySide, self).__init__()
        self.x = x
        self.y = y

        self.input_rect = QRect(x, y, 100, SLOT_RADIUS+2)

        self.dot = SlotDotPySide(self.x, self.y - SLOT_RADIUS)
        self.dot.setParentItem(self)

        self.slot = slot
        self.text = self.slot.name
        self.text_color = TEXT_COLOR


    def boundingRect(self):
        return self.input_rect

    def paint(self, painter, option, widget):
        # Input Labels
        #painter.setFont(SLOT_FONT)
        painter.setPen(_color(self.text_color))
        painter.drawText(self.x + TEXT_DOT_PADDING, self.y, self.text)

class InputSlotPySide(SlotPySide):
    def __init__(self,x,y,slot=InputSlot):
        super(InputSlotPySide, self).__init__(x, y, slot=slot)
        self.x = 0
        self.dot.color_brush = BRUSH_INPUTSLOT_COLOR

class OutputSlotPySide(SlotPySide):
    def __init__(self,x,y,slot=InputSlot):
        super(OutputSlotPySide, self).__init__(x, y, slot=slot)
        self.dot.color_brush = BRUSH_OUTPUTSLOT_COLOR