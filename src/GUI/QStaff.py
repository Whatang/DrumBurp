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
from QMeasure import QMeasure
from QMeasureLine import QMeasureLine
from QLineLabel import QLineLabel
from Data.NotePosition import NotePosition
import itertools

class QStaff(QtGui.QGraphicsItemGroup):
    '''
    classdocs
    '''


    def __init__(self, staff, index, scene, qScore = None):
        '''
        Constructor
        '''
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
        lastMeasure = None
        for measure in self._staff:
            self._addMeasureLine(lastMeasure, measure)
            self._addMeasure(measure)
            lastMeasure = measure
        self._addMeasureLine(lastMeasure, None)

    def numMeasures(self):
        return len(self._measures)

    def _addLineLabel(self, drum):
        qLabel = QLineLabel(drum, self.scene(), self)
        self._lineLabels.append(qLabel)
        self.addToGroup(qLabel)

    def _addMeasure(self, measure):
        qMeasure = QMeasure(self.numMeasures(), self._qScore,
                            measure, parent = self)
        self._measures.append(qMeasure)
        self.addToGroup(qMeasure)

    def _addMeasureLine(self, lastMeasure, nextMeasure):
        qMeasureLine = QMeasureLine(self.scene(),
                                    lastMeasure, nextMeasure,
                                    len(self._measureLines),
                                    self._index,
                                    parent = self)
        self._measureLines.append(qMeasureLine)
        self.addToGroup(qMeasureLine)

    def placeMeasures(self):
        lineOffsets = self._qScore.lineOffsets
        xOffset = 0
        for yOffset, label in zip(lineOffsets[-len(self._lineLabels):],
                                  self._lineLabels):
            label.setPos(xOffset, yOffset)
        xOffset += self._lineLabels[0].cellWidth()
        for qMeasureLine, qMeasure in zip(self._measureLines[:-1],
                                          self._measures):
            qMeasureLine.setPos(xOffset, self.scene().ySpacing)
            qMeasureLine.setDimensions()
            xOffset += qMeasureLine.width()
            qMeasure.setPos(xOffset, 0)
            xOffset += qMeasure.width()
        self._measureLines[-1].setPos(xOffset, self.scene().ySpacing)
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
            qMeasureLine.setPos(xOffset, self.scene().ySpacing)
            qMeasureLine.xSpacingChanged()
            xOffset += qMeasureLine.width()
            qMeasure.setPos(xOffset, 0)
            qMeasure.xSpacingChanged()
            xOffset += qMeasure.width()
        self._measureLines[-1].xSpacingChanged()
        self._measureLines[-1].setPos(xOffset, self.scene().ySpacing)
        self._width = xOffset + self._measureLines[-1].width()

    def ySpacingChanged(self):
        lineOffsets = self._qScore.lineOffsets
        for yOffset, label in zip(lineOffsets[-len(self._lineLabels):],
                                  self._lineLabels):
            label.setY(yOffset)
            label.ySpacingChanged()
        for qMeasureLine, qMeasure in zip(self._measureLines[:-1],
                                          self._measures):
            qMeasureLine.ySpacingChanged()
            qMeasure.ySpacingChanged()
        self._measureLines[-1].ySpacingChanged()
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
        if notePosition.measureIndex is not None:
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

    def changeRepeatCount(self, np):
        qMeasure = self._measures[np.measureIndex]
        qMeasure.changeRepeatCount()

    def getQMeasure(self, np):
        return self._measures[np.measureIndex]

