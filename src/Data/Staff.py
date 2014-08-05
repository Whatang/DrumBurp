# Copyright 2011 Michael Thomas
#
# See www.whatang.org for more information.
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DrumBurp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DrumBurp.  If not, see <http://www.gnu.org/licenses/>
'''
Created on 12 Dec 2010

@author: Mike Thomas

'''
from DBErrors import BadTimeError
from DBConstants import (EMPTY_NOTE, DRUM_ABBR_WIDTH,
                         REPEAT_STARTER, REPEAT_END,
                         REPEAT_EXTENDER, ALTERNATE_EXTENDER)
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

    def pasteMeasure(self, position, notes, copyMeasureDecorations = False):
        if not (0 <= position.measureIndex <= self.numMeasures()):
            raise BadTimeError(position)
        return self[position.measureIndex].pasteMeasure(notes,
                                                        copyMeasureDecorations)

    def setSectionEnd(self, position, onOff):
        if not (0 <= position.measureIndex < self.numMeasures()):
            raise BadTimeError(position)
        self._measures[position.measureIndex].setSectionEnd(onOff)

    def isSectionEnd(self):
        return self.numMeasures() > 0 and self[-1].isSectionEnd()

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
        return (len(self) + self.numMeasures() + 1)

    def getNote(self, position):
        if not (0 <= position.measureIndex < self.numMeasures()):
            raise BadTimeError(position)
        return self[position.measureIndex].getNote(position)

    def getItemAtPosition(self, position):
        if not (0 <= position.measureIndex < self.numMeasures()):
            raise BadTimeError(position)
        measure = self[position.measureIndex]
        if position.noteTime is None:
            return measure
        return measure.getNote(position)

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

    def lineIsVisible(self, index):
        return any(measure.lineIsVisible(index) for measure in self)

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


    def _getRepeatString(self, isRepeating, repeatExtender):
        staffString = []
        hasRepeat = isRepeating or any(measure.isRepeatStart()
                                       for measure in self)
        if not hasRepeat:
            return staffString, isRepeating, repeatExtender
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
                    repeatExtender = REPEAT_EXTENDER
                    repeatString += REPEAT_STARTER
                elif (lastMeasure and
                    lastMeasure.isRepeatEnd()):
                    repeatString += REPEAT_END
                elif measure:
                    repeatString += " "
            else:
                repeatString += repeatExtender
            if measure is not None:
                if measure.alternateText:
                    repeatString += measure.alternateText
                    delta += len(measure.alternateText)
                    repeatExtender = ALTERNATE_EXTENDER
                    isRepeating = True
                if isRepeating:
                    repeatString += repeatExtender * (len(measure) - delta)
                    delta = 0
                else:
                    repeatString += " " * len(measure)
            if isRepeating and measure and measure.isRepeatEnd():
                isRepeating = False
                if repeatExtender == REPEAT_EXTENDER:
                    repeatCount = "%dx" % measure.repeatCount
                    repeatCountLength = len(repeatCount)
                    repeatString = (repeatString[:-(repeatCountLength + 1)]
                                    + repeatCount + repeatString[-1:])
            lastMeasure = measure
        staffString = [repeatString]
        return (staffString, isRepeating, repeatExtender)

    def exportASCII(self, kit, settings, isRepeating, repeatExtender):
        kitSize = len(kit)
        indices = range(0, kitSize)
        indices.reverse()
        position = NotePosition()
        staffString, isRepeating, repeatExtender = self._getRepeatString(isRepeating, repeatExtender)
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
        return staffString, isRepeating, repeatExtender
