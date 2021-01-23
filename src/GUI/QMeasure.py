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
                             MeasureCountContext,
                             SetSticking,
                             SetBpmEvent)


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
        self._bpmBase = 0
        self._repeatBottom = 0
        self._notesTop = 0
        self._notesBottom = 0
        self._stickingBelowTop = 0
        self._measureIndex = qScore.score.measurePositionToIndex(
            self.measurePosition())
        self._highlight = None
        self._rect = QtCore.QRectF(0, 0, 0, 0)
        self._repeatCountRect = None
        self._bpmRect = None
        self._alternate = None
        self._stickingAbove = None
        self._stickingBelow = None
        self._showStickingHighlight = False
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
        self._isFirst = False
        self.update()

    def numLines(self):
        return self.parentItem().numLines()

    def lineIndex(self, index):
        return self.parentItem().lineIndex(index)

    def _setDimensions(self):
        self.prepareGeometryChange()
        if self.isSimile():
            referredMeasure = self._qScore.score.getReferredMeasure(
                self._measureIndex)
            self._displayCols = referredMeasure.counter.numBeats()
        else:
            self._displayCols = len(self._measure)
        self._width = self._qScore.xSpacing * self._displayCols
        self._height = 0
        self._base = 0
        self._bpmBase = 0
        if self.parentItem().anyMeasureHasBpm():
            self._base += self._props.bpmHeight()
        if self._props.measureCountsVisible:
            self._base += self._props.measureCountHeight()
        self._repeatBottom = self._base + self.parentItem().alternateHeight()
        self._notesTop = self._repeatBottom
        if self.parentItem().showStickingAbove():
            self._notesTop += self._qScore.ySpacing
        self._height = self._notesTop
        self._height += self.numLines() * self._qScore.ySpacing
        self._notesBottom = self._height
        if self._props.beatCountVisible:
            self._height += self._qScore.ySpacing
        self._stickingBelowTop = self._height
        if self.parentItem().showStickingBelow():
            self._height += self._qScore.ySpacing
        self._rect.setBottomRight(QtCore.QPointF(self._width, self._height))

    def boundingRect(self):
        return self._rect

    def width(self):
        return self._width

    def height(self):
        return self._height

    def setFirst(self, trueFalse):
        self._isFirst = trueFalse

    def _colourScheme(self):
        return self._qScore.parent().colourScheme

    def isSimile(self):
        return self._measure.simileDistance > 0

    @_painterSaver
    def _paintNotes(self, painter, xValues):
        scheme = self._colourScheme()
        scheme.text.setPainter(painter)
        font = painter.font()
        fontMetric = QtGui.QFontMetrics(font)
        numLines = self.numLines()
        baseline = self._notesBottom - self._qScore.ySpacing
        lineHeight = baseline + (self._qScore.ySpacing / 2.0) - 1
        dot = self._qScore.scale
        potential = False
        if self.isSimile():
            simText = "%%%d" % self._measure.simileDistance
            left = " "
            right = " "
            if self._measure.simileIndex > 0:
                left = "-"
            if self._measure.simileIndex < self._measure.simileDistance - 1:
                right = "-"
            while len(simText) < len(xValues):
                simText = left + simText + right
        for drumIndex in range(numLines):
            lineIndex = self.lineIndex(drumIndex)
            for noteTime, x in enumerate(xValues):
                if self.isSimile():
                    if drumIndex == numLines / 2:
                        text = simText[noteTime]
                    else:
                        text = " "
                elif (lineIndex == self._potentialDrum
                      and noteTime in self._potentialSet):
                    text = self._potentialHead
                    potential = True
                    scheme.potential.setPainter(painter)
                elif (noteTime, drumIndex) == self._highlight:
                    potential = True
                    current = self._measure.noteAt(noteTime, lineIndex)
                    potentialHead = self._qScore.getCurrentHead()
                    if potentialHead is None:
                        potentialHead = self._qScore.score.drumKit.getDefaultHead(
                            lineIndex)
                    if current == potentialHead:
                        text = current
                        scheme.delete.setPainter(painter)
                    else:
                        text = potentialHead
                        scheme.potential.setPainter(painter)
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
                    scheme.text.setPainter(painter)
                    potential = False
            baseline -= self._qScore.ySpacing
            lineHeight -= self._qScore.ySpacing
#         painter.drawRect(self._rect)  # Draw bounding box

    @_painterSaver
    def _paintHighlight(self, painter, xValues):
        if self._highlight is None:
            return
        noteTime, drumIndex = self._highlight  # IGNORE:unpacking-non-sequence
        baseline = self._notesTop
        countLine = self._notesBottom
        x = xValues[noteTime]
        scheme = self._colourScheme()
        # Highlight count
        scheme.noteHighlight.setPainter(painter)
        painter.drawRect(x, countLine,
                         self._qScore.xSpacing - 1,
                         self._qScore.ySpacing - 1)
        # Highlight notes column
        scheme.timeHighlight.setPainter(painter)
        painter.drawRect(x, baseline,
                         self._qScore.xSpacing - 1,
                         self._notesBottom - self._notesTop - 1)

    @_painterSaver
    def _paintBeatCount(self, painter, xValues):
        font = painter.font()
        fontMetric = QtGui.QFontMetrics(font)
        baseline = self._notesBottom
        if self.isSimile():
            counter = ["%d" % (beat + 1) for beat in
                       range(self._displayCols)]
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
        self._colourScheme().text.setPainter(painter)
        repeatText = '%dx' % self._measure.repeatCount
        textWidth = QtGui.QFontMetrics(painter.font()).width(repeatText)
        textLocation = QtCore.QPointF(self.width() - textWidth - 2 * spacing,
                                      self._repeatBottom - spacing)
        painter.drawText(textLocation, repeatText)
        if self._repeatCountRect is None:
            self._repeatCountRect = QtCore.QRectF(0, 0, 0, 0)
        self._repeatCountRect.setSize(QtCore.QSizeF(textWidth,
                                                    self._repeatBottom - self._base))
        self._repeatCountRect.moveTopRight(QtCore.QPointF(self.width() - 2 * spacing,
                                                          self._base - spacing))

    @_painterSaver
    def _paintAlternate(self, painter):
        altHeight = self.parentItem().alternateHeight()
        spacing = self._qScore.scale
        self._colourScheme().text.setPainter(painter)
        painter.drawLine(0, self._base, self.width() - spacing * 2, self._base)
        painter.drawLine(0, self._base, 0, self._notesTop - spacing * 2)
        font = painter.font()
        font.setItalic(True)
        painter.setFont(font)
        if self._alternate is None:
            self._alternate = QtCore.QRectF(0, 0, 0, 0)
        text = self._measure.alternateText
        textWidth = QtGui.QFontMetrics(font).width(text)
        self._alternate.setSize(QtCore.QSizeF(textWidth, altHeight))
        bottomLeft = QtCore.QPointF(2 * spacing, self._repeatBottom - spacing)
        self._alternate.moveBottomLeft(bottomLeft)
        painter.drawText(2 * spacing, self._repeatBottom - spacing, text)

    @_painterSaver
    def _paintPlayingHighlight(self, painter):
        scheme = self._colourScheme()
        if self._playing:
            scheme.playingHighlight.setPainter(painter)
        elif self._nextToPlay:
            scheme.nextPlayingHighlight.setPainter(painter)
        else:
            return
        painter.drawRect(-1, -1, self.width() + 1, self.height() + 1)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

    @_painterSaver
    def _paintMeasureCount(self, painter):
        self._colourScheme().text.setPainter(painter)
        font = painter.font()
        font.setItalic(True)
        painter.setFont(font)
        painter.drawText(1, self._base - 2, "%d" % (1 + self._measureIndex))

    @_painterSaver
    def _paintDragHighlight(self, painter):
        scheme = self._colourScheme()
        scheme.selectedMeasure.setPainter(painter)
        painter.drawRect(self._rect)

    def _paintSticking(self, painter, sticking, baseline, xValues):
        font = painter.font()
        fontMetric = QtGui.QFontMetrics(font)
        for text, x in zip(sticking, xValues):
            if text == " ":
                pass
            else:
                br = fontMetric.tightBoundingRect(text)
                left = x + (self._qScore.xSpacing - br.width()) / 2
                offset = br.y() - (self._qScore.ySpacing - br.height()) / 2
                painter.drawText(QtCore.QPointF(left, baseline - offset),
                                 text)

    @_painterSaver
    def _paintStickingHighlight(self, painter, stickingRect):
        scheme = self._colourScheme()
        scheme.sticking.setPainter(painter)
        painter.drawRect(stickingRect)

    @_painterSaver
    def _paintStickingAbove(self, painter, xValues):
        if not self.parentItem().showStickingAbove():
            self._stickingAbove = None
            return
        self._stickingAbove = QtCore.QRectF(0, 0, 0, 0)
        self._stickingAbove.setSize(QtCore.QSizeF(self.width(),
                                                  self._qScore.ySpacing))
        spacing = self._qScore.scale
        baseline = self._notesTop - spacing
        bottomLeft = QtCore.QPointF(0, baseline)
        self._stickingAbove.moveBottomLeft(bottomLeft)
        sticking = self._measure.aboveText
        if self._showStickingHighlight:
            self._paintStickingHighlight(painter, self._stickingAbove)
        self._paintSticking(painter, sticking,
                            baseline - self._qScore.ySpacing, xValues)

    @_painterSaver
    def _paintStickingBelow(self, painter, xValues):
        if not self.parentItem().showStickingBelow():
            self._stickingBelow = None
            return
        self._stickingBelow = QtCore.QRectF(0, 0, 0, 0)
        self._stickingBelow.setSize(QtCore.QSizeF(self.width(),
                                                  self._qScore.ySpacing))
        bottomLeft = QtCore.QPointF(0, self._height)
        self._stickingBelow.moveBottomLeft(bottomLeft)
        sticking = self._measure.belowText
        if self._showStickingHighlight:
            self._paintStickingHighlight(painter, self._stickingBelow)
        self._paintSticking(painter, sticking,
                            self._height - self._qScore.ySpacing, xValues)

    @_painterSaver
    def _paintNewBpm(self, painter):
        text = "BPM = %d" % self._measure.newBpm
        painter.drawText(1, self._bpmBase + self._props.bpmHeight() - 1, text)
        textWidth = QtGui.QFontMetrics(painter.font()).width(text)
        if self._bpmRect is None:
            self._bpmRect = QtCore.QRectF(0, 0, 0, 0)
        self._bpmRect.setSize(QtCore.QSizeF(
            textWidth, self._props.bpmHeight()))
        self._bpmRect.moveTopLeft(QtCore.QPointF(1, self._bpmBase))

    @_painterSaver
    def paint(self, painter, dummyOption, dummyWidget=None):
        if self._dragHighlight:
            self._paintDragHighlight(painter)
        self._colourScheme().text.setPainter(painter)
        font = self._props.noteFont
        if font is None:
            font = painter.font()
        painter.setFont(font)
        xValues = [noteTime * self._qScore.xSpacing
                   for noteTime in range(self._displayCols)]
        if not self.isSimile() and self._highlight:
            self._paintHighlight(painter, xValues)
        self._paintNotes(painter, xValues)
        if self._measure.newBpm != 0:
            self._paintNewBpm(painter)
        else:
            self._bpmRect = None
        if self._props.beatCountVisible:
            self._paintBeatCount(painter, xValues)
        if self._props.measureCountsVisible and self._isFirst:
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
        # Sticking
        if not self.isSimile():
            self._paintStickingAbove(painter, xValues)
            self._paintStickingBelow(painter, xValues)

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

    def _isOverStickingAbove(self, point):
        return (self._stickingAbove is not None
                and self._stickingAbove.contains(point))

    def _isOverStickingBelow(self, point):
        return (self._stickingBelow is not None
                and self._stickingBelow.contains(point))

    def _isOverBpmChange(self, point):
        return (self._bpmRect is not None
                and self._bpmRect.contains(point))

    def _getMouseLine(self, point):
        offset = point.y() - self._notesTop
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
        # Set line & time highlights
        if self._isOverNotes(lineIndex):
            if (noteTime, lineIndex) != self._highlight:
                self._highlight = noteTime, lineIndex
                self.update()
                self.parentItem().setLineHighlight(lineIndex)
                realIndex = self.parentItem().lineIndex(lineIndex)
                self._qScore.setCurrentHeads(realIndex)
        elif self._isOverStickingAbove(point) or self._isOverStickingBelow(point):
            self._highlight = noteTime, None
            self.update()
        elif self._highlight != None:
            self._highlight = None
            self.parentItem().clearHighlight()
            self.update()
        # Set status message and cursor
        if self._isOverStickingAbove(point) or self._isOverStickingBelow(point):
            self._qScore.setStatusMessage("Click to rotate sticking.")
            self.setCursor(QtCore.Qt.PointingHandCursor)
        elif self._isOverNotes(lineIndex):
            if self.isSimile():
                self._qScore.setStatusMessage("Right click for options.")
            else:
                self._qScore.setStatusMessage("Click to toggle notes; "
                                              "middle click to toggle special noteheads; "
                                              "right click for options.")
            self.setCursor(QtCore.Qt.ArrowCursor)
        elif self._isOverCount(lineIndex):
            if self.isSimile():
                self._qScore.setStatusMessage("Right click for count options.")
            else:
                self._qScore.setStatusMessage("Double click to edit measure count; "
                                              "right click for count options.")
            self.setCursor(QtCore.Qt.PointingHandCursor)
        elif self._isOverRepeatCount(point):
            self._qScore.setStatusMessage("Double click to edit repeat count.")
            self.setCursor(QtCore.Qt.PointingHandCursor)
        elif self._isOverBpmChange(point):
            self._qScore.setStatusMessage("Double click to edit BPM change.")
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
        self._showStickingHighlight = True
        event.accept()

    def hoverMoveEvent(self, event):
        self._hovering(event)
        event.accept()

    def hoverLeaveEvent(self, event):
        self._highlight = None
        self._showStickingHighlight = False
        self.update()
        self.parentItem().clearHighlight()
        self._qScore.setCurrentHeads(None)
        self.setCursor(QtCore.Qt.ArrowCursor)
        self._qScore.setStatusMessage()
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
        elif self._isOverStickingAbove(point) and not self.isSimile():
            self.setSticking(point, True)
        elif self._isOverStickingBelow(point) and not self.isSimile():
            self.setSticking(point, False)
        self._qScore.sendFsmEvent(MouseRelease(self, np))

    def mouseDoubleClickEvent(self, event):
        point = self.mapFromScene(event.scenePos())
        lineIndex = self._getMouseLine(point)
        if self._isOverCount(lineIndex) and not self.isSimile():
            counter = self._measure.counter
            fsmEvent = EditMeasureProperties(counter,
                                             self._props.counterRegistry,
                                             self.measurePosition())
            self._qScore.sendFsmEvent(fsmEvent)
        elif self._isOverRepeatCount(point):
            fsmEvent = ChangeRepeatCount(self._measure.repeatCount,
                                         self.measurePosition())
            self._qScore.sendFsmEvent(fsmEvent)
        elif self._isOverBpmChange(point):
            self.setNewBpm()
        elif self._isOverAlternate(point):
            self.setAlternate()
        elif self._isOverStickingAbove(point) or self._isOverStickingBelow(point):
            # Want this to get picked up by the normal mouseReleaseEvent:
            # don't ignore it, or it gets passed to the parent for handling
            # as a double click event
            event.accept()
        else:
            event.ignore()

    def makeNotePosition(self, noteTime, drumIndex):
        np = NotePosition(measureIndex=self._index,
                          noteTime=noteTime,
                          drumIndex=drumIndex)
        return self.parentItem().augmentNotePosition(np)

    def measurePosition(self):
        np = NotePosition(measureIndex=self._index)
        return self.parentItem().augmentNotePosition(np)

    def setAlternate(self):
        self._qScore.sendFsmEvent(SetAlternateEvent(self._measure.alternateText,
                                                    self.measurePosition()))

    def setNewBpm(self):
        bpm = self._measure.newBpm
        if bpm == 0:
            bpm = self._qScore.score.bpmAtMeasureByPosition(
                self.measurePosition())
        if bpm == 0:
            bpm = 120
        self._qScore.sendFsmEvent(SetBpmEvent(self.measurePosition(), bpm))

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

    def setPotentials(self, notes=None, head=None):
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

    def setSticking(self, point, above):
        noteTime = self._getNoteTime(point)
        if not self._measure.hasAnyNoteAt(noteTime):
            return
        notePos = self.makeNotePosition(noteTime, 0)
        self._qScore.sendFsmEvent(SetSticking(notePos, above))
