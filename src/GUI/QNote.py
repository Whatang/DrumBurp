'''
Created on 5 Dec 2010

@author: Mike Thomas

'''
from PyQt4 import QtGui, QtCore
from Data import DBConstants
from Data.NotePosition import NotePosition

_CHAR_PIXMAPS = {}
def _stringToPixMap(character, font, scene):
    key = (character, font.key())
    if key not in _CHAR_PIXMAPS:
        fm = QtGui.QFontMetrics(font)
        br = fm.tightBoundingRect(character)
        dx = -br.x() + 1
        dy = -br.y() + 1
        br.translate(dx, dy)
        pix = QtGui.QPixmap(br.width() + 2, br.height() + 2)
        painter = QtGui.QPainter(pix)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(scene.palette().base())
        painter.drawRect(0, 0, br.width() + 2, br.height() + 2)
        painter.setBrush(scene.palette().text())
        painter.setPen(QtCore.Qt.SolidLine)
        painter.setFont(font)
        painter.drawText(dx, dy, character)
        painter.end()
        _CHAR_PIXMAPS[key] = pix
    return _CHAR_PIXMAPS[key]


class QDBGridItem(QtGui.QGraphicsItem):
    def __init__(self, qScore, parent):
        super(QDBGridItem, self).__init__(parent = None,
                                          scene = qScore)
        self._text = ""
        self._qScore = qScore
        self._props = qScore.getProperties()
        self._rect = QtCore.QRectF(0, 0,
                                   self.cellWidth(),
                                   self.cellHeight())

    def setText(self, text):
        self._text = text
        self.update()

    def setDimensions(self):
        self.prepareGeometryChange()
        self._rect.setBottomRight(QtCore.QPointF(self.cellWidth(),
                                                 self.cellHeight()))

    def boundingRect(self):
        return self._rect

    def paint(self, painter, dummyOption, dummyWidget = None):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.scene().palette().base())
        painter.drawRect(self._rect)
        if len(self._text) > 0:
            painter.setPen(QtCore.Qt.SolidLine)
            if self._text == DBConstants.EMPTY_NOTE:
                y = self.cellHeight() / 2.0
                painter.drawLine(1, y,
                                 self.cellWidth() - 1, y)
            else:
                font = self._props.noteFont
                if font is None:
                    font = painter.font()
                pix = _stringToPixMap(self._text, font, self.scene())
                left = (self.cellWidth() - pix.width() + 2) / 2
                top = (self.cellHeight() - pix.height() + 2) / 2
                painter.drawPixmap(left, top, pix)

class QNote(QDBGridItem):
    '''
    classdocs
    '''

    def __init__(self, qScore, parent):
        super(QNote, self).__init__(qScore, parent)
        self._qMeasure = parent
        self._drumIndex = None
        self._noteTime = None
        self._notePosition = NotePosition()
        self._text = DBConstants.EMPTY_NOTE

    def toggleNote(self, head = None):
        np = NotePosition(drumIndex = self._drumIndex,
                          noteTime = self._noteTime)
        self._qMeasure.toggleNote(np, head)

    def setIndex(self, drumIndex, noteTime):
        if (drumIndex, noteTime) != (self._drumIndex, self._noteTime):
            self._drumIndex = drumIndex
            self._noteTime = noteTime
            self._notePosition.drumIndex = drumIndex
            self._notePosition.noteTime = noteTime

    def cellWidth(self):
        return self._props.xSpacing

    def cellHeight(self):
        return self._props.ySpacing

    def xSpacingChanged(self):
        self.prepareGeometryChange()
        self._rect.setRight(self.cellWidth())

    def ySpacingChanged(self):
        self.prepareGeometryChange()
        self._rect.setBottom(self.cellHeight())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            event.accept()
            menu = QtGui.QMenu()
            for noteHead in self._props.allowedNoteHeads():
                action = menu.addAction(noteHead)
                def noteAction(nh = noteHead):
                    self.toggleNote(nh)
                menu.connect(action, QtCore.SIGNAL("triggered()"), noteAction)
            menu.exec_(event.screenPos())
        elif event.button() == QtCore.Qt.RightButton:
            event.accept()
            menu = QtGui.QMenu()
            actionText = "Insert Default Measure"
            insertDefaultMeasureAction = menu.addAction(actionText)
            menu.connect(insertDefaultMeasureAction,
                         QtCore.SIGNAL("triggered()"),
                         self._qMeasure.insertMeasureBefore)
            deleteAction = menu.addAction("Delete Measure")
            menu.connect(deleteAction, QtCore.SIGNAL("triggered()"),
                         self._qMeasure.deleteMeasure)
            menu.addSeparator()
            insertMenu = menu.addMenu("Insert...")
            insertAfterAction = insertMenu.addAction("Default Measure After")
            insertMenu.connect(insertAfterAction,
                               QtCore.SIGNAL("triggered()"),
                               self._qMeasure.insertMeasureAfter)
            insertOtherMeasures = insertMenu.addAction("Other Measures")
            insertMenu.connect(insertOtherMeasures,
                               QtCore.SIGNAL("triggered()"),
                               self._qMeasure.insertOtherMeasures)
            menu.exec_(event.screenPos())
        else:
            event.ignore()


    def mouseReleaseEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton and
            self._qScore.getMousePressStartItem() == self):
            self.toggleNote()
            event.accept()
        else:
            event.ignore()

class QLineLabel(QDBGridItem):
    def __init__(self, lineName, qScore, parent):
        super(QLineLabel, self).__init__(qScore, parent)
        self._index = None
        self.setText(lineName)

    def cellHeight(self):
        return self._props.ySpacing

    def cellWidth(self):
        return self._props.LINELABELWIDTH

    def ySpacingChanged(self):
        self.prepareGeometryChange()
        self._rect.setBottom(self.cellHeight())

    def setIndex(self, index):
        self._index = index
