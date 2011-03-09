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
        for drum in self._qScore.score.drumKit:
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
                                    lastMeasure, nextMeasure, parent = self)
        qMeasureLine.setIndex(len(self._measureLines))
        self._measureLines.append(qMeasureLine)
        self.addToGroup(qMeasureLine)

    def placeMeasures(self):
        lineOffsets = self._qScore.lineOffsets
        xOffset = 0
        for yOffset, label in zip(lineOffsets, self._lineLabels):
            label.setPos(xOffset, yOffset)
        xOffset += self._lineLabels[0].cellWidth()
        for qMeasureLine, qMeasure in zip(self._measureLines[:-1],
                                          self._measures):
            qMeasureLine.setPos(xOffset, self._props.ySpacing)
            qMeasureLine.setDimensions()
            xOffset += qMeasureLine.width()
            qMeasure.setPos(xOffset, 0)
            xOffset += qMeasure.width()
        self._measureLines[-1].setPos(xOffset, self._props.ySpacing)
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
            qMeasureLine.setPos(xOffset, self._props.ySpacing)
            qMeasureLine.xSpacingChanged()
            xOffset += qMeasureLine.width()
            qMeasure.setPos(xOffset, 0)
            qMeasure.xSpacingChanged()
            xOffset += qMeasure.width()
        self._measureLines[-1].xSpacingChanged()
        self._measureLines[-1].setPos(xOffset, self._props.ySpacing)
        self._width = xOffset + self._measureLines[-1].width()

    def ySpacingChanged(self):
        lineOffsets = self._qScore.lineOffsets
        for yOffset, label in zip(lineOffsets, self._lineLabels):
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
        np = NotePosition(measureIndex = self._index)
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
