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
Created on 5 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore
from Data.NotePosition import NotePosition
from DBFSMEvents import MeasureLineContext

class QMeasureLine(QtGui.QGraphicsItem):
    '''
    classdocs
    '''


    def __init__(self, qScore, lastMeasure, nextMeasure, index,
                 staffIndex, parent = None):
        '''
        Constructor
        '''
        super(QMeasureLine, self).__init__(parent)
        self._qStaff = parent
        self._qScore = qScore
        self._props = qScore.displayProperties
        self._height = None
        self._rect = QtCore.QRectF(0, 0, 0, 0)
        self._lastMeasure = lastMeasure
        self._nextMeasure = nextMeasure
        self._painter = None
        self._setPainter()
        self._index = index
        self._base = 0
        self._staffIndex = staffIndex
        self.setDimensions()
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return self._rect

    def _setPainter(self):
        self._painter = PAINTER_FACTORY(self._lastMeasure, self._nextMeasure)

    def paint(self, painter, dummyOption, dummyWidget = None):
        self._painter(self, painter, dummyOption,
                      self._qScore.scale, self._base, dummyWidget = None)

    def _setHeight(self):
        if self._props.emptyLinesVisible:
            self._height = self._qScore.ySpacing * self._qScore.kitSize
        else:
            score = self._qScore.score
            self._height = (self._qScore.ySpacing *
                            score.numVisibleLines(self._staffIndex))
        if self._props.measureCountsVisible:
            self._base = self._props.measureCountHeight()
        self._height += self._base

    def setDimensions(self):
        self.prepareGeometryChange()
        self._setHeight()
        self._rect.setBottomRight(QtCore.QPointF(self._qScore.xSpacing,
                                                 self._height))

    def xSpacingChanged(self):
        self.prepareGeometryChange()
        self._rect.setRight(self._qScore.xSpacing)

    def ySpacingChanged(self):
        self._setHeight()
        self.prepareGeometryChange()
        self._rect.setBottom(self._height)

    def height(self):
        return self._height

    def width(self):
        return self._qScore.xSpacing

    def _getEndNotePosition(self):
        if self._index == 0:
            return None
        np = NotePosition(measureIndex = self._index - 1)
        return self._qStaff.augmentNotePosition(np)

    def _getStartNotePosition(self):
        np = NotePosition(measureIndex = self._index)
        return self._qStaff.augmentNotePosition(np)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            event.accept()
            fsmEvent = MeasureLineContext(self._lastMeasure, self._nextMeasure,
                                          self._getEndNotePosition(),
                                          self._getStartNotePosition(),
                                          event.screenPos())
            self._qScore.sendFsmEvent(fsmEvent)
        else:
            event.ignore()

    def hoverEnterEvent(self, *args, **kwargs):
        self._qScore.setStatusMessage("Right-click for barline options.")
        return super(QMeasureLine, self).hoverEnterEvent(*args, **kwargs)

    def hoverLeaveEvent(self, *args, **kwargs):
        self._qScore.setStatusMessage()
        return super(QMeasureLine, self).hoverLeaveEvent(*args, **kwargs)

#pylint:disable-msg=R0913
class BarLinePainter(object):
    THICK_LINE_WIDTH = 3
    THICK_LINE_OFFSET = 1
    EXTRA_LINE_OFFSET = 3
    DOT_OFFSET = 5
    DOT_RADIUS = 2

    def __call__(self, qMeasureLine, painter, dummyOption,
                 dummyScale, base, dummyWidget = None):
        raise NotImplementedError()

    @classmethod
    def _clearBase(cls, painter, palette, boundingRect):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(palette.base())
        painter.drawRect(boundingRect)

    @classmethod
    def _drawThickLine(cls, painter, xCenter, yBase, height, palette, scale):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(palette.text())
        painter.drawRect(xCenter - cls.THICK_LINE_OFFSET * scale, yBase,
                         cls.THICK_LINE_WIDTH * scale, height + 1)

    @classmethod
    def _drawDot(cls, painter, x, y, palette, scale):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(palette.text())
        painter.drawEllipse(QtCore.QPointF(x, y),
                            cls.DOT_RADIUS * scale, cls.DOT_RADIUS * scale)

    @classmethod
    def _drawExtraLineBefore(cls, painter, xCenter, yBase, height, palette, scale):
        painter.setPen(QtCore.Qt.SolidLine)
        painter.setBrush(palette.text())
        painter.drawLine(xCenter - cls.EXTRA_LINE_OFFSET * scale, yBase,
                         xCenter - cls.EXTRA_LINE_OFFSET * scale, height)

    @classmethod
    def _drawExtraLineAfter(cls, painter, xCenter, yBase, height, palette, scale):
        painter.setPen(QtCore.Qt.SolidLine)
        painter.setBrush(palette.text())
        painter.drawLine(xCenter + cls.EXTRA_LINE_OFFSET * scale, yBase,
                         xCenter + cls.EXTRA_LINE_OFFSET * scale, height)

    @classmethod
    def _drawRepeatBefore(cls, painter, xCenter, yBase, height, palette, scale):
        cls._drawExtraLineBefore(painter, xCenter, yBase, height, palette, scale)
        y = height / 3
        cls._drawDot(painter,
                     xCenter - cls.DOT_OFFSET * scale, yBase + y, palette, scale)
        cls._drawDot(painter,
                     xCenter - cls.DOT_OFFSET * scale, yBase + 2 * y, palette, scale)

    @classmethod
    def _drawRepeatAfter(cls, painter, xCenter, yBase, height, palette, scale):
        cls._drawExtraLineAfter(painter, xCenter, yBase, height, palette, scale)
        y = height / 3
        cls._drawDot(painter,
                     xCenter + cls.DOT_OFFSET * scale, yBase + y, palette, scale)
        cls._drawDot(painter,
                     xCenter + cls.DOT_OFFSET * scale, yBase + 2 * y, palette, scale)

class NormalBarLinePainter(BarLinePainter):
    def __call__(self, qMeasureLine, painter,
                 dummyOption, dummyScale, base, dummyWidget = None):
        palette = qMeasureLine.scene().palette()
        self._clearBase(painter, palette, qMeasureLine.boundingRect())
        painter.setPen(QtCore.Qt.SolidLine)
        x = qMeasureLine.width() / 2
        painter.drawLine(x, base, x, qMeasureLine.height())

class RepeatStartLinePainter(BarLinePainter):
    def __call__(self, qMeasureLine, painter,
                 dummyOption, scale, base, dummyWidget = None):
        palette = qMeasureLine.scene().palette()
        self._clearBase(painter, palette, qMeasureLine.boundingRect())
        x = qMeasureLine.width() / 2
        height = qMeasureLine.height() - base
        self._drawThickLine(painter, x, base, height, palette, scale)
        self._drawRepeatAfter(painter, x, base, height, palette, scale)


class RepeatEndLinePainter(BarLinePainter):
    def __call__(self, qMeasureLine, painter,
                 dummyOption, scale, base, dummyWidget = None):
        palette = qMeasureLine.scene().palette()
        self._clearBase(painter, palette, qMeasureLine.boundingRect())
        x = qMeasureLine.width() / 2
        height = qMeasureLine.height() - base
        self._drawThickLine(painter, x, base, height, palette, scale)
        self._drawRepeatBefore(painter, x, base, height, palette, scale)

class RepeatStartEndLinePainter(BarLinePainter):
    def __call__(self, qMeasureLine, painter,
                 dummyOption, scale, base, dummyWidget = None):
        palette = qMeasureLine.scene().palette()
        self._clearBase(painter, palette, qMeasureLine.boundingRect())
        x = qMeasureLine.width() / 2
        height = qMeasureLine.height() - base
        self._drawThickLine(painter, x, base, height , palette, scale)
        self._drawRepeatBefore(painter, x, base, height, palette, scale)
        self._drawRepeatAfter(painter, x, base, height, palette, scale)

class SectionEndLinePainter(BarLinePainter):
    def __call__(self, qMeasureLine, painter,
                 dummyOption, scale, base, dummyWidget = None):
        palette = qMeasureLine.scene().palette()
        self._clearBase(painter, palette, qMeasureLine.boundingRect())
        x = qMeasureLine.width() / 2
        height = qMeasureLine.height() - base
        self._drawThickLine(painter, x, base, height, palette, scale)
        self._drawExtraLineBefore(painter, x, base, height, palette, scale)

class BarLinePainterFactory(object):
    def __init__(self):
        self._painterCache = {}
        self._normalLinePainter = NormalBarLinePainter()
        self._painterCache[(True, False, False)] = RepeatStartLinePainter()
        self._painterCache[(False, True, False)] = RepeatEndLinePainter()
        self._painterCache[(True, True, False)] = RepeatStartEndLinePainter()
        self._painterCache[(False, False, True)] = SectionEndLinePainter()
        self._painterCache[(False, True, True)] = RepeatEndLinePainter()

    @staticmethod
    def _pairKey(lastMeasure, nextMeasure):
        key = (nextMeasure is not None and nextMeasure.isRepeatStart(),
               lastMeasure is not None and lastMeasure.isRepeatEnd(),
               lastMeasure is not None and lastMeasure.isSectionEnd())
        return key

    def __call__(self, lastMeasure, nextMeasure):
        pairKey = self._pairKey(lastMeasure, nextMeasure)
        return self._painterCache.get(pairKey, self._normalLinePainter)

PAINTER_FACTORY = BarLinePainterFactory()

