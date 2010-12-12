'''
Created on 5 Dec 2010

@author: Mike Thomas

'''
from PyQt4 import QtGui, QtCore
from Data import Constants
from DBSignals import XSPACING_SIGNAL, YSPACING_SIGNAL
OFFSET = 24

_charMaps = {}
def _stringToPixMap(character, font, scene):
    key = (character, font.key())
    if key not in _charMaps:
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
        _charMaps[key] = pix
    return _charMaps[key]


class QDBGridItem(QtGui.QGraphicsItem):
    def __init__(self, lineIndex, scoreScene, parent = None):
        super(QDBGridItem, self).__init__(parent = parent,
                                          scene = scoreScene)
        self.catcher = QtCore.QObject()
        self._scene = scoreScene
        self.catcher.connect(self._scene, QtCore.SIGNAL(XSPACING_SIGNAL),
                             self._xSpacingChanged)
        self.catcher.connect(self._scene, QtCore.SIGNAL(YSPACING_SIGNAL),
                             self._ySpacingChanged)
        self._system = parent
        self._text = ""
        self._lineIndex = lineIndex
        self._rect = QtCore.QRectF(0, 0,
                                   self.cellWidth(), self.cellHeight())

    def setText(self, text):
        self._text = text
        self.update()

    def boundingRect(self):
        return self._rect

    def paint(self, painter, dummyOption, dummyWidget = None):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self._scene.palette().base())
        painter.drawRect(self._rect)
        if len(self._text) > 0:
            painter.setPen(QtCore.Qt.SolidLine)
            if self._text == Constants.EMPTY_NOTE:
                y = self.cellHeight() / 2.0
                painter.drawLine(1, y,
                                 self.cellWidth() - 1, y)
            else:
                font = self._scene.noteFont
                if font is None:
                    font = painter.font()
                pix = _stringToPixMap(self._text, font, self._scene)
                left = (self.cellWidth() - pix.width() + 2) / 2
                top = (self.cellHeight() - pix.height() + 2) / 2
                painter.drawPixmap(left, top, pix)
#        painter.setPen(QtCore.Qt.DotLine)
#        painter.drawLine(self.cellWidth() / 2, 0, self.cellWidth() / 2, self.cellHeight())
#        painter.drawLine(0, self.cellHeight() / 2, self.cellWidth(), self.cellHeight() / 2)


    def cellWidth(self):
        return self._scene.xSpace

    def cellHeight(self):
        return self._scene.ySpace

    def xPosition(self):
        raise NotImplementedError()

    def yPosition(self):
        raise NotImplementedError()

    def _xSpacingChanged(self):
        self.prepareGeometryChange()
        self._rect.setRight(self.cellWidth())
        self.setPos(self.xPosition(), self.y())

    def _ySpacingChanged(self):
        self.prepareGeometryChange()
        self._rect.setBottom(self.cellHeight())
        self.setPos(self.x(), self.yPosition())

class QNote(QDBGridItem):
    '''
    classdocs
    '''


    def __init__(self, timeIndex, lineIndex, scoreScene, parent = None):
        super(QNote, self).__init__(lineIndex, scoreScene, parent)
        self._timeIndex = timeIndex
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)

    def toggleNote(self, head):
        self._system.toggleNote(self._timeIndex, self._lineIndex, head)

    def xPosition(self):
        return OFFSET + self._timeIndex * self.cellWidth()

    def yPosition(self):
        return (self._scene.numLines - self._lineIndex - 1) * self._scene.ySpace

class QLineLabel(QDBGridItem):
    def __init__(self, lineName, lineIndex, scoreScene, parent = None):
        super(QLineLabel, self).__init__(lineIndex, scoreScene, parent)
        self.setText(lineName)

    def cellWidth(self):
        return OFFSET

    def xPosition(self):
        return 0

    def yPosition(self):
        return (self._scene.numLines - self._lineIndex - 1) * self._scene.ySpace
