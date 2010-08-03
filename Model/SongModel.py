'''
Created on 31 Jul 2010

@author: Mike Thomas

'''

from Model.ScoreSystem import ScoreSystem
from PyQt4.QtCore import Qt, QVariant, QAbstractTableModel, QModelIndex, SIGNAL, QSize
import Data.Score

class _NoDataError(StandardError):
    '''
    There is nothing defined for the Score in this grid.
    '''

def _makeDirtyProperty(name):
    def _set(self, value):
        if value != getattr(self, name):
            setattr(self, name, value)
            self._recalculate = True
    def _get(self):
        return getattr(self, name)
    return property(_get, _set)


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
        self._width = 80
        self._systems = []
        self._recalculate = True
        self._calculateSystems()

    width = _makeDirtyProperty("_width")

    def rowCount(self, unusedIndex = QModelIndex()):
        if self._recalculate:
            self._calculateSystems()
        return max(0,
                   (len(self._systems) * (len(self.score) + 1)) - 1)

    def columnCount(self, unusedIndex = QModelIndex()):
        if self._recalculate:
            self._calculateSystems()
        return self.width

    def _rowToSystemNumber(self, row):
        return row / (len(self.score) + 1)

    def _rowToLineIndex(self, row):
        if (row % (len(self.score) + 1)) == len(self.score):
            raise _NoDataError()
        return len(self.score) - (row % (len(self.score) + 1)) - 1

    def _gridToTimeAndLineIndex(self, row, col):
        scoreSystem = self._systems[self._rowToSystemNumber(row)]
        if col > scoreSystem.lastTime:
            raise _NoDataError()
        return (scoreSystem.startTime + col, self._rowToLineIndex(row))

    def _calculateSystems(self):
        self._recalculate = False
        self._systems = []
        measures = []
        thisMeasure = []
        for note in self.score.iterNotes():
            thisMeasure.append(note)
            if note.head == Data.MEASURE_SPLIT:
                measures.append(thisMeasure)
                thisMeasure = []
        startTime = 0
        thisSystem = ScoreSystem(startTime)
        for measure in measures:
            lastNote = measure[-1]
            if lastNote.time - startTime < self.width:
                thisSystem.addNotes(measure)
            else:
                if thisSystem.lastTime != thisSystem.startTime:
                    # i.e. there is at least one measure on this line
                    # already, so end the line and start a new one
                    self._systems.append(thisSystem)
                    startTime = thisSystem.lastTime + 1
                    thisSystem = ScoreSystem(startTime)
                while startTime + self.width < lastNote.time:
                    # Add systems until we have enough for this measure
                    thisSystem.addNotes(n for n in measure if
                                        0 <= (n.time - startTime) < self.width)
                    thisSystem.lastTime = startTime + self.width - 1
                    self._systems.append(thisSystem)
                    startTime += self.width
                    thisSystem = ScoreSystem(startTime)
                thisSystem.addNotes(n for n in measure
                                    if startTime <= n.time)
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
                time, line = self._gridToTimeAndLineIndex(index.row(),
                                                          index.column())
            except _NoDataError:
                return QVariant()
            system = self._systems[self._rowToSystemNumber(index.row())]
            gridValue = system.getNoteHead(time, line)
            return QVariant(gridValue)
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
            time, lineIndex = self._gridToTimeAndLineIndex(index.row(),
                                                           index.column())
        except _NoDataError:
            return
        system = self._systems[self._rowToSystemNumber(index.row())]
        self.score.addNote(time, lineIndex, head)
        head = self.score.getNote(time, lineIndex)
        system.addNotes([Data.Note.Note(time, lineIndex, head)])
        self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)

    def delNote(self, index):
        try:
            time, lineIndex = self._gridToTimeAndLineIndex(index.row(),
                                                           index.column())
        except _NoDataError:
            return
        system = self._systems[self._rowToSystemNumber(index.row())]
        self.score.delNote(time, lineIndex)
        system.delNote(time, lineIndex)
        self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
