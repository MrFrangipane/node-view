import pickle
import tempfile
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

class SlotDotPySide(QGraphicsItem):
    def __init__(self,x=0 ,y=0, slot=None, parent=None):
        super(SlotDotPySide, self).__init__()
        #args
        self.x = x
        self.y = y
        self.slot = slot
        #attributes
        self.input_rect = QRect(self.x, self.y, SLOT_RADIUS, SLOT_RADIUS)
        self.color_pen = FRAME_SLOT_COLOR
        self.color_brush = (0,0,0)
        self._slot_input_hovered = False
        #mime data for dragdrop
        self.mimeSlot = QMimeData()
        self.mimePos = QMimeData()
        #creation du path du slot 'nodename|slotname'
        self.slot.path_name = self.slot.parent_node.name + '|' + self.slot.name
        #setflag pour hover et drops
        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)

    def boundingRect(self):
        return self.input_rect

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            event.ignore()
            return
        self.mimeSlot.setText(self.slot.path_name)

    def dragEnterEvent(self, event):
        event.setAccepted(True)

    def dropEvent(self, event):
        self.dragOver = False
        self.slot.connect_to = event.mimeData().text()
        self.eval_connection_slot()

    def mouseMoveEvent(self, event):
        if QLineF(QPointF(event.screenPos()), QPointF(
                event.buttonDownScreenPos(Qt.LeftButton))).length() < QApplication.startDragDistance():
            return
        drag = QDrag(event.widget())
        drag.setMimeData(self.mimeSlot)
        drag.exec_()

    def eval_connection_slot(self):
        for item in self.scene().items():
            if isinstance(item, SlotPySide):
                if item.objectName() == self.slot.connect_to:
                    self.slot.connect(item.slot)
                    break
        #MARCHE PAS JE SAIS PAS POURQUOIIII :
        #print self.scene().findChild(QGraphicsObject, self.slot.connect_to)

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
        painter.drawEllipse(self.input_rect)



class SlotPySide(QGraphicsObject):
    def __init__(self, x, y, slot=AbstractSlot):
        super(SlotPySide, self).__init__()
        self.x = x
        self.y = y
        self.slot = slot

        self.input_rect = QRect(self.x, self.y, WIDTH, ROW_HEIGHT)

        self.dot = SlotDotPySide(self.input_rect.x(), self.input_rect.y()+1, slot=self.slot)
        self.dot.setParentItem(self)

        self.setObjectName(self.dot.slot.path_name)

        self.text = self.slot.name
        self.text_color = TEXT_COLOR
        self.text_align = Qt.AlignLeft

        self.setAcceptDrops(True)
        self.mime = QMimeData()

    def boundingRect(self):
        return self.input_rect

    def paint(self, painter, option, widget):
        painter.setPen(_color(self.text_color))
        painter.drawText(self.input_rect, self.text_align, self.text)



class InputSlotPySide(SlotPySide):
    def __init__(self,x,y,slot=InputSlot):
        super(InputSlotPySide, self).__init__(x, y, slot=slot)
        self.x = 0
        self.dot.color_brush = BRUSH_INPUTSLOT_COLOR

class OutputSlotPySide(SlotPySide):
    def __init__(self,x,y,slot=InputSlot):
        super(OutputSlotPySide, self).__init__(x, y, slot=slot)
        self.dot.setPos(WIDTH,0)
        self.dot.color_brush = BRUSH_OUTPUTSLOT_COLOR
        self.text_align = Qt.AlignRight