'''
Created on 12 Dec 2010

@author: Mike Thomas

'''
from DBErrors import BadTimeError
from DBConstants import COMBINED_BARLINE_STRING
from NotePosition import NotePosition
from Measure import Measure

#pylint:disable-msg=R0904
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

    def _runCallBack(self, position):
        if self._callBack is not None:
            self._callBack(position)

    def setCallBack(self, callBack):
        self._callBack = callBack

    def clearCallBack(self):
        self._callBack = None

    def __len__(self):
        return sum(len(m) for m in self._measures)

    def __iter__(self):
        return iter(self._measures)

    def iterNotes(self):
        for mIndex, measure in enumerate(self._measures):
            for np, head in measure:
                np.measureIndex = mIndex
                yield np, head

    def __getitem__(self, index):
        return self._measures[index]

    def numMeasures(self):
        return len(self._measures)

    def _setMeasureCallBack(self, measure, measureIndex):
        def wrappedCallBack(position):
            position.measureIndex = measureIndex
            self._runCallBack(position)
        measure.setCallBack(wrappedCallBack)

    def addMeasure(self, measure):
        self._measures.append(measure)
        self._setMeasureCallBack(self._measures[-1], len(self._measures) - 1)

    def deleteLastMeasure(self):
        if self.numMeasures() > 0:
            measure = self._measures.pop()
            measure.clearCallBack()

    def deleteMeasure(self, position):
        if not (0 <= position.measureIndex < self.numMeasures()):
            raise BadTimeError(position)
        measure = self._measures.pop(position.measureIndex)
        measure.clearCallBack()
        iterator = enumerate(self._measures[position.measureIndex:])
        for index, nextMeasure in iterator:
            self._setMeasureCallBack(nextMeasure,
                                     position.measureIndex + index)

    def insertMeasure(self, position, measure):
        if not (0 <= position.measureIndex <= self.numMeasures()):
            raise BadTimeError(position)
        self._measures.insert(position.measureIndex, measure)
        for index in range(position.measureIndex, self.numMeasures()):
            nextMeasure = self[index]
            self._setMeasureCallBack(nextMeasure, index)

    def copyMeasure(self, position):
        if not (0 <= position.measureIndex <= self.numMeasures()):
            raise BadTimeError(position)
        return self[position.measureIndex].copyMeasure()

    def pasteMeasure(self, position, notes):
        if not (0 <= position.measureIndex <= self.numMeasures()):
            raise BadTimeError(position)
        self[position.measureIndex].pasteMeasure(position, notes)

    def setMeasureBeatCount(self, position, beats, counter):
        if not (0 <= position.measureIndex <= self.numMeasures()):
            raise BadTimeError(position)
        self[position.measureIndex].setBeatCount(beats, counter)

    def setSectionEnd(self, position, onOff):
        if not (0 <= position.measureIndex < self.numMeasures()):
            raise BadTimeError(position)
        self._measures[position.measureIndex].setSectionEnd(onOff)

    def isSectionEnd(self):
        return self[-1].isSectionEnd()

    def isConsistent(self):
        ok = True
        for measure in self[:-1]:
            ok = ok and not measure.isSectionEnd()
        return ok

    def setLineBreak(self, position, onOff):
        if not (0 <= position.measureIndex < self.numMeasures()):
            raise BadTimeError(position)
        self._measures[position.measureIndex].setLineBreak(onOff)

    def setRepeatEnd(self, position, onOff):
        if not (0 <= position.measureIndex < self.numMeasures()):
            raise BadTimeError(position)
        self._measures[position.measureIndex].setRepeatEnd(onOff)

    def setRepeatStart(self, position, onOff):
        if not (0 <= position.measureIndex < self.numMeasures()):
            raise BadTimeError(position)
        self._measures[position.measureIndex].setRepeatStart(onOff)

    def clear(self):
        for measure in self:
            measure.clearCallBack()
        self._measures = []

    def characterWidth(self):
        if self.numMeasures() == 0:
            return 0
        total = len(self)
        lastBar = None
        for measure in self:
            key = Measure.barlineKey(lastBar, measure)
            total += len(COMBINED_BARLINE_STRING[key])
            lastBar = measure
        key = Measure.barlineKey(lastBar, None)
        total += len(COMBINED_BARLINE_STRING[key])
        return total

    def gridWidth(self):
        if self.numMeasures() == 0:
            return 0
        return len(self) + self.numMeasures() + 1

    def getNote(self, position):
        if not (0 <= position.measureIndex < self.numMeasures()):
            raise BadTimeError(position)
        return self[position.measureIndex].getNote(position)

    def addNote(self, position, head):
        if not (0 <= position.measureIndex < self.numMeasures()):
            raise BadTimeError(position)
        self[position.measureIndex].addNote(position, head)

    def deleteNote(self, position):
        if not (0 <= position.measureIndex < self.numMeasures()):
            raise BadTimeError(position)
        self[position.measureIndex].deleteNote(position)

    def toggleNote(self, position, head):
        if not (0 <= position.measureIndex < self.numMeasures()):
            raise BadTimeError(position)
        self[position.measureIndex].toggleNote(position, head)

    def _getDrumLine(self, drum, position, drumIndex):
        position.drumIndex = drumIndex
        lastBar = None
        lineString = "%2s" % drum.abbr
        for measureIndex, measure in enumerate(self):
            position.measureIndex = measureIndex
            key = Measure.barlineKey(lastBar, measure)
            barString = COMBINED_BARLINE_STRING[key]
            lineString += barString
            lastBar = measure
            for noteTime in range(len(measure)):
                position.noteTime = noteTime
                note = measure.getNote(position)
                lineString += note
        key = Measure.barlineKey(lastBar, None)
        barString = COMBINED_BARLINE_STRING[key]
        lineString += barString
        return lineString

    def _getCountLine(self):
        countString = "  "
        lastBar = None
        for measure in self:
            key = Measure.barlineKey(lastBar, measure)
            barString = COMBINED_BARLINE_STRING[key]
            lastBar = measure
            countString += " " * len(barString)
            countString += "".join(measure.count())
        key = Measure.barlineKey(lastBar, None)
        barString = COMBINED_BARLINE_STRING[key]
        countString += " " * len(barString)
        return countString

    def exportASCII(self, kit):
        kitSize = len(kit)
        indices = range(0, kitSize)
        indices.reverse()
        position = NotePosition()
        staffString = []
        for drumIndex in indices:
            drum = kit[drumIndex]
            lineString = self._getDrumLine(drum,
                                           position,
                                           drumIndex)
            staffString.append(lineString)
        countString = self._getCountLine()
        staffString.append(countString)
        return staffString
