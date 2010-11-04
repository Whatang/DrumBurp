'''
Created on 31 Jul 2010

@author: Mike Thomas

'''

from Model.ScoreSystem import ScoreSystem
from PyQt4.QtCore import Qt, QVariant, QAbstractTableModel, QModelIndex, SIGNAL, QSize
import Data.Score
from Model.Measure import Measure
import time

class _NoDataError(StandardError):
    '''
    There is nothing defined for the Score in this grid.
    '''

class SongModel(QAbstractTableModel):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(SongModel, self).__init__()
        self.score = Data.Score.makeEmptyScore(8, 16)
        self._desiredWidth = 80
        self._actualWidth = 80
        self._systems = []
        self._recalculate = True
        self._measures = []
        self._dataCache = {}
        self.calculateMeasures()
        self._calculateSystems()

    def _setWidth(self, value):
        if value != self._desiredWidth:
            self._desiredWidth = value
            self._calculateSystems()
    def _getWidth(self):
        return self._desiredWidth
    width = property(fget = _getWidth, fset = _setWidth)

    def rowCount(self, unusedIndex = QModelIndex()):
        if self._recalculate:
            self._calculateSystems()
        return max(0,
                   (len(self._systems) * (len(self.score) + 1)) - 1)

    def columnCount(self, unusedIndex = QModelIndex()):
        if self._recalculate:
            self._calculateSystems()
        return self._actualWidth

    def _rowToSystemNumber(self, row):
        return row / (len(self.score) + 1)

    def _rowToLineIndex(self, row):
        if (row % (len(self.score) + 1)) == len(self.score):
            raise _NoDataError()
        return len(self.score) - (row % (len(self.score) + 1)) - 1

    def _gridToTimeAndLineIndex(self, row, col):
        scoreSystem = self._systems[self._rowToSystemNumber(row)]
        if scoreSystem.startTime + col > scoreSystem.lastTime:
            raise _NoDataError()
        return (scoreSystem.startTime + col, self._rowToLineIndex(row))

    def calculateMeasures(self):
        self._measures = []
        thisMeasure = Measure(score = self.score, startTime = 0)
        for note in self.score.iterNotes():
            thisMeasure.recordNote(note)
            if note.head == Data.MEASURE_SPLIT:
                self._measures.append(thisMeasure)
                thisMeasure = Measure(score = self.score,
                                      startTime = thisMeasure.lastTime + 1)

    def _calculateSystems(self):
        self._recalculate = False
        self._dataCache = {}
        self._systems = []
        startTime = 0
        thisSystem = ScoreSystem(self.score, startTime)
        self._actualWidth = self.width
        for measure in self._measures:
            endTime = measure.lastTime
            if endTime - startTime < self.width:
                thisSystem.addMeasure(measure)
            else:
                if thisSystem.lastTime != thisSystem.startTime:
                    # i.e. there is at least one measure on this line
                    # already, so end the line and start a new one
                    self._systems.append(thisSystem)
                    startTime = thisSystem.lastTime + 1
                    thisSystem = ScoreSystem(self.score, startTime)
                    thisSystem.addMeasure(measure)
                else:
                    # Just stick the measure on this line, and make the width 
                    # of the table bigger to accommodate it if necessary
                    thisSystem.addMeasure(measure)
                    startTime = thisSystem.lastTime + 1
                    thisSystem = ScoreSystem(self.score, startTime)
                    self._actualWidth = max(self._actualWidth, measure.width)
        if thisSystem.lastTime != thisSystem.startTime:
            self._systems.append(thisSystem)
        self.emit(SIGNAL("modelReset()"))

    def data(self, index, role = Qt.DisplayRole):
        if self._recalculate:
            self._calculateSystems()
        if (not index.isValid() or
            not (0 <= index.row() < self.rowCount(index))):
            return QVariant()
        if role == Qt.DisplayRole:
            try:
                gridTime, line = self._gridToTimeAndLineIndex(index.row(),
                                                              index.column())
            except _NoDataError:
                return QVariant()
            if (gridTime, line) not in self._dataCache:
                system = self._systems[self._rowToSystemNumber(index.row())]
                gridValue = system.getNoteHead(gridTime, line)
                self._dataCache[(gridTime, line)] = QVariant(gridValue)
            return self._dataCache[(gridTime, line)]
        elif role == Qt.TextAlignmentRole:
            return QVariant(Qt.AlignCenter)
        elif role == Qt.SizeHintRole:
            return QSize(10, 10)
        else:
            return QVariant()

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            return QVariant("%02d" % (int(section) + 1))
        else:
            try:
                lineIndex = self._rowToLineIndex(int(section))
            except _NoDataError:
                return QVariant()
            return QVariant(self.score[lineIndex].instrument.abbr)

    def addNote(self, index, head = None):
        try:
            gridTime, lineIndex = self._gridToTimeAndLineIndex(index.row(),
                                                           index.column())
        except _NoDataError:
            return
        system = self._systems[self._rowToSystemNumber(index.row())]
        system.addNote(gridTime, lineIndex, head)
        self._dataCache.pop((gridTime, lineIndex), None)
        self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)

    def delNote(self, index):
        try:
            gridTime, lineIndex = self._gridToTimeAndLineIndex(index.row(),
                                                           index.column())
        except _NoDataError:
            return
        system = self._systems[self._rowToSystemNumber(index.row())]
        system.delNote(gridTime, lineIndex)
        self._dataCache.pop((gridTime, lineIndex), None)
        self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)

    def toggleNote(self, index, noteHead):
        print index.column()
        try:
            gridTime, lineIndex = self._gridToTimeAndLineIndex(index.row(),
                                                           index.column())
        except _NoDataError:
            return
        system = self._systems[self._rowToSystemNumber(index.row())]
        self._dataCache.pop((gridTime, lineIndex), None)
        system.toggleNote(gridTime, lineIndex, noteHead)
        self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
