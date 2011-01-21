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

#pylint: disable-msg=R0904
class QStaff(QtGui.QGraphicsItemGroup):
    '''
    classdocs
    '''


    def __init__(self, staff, parent = None):
        '''
        Constructor
        '''
        super(QStaff, self).__init__(scene = parent)
        self._qScore = parent
        self._score = self._qScore.getScore()
        self._props = self._qScore.getProperties()
        self._staff = None
        self._index = None
        self._lineLabels = []
        self._measures = []
        self._measureLines = []
        self._width = 0
        self._height = 0
        self.setStaff(staff)
        self.setHandlesChildEvents(False)

    def width(self):
        return self._width

    def height(self):
        return self._height

    def setIndex(self, index):
        self._index = index

    def setStaff(self, staff):
        if staff != self._staff:
            self._staff = staff
            self.build()

    def clear(self):
        self._lineLabels = []
        self._measures = []
        self._measureLines = []

    def build(self):
        self.clear()
        for label in self._qScore.iterLineLabels():
            self.addLineLabel(label)
        lastMeasure = None
        for measure in self._staff:
            self.addMeasureLine(lastMeasure, measure)
            self.addMeasure(measure)
            lastMeasure = measure
        self.addMeasureLine(lastMeasure, None)

    def numMeasures(self):
        return len(self._measures)

    def addLineLabel(self, label):
        qLabel = QLineLabel(label, self._qScore, self)
        qLabel.setIndex(len(self._lineLabels))
        self._lineLabels.append(qLabel)
        self.addToGroup(qLabel)

    def addMeasure(self, measure):
        qMeasure = QMeasure(self._qScore, measure, parent = self)
        qMeasure.setIndex(self.numMeasures())
        self._measures.append(qMeasure)
        self.addToGroup(qMeasure)

    def addMeasureLine(self, lastMeasure, nextMeasure):
        qMeasureLine = QMeasureLine(self._qScore,
                                    lastMeasure, nextMeasure, parent = self)
        qMeasureLine.setIndex(len(self._measureLines))
        self._measureLines.append(qMeasureLine)
        self.addToGroup(qMeasureLine)

    def placeMeasures(self):
        lineOffsets = self._qScore.lineOffsets()
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
        lineOffsets = self._qScore.lineOffsets()
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
                           zip(self._measures, self._measureLines))

    def setNote(self, np, head):
        self._measures[np.measureIndex].setNote(np, head)

    def _makeNotePosition(self):
        np = NotePosition(measureIndex = self._index)
        return np

    def _augmentNotePosition(self, np):
        np.staffIndex = self._index

    def toggleNote(self, np, head):
        self._augmentNotePosition(np)
        self._qScore.toggleNote(np, head)

    def repeatNote(self, np, head):
        self._augmentNotePosition(np)
        self._qScore.repeatNote(np, head)

    def insertMeasure(self, np):
        self._augmentNotePosition(np)
        self._qScore.insertMeasure(np)

    def insertOtherMeasures(self, np):
        self._augmentNotePosition(np)
        self._qScore.insertOtherMeasures(np)

    def deleteMeasure(self, np):
        self._augmentNotePosition(np)
        self._qScore.deleteMeasure(np)

    def copyMeasure(self, np):
        self._augmentNotePosition(np)
        self._qScore.copyMeasure(np)

    def pasteMeasure(self, np):
        self._augmentNotePosition(np)
        self._qScore.pasteMeasure(np)

    def editMeasureProperties(self, np, numTicks, counter):
        self._augmentNotePosition(np)
        self._qScore.editMeasureProperties(np, numTicks, counter)

    def countChanged(self, np):
        measure = self._measures[np.measureIndex]
        measure.countChanged()

    def setSectionEnd(self, np, onOff):
        self._augmentNotePosition(np)
        self._qScore.setSectionEnd(np, onOff)

    def setRepeatEnd(self, np, onOff):
        self._augmentNotePosition(np)
        self._qScore.setRepeatEnd(np, onOff)

    def setRepeatStart(self, np, onOff):
        self._augmentNotePosition(np)
        self._qScore.setRepeatStart(np, onOff)
