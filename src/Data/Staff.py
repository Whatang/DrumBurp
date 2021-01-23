# Copyright 2011-12 Michael Thomas
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
from Data.DBErrors import BadTimeError


class Staff(object):
    def __init__(self):
        self._measures = []
        self._callBack = None
        self._visibleLines = {}

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

    def __getitem__(self, index):
        return self._measures[index]

    def numMeasures(self):
        return len(self._measures)

    def _setMeasureCallBack(self, measure, measureIndex):
        def wrappedCallBack(position):
            position.measureIndex = measureIndex
            self._runCallBack(position)
        measure.setCallBack(wrappedCallBack)

    def _isValidPosition(self, position, afterOk=False):
        if not (0 <= position.measureIndex < self.numMeasures()):
            if not (afterOk and position.measureIndex == self.numMeasures()):
                raise BadTimeError(position)

    def addMeasure(self, measure):
        self._measures.append(measure)
        self._setMeasureCallBack(self._measures[-1], len(self._measures) - 1)
        self._visibleLines = {}

    def deleteLastMeasure(self):
        if self.numMeasures() > 0:
            measure = self._measures.pop()
            measure.clearCallBack()
            self._visibleLines = {}

    def deleteMeasure(self, position):
        self._isValidPosition(position)
        measure = self._measures.pop(position.measureIndex)
        measure.clearCallBack()
        self._visibleLines = {}
        iterator = enumerate(self._measures[position.measureIndex:])
        for index, nextMeasure in iterator:
            self._setMeasureCallBack(nextMeasure,
                                     position.measureIndex + index)

    def insertMeasure(self, position, measure):
        self._isValidPosition(position, True)
        self._measures.insert(position.measureIndex, measure)
        self._visibleLines = {}
        for index in range(position.measureIndex, self.numMeasures()):
            nextMeasure = self[index]
            self._setMeasureCallBack(nextMeasure, index)

    def copyMeasure(self, position):
        self._isValidPosition(position)
        return self[position.measureIndex].copyMeasure()

    def pasteMeasure(self, position, notes, copyMeasureDecorations=False):
        self._isValidPosition(position)
        self._visibleLines = {}
        return self[position.measureIndex].pasteMeasure(notes,
                                                        copyMeasureDecorations)

    def setSectionEnd(self, position, onOff):
        self._isValidPosition(position)
        self._measures[position.measureIndex].setSectionEnd(onOff)

    def isSectionEnd(self):
        return self.numMeasures() > 0 and self[-1].isSectionEnd()

    def isConsistent(self):
        ok = True
        for measure in self[:-1]:
            ok = ok and not measure.isSectionEnd()
        return ok

    def clear(self):
        for measure in self:
            measure.clearCallBack()
        self._measures = []
        self._visibleLines = {}

    def addNote(self, position, head):
        self._isValidPosition(position)
        self[position.measureIndex].addNote(position, head)
        if position.drumIndex in self._visibleLines:
            self._visibleLines.pop(position.drumIndex)

    def deleteNote(self, position):
        self._isValidPosition(position)
        self[position.measureIndex].deleteNote(position)
        if position.drumIndex in self._visibleLines:
            self._visibleLines.pop(position.drumIndex)

    def toggleNote(self, position, head):
        self._isValidPosition(position)
        self[position.measureIndex].toggleNote(position, head)
        if position.drumIndex in self._visibleLines:
            self._visibleLines.pop(position.drumIndex)

    def lineIsVisible(self, index):
        if index not in self._visibleLines:
            visible = any(measure.lineIsVisible(index) for measure in self)
            self._visibleLines[index] = visible
        return self._visibleLines[index]
