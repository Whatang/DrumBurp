'''
Created on 19 Jan 2011

@author: Mike Thomas
'''
from PyQt4 import QtGui, QtCore
from Data import DBConstants

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

    def xSpacingChanged(self):
        self.prepareGeometryChange()
        self._rect.setRight(self.cellWidth())

    def ySpacingChanged(self):
        self.prepareGeometryChange()
        self._rect.setBottom(self.cellHeight())

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

    def cellWidth(self):
        raise NotImplementedError()

    def cellHeight(self):
        raise NotImplementedError()
