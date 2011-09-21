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

from collections import defaultdict
from DBConstants import EMPTY_NOTE, BARLINE, BAR_TYPES
from DBErrors import BadTimeError
from NotePosition import NotePosition
from Data import MeasureCount
import copy

class NoteDictionary(dict):
    def __init__(self, *args, **kwargs):
        super(NoteDictionary, self).__init__(*args, **kwargs)
        self.noteTimes = []

    def __iter__(self):
        return iter(self.noteTimes)

    def iterkeys(self):
        return iter(self.noteTimes)

    def itervalues(self):
        for noteTime in self.noteTimes:
            yield self[noteTime]

    def iteritems(self):
        for noteTime in self.noteTimes:
            yield (noteTime, self[noteTime])

    def __contains__(self, key):
        return key in self.noteTimes

    def __getitem__(self, key):
        if key not in self:
            self[key] = defaultdict(dict)
        return dict.__getitem__(self, key)

    def __setitem__(self, index, value):
        if index not in self:
            self.noteTimes.append(index)
            self.noteTimes.sort()
        super(NoteDictionary, self).__setitem__(index, value)

    def __delitem__(self, key):
        self.noteTimes.remove(key)
        dict.__delitem__(self, key)

    def clear(self):
        dict.clear(self)
        self.noteTimes = []

    def get(self, key, default = None):
        if key not in self:
            return default
        return self[key]

    def items(self):
        return list(self.iteritems())

    def keys(self):
        return list(self.iterkeys())

    def pop(self, key):
        item = dict.pop(self, key)
        self.noteTimes.remove(key)
        return item

    def popitem(self):
        key, value = dict.popitem(self)
        self.noteTimes.remove(key)
        return key, value

    def setdefault(self, key, default = None):
        if key not in self:
            self.noteTimes.append(default)
            self.noteTimes.sort()
        dict.setdefault(key, default)

    def values(self):
        return list(self.itervalues())




def _makeNoteDict():
    return NoteDictionary()

_DEFAULTREPEATCOUNT = 1

class Measure(object):
    '''
    classdocs
    '''

    def __init__(self, width = 0):
        self._width = width
        self._notes = _makeNoteDict()
        self.startBar = BAR_TYPES["NORMAL_BAR"]
        self.endBar = BAR_TYPES["NORMAL_BAR"]
        self._callBack = None
        self._isRepeatEnd = False
        self._isRepeatStart = False
        self._isSectionEnd = False
        self._isLineBreak = False
        self._repeatCount = _DEFAULTREPEATCOUNT
        self.counter = None
        self.alternateText = None

    @staticmethod
    def barString(first, second):
        if first is None and second is None:
            return ""
        else:
            return BARLINE

    def _getrepeatCount(self):
        return self._repeatCount
    def _setrepeatCount(self, value):
        if value != self._repeatCount:
            if self.isRepeatEnd():
                self._repeatCount = max(value, 2)
            else:
                self._repeatCount = 1
            self._runCallBack(NotePosition())
    repeatCount = property(fget = _getrepeatCount,
                         fset = _setrepeatCount)

    def __len__(self):
        return self._width

    def __iter__(self):
        for noteTime, drumDict in self._notes.iteritems():
            for drumIndex, drumHead in drumDict.iteritems():
                yield (NotePosition(noteTime = noteTime,
                                    drumIndex = drumIndex),
                       drumHead)

    def numNotes(self):
        return sum(len(drumIndex) for drumIndex in self._notes.itervalues())

    def _runCallBack(self, position):
        if self._callBack is not None:
            self._callBack(position)

    def setCallBack(self, callBack):
        self._callBack = callBack

    def clearCallBack(self):
        self._callBack = None

    def isEmpty(self):
        return (len(list(self)) == 0
                and not (self.isRepeatEnd() or
                         self.isSectionEnd()))

    def setSectionEnd(self, boolean):
        self._isSectionEnd = boolean
        if boolean:
            self.endBar |= BAR_TYPES["SECTION_END"]
        else:
            self.endBar &= ~BAR_TYPES["SECTION_END"]

    def setRepeatStart(self, boolean):
        self._isRepeatStart = boolean
        if boolean:
            self.startBar |= BAR_TYPES["REPEAT_START"]
        else:
            self.startBar &= ~BAR_TYPES["REPEAT_START"]

    def setRepeatEnd(self, boolean):
        self._isRepeatEnd = boolean
        if boolean:
            self.endBar |= BAR_TYPES["REPEAT_END"]
            self.repeatCount = max(self.repeatCount, 2)
        else:
            self.repeatCount = 1
            self.endBar &= ~BAR_TYPES["REPEAT_END"]

    def setLineBreak(self, boolean):
        self._isLineBreak = boolean
        if boolean:
            self.endBar |= BAR_TYPES["LINE_BREAK"]
        else:
            self.endBar &= ~BAR_TYPES["LINE_BREAK"]

    def isSectionEnd(self):
        return self._isSectionEnd

    def isRepeatStart(self):
        return self._isRepeatStart

    def isRepeatEnd(self):
        return self._isRepeatEnd

    def isLineBreak(self):
        return self._isLineBreak

    def isLineEnd(self):
        return self.isLineBreak() or self.isSectionEnd()

    def getNote(self, position):
        return self.noteAt(position.noteTime, position.drumIndex)

    def noteAt(self, noteTime, drumIndex):
        if not(0 <= noteTime < len(self)):
            raise BadTimeError(noteTime)
        if (noteTime in self._notes and
            drumIndex in self._notes[noteTime]):
            return self._notes[noteTime][drumIndex]
        return EMPTY_NOTE

    def clear(self):
        for pos, dummyHead in self:
            self.deleteNote(pos)

    def addNote(self, position, head):
        if not(0 <= position.noteTime < len(self)):
            raise BadTimeError(position)
        if head != self._notes[position.noteTime][position.drumIndex]:
            self._notes[position.noteTime][position.drumIndex] = head
            self._runCallBack(position)

    def deleteNote(self, position):
        if not(0 <= position.noteTime < len(self)):
            raise BadTimeError(position)
        if (position.noteTime in self._notes
            and position.drumIndex in self._notes[position.noteTime]):
            del self._notes[position.noteTime][position.drumIndex]
            if len(self._notes[position.noteTime]) == 0:
                del self._notes[position.noteTime]
            self._runCallBack(position)

    def toggleNote(self, position, head):
        if not(0 <= position.noteTime < len(self)):
            raise BadTimeError(position)
        if (position.noteTime in self._notes
            and position.drumIndex in self._notes[position.noteTime]
            and self.getNote(position) == head):
            self.deleteNote(position)
        else:
            self.addNote(position, head)

    def _setWidth(self, newWidth):
        assert(newWidth > 0)
        if newWidth == len(self):
            return
        self._width = newWidth
        badTimes = [noteTime for noteTime in self._notes
                    if noteTime >= self._width]
        for badTime in badTimes:
            del self._notes[badTime]
        self._runCallBack(NotePosition())

    def setBeatCount(self, counter):
        if counter == self.counter:
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
                for drumIndex, head in oldNotes[oldIndex].iteritems():
                    self._notes[newIndex][drumIndex] = head
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
        self._setWidth(len(other))
        self.counter = other.counter
        for pos, head in other:
            try:
                self.addNote(pos, head)
            except BadTimeError:
                continue
        if copyMeasureDecorations:
            self.setRepeatStart(other.isRepeatStart())
            self.setRepeatEnd(other.isRepeatEnd())
            self.setSectionEnd(other.isSectionEnd())
            self.setLineBreak(other.isLineBreak())
            self.repeatCount = other.repeatCount
            self.alternateText = other.alternateText
        return oldMeasure


    def changeKit(self, newKit, changes):
        transposed = _makeNoteDict()
        for noteTime, line in self._notes.iteritems():
            for drumIndex, head in line.iteritems():
                transposed[drumIndex][noteTime] = head
        self._notes = _makeNoteDict()
        for newDrumIndex, newDrum in enumerate(newKit):
            oldDrumIndex = changes[newDrumIndex]
            if oldDrumIndex == -1:
                continue
            for noteTime, head in transposed[oldDrumIndex].iteritems():
                if not newDrum.isAllowedHead(head):
                    head = newDrum.head
                self._notes[noteTime][newDrumIndex] = head

    def lineIsVisible(self, index):
        return (len(self._notes) > 0 and
                any(index in drumData for drumData in self._notes.itervalues()))

    def write(self, handle, indenter):
        print >> handle, indenter("START_BAR %d" % len(self))
        indenter.increase()
        if self.counter is not None:
            self.counter.write(handle, indenter)
        startString = [name for name, value in BAR_TYPES.iteritems()
                       if (self.startBar & value) == value]
        print >> handle, indenter("BARLINE %s" % ",".join(startString))
        for pos, head in self:
            print >> handle, indenter("NOTE %d,%d,%s" % (pos.noteTime,
                                                         pos.drumIndex,
                                                         head))
        endString = [name for name, value in BAR_TYPES.iteritems()
                     if (self.endBar & value) == value ]
        print >> handle, indenter("BARLINE %s" % ",".join(endString))
        if self.repeatCount != _DEFAULTREPEATCOUNT:
            print >> handle, indenter("REPEAT_COUNT %d" % self.repeatCount)
        if self.alternateText is not None:
            print >> handle, indenter("ALTERNATE %s" % self.alternateText)
        indenter.decrease()
        print >> handle, indenter("END_BAR")

    def read(self, scoreIterator):
        seenStartLine = False
        seenEndLine = False
        def doNothing(dummy):
            pass
        mapping = {"NO_BAR" : doNothing,
                   "NORMAL_BAR" : doNothing,
                   "REPEAT_START": self.setRepeatStart,
                   "REPEAT_END": self.setRepeatEnd,
                   "SECTION_END": self.setSectionEnd,
                   "LINE_BREAK": self.setLineBreak}
        for lineType, lineData in scoreIterator:
            if  lineType == "BARLINE":
                if not seenStartLine:
                    self.startBar = 0
                    for barType in lineData.split(","):
                        self.startBar |= BAR_TYPES[barType]
                        mapping[barType](True)
                    seenStartLine = True
                elif not seenEndLine:
                    self.endBar = 0
                    for barType in lineData.split(","):
                        self.endBar |= BAR_TYPES[barType]
                        mapping[barType](True)
                    seenEndLine = True
                else:
                    raise IOError("Too many bar lines")
            elif lineType == "NOTE":
                noteTime, drumIndex, head = lineData.split(",")
                pos = NotePosition(noteTime = int(noteTime),
                                   drumIndex = int(drumIndex))
                self.addNote(pos, head)
            elif lineType == "END_BAR":
                break
            elif lineType == "BEATLENGTH":
                # Old-style count information
                self.counter = MeasureCount.counterMaker(int(lineData),
                                                         len(self))
            elif lineType == "COUNT_INFO_START":
                # New-style count information
                self.counter = MeasureCount.MeasureCount()
                self.counter.read(scoreIterator)
            elif lineType == "REPEAT_COUNT":
                self.repeatCount = int(lineData)
            elif lineType == "ALTERNATE":
                self.alternateText = lineData
            else:
                raise IOError("Unrecognised line type")
