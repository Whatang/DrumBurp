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

from GUI.DBFSMEvents import (LeftPress, MidPress, RightPress,
                             EditMeasureProperties,
                             MouseMove, MouseRelease,
                             ChangeRepeatCount,
                             SetAlternateEvent,
                             MeasureCountContext)

def _painterSaver(method):
    def wrapper(self, painter, *args, **kwargs):
        painter.save()
        try:
            method(self, painter, *args, **kwargs)
        finally:
            painter.restore()
    return wrapper

class QMeasure(QtGui.QGraphicsItem):
    def __init__(self, index, qScore, measure, parent):
        super(QMeasure, self).__init__(parent)
        self._props = qScore.displayProperties
        self._qScore = qScore
        self._index = index
        self._width = 0
        self._height = 0
        self._base = 0
        self._measureIndex = qScore.score.getMeasureIndex(self.measurePosition())
        self._highlight = None
        self._rect = QtCore.QRectF(0, 0, 0, 0)
        self._repeatCountRect = None
        self._alternate = None
        self._playing = False
        self._nextToPlay = False
        self._dragHighlight = False
        self._potentials = []
        self._potentialDrum = None
        self._potentialHead = None
        self._potentialSet = None
        self.setAcceptsHoverEvents(True)
        self._measure = measure
        self._displayCols = 0
        self._setDimensions()
        self.update()

    def numLines(self):
        return self.parentItem().numLines()

    def lineIndex(self, index):
        return self.parentItem().lineIndex(index)

    def _setDimensions(self):
        self.prepareGeometryChange()
        if self._measure.simileDistance > 0:
            referredMeasure = self._qScore.score.getReferredMeasure(self._measureIndex)
            self._displayCols = referredMeasure.counter.numBeats()
        else:
            self._displayCols = len(self._measure)
        self._width = self._qScore.xSpacing * self._displayCols
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

    def _colourScheme(self):
        return self._qScore.parent().colourScheme

    @staticmethod
    def _setPainterColour(painter, colourItem):
        pen = QtGui.QPen(colourItem.borderStyle)
        pen.setColor(colourItem.borderColour)
        painter.setPen(pen)
        painter.setBrush(colourItem.backgroundColour)

    @_painterSaver
    def _paintNotes(self, painter, xValues):
        font = painter.font()
        fontMetric = QtGui.QFontMetrics(font)
        baseline = (self.numLines() - 1) * self._qScore.ySpacing + self._base + self.parentItem().alternateHeight()
        dot = self._qScore.scale
        potential = False
        isSimile = self._measure.simileDistance > 0
        for drumIndex in xrange(self.numLines()):
            lineHeight = baseline + (self._qScore.ySpacing / 2.0) - 1
            lineIndex = self.lineIndex(drumIndex)
            for noteTime, x in enumerate(xValues):
                if isSimile:
                    text = "%"
                elif (lineIndex == self._potentialDrum
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
                    left = x + (self._qScore.xSpacing - br.width()) / 2
                    offset = br.y() - (self._qScore.ySpacing - br.height()) / 2
                    painter.drawText(QtCore.QPointF(left, baseline - offset),
                                     text)
                if potential:
                    painter.setPen(QtGui.QColor(QtCore.Qt.black))
                    potential = False
            baseline -= self._qScore.ySpacing
#         painter.drawRect(self._rect) # Draw bounding box

    @_painterSaver
    def _paintHighlight(self, painter, xValues):
        if self._highlight is None:
            return
        noteTime, drumIndex = self._highlight  # IGNORE:unpacking-non-sequence
        baseline = self._base + self.parentItem().alternateHeight()
        noteLine = (self.numLines() - drumIndex - 1) * self._qScore.ySpacing + self._base + self.parentItem().alternateHeight()
        countLine = (self.numLines() * self._qScore.ySpacing) + self._base + self.parentItem().alternateHeight()
        x = xValues[noteTime]
        scheme = self._colourScheme()
        self._setPainterColour(painter, scheme.noteHighlight)
        painter.drawRect(x, countLine,
                         self._qScore.xSpacing - 1,
                         self._qScore.ySpacing - 1)
        painter.drawRect(x, noteLine,
                         self._qScore.xSpacing - 1,
                         self._qScore.ySpacing - 1)
        self._setPainterColour(painter, scheme.timeHighlight)
        painter.drawRect(x, baseline,
                         self._qScore.xSpacing - 1,
                         self.numLines() * self._qScore.ySpacing - 1)
        painter.setPen(self._qScore.palette().text().color())

    @_painterSaver
    def _paintBeatCount(self, painter, xValues):
        font = painter.font()
        fontMetric = QtGui.QFontMetrics(font)
        baseline = (self.numLines() * self._qScore.ySpacing) + self._base + self.parentItem().alternateHeight()
        if self._measure.simileDistance > 0:
            counter = ["%d" % (beat + 1) for beat in
                       xrange(self._displayCols)]
        else:
            counter = self._measure.count()
        for noteTime, count in enumerate(counter):
            x = xValues[noteTime]
            br = fontMetric.tightBoundingRect(count)
            left = x + (self._qScore.xSpacing - br.width()) / 2
            offset = br.y() - (self._qScore.ySpacing - br.height()) / 2
            painter.drawText(QtCore.QPointF(left, baseline - offset), count)

    @_painterSaver
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

    @_painterSaver
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

    @_painterSaver
    def _paintPlayingHighlight(self, painter):
        scheme = self._colourScheme()
        if self._playing:
            self._setPainterColour(painter, scheme.playingHighlight)
        elif self._nextToPlay:
            self._setPainterColour(painter, scheme.nextPlayingHighlight)
        else:
            return
        painter.drawRect(-1, -1, self.width() + 1, self.height() + 1)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

    @_painterSaver
    def _paintMeasureCount(self, painter):
        painter.setPen(QtCore.Qt.black)
        font = painter.font()
        font.setItalic(True)
        painter.setFont(font)
        painter.drawText(1, self._base - 2, "%d" % (1 + self._measureIndex))


    @_painterSaver
    def _paintDragHighlight(self, painter):
        scheme = self._colourScheme()
        self._setPainterColour(painter, scheme.selectedMeasure)
        painter.drawRect(self._rect)

    def paint(self, painter, dummyOption, dummyWidget = None):
        painter.save()
        if self._dragHighlight:
            self._paintDragHighlight(painter)
        painter.setPen(QtCore.Qt.SolidLine)
        font = self._props.noteFont
        if font is None:
            font = painter.font()
        painter.setFont(font)
        xValues = [noteTime * self._qScore.xSpacing
                   for noteTime in xrange(self._displayCols)]
        if not self._measure.simileDistance > 0 and self._highlight:
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
        if self._playing or self._nextToPlay:
            self._paintPlayingHighlight(painter)
        if self._measure.alternateText is not None:
            self._paintAlternate(painter)
        else:
            self._alternate = None
        painter.restore()

    def dataChanged(self, notePosition_):
        self._setDimensions()
        self.update()
        self.parentItem().placeMeasures()

    def xSpacingChanged(self):
        self._setDimensions()
        self.update()

    def ySpacingChanged(self):
        self._setDimensions()
        self.update()

    def _isOverNotes(self, lineIndex):
        return 0 <= lineIndex < self.numLines()

    @staticmethod
    def _isOverCount(lineIndex):
        return lineIndex == -1

    def _isOverRepeatCount(self, point):
        return (self._repeatCountRect is not None
                and self._repeatCountRect.contains(point))

    def _isOverAlternate(self, point):
        return (self._alternate is not None
                and self._alternate.contains(point))

    def _getMouseLine(self, point):
        offset = point.y() - self._base - self.parentItem().alternateHeight()
        if offset < 0:
            return self.numLines()
        else:
            return self.numLines() - int(offset / self._qScore.ySpacing) - 1

    def _getMouseCoords(self, point):
        return self._getNoteTime(point), self._getMouseLine(point)

    def _getNotePosition(self, point):
        x, y = self._getMouseCoords(point)
        y = self.lineIndex(y)
        return x, y

    def _getNoteTime(self, point):
        return int(point.x() / self._qScore.xSpacing)

    def _hovering(self, event):
        point = self.mapFromScene(event.scenePos())
        noteTime, lineIndex = self._getMouseCoords(point)
        if self._isOverNotes(lineIndex):
            if (noteTime, lineIndex) != self._highlight:
                self._highlight = noteTime, lineIndex
                self.update()
                self.parentItem().setLineHighlight(lineIndex)
                realIndex = self.parentItem().lineIndex(lineIndex)
                self._qScore.setCurrentHeads(realIndex)
        elif self._highlight != None:
            self._highlight = None
            self.parentItem().clearHighlight()
            self.update()
        if self._isOverCount(lineIndex):
            self._qScore.setStatusMessage("Double click to edit measure count; right click for count options.")
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
        event.accept()

    def hoverMoveEvent(self, event):
        self._hovering(event)
        event.accept()

    def hoverLeaveEvent(self, event):
        self._highlight = None
        self.update()
        self.parentItem().clearHighlight()
        self._qScore.setCurrentHeads(None)
        self.setCursor(QtCore.Qt.ArrowCursor)
        event.accept()

    def mousePressEvent(self, event):
        point = self.mapFromScene(event.scenePos())
        eventType = LeftPress
        np = None
        lineIndex = self._getMouseLine(point)
        if self._isOverNotes(lineIndex):
            noteTime, drumIndex = self._getNotePosition(point)
            np = self.makeNotePosition(noteTime, drumIndex)
            if event.button() == QtCore.Qt.MidButton:
                eventType = MidPress
            elif event.button() == QtCore.Qt.RightButton:
                eventType = RightPress
        elif self._isOverCount(lineIndex):
            if event.button() == QtCore.Qt.RightButton:
                eventType = MeasureCountContext
                noteTime = self._getNoteTime(point)
                np = self.makeNotePosition(noteTime, -1)
        self._qScore.sendFsmEvent(eventType(self, np, event.screenPos()))

    def mouseMoveEvent(self, event):
        item = self._qScore.itemAt(event.scenePos())
        if item is self:
            point = self.mapFromScene(event.scenePos())
            if self._isOverNotes(self._getMouseLine(point)):
                np = self._getNotePosition(point)
                np = self.makeNotePosition(*np)
                self._qScore.sendFsmEvent(MouseMove(self, np))
        elif isinstance(item, QMeasure):
            item.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        point = self.mapFromScene(event.scenePos())
        np = None
        if self._isOverNotes(self._getMouseLine(point)):
            noteTime, drumIndex = self._getNotePosition(point)
            np = self.makeNotePosition(noteTime, drumIndex)
        self._qScore.sendFsmEvent(MouseRelease(self, np))

    def mouseDoubleClickEvent(self, event):
        point = self.mapFromScene(event.scenePos())
        lineIndex = self._getMouseLine(point)
        if self._isOverCount(lineIndex) and not self._measure.simileDistance > 0:
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

    def setNextToPlay(self, onOff):
        self._nextToPlay = onOff
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

