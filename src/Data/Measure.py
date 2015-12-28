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

from collections import defaultdict
from Data.DBConstants import EMPTY_NOTE, BAR_TYPES, NORMAL_BAR, REPEAT_END_STR, REPEAT_START, LINE_BREAK, SECTION_END
from Data.DBErrors import BadTimeError
from Data.NotePosition import NotePosition
from Data import MeasureCount
from Data import Counter
import copy

class _NoteDictionary(object):
    def __init__(self):
        self._notes = defaultdict(defaultdict)
        self._notesOnLine = defaultdict(int)
        self._noteTimes = []

    def __len__(self):
        return len(self._noteTimes)

    def numNotes(self):
        return sum(self._notesOnLine.itervalues())

    def iterTimes(self):
        return iter(self._noteTimes)

    def iterNotesAtTime(self, noteTime):
        for index, head in self._notes[noteTime].iteritems():
            yield (NotePosition(noteTime = noteTime,
                                drumIndex = index),
                       head)

    def iterNotesAndHeads(self):
        for noteTime in self.iterTimes():
            drumDict = self._notes[noteTime]
            for drumIndex, drumHead in drumDict.iteritems():
                yield (NotePosition(noteTime = noteTime,
                                   drumIndex = drumIndex),
                       drumHead)

    def __contains__(self, noteTime):
        return noteTime in self._notes

    def setNote(self, noteTime, drumIndex, head):
        if noteTime not in self._notes:
            self._noteTimes.append(noteTime)
            self._noteTimes.sort()
        if drumIndex not in self._notes[noteTime]:
            self._notesOnLine[drumIndex] += 1
        elif head == self._notes[noteTime][drumIndex]:
            return False
        self._notes[noteTime][drumIndex] = head
        return True

    def delNote(self, noteTime, drumIndex):
        if noteTime in self and drumIndex in self._notes[noteTime]:
            del self._notes[noteTime][drumIndex]
            self._notesOnLine[drumIndex] -= 1
            if len(self._notes[noteTime]) == 0:
                del self._notes[noteTime]
                self._noteTimes.remove(noteTime)
            return True
        return False

    def deleteAllNotesAtTime(self, noteTime):
        if noteTime not in self:
            return
        self._noteTimes.remove(noteTime)
        for drumIndex in self._notes[noteTime]:
            self._notesOnLine[drumIndex] -= 1
        del self._notes[noteTime]

    def getNote(self, noteTime, drumIndex):
        if noteTime not in self or drumIndex not in self._notes[noteTime]:
            return EMPTY_NOTE
        return self._notes[noteTime][drumIndex]

    def notesOnLine(self, index):
        return self._notesOnLine[index]

    def clear(self):
        self._notes.clear()
        self._noteTimes = []
        self._notesOnLine.clear()

class MeasureInfo(object):
    def __init__(self):
        self.isRepeatEnd = False
        self.isRepeatStart = False
        self.isSectionEnd = False
        self.isLineBreak = False
        self.repeatCount = 1


class Measure(object):
    def __init__(self, width = 0):
        self._width = width
        self._notes = _NoteDictionary()
        self._callBack = None
        self._info = MeasureInfo()
        self._counter = None
        self.alternateText = None
        self.simileDistance = 0
        self.simileIndex = 0
        self._above = " " * width
        self._below = " " * width
        self.showAbove = False
        self.showBelow = False

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, counter):
        self.setBeatCount(counter)

    @property
    def repeatCount(self):
        return self._info.repeatCount

    @repeatCount.setter
    def repeatCount(self, value):
        if value != self._info.repeatCount:
            if self.isRepeatEnd():
                self._info.repeatCount = max(value, 2)
            else:
                self._info.repeatCount = 1
            self._runCallBack(NotePosition())

    def __len__(self):
        return self._width

    def __iter__(self):
        return self._notes.iterNotesAndHeads()

    def numNotes(self):
        return self._notes.numNotes()

    def numBeats(self):
        return self.counter.numBeats()

    def _runCallBack(self, position):
        if self._callBack is not None:
            self._callBack(position)

    def setCallBack(self, callBack):
        self._callBack = callBack

    def clearCallBack(self):
        self._callBack = None

    def isEmpty(self):
        return (len(self._notes) == 0
                and not (self.isRepeatEnd() or
                         self.isSectionEnd()))

    @property
    def startBar(self):
        val = BAR_TYPES[NORMAL_BAR]
        if self.isRepeatStart():
            val |= BAR_TYPES[REPEAT_START]
        return val

    @startBar.setter
    def startBar(self, value):
        self.setRepeatStart(value & BAR_TYPES[REPEAT_START] != 0)

    @property
    def endBar(self):
        val = BAR_TYPES[NORMAL_BAR]
        if self.isRepeatEnd():
            val |= BAR_TYPES[REPEAT_END_STR]
        if self.isSectionEnd():
            val |= BAR_TYPES[SECTION_END]
        if self.isLineBreak():
            val |= BAR_TYPES[LINE_BREAK]
        return val

    @endBar.setter
    def endBar(self, value):
        self.setRepeatEnd(value & BAR_TYPES[REPEAT_END_STR] != 0)
        self.setLineBreak(value & BAR_TYPES[LINE_BREAK] != 0)
        self.setSectionEnd(value & BAR_TYPES[SECTION_END] != 0)

    def setSectionEnd(self, boolean):
        self._info.isSectionEnd = boolean

    def setRepeatStart(self, boolean):
        self._info.isRepeatStart = boolean

    def setRepeatEnd(self, boolean):
        self._info.isRepeatEnd = boolean
        if boolean:
            self.repeatCount = max(self.repeatCount, 2)
        else:
            self.repeatCount = 1

    def setLineBreak(self, boolean):
        self._info.isLineBreak = boolean

    def isSectionEnd(self):
        return self._info.isSectionEnd

    def isRepeatStart(self):
        return self._info.isRepeatStart

    def isRepeatEnd(self):
        return self._info.isRepeatEnd

    def isLineBreak(self):
        return self._info.isLineBreak

    def isLineEnd(self):
        return self.isLineBreak() or self.isSectionEnd()

    def getNote(self, position):
        return self.noteAt(position.noteTime, position.drumIndex)

    def _checkValidNoteTime(self, noteTime):
        if not(0 <= noteTime < len(self)):
            raise BadTimeError(noteTime)

    def _checkValidPosition(self, position):
        self._checkValidNoteTime(position.noteTime)

    def noteAt(self, noteTime, drumIndex):
        self._checkValidNoteTime(noteTime)
        return self._notes.getNote(noteTime, drumIndex)

    def clear(self):
        self._notes.clear()
        self._above = " " * len(self)
        self._below = " " * len(self)
        self._runCallBack(NotePosition())

    def addNote(self, position, head):
        self._checkValidPosition(position)
        if self._notes.setNote(position.noteTime, position.drumIndex, head):
            self._runCallBack(position)

    def deleteNote(self, position):
        self._checkValidPosition(position)
        if self._notes.delNote(position.noteTime, position.drumIndex):
            self._runCallBack(position)

    def toggleNote(self, position, head):
        self._checkValidPosition(position)
        oldHead = self._notes.getNote(position.noteTime, position.drumIndex)
        if oldHead == head:
            self.deleteNote(position)
        else:
            self.addNote(position, head)

    def _setWidth(self, newWidth):
        assert newWidth > 0
        if newWidth == len(self):
            return
        elif newWidth > self._width:
            self._above += " " * (newWidth - self._width)
            self._below += " " * (newWidth - self._width)
        else:
            self._above = self._above[:newWidth]
            self._below = self._below[:newWidth]
        self._width = newWidth
        badTimes = [noteTime for noteTime in self._notes.iterTimes()
                    if noteTime >= self._width]
        for badTime in badTimes:
            self._notes.deleteAllNotesAtTime(badTime)
        self._runCallBack(NotePosition())

    def setBeatCount(self, counter):  # TODO: change this to setMeasureCount
        if counter == self._counter:
            return
        oldAbove = self._above
        oldBelow = self._below
        if self._counter is None:
            self._counter = counter
            self._setWidth(len(counter))
            return
        oldNotes = copy.deepcopy(self._notes)
        oldTimes = list(self._counter.iterTime())
        self._setWidth(len(counter))
        self.clear()
        newTimes = list(counter.iterTime())
        oldIndex = 0
        newIndex = 0
        while oldIndex < len(oldTimes) and newIndex < len(newTimes):
            oldBeat, oldTick, oldCount = oldTimes[oldIndex]
            newBeat, newTick, newCount = newTimes[newIndex]
            if oldBeat < newBeat:
                oldIndex += 1
                continue
            elif newBeat < oldBeat:
                newIndex += 1
                continue
            prod1 = oldTick * newCount
            prod2 = newTick * oldCount
            if prod1 < prod2:
                oldIndex += 1
                continue
            elif prod2 < prod1:
                newIndex += 1
                continue
            if oldIndex in oldNotes:
                for position, head in oldNotes.iterNotesAtTime(oldIndex):
                    self._notes.setNote(newIndex, position.drumIndex, head)
                self.setAbove(newIndex, oldAbove[oldIndex])
                self.setBelow(newIndex, oldBelow[oldIndex])
            oldIndex += 1
            newIndex += 1
        self._counter = counter
        self._runCallBack(NotePosition())

    def copyMeasure(self):
        copyMeasure = copy.deepcopy(self)
        copyMeasure.clearCallBack()
        return copyMeasure

    def count(self):
        if self.counter is None:
            return [" "] * len(self)
        else:
            return list(self.counter.count())

    def pasteMeasure(self, other, copyMeasureDecorations = False):
        oldMeasure = self.copyMeasure()
        self.clear()
        if other.counter is None:
            self._setWidth(len(other))
        self.setBeatCount(other.counter)
        for pos, head in other:
            self.addNote(pos, head)
        if copyMeasureDecorations:
            self.setRepeatStart(other.isRepeatStart())
            self.setRepeatEnd(other.isRepeatEnd())
            self.setSectionEnd(other.isSectionEnd())
            self.setLineBreak(other.isLineBreak())
            self.repeatCount = other.repeatCount
            self.alternateText = other.alternateText
            self.simileDistance = other.simileDistance
            self.simileIndex = other.simileIndex
            self.aboveText = other.aboveText
            self.belowText = other.belowText
            self.showAbove = other.showAbove
            self.showBelow = other.showBelow
        return oldMeasure


    def changeKit(self, newKit, changes):
        transposed = defaultdict(lambda: defaultdict(dict))
        for note, head in self._notes.iterNotesAndHeads():
            transposed[note.drumIndex][note.noteTime] = head
        self._notes.clear()
        for newDrumIndex, newDrum in enumerate(newKit):
            oldDrumIndex = changes[newDrumIndex]
            if oldDrumIndex == -1:
                continue
            for noteTime, head in transposed[oldDrumIndex].iteritems():
                if not newDrum.isAllowedHead(head):
                    head = newDrum.head
                self.addNote(NotePosition(None, None,
                                          noteTime, newDrumIndex),
                             head)

    def lineIsVisible(self, index):
        return self._notes.notesOnLine(index) > 0

    def getSmallestSimpleCount(self):
        if not self.counter.isSimpleCount():
            return None
        numBeats = self.counter.numBeats()
        maxLen = len(self)
        newCount = None
        for unused_, count in Counter.DEFAULT_REGISTRY:
            if len(count) * numBeats >= maxLen:
                continue
            mcount = MeasureCount.makeSimpleCount(count, numBeats)
            newMeasure = self.copyMeasure()
            newMeasure.setBeatCount(mcount)
            if self.numNotes() == newMeasure.numNotes():
                newCount = mcount
        return newCount

    def _replace(self, text, noteTime, value):
        self._checkValidNoteTime(noteTime)
        value = " " if not value else value
        if len(text) == 1:
            return value
        elif noteTime == 0:
            return value + text[1:]
        elif noteTime == len(text) - 1:
            return text[:-1] + value
        else:
            return text[:noteTime] + value + text[noteTime + 1:]

    def setAbove(self, noteTime, value):
        self._above = self._replace(self._above, noteTime, value)
        self._runCallBack(NotePosition())

    def setBelow(self, noteTime, value):
        self._below = self._replace(self._below, noteTime, value)
        self._runCallBack(NotePosition())

    @property
    def aboveText(self):
        return self._above

    @aboveText.setter
    def aboveText(self, value):
        if len(value) > len(self):
            value = value[:len(self)]
        elif len(value) < len(self):
            value += " " * (len(self) - len(value))
        self._above = value

    @property
    def belowText(self):
        return self._below

    @belowText.setter
    def belowText(self, value):
        if len(value) > len(self):
            value = value[:len(self)]
        elif len(value) < len(self):
            value += " " * (len(self) - len(value))
        self._below = value
