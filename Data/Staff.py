'''
Created on 12 Dec 2010

@author: Mike Thomas

'''
from DBErrors import BadTimeError
from DBConstants import COMBINED_BARLINE_STRING, BAR_TYPES
class Staff(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._measures = []
        self._callBack = None

    def _runCallBack(self, measureIndex, noteTime, drumIndex):
        if self._callBack is not None:
            self._callBack(measureIndex, noteTime, drumIndex)

    def setCallBack(self, callBack):
        self._callBack = callBack

    def clearCallBack(self):
        self._callBack = None

    def __len__(self):
        return sum(len(m) for m in self._measures)

    def __iter__(self):
        return iter(self._measures)

    def __getitem__(self, index):
        return self._measures[index]

    def numMeasures(self):
        return len(self._measures)

    def _setMeasureCallBack(self, measure, measureIndex):
        def wrappedCallBack(noteTime, drumIndex):
            self._runCallBack(measureIndex, noteTime, drumIndex)
        measure.setCallBack(wrappedCallBack)

    def addMeasure(self, measure):
        self._measures.append(measure)
        self._setMeasureCallBack(self._measures[-1], len(self._measures) - 1)

    def deleteMeasure(self, index):
        if not (0 <= index < self.numMeasures()):
            raise BadTimeError(index)
        measure = self._measures.pop(index)
        measure.clearCallBack()
        for measureIndex, nextMeasure in enumerate(self._measures[index:]):
            self._setMeasureCallBack(nextMeasure, index + measureIndex)

    def insertMeasure(self, index, measure):
        if not (0 <= index <= self.numMeasures()):
            raise BadTimeError(index)
        self._measures.insert(index, measure)
        for measureIndex in range(index, self.numMeasures()):
            nextMeasure = self[measureIndex]
            self._setMeasureCallBack(nextMeasure, measureIndex)

    def clear(self):
        self._measures = []

    def characterWidth(self):
        if self.numMeasures() == 0:
            return 0
        total = len(self)
        lastEnd = BAR_TYPES["NO_BAR"]
        for measure in self:
            key = (lastEnd, measure.startBar)
            total += len(COMBINED_BARLINE_STRING[key])
            lastEnd = measure.endBar
        key = (lastEnd, BAR_TYPES["NO_BAR"])
        total += len(COMBINED_BARLINE_STRING[key])
        return total

    def gridWidth(self):
        if self.numMeasures() == 0:
            return 0
        return len(self) + self.numMeasures() + 1

    def getNote(self, measureIndex, timeIndex, noteIndex):
        if not (0 <= measureIndex < self.numMeasures()):
            raise BadTimeError(measureIndex)
        return self[measureIndex].getNote(timeIndex, noteIndex)

    def addNote(self, measureIndex, timeIndex, noteIndex, head):
        if not (0 <= measureIndex < self.numMeasures()):
            raise BadTimeError(measureIndex)
        self[measureIndex].addNote(timeIndex, noteIndex, head)

    def deleteNote(self, measureIndex, timeIndex, noteIndex):
        if not (0 <= measureIndex < self.numMeasures()):
            raise BadTimeError(measureIndex)
        self[measureIndex].deleteNote(timeIndex, noteIndex)

    def toggleNote(self, measureIndex, timeIndex, noteIndex, head):
        if not (0 <= measureIndex < self.numMeasures()):
            raise BadTimeError(measureIndex)
        self[measureIndex].toggleNote(timeIndex, noteIndex, head)

