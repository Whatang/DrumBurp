'''
Created on 4 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui
from QMeasure import QMeasure
from QMeasureLine import QMeasureLine

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
        self._measures = []
        self._measureLines = []
        self._width = 0
        self._height = 0
        self.setStaff(staff)

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
        for measure in self._measures:
            measure.clear()
#        for measureLine in self._measureLines:
#            measureLine.clear()
        self._measures = []
        self._measureLines = []

    def build(self):
        self.clear()
        lastMeasure = None
        for measure in self._staff:
            self.addMeasureLine(lastMeasure, measure)
            self.addMeasure(measure)
            lastMeasure = measure
        self.addMeasureLine(lastMeasure, None)

    def numMeasures(self):
        return len(self._measures)

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
        xOffset = 0
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
        self._height = self._measureLines[0].height()

    def xSpacingChanged(self):
#        self.prepareGeometryChange()
        xOffset = 0
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
#        self.prepareGeometryChange()
        for qMeasureLine, qMeasure in zip(self._measureLines[:-1],
                                          self._measures):
            qMeasureLine.ySpacingChanged()
            qMeasure.ySpacingChanged()
        self._measureLines[-1].ySpacingChanged()
        self._height = self._measureLines[0].height()

    def setNote(self, np, head):
        self._measures[np.measureIndex].setNote(np, head)

    def toggleNote(self, np):
        np.staffIndex = self._index
        self._qScore.toggleNote(np)

#    def boundingRect(self):
#        return QtCore.QRectF(0, 0, self._width, self._height)
