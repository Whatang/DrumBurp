'''
Created on 12 Dec 2010

@author: Mike Thomas

'''
from DBErrors import BadTimeError
from DBConstants import (EMPTY_NOTE, DRUM_ABBR_WIDTH,
                         REPEAT_STARTER, REPEAT_END, REPEAT_EXTENDER)
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
        return self[position.measureIndex].pasteMeasure(notes)

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
        return self.gridWidth()

    def gridWidth(self):
        if self.numMeasures() == 0:
            return 0
        return (len(self) + self.numMeasures() + 1
                + DRUM_ABBR_WIDTH)

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
        lineString = "%*s" % (DRUM_ABBR_WIDTH, drum.abbr)
        lineOk = False
        for measureIndex, measure in enumerate(self):
            position.measureIndex = measureIndex
            barString = Measure.barString(lastBar, measure)
            lineString += barString
            lastBar = measure
            for noteTime in range(len(measure)):
                position.noteTime = noteTime
                note = measure.getNote(position)
                lineString += note
                lineOk = lineOk or note != EMPTY_NOTE
        barString = Measure.barString(lastBar, None)
        lineString += barString
        return lineString, lineOk

    def _getCountLine(self):
        countString = "  "
        lastBar = None
        for measure in self:
            barString = Measure.barString(lastBar, measure)
            lastBar = measure
            countString += " " * len(barString)
            countString += "".join(measure.count())
        barString = Measure.barString(lastBar, None)
        countString += " " * len(barString)
        return countString


    def _getRepeatString(self, isRepeating):
        staffString = []
        hasRepeat = isRepeating or any(measure.isRepeatStart()
                                       for measure in self)
        if not hasRepeat:
            return staffString, isRepeating
        repeatString = "  "
        lastMeasure = None
        delta = 0
        for measure in list(self) + [None]:
            if not isRepeating:
                if measure and measure.isRepeatStart():
                    if (lastMeasure and lastMeasure.isRepeatEnd()):
                        repeatString += REPEAT_END
                        delta = 1
                    isRepeating = True
                    repeatString += REPEAT_STARTER
                elif (lastMeasure and
                    lastMeasure.isRepeatEnd()):
                    repeatString += REPEAT_END
                elif measure:
                    repeatString += " "
            elif isRepeating:
                repeatString += REPEAT_EXTENDER
            if measure is not None:
                if isRepeating:
                    repeatString += REPEAT_EXTENDER * (len(measure) - delta)
                    delta = 0
                else:
                    repeatString += " " * len(measure)
            if isRepeating and measure and measure.isRepeatEnd():
                isRepeating = False
                repeatCount = "%dx" % measure.repeatCount
                repeatCountLength = len(repeatCount)
                repeatString = repeatString[:-(repeatCountLength + 1)] + repeatCount + repeatString[-1:]
            lastMeasure = measure

        staffString = [repeatString]
        return staffString, isRepeating

    def exportASCII(self, kit, settings, isRepeating):
        kitSize = len(kit)
        indices = range(0, kitSize)
        indices.reverse()
        position = NotePosition()
        staffString, isRepeating = self._getRepeatString(isRepeating)
        for drumIndex in indices:
            drum = kit[drumIndex]
            lineString, lineOk = self._getDrumLine(drum,
                                                   position,
                                                   drumIndex)
            if lineOk or drum.locked or not settings.omitEmpty:
                staffString.append(lineString)
        if settings.printCounts:
            countString = self._getCountLine()
            staffString.append(countString)
        return staffString, isRepeating
