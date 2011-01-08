'''
Created on 5 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore
from QNote import QNote

class QMeasure(QtGui.QGraphicsItemGroup):
    '''
    classdocs
    '''


    def __init__(self, qScore, measure, parent):
        '''
        Constructor
        '''
        super(QMeasure, self).__init__(parent)
        self._qStaff = parent
        self._qScore = qScore
        self._score = self._qScore.getScore()
        self._props = self._qScore.getProperties()
        self._measure = None
        self._index = None
        self._notes = []
        self._width = 0
        self._height = 0
        self.setMeasure(measure)

    def width(self):
        return self._width

    def height(self):
        return self._height

    def setMeasure(self, measure):
        if self._measure != measure:
            self._measure = measure
            self.build()

    def setIndex(self, index):
        self._index = index

    def clear(self):
        self._notes = []

    def build(self):
        self.clear()
        for drumIndex in range(0, len(self._score.drumKit)):
            noteLine = []
            self._notes.append(noteLine)
            for noteTime in range(0, len(self._measure)):
                qNote = QNote(self._qScore, parent = self)
                qNote.setIndex(drumIndex, noteTime)
                noteLine.append(qNote)
                self.addToGroup(qNote)

    def placeNotes(self):
        yOffsets = [drumIndex * self._props.ySpacing
                    for drumIndex in range(0, len(self._score.drumKit))]
        for noteTime in range(0, len(self._measure)):
            xOffset = noteTime * self._props.xSpacing
            for drumIndex, yOffset in enumerate(yOffsets):
                qNote = self._notes[drumIndex][noteTime]
                qNote.setDimensions()
                qNote.setPos(xOffset, yOffset)
        self._setWidth()
        self._setHeight()

    def _setWidth(self):
        self._width = len(self._measure) * self._props.xSpacing

    def _setHeight(self):
        self._height = len(self._score.drumKit) * self._props.ySpacing

    def toggleNote(self, np, head):
        np.measureIndex = self._index
        self._qStaff.toggleNote(np, head)

    def setNote(self, np, head):
        self._notes[np.drumIndex][np.noteTime].setText(head)

    def xSpacingChanged(self):
        yOffsets = [drumIndex * self._props.ySpacing
                    for drumIndex in range(0, len(self._score.drumKit))]
        for noteTime in range(0, len(self._measure)):
            xOffset = noteTime * self._props.xSpacing
            for drumIndex, yOffset in enumerate(yOffsets):
                qNote = self._notes[drumIndex][noteTime]
                qNote.setPos(xOffset, yOffset)
                qNote.xSpacingChanged()
        self._setWidth()

    def ySpacingChanged(self):
        yOffsets = [drumIndex * self._props.ySpacing
                    for drumIndex in range(0, len(self._score.drumKit))]
        for noteTime in range(0, len(self._measure)):
            xOffset = noteTime * self._props.xSpacing
            for drumIndex, yOffset in enumerate(yOffsets):
                qNote = self._notes[drumIndex][noteTime]
                qNote.setPos(xOffset, yOffset)
                qNote.ySpacingChanged()
        self._setHeight()
