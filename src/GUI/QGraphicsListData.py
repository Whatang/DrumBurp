# Copyright 2011-12 Michael Thomas
#
# See www.whatang.org for more information.
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DrumBurp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DrumBurp.  If not, see <http://www.gnu.org/licenses/>
'''
Created on 13 Mar 2011

@author: Mike Thomas

'''


from PyQt4.QtGui import QGraphicsItem, QFontMetrics
from PyQt4.QtCore import QPoint, QRectF, QPointF, Qt

class QGraphicsListData(QGraphicsItem):
    '''
    classdocs
    '''

    _editName = ""

    def __init__(self, qScore, parent = None):
        '''
        Constructor
        '''
        super(QGraphicsListData, self).__init__(parent = parent, scene = qScore)
        self._qScore = qScore
        self._props = qScore.displayProperties
        self._rect = QRectF(0, 0, 0, 0)
        self.setRect()
        self.setCursor(Qt.PointingHandCursor)
        self.setAcceptsHoverEvents(True)

    def _iterData(self):
        raise NotImplementedError()

    def _dataLen(self):
        raise NotImplementedError()

    def font(self):
        raise NotImplementedError()

    def setRect(self, fm = None):
        if fm is None:
            font = self.font()
            if font is None:
                return
            fm = QFontMetrics(font)
        lineHeight = fm.height()
        height = lineHeight * self._dataLen() * 1.1
        width = max(fm.width(data) for data in self._iterData()) + 10
        if height != self._rect.height() or width != self._rect.width():
            self.prepareGeometryChange()
            self._rect.setBottomRight(QPointF(width, height))

    def boundingRect(self):
        return self._rect

    def paint(self, painter, dummyOption, dummyWidget = None):
        painter.save()
        try:
            font = self.font()
            if font is None:
                font = painter.font()
            else:
                painter.setFont(font)
            fm = QFontMetrics(painter.font())
            self.setRect(fm)
            lineHeight = fm.height()
            for index, data in enumerate(self._iterData()):
                painter.drawText(QPoint(5, (index + 1) * lineHeight), data)
        finally:
            painter.restore()

    def fontChanged(self):
        self.update()

    def update(self):
        self.setRect()
        super(QGraphicsListData, self).update()

    def hoverEnterEvent(self, *args, **kwargs):
        self._qScore.setStatusMessage("Double click to edit %s."
                                      % self._editName)
        return super(QGraphicsListData, self).hoverEnterEvent(*args, **kwargs)

    def hoverLeaveEvent(self, *args, **kwargs):
        self._qScore.setStatusMessage()
        return super(QGraphicsListData, self).hoverLeaveEvent(*args, **kwargs)
