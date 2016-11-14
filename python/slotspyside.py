import pickle
import tempfile
from PySide.QtGui import *
from PySide.QtCore import *

from slots import *

WIDTH = 200
ROW_HEIGHT = 25

BACKGROUND_COLOR = (.22, .22, .22, 1)
FRAME_SLOT_COLOR = (0, 0, 0)
BRUSH_INPUTSLOT_COLOR = (1, 0.5, 1)
BRUSH_OUTPUTSLOT_COLOR = (0.5, 1, 1)

NAME_FONT = QFont()
NAME_FONT.setBold(True)
TEXT_COLOR = (1, 1, 1)

SLOT_RADIUS = 10
SLOT_COLOR_HOVERED = TEXT_COLOR

def _color(values):
    """
    Convert rgb value to hex color
    :param values: color as (r, g, b)
    :type values: tuple
    :return: QColor
    """
    return QColor.fromRgbF(*values)

class SlotDotPySide(QGraphicsItem):
    def __init__(self,x=0 ,y=0, slot=None, parent=None):
        """
        UI object it's the dot who manage connection, usually parent to SlotPySide objet. It manage drag and drop mode too
        :param x: x position
        :param y: y position
        :param slot: the Slot object from slots module passing from SlotPySide
        :param parent: it's parent item
        """
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
        self.dot_pos = self.mapToScene(self.input_rect)
        #creation du path du slot 'nodename|slotname'
        self.slot.path_name = self.slot.parent_node.name + '|' + self.slot.name
        #setflag pour hover et drops
        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)

    def update_pos(self):
        """
        update dot pos
        :return: None
        """
        mapped_pos = self.mapToScene(self.input_rect)
        self.dot_pos = (mapped_pos.boundingRect().x() + SLOT_RADIUS / 2.0,
                        mapped_pos.boundingRect().y() + SLOT_RADIUS / 2.0)

    #PySide def
    def boundingRect(self):
        return self.input_rect

    def mousePressEvent(self, event):
        #check left button
        if event.button() != Qt.LeftButton:
            event.ignore()
            return
        #mimeData creation for drag data
        self.mimePos = QMimeData()
        #Mime Data path name
        self.mimePos.setText(self.slot.path_name)

        ##Warn Scene
        #set click pos to scene
        self.scene()._mouse_previous_position = event.scenePos()
        #edge free creation
        if isinstance(self.parentItem(), InputSlotPySide):
            self.scene().input_slot_pressed(self.slot)
        if isinstance(self.parentItem(), OutputSlotPySide):
            self.scene().output_slot_pressed(self.slot)

    def mouseReleaseEvent(self, event):
        ##Warn scene
        #leave freeedge at release on dot
        self.scene()._leave_drawing_edge()

    def dragEnterEvent(self, event):
        event.setAccepted(True)
        #set hovered color during drag
        self._slot_input_hovered = True
        self.prepareGeometryChange()

    def dragLeaveEvent(self, event):
        #back color from hovered during drag
        self._slot_input_hovered = False
        self.prepareGeometryChange()

    def dropEvent(self, event):
        #assign path name from mimeData dropped to connect_to
        self.slot.connect_to = event.mimeData().text()
        #Call def for do connection
        self.eval_connection_slot()

    def mouseMoveEvent(self, event):
        super(SlotDotPySide, self).mouseMoveEvent(event)
        #begin drag at this condition
        if QLineF(QPointF(event.screenPos()), QPointF(
                event.buttonDownScreenPos(Qt.LeftButton))).length() < QApplication.startDragDistance():
            return
        #create drag object and store mmimeData on it
        drag = QDrag(event.widget())
        drag.setMimeData(self.mimePos)
        drag.setPixmap(QPixmap(1,1))
        drag.exec_(Qt.IgnoreAction)

    def eval_connection_slot(self):
        #TMP
        #search the right slot item
        for item in self.scene().items():
            if isinstance(item, SlotPySide):
                if item.objectName() == self.slot.connect_to:
                    #connect them
                    self.slot.connect(item.slot)
                    #exit
                    break
        #MARCHE PAS JE SAIS PAS POURQUOI:
        #print self.scene().findChild(InputSlotPySide, self.slot.connect_to)

    def hoverMoveEvent(self, event):
        #hovered without drag
        self._slot_input_hovered = True
        self.prepareGeometryChange()

    def hoverLeaveEvent(self, event):
        #leave hovered without drag
        self._slot_input_hovered = False
        self.prepareGeometryChange()

    def paint(self, painter, option, widget):
        #do paint
        painter.setPen(_color(self.color_pen))
        painter.setBrush(_color(self.color_brush))
        #paint hovered
        if self._slot_input_hovered:
            painter.setBrush(_color((1, 1, 1)))
        painter.drawEllipse(self.input_rect)

class SlotPySide(QGraphicsObject):
    def __init__(self, x, y, slot=AbstractSlot):
        """
        BaseUI class for InputSlotPySide and OutPutSlotPySide.
        :param x:
        :param y:
        :param slot:
        """
        super(SlotPySide, self).__init__()
        self.x = x
        self.y = y
        self.slot = slot
        #Attributes
        self.input_rect = QRect(self.x, self.y, WIDTH, ROW_HEIGHT)
        self.text = self.slot.name
        self.text_color = TEXT_COLOR
        self.text_align = Qt.AlignLeft
        #dot object
        self.dot = SlotDotPySide(self.input_rect.x(), self.input_rect.y()+1, slot=self.slot)
        self.dot.setParentItem(self)

        self.setObjectName(self.dot.slot.path_name)

    def update_pos(self):
        #update dot position
        self.dot.update_pos()

    def boundingRect(self):
        return self.input_rect

    def paint(self, painter, option, widget):
        painter.setPen(_color(self.text_color))
        painter.drawText(self.input_rect, self.text_align, self.text)

class InputSlotPySide(SlotPySide):
    def __init__(self,x,y,slot=InputSlot):
        """
        UI Slot derive from SlotPySide, set specifics values form input slot only
        :param x: x pos
        :param y: y pos
        :param slot: slot object from slots module
        """
        super(InputSlotPySide, self).__init__(x, y, slot=slot)
        #force to 0
        self.x = 0
        #change color
        self.dot.color_brush = self.slot.color

class OutputSlotPySide(SlotPySide):
    def __init__(self,x,y,slot=InputSlot):
        """
        UI Slot derive from SlotPySide, set specifics values form output slot only
        :param x: x pos
        :param y: y pos
        :param slot: slot object from slots module
        """
        super(OutputSlotPySide, self).__init__(x, y, slot=slot)
        #move dot position
        self.dot.setPos(WIDTH,0)
        #change color
        self.dot.color_brush = self.slot.color
        #switch align text to right
        self.text_align = Qt.AlignRight

    def boundingRect(self):
        #tweak bounding rect for get right rect and extra out side
        return QRect(self.x + 50, self.y, WIDTH - 50 , ROW_HEIGHT)

