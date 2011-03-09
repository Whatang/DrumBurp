'''
Created on 19 Jan 2011

@author: Mike Thomas
'''
from PyQt4 import QtGui, QtCore
from Data import DBConstants

#pylint: disable-msg=R0921
class QDBGridItem(QtGui.QGraphicsItem):
    def __init__(self, qScore, parent):
        super(QDBGridItem, self).__init__(parent = None,
                                          scene = qScore)
        self._text = ""
        self._props = qScore.displayProperties
        self._rect = QtCore.QRectF(0, 0,
                                   self.cellWidth(),
                                   self.cellHeight())
        self._highlighted = False

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
                br = QtGui.QFontMetrics(font).tightBoundingRect(self._text)
                w = br.width()
                h = br.height()
                textLocation = QtCore.QPointF((self.cellWidth() - w + 2) / 2,
                                              (self.cellHeight() + h) / 2)
                painter.drawText(textLocation, self._text)
        if self._highlighted:
            painter.setPen(QtCore.Qt.SolidLine)
            painter.setPen(self.scene().palette().highlight().color())
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawRect(0, 0, self.cellWidth() - 1, self.cellHeight())

    def cellWidth(self):
        raise NotImplementedError()

    def cellHeight(self):
        raise NotImplementedError()

    def setHighlight(self, onOff):
        if onOff != self._highlighted:
            self._highlighted = onOff
            self.update()

