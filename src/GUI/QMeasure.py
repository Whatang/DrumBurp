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
from Data import DBConstants

from DBFSMEvents import (LeftPress, MidPress, RightPress,
                         EditMeasureProperties,
                         MouseMove, MouseRelease,
                         ChangeRepeatCount,
                         SetAlternateEvent)

def _painter_saver(method):
    def wrapper(self, painter, *args, **kwargs):
        painter.save()
        try:
            method(self, painter, *args, **kwargs)
        finally:
            painter.restore()
    return wrapper

class QMeasure(QtGui.QGraphicsItem):
    '''
    classdocs
    '''


    def __init__(self, index, qScore, measure, parent):
        '''
        Constructor
        '''
        super(QMeasure, self).__init__(parent)
        self._props = qScore.displayProperties
        self._qScore = qScore
        self._measure = None
        self._index = index
        self._width = 0
        self._height = 0
        self._base = 0
        self._measureCount = qScore.score.getMeasureIndex(self.measurePosition())
        self._highlight = None
        self._rect = QtCore.QRectF(0, 0, 0, 0)
        self._repeatCountRect = None
        self._alternate = None
        self._playing = False
        self._dragHighlight = False
        self._potentials = []
        self._potentialDrum = None
        self._potentialHead = None
        self._potentialSet = None
        self.setAcceptsHoverEvents(True)
        self._setMeasure(measure)

    def numLines(self):
        return self.parentItem().numLines()

    def lineIndex(self, index):
        return self.parentItem().lineIndex(index)

    def _setDimensions(self):
        self.prepareGeometryChange()
        self._width = self._qScore.xSpacing * len(self._measure)
        self._height = self.numLines() * self._qScore.ySpacing
        self._height += self.parentItem().alternateHeight()
        if self._props.beatCountVisible:
            self._height += self._qScore.ySpacing
        self._base = 0
        if self._props.measureCountsVisible:
            self._base = self._props.measureCountHeight()
        self._height += self._base
        self._rect.setBottomRight(QtCore.QPointF(self._width, self._height))

    def boundingRect(self):
        return self._rect

    def width(self):
        return self._width

    def height(self):
        return self._height

    def _setMeasure(self, measure):
        if self._measure != measure:
            self._measure = measure
            self._setDimensions()
            self.update()

    @_painter_saver
    def _paintNotes(self, painter, xValues):
        font = painter.font()
        fontMetric = QtGui.QFontMetrics(font)
        baseline = (self.numLines() - 1) * self._qScore.ySpacing + self._base + self.parentItem().alternateHeight()
        dot = self._qScore.scale
        potential = False
        for drumIndex in range(0, self.numLines()):
            lineHeight = baseline + (self._qScore.ySpacing / 2.0) - 1
            lineIndex = self.lineIndex(drumIndex)
            for noteTime, x in enumerate(xValues):
                if (lineIndex == self._potentialDrum
                    and noteTime in self._potentialSet):
                    text = self._potentialHead
                    potential = True
                    painter.setPen(QtGui.QColor(QtCore.Qt.blue))
                else:
                    text = self._measure.noteAt(noteTime, lineIndex)
                if text == DBConstants.EMPTY_NOTE:
                    painter.drawLine(x + dot, lineHeight,
                                     x + self._qScore.xSpacing - dot,
                                     lineHeight)
                else:
                    br = fontMetric.tightBoundingRect(text)
                    left = x + (self._qScore.xSpacing - br.width() + 2) / 2 - 2
                    offset = br.y() - (self._qScore.ySpacing - br.height()) / 2
                    painter.drawText(QtCore.QPointF(left, baseline - offset),
                                     text)
                if potential:
                    painter.setPen(QtGui.QColor(QtCore.Qt.black))
                    potential = False
            baseline -= self._qScore.ySpacing

    @_painter_saver
    def _paintHighlight(self, painter, xValues):
        noteTime, drumIndex = self._highlight
        baseline = (self.numLines() - drumIndex - 1) * self._qScore.ySpacing + self._base + self.parentItem().alternateHeight()
        countLine = (self.numLines() + 1) * self._qScore.ySpacing + self._base
        x = xValues[noteTime]
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(QtCore.Qt.yellow).lighter())
        painter.drawRect(x, baseline,
                         self._qScore.xSpacing - 1, self._qScore.ySpacing - 1)
        painter.drawRect(x, countLine,
                         self._qScore.xSpacing - 1,
                         self._qScore.ySpacing - 1)
        painter.setPen(self._qScore.palette().text().color())

    @_painter_saver
    def _paintBeatCount(self, painter, xValues):
        font = painter.font()
        fontMetric = QtGui.QFontMetrics(font)
        baseline = (self.numLines() * self._qScore.ySpacing) + self._base + self.parentItem().alternateHeight()
        for noteTime, count in enumerate(self._measure.count()):
            x = xValues[noteTime]
            br = fontMetric.tightBoundingRect(count)
            left = x + (self._qScore.xSpacing - br.width()) / 2 - 2
            offset = br.y() - (self._qScore.ySpacing - br.height()) / 2
            painter.drawText(QtCore.QPointF(left, baseline - offset), count)

    @_painter_saver
    def _paintRepeatCount(self, painter):
        spacing = self._qScore.scale
        painter.setPen(self._qScore.palette().text().color())
        repeatText = '%dx' % self._measure.repeatCount
        textWidth = QtGui.QFontMetrics(painter.font()).width(repeatText)
        textLocation = QtCore.QPointF(self.width() - textWidth - 2 * spacing,
                                      self.parentItem().alternateHeight() + self._base - spacing)
        painter.drawText(textLocation, repeatText)
        if self._repeatCountRect is None:
            self._repeatCountRect = QtCore.QRectF(0, 0, 0, 0)
        self._repeatCountRect.setSize(QtCore.QSizeF(textWidth,
                                                    self.parentItem().alternateHeight()))
        self._repeatCountRect.setTopRight(QtCore.QPointF(self.width() - 2 * spacing, self._base - spacing))

    @_painter_saver
    def _paintAlternate(self, painter):
        altHeight = self.parentItem().alternateHeight()
        spacing = self._qScore.scale
        painter.setPen(self._qScore.palette().text().color())
        painter.drawLine(0, self._base, self.width() - spacing * 2, self._base)
        painter.drawLine(0, self._base, 0, altHeight - spacing * 2 + self._base)
        font = painter.font()
        font.setItalic(True)
        painter.setFont(font)
        if self._alternate is None:
            self._alternate = QtCore.QRectF(0, 0, 0, 0)
        text = self._measure.alternateText
        textWidth = QtGui.QFontMetrics(font).width(text)
        self._alternate.setSize(QtCore.QSizeF(textWidth, altHeight))
        bottomLeft = QtCore.QPointF(2 * spacing, altHeight - spacing + self._base)
        self._alternate.setBottomLeft(bottomLeft)
        painter.drawText(2 * spacing, altHeight - spacing + self._base, text)

    @_painter_saver
    def _paintPlayingHighlight(self, painter):
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtCore.Qt.blue)
        painter.drawRect(-1, -1, self.width() + 1, self.height() + 1)
        painter.setPen(QtGui.QColor(QtCore.Qt.blue).lighter())
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

    @_painter_saver
    def _paintMeasureCount(self, painter):
        painter.setPen(QtCore.Qt.black)
        font = painter.font()
        font.setItalic(True)
        painter.setFont(font)
        painter.drawText(1, self._base, "%d" % self._measureCount)

    def paint(self, painter, dummyOption, dummyWidget = None):
        painter.save()
        if self._dragHighlight:
            color = QtGui.QColor(QtCore.Qt.gray).lighter()
            painter.setBrush(color)
            painter.setPen(color)
            painter.drawRect(self._rect)
        painter.setPen(QtCore.Qt.SolidLine)
        font = self._props.noteFont
        if font is None:
            font = painter.font()
        painter.setFont(font)
        xValues = [noteTime * self._qScore.xSpacing
                   for noteTime in range(0, len(self._measure))]
        if self._highlight:
            self._paintHighlight(painter, xValues)
        self._paintNotes(painter, xValues)
        if self._props.beatCountVisible:
            self._paintBeatCount(painter, xValues)
        if self._props.measureCountsVisible:
            self._paintMeasureCount(painter)
        if self._measure.isRepeatEnd() and self._measure.repeatCount > 2:
            self._paintRepeatCount(painter)
        else:
            self._repeatCountRect = None
        if self._playing:
            self._paintPlayingHighlight(painter)
        if self._measure.alternateText is not None:
            self._paintAlternate(painter)
        else:
            self._alternate = None
        painter.restore()

    def dataChanged(self, notePosition):
        if None not in (notePosition.noteTime, notePosition.drumIndex):
            self.update()
        else:
            self._setDimensions()
            self.update()
            self.parentItem().placeMeasures()

    def xSpacingChanged(self):
        self._setDimensions()
        self.update()

    def ySpacingChanged(self):
        self._setDimensions()
        self.update()

    def _isOverNotes(self, point):
        return (0 <= ((point.y() - self._base - self.parentItem().alternateHeight()) / self._qScore.ySpacing)
                < self.numLines())

    def _isOverCount(self, point):
        return ((point.y() - self._base - self.parentItem().alternateHeight()) / self._qScore.ySpacing) >= self.numLines() + 1

    def _isOverRepeatCount(self, point):
        return (self._repeatCountRect is not None
                and self._repeatCountRect.contains(point))

    def _isOverAlternate(self, point):
        return (self._alternate is not None
                and self._alternate.contains(point))


    def _getMouseCoords(self, point):
        x = self._getNoteTime(point)
        y = self.numLines() - int((point.y() - self._base - self.parentItem().alternateHeight()) / self._qScore.ySpacing) - 1
        return x, y

    def _getNotePosition(self, point):
        x, y = self._getMouseCoords(point)
        y = self.lineIndex(y)
        return x, y

    def _getNoteTime(self, point):
        return int(point.x() / self._qScore.xSpacing)

    def _hovering(self, event):
        point = self.mapFromScene(event.scenePos())
        if self._isOverNotes(point):
            newPlace = self._getMouseCoords(point)
            if newPlace != self._highlight:
                self._highlight = newPlace
                self.update()
                self.parentItem().setLineHighlight(newPlace[1])
                realIndex = self.parentItem().lineIndex(newPlace[1])
                self._qScore.setCurrentHeads(realIndex)
        elif self._highlight != None:
            self._highlight = None
            self.parentItem().clearHighlight()
            self.update()
        if self._isOverCount(point):
            self._qScore.setStatusMessage("Double click to edit measure count.")
            self.setCursor(QtCore.Qt.PointingHandCursor)
        elif self._isOverRepeatCount(point):
            self._qScore.setStatusMessage("Double click to edit repeat count.")
            self.setCursor(QtCore.Qt.PointingHandCursor)
        elif self._isOverAlternate(point):
            self._qScore.setStatusMessage("Double click to edit "
                                          "alternate ending.")
            self.setCursor(QtCore.Qt.PointingHandCursor)
        else:
            self._qScore.setStatusMessage()
            self.setCursor(QtCore.Qt.ArrowCursor)

    def hoverEnterEvent(self, event):
        self._hovering(event)

    def hoverMoveEvent(self, event):
        self._hovering(event)

    def hoverLeaveEvent(self, event_):
        self._highlight = None
        self.update()
        self.parentItem().clearHighlight()
        self._qScore.setCurrentHeads(None)
        self.setCursor(QtCore.Qt.ArrowCursor)

    def mousePressEvent(self, event):
        point = self.mapFromScene(event.scenePos())
        eventType = LeftPress
        np = None
        if self._isOverNotes(point):
            noteTime, drumIndex = self._getNotePosition(point)
            np = self.makeNotePosition(noteTime, drumIndex)
            if event.button() == QtCore.Qt.MidButton:
                eventType = MidPress
            elif event.button() == QtCore.Qt.RightButton:
                eventType = RightPress
        self._qScore.sendFsmEvent(eventType(self, np, event.screenPos()))

    def mouseMoveEvent(self, event):
        item = self._qScore.itemAt(event.scenePos())
        if item is self:
            point = self.mapFromScene(event.scenePos())
            if self._isOverNotes(point):
                np = self._getNotePosition(point)
                np = self.makeNotePosition(*np)
                self._qScore.sendFsmEvent(MouseMove(self, np))
        elif isinstance(item, QMeasure):
            item.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        point = self.mapFromScene(event.scenePos())
        np = None
        if self._isOverNotes(point):
            noteTime, drumIndex = self._getNotePosition(point)
            np = self.makeNotePosition(noteTime, drumIndex)
        self._qScore.sendFsmEvent(MouseRelease(self, np))

    def mouseDoubleClickEvent(self, event):
        point = self.mapFromScene(event.scenePos())
        if self._isOverCount(point):
            counter = self._measure.counter
            fsmEvent = EditMeasureProperties(counter,
                                             self._props.counterRegistry,
                                             self.measurePosition())
            self._qScore.sendFsmEvent(fsmEvent)
        elif self._isOverRepeatCount(point):
            fsmEvent = ChangeRepeatCount(self._measure.repeatCount,
                                         self.measurePosition())
            self._qScore.sendFsmEvent(fsmEvent)
        elif self._isOverAlternate(point):
            self.setAlternate()
        else:
            event.ignore()

    def makeNotePosition(self, noteTime, drumIndex):
        np = NotePosition(measureIndex = self._index,
                          noteTime = noteTime,
                          drumIndex = drumIndex)
        return self.parentItem().augmentNotePosition(np)

    def measurePosition(self):
        np = NotePosition(measureIndex = self._index)
        return self.parentItem().augmentNotePosition(np)

    def setAlternate(self):
        self._qScore.sendFsmEvent(SetAlternateEvent(self._measure.alternateText,
                                                    self.measurePosition()))

    def setPlaying(self, onOff):
        self._playing = onOff
        self.update()

    def setDragHighlight(self, onOff):
        self._dragHighlight = onOff
        self.update()

    def noteAt(self, np):
        return self._measure.noteAt(np.noteTime, np.drumIndex)

    def alternateText(self):
        return self._measure.alternateText

    def setPotentials(self, notes = None, head = None):
        if notes is None:
            newNotes = []
            self._potentialDrum = None
        else:
            newNotes = [np.noteTime for np in notes]
            self._potentialDrum = notes[0].drumIndex
        if newNotes != self._potentials:
            self._potentials = newNotes
            self._potentialSet = set(self._potentials)
            self._potentialHead = head
            self.update()

