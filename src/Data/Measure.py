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
from DBConstants import EMPTY_NOTE, BAR_TYPES
from DBErrors import BadTimeError, TooManyBarLines
from NotePosition import NotePosition
from Data import MeasureCount
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
    '''
    classdocs
    '''

    def __init__(self, width = 0):
        self._width = width
        self._notes = _NoteDictionary()
        self.startBar = BAR_TYPES["NORMAL_BAR"]
        self.endBar = BAR_TYPES["NORMAL_BAR"]
        self._callBack = None
        self._info = MeasureInfo()
        self.counter = None
        self.alternateText = None

    def _getrepeatCount(self):
        return self._info.repeatCount
    def _setrepeatCount(self, value):
        if value != self._info.repeatCount:
            if self.isRepeatEnd():
                self._info.repeatCount = max(value, 2)
            else:
                self._info.repeatCount = 1
            self._runCallBack(NotePosition())
    repeatCount = property(fget = _getrepeatCount,
                         fset = _setrepeatCount)

    def __len__(self):
        return self._width

    def __iter__(self):
        return self._notes.iterNotesAndHeads()

    def numNotes(self):
        return self._notes.numNotes()

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

    def setSectionEnd(self, boolean):
        self._info.isSectionEnd = boolean
        if boolean:
            self.endBar |= BAR_TYPES["SECTION_END"]
        else:
            self.endBar &= ~BAR_TYPES["SECTION_END"]

    def setRepeatStart(self, boolean):
        self._info.isRepeatStart = boolean
        if boolean:
            self.startBar |= BAR_TYPES["REPEAT_START"]
        else:
            self.startBar &= ~BAR_TYPES["REPEAT_START"]

    def setRepeatEnd(self, boolean):
        self._info.isRepeatEnd = boolean
        if boolean:
            self.endBar |= BAR_TYPES["REPEAT_END"]
            self.repeatCount = max(self.repeatCount, 2)
        else:
            self.repeatCount = 1
            self.endBar &= ~BAR_TYPES["REPEAT_END"]

    def setLineBreak(self, boolean):
        self._info.isLineBreak = boolean
        if boolean:
            self.endBar |= BAR_TYPES["LINE_BREAK"]
        else:
            self.endBar &= ~BAR_TYPES["LINE_BREAK"]

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

    def noteAt(self, noteTime, drumIndex):
        if not(0 <= noteTime < len(self)):
            raise BadTimeError(noteTime)
        return self._notes.getNote(noteTime, drumIndex)

    def clear(self):
        self._notes.clear()
        self._runCallBack(NotePosition())

    def addNote(self, position, head):
        if not(0 <= position.noteTime < len(self)):
            raise BadTimeError(position)
        if self._notes.setNote(position.noteTime, position.drumIndex, head):
            self._runCallBack(position)

    def deleteNote(self, position):
        if not(0 <= position.noteTime < len(self)):
            raise BadTimeError(position)
        if self._notes.delNote(position.noteTime, position.drumIndex):
            self._runCallBack(position)

    def toggleNote(self, position, head):
        if not(0 <= position.noteTime < len(self)):
            raise BadTimeError(position)
        oldHead = self._notes.getNote(position.noteTime, position.drumIndex)
        if (oldHead == head):
            self.deleteNote(position)
        else:
            self.addNote(position, head)

    def _setWidth(self, newWidth):
        assert(newWidth > 0)
        if newWidth == len(self):
            return
        self._width = newWidth
        badTimes = [noteTime for noteTime in self._notes.iterTimes()
                    if noteTime >= self._width]
        for badTime in badTimes:
            self._notes.deleteAllNotesAtTime(badTime)
        self._runCallBack(NotePosition())

    def setBeatCount(self, counter):
        if counter == self.counter:
            return
        if self.counter is None:
            self.counter = counter
            self._setWidth(len(counter))
            return
        oldNotes = copy.deepcopy(self._notes)
        oldTimes = list(self.counter.iterTime())
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
            oldIndex += 1
            newIndex += 1
        self.counter = counter
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
        return (self._notes.notesOnLine(index) > 0)

    def write(self, indenter):
        with indenter.section("START_BAR %d" % len(self), "END_BAR"):
            if self.counter is not None:
                self.counter.write(indenter)
            startString = [name for name, value in BAR_TYPES.iteritems()
                           if (self.startBar & value) == value]
            indenter("BARLINE %s" % ",".join(startString))
            for pos, head in self:
                indenter("NOTE %d,%d,%s" % (pos.noteTime, pos.drumIndex, head))
            endString = [name for name, value in BAR_TYPES.iteritems()
                         if (self.endBar & value) == value ]
            indenter("BARLINE %s" % ",".join(endString))
            if self.repeatCount != 1:
                indenter("REPEAT_COUNT %d" % self.repeatCount)
            if self.alternateText is not None:
                indenter("ALTERNATE %s" % self.alternateText)

    class _BarlineTracker(object):
        @staticmethod
        def doNothing(dummy):
            pass

        def __init__(self, measure):
            self.measure = measure
            self.seenStartLine = False
            self.seenEndLine = False
            self.mapping = {"NO_BAR" : self.doNothing,
                            "NORMAL_BAR" : self.doNothing,
                            "REPEAT_START": measure.setRepeatStart,
                            "REPEAT_END": measure.setRepeatEnd,
                            "SECTION_END": measure.setSectionEnd,
                            "LINE_BREAK": measure.setLineBreak}

        def processBarline(self, lineData):
            if not self.seenStartLine:
                self.measure.startBar = 0
                for barType in lineData.split(","):
                    self.measure.startBar |= BAR_TYPES[barType]
                    self.mapping[barType](True)
                self.seenStartLine = True
            elif not self.seenEndLine:
                self.measure.endBar = 0
                for barType in lineData.split(","):
                    self.measure.endBar |= BAR_TYPES[barType]
                    self.mapping[barType](True)
                self.seenEndLine = True
            else:
                raise TooManyBarLines("Too many bar lines")

    def _readNote(self, lineData):
        noteTime, drumIndex, head = lineData.split(",")
        pos = NotePosition(noteTime = int(noteTime),
                           drumIndex = int(drumIndex))
        self.addNote(pos, head)

    def _makeOldMeasure(self, lineData):
        self.counter = MeasureCount.counterMaker(int(lineData),
                                                 len(self))

    def _readCounter(self, scoreIterator):
        counter = MeasureCount.MeasureCount()
        counter.read(scoreIterator)
        self.setBeatCount(counter)

    def read(self, scoreIterator):
        tracker = self._BarlineTracker(self)
        self.counter = MeasureCount.MeasureCount()
        with scoreIterator.section("START_BAR", "END_BAR") as section:
            section.readCallback("BARLINE", tracker.processBarline)
            section.readCallback("NOTE", self._readNote)
            section.readSubsection("COUNT_INFO_START", self._readCounter)
            section.readCallback("BEATLENGTH", self._makeOldMeasure)
            section.readPositiveInteger("REPEAT_COUNT", self, "repeatCount")
            section.readString("ALTERNATE", self, "alternateText")
