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
Created on 4 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui
import itertools
from GUI.QMeasure import QMeasure
from GUI.QMeasureLine import QMeasureLine
from GUI.QLineLabel import QLineLabel
from Data.NotePosition import NotePosition

class QStaff(QtGui.QGraphicsItemGroup):
    def __init__(self, staff, index, scene, qScore = None):
        super(QStaff, self).__init__(scene = scene)
        self._qScore = qScore if qScore is not None else scene
        self._props = self._qScore.displayProperties
        self._staff = None
        self._index = index
        self._highlightedLine = None
        self._lineLabels = []
        self._measures = []
        self._measureLines = []
        self._width = 0
        self._height = 0
        self._hasAlternate = False
        self._setStaff(staff)
        self.setHandlesChildEvents(False)

    def numLines(self):
        if self._props.emptyLinesVisible:
            return self._qScore.kitSize
        else:
            return self._qScore.score.numVisibleLines(self._index)

    def lineIndex(self, index):
        if self._props.emptyLinesVisible:
            return index
        else:
            return self._qScore.score.nthVisibleLineIndex(self._index,
                                                          index)

    def width(self):
        return self._width

    def height(self):
        return self._height

    def _setStaff(self, staff):
        if staff != self._staff:
            self._staff = staff
            self._build()

    def isSectionEnd(self):
        return self._staff.isSectionEnd()

    def _clear(self):
        self._lineLabels = []
        self._measures = []
        self._measureLines = []

    def _build(self):
        self._clear()
        iterable = self._qScore.score.drumKit
        if not self._props.emptyLinesVisible:
            iterable = self._qScore.score.iterVisibleLines(self._index)
        for drum in iterable:
            self._addLineLabel(drum)
        for measure in self._staff:
            if (not self._hasAlternate and
                (measure.alternateText or
                 (measure.isRepeatEnd() and measure.repeatCount > 2))):
                self._hasAlternate = True
        lastMeasure = None
        for measure in self._staff:
            self._addMeasureLine(lastMeasure, measure)
            self._addMeasure(measure)
            lastMeasure = measure
        self._addMeasureLine(lastMeasure, None)

    def numMeasures(self):
        return len(self._measures)

    def _addLineLabel(self, drum):
        qLabel = QLineLabel(drum, self._qScore, self)
        self._lineLabels.append(qLabel)
        self.addToGroup(qLabel)

    def _addMeasure(self, measure):
        qMeasure = QMeasure(self.numMeasures(), self._qScore,
                            measure,
                            parent = self)
        self._measures.append(qMeasure)
        self.addToGroup(qMeasure)

    def _addMeasureLine(self, lastMeasure, nextMeasure):
        qMeasureLine = QMeasureLine(self._qScore,
                                    lastMeasure, nextMeasure,
                                    len(self._measureLines),
                                    self._index,
                                    parent = self)
        self._measureLines.append(qMeasureLine)
        self.addToGroup(qMeasureLine)

    def placeMeasures(self):
        lineOffsets = self._qScore.lineOffsets
        xOffset = 0
        base = self.alternateHeight()
        if self._props.measureCountsVisible:
            base += self._props.measureCountHeight()
        if self.showStickingAbove():
            base += self._qScore.ySpacing
        for yOffset, label in zip(lineOffsets[-len(self._lineLabels):],
                                  self._lineLabels):
            label.setPos(xOffset, yOffset + base)
        xOffset += self._lineLabels[0].cellWidth()
        isFirst = True
        for qMeasureLine, qMeasure in zip(self._measureLines[:-1],
                                          self._measures):
            qMeasureLine.setPos(xOffset, base)
            qMeasureLine.setDimensions()
            qMeasureLine.setZValue(0)
            xOffset += qMeasureLine.width()
            qMeasure.setPos(xOffset, 0)
            qMeasure.setZValue(1)
            xOffset += qMeasure.width()
            qMeasure.setFirst(isFirst)
            isFirst = False
        self._measureLines[-1].setPos(xOffset, base)
        self._measureLines[-1].setDimensions()
        self._width = xOffset + self._measureLines[-1].width()
        self._height = max(element.height()
                           for element in
                           itertools.chain(self._measures, self._measureLines))

    def xSpacingChanged(self):
        xOffset = self._lineLabels[0].cellWidth()
        for label in self._lineLabels:
            label.xSpacingChanged()
        for qMeasureLine, qMeasure in zip(self._measureLines[:-1],
                                          self._measures):
            qMeasureLine.setX(xOffset)
            qMeasureLine.xSpacingChanged()
            xOffset += qMeasureLine.width()
            qMeasure.setX(xOffset)
            qMeasure.xSpacingChanged()
            xOffset += qMeasure.width()
        self._measureLines[-1].xSpacingChanged()
        self._measureLines[-1].setX(xOffset)
        self._width = xOffset + self._measureLines[-1].width()

    def ySpacingChanged(self):
        lineOffsets = self._qScore.lineOffsets
        base = self.alternateHeight()
        if self._props.measureCountsVisible:
            base += self._props.measureCountHeight()
        for yOffset, label in zip(lineOffsets[-len(self._lineLabels):],
                                  self._lineLabels):
            label.setY(yOffset + base)
            label.ySpacingChanged()
        for qMeasureLine, qMeasure in zip(self._measureLines[:-1],
                                          self._measures):
            qMeasureLine.ySpacingChanged()
            qMeasureLine.setY(base)
            qMeasure.ySpacingChanged()
        self._measureLines[-1].ySpacingChanged()
        self._measureLines[-1].setY(base)
        self._height = max(element.height()
                           for element in
                           itertools.chain(self._measures, self._measureLines))

    def clearHighlight(self):
        if self._highlightedLine != None:
            self._lineLabels[self._highlightedLine].setHighlight(False)
        self._highlightedLine = None

    def setLineHighlight(self, lineIndex):
        if lineIndex != self._highlightedLine:
            if self._highlightedLine != None:
                self._lineLabels[self._highlightedLine].setHighlight(False)
            self._highlightedLine = lineIndex
            self._lineLabels[self._highlightedLine].setHighlight(True)

    def dataChanged(self, notePosition):
        if notePosition.measureIndex is not None and notePosition.measureIndex < self.numMeasures():
            measure = self._measures[notePosition.measureIndex]
            measure.dataChanged(notePosition)
        else:
            self._build()

    def _makeNotePosition(self):
        np = NotePosition(staffIndex = self._index)
        return np

    def augmentNotePosition(self, np):
        np.staffIndex = self._index
        return np

    def setHighlight(self, np, onOff):
        lineLabel = self._lineLabels[np.drumIndex]
        lineLabel.setHighlight(onOff)
        qMeasure = self._measures[np.measureIndex]
        qMeasure.setHighlight(np, onOff)

    def getQMeasure(self, np):
        return self._measures[np.measureIndex]

    def alternateHeight(self):
        if self._hasAlternate:
            return self._props.alternateHeight()
        else:
            return 0

    def showStickingAbove(self):
        return any(measure.showAbove for measure in self._staff)

    def showStickingBelow(self):
        return any(measure.showBelow for measure in self._staff)

    def checkAlternate(self):
        newAlternate = False
        for measure in self._staff:
            if (measure.alternateText or
                (measure.isRepeatEnd() and measure.repeatCount > 2)):
                newAlternate = True
                break
        return self._hasAlternate != newAlternate
