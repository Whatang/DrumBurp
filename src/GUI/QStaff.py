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


    def __init__(self, staff, qScore):
        '''
        Constructor
        '''
        super(QStaff, self).__init__(scene = qScore)
        self._props = qScore.displayProperties
        self._staff = None
        self._index = None
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

    def setIndex(self, index):
        self._index = index

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
        for drum in self.scene().score.drumKit:
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
        qMeasure = QMeasure(self.scene(), measure, parent = self)
        qMeasure.setIndex(self.numMeasures())
        self._measures.append(qMeasure)
        self.addToGroup(qMeasure)

    def _addMeasureLine(self, lastMeasure, nextMeasure):
        qMeasureLine = QMeasureLine(self.scene(),
                                    lastMeasure, nextMeasure, parent = self)
        qMeasureLine.setIndex(len(self._measureLines))
        self._measureLines.append(qMeasureLine)
        self.addToGroup(qMeasureLine)

    def placeMeasures(self):
        lineOffsets = self.scene().lineOffsets
        xOffset = 0
        for yOffset, label in zip(lineOffsets, self._lineLabels):
            label.setPos(xOffset, yOffset)
        xOffset += self._props.LINELABELWIDTH
        for qMeasureLine, qMeasure in zip(self._measureLines[:-1],
                                          self._measures):
            qMeasureLine.setPos(xOffset, 0)
            qMeasureLine.setDimensions()
            xOffset += qMeasureLine.width()
            qMeasure.setPos(xOffset, 0)
            qMeasure.placeNotes()
            xOffset += qMeasure.width()
        self._measureLines[-1].setPos(xOffset, 0)
        self._measureLines[-1].setDimensions()
        self._width = xOffset + self._measureLines[-1].width()
        self._height = max(element.height()
                           for element in
                           itertools.chain(self._measures, self._measureLines))

    def xSpacingChanged(self):
        xOffset = self._props.LINELABELWIDTH
        for qMeasureLine, qMeasure in zip(self._measureLines[:-1],
                                          self._measures):
            qMeasureLine.setPos(xOffset, 0)
            qMeasureLine.xSpacingChanged()
            xOffset += qMeasureLine.width()
            qMeasure.setPos(xOffset, 0)
            qMeasure.xSpacingChanged()
            xOffset += qMeasure.width()
        self._measureLines[-1].xSpacingChanged()
        self._measureLines[-1].setPos(xOffset, 0)
        self._width = xOffset + self._measureLines[-1].width()

    def ySpacingChanged(self):
        lineOffsets = self.scene().lineOffsets
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

    def setNote(self, np, head):
        self._measures[np.measureIndex].setNote(np, head)

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
