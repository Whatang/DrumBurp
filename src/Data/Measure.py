'''
Created on 12 Dec 2010

@author: Mike Thomas

'''

from collections import defaultdict
from DBConstants import EMPTY_NOTE, BAR_TYPES
from DBErrors import BadTimeError
from NotePosition import NotePosition
import TimeCounter

class Measure(object):
    '''
    classdocs
    '''

    def __init__(self, width = 0):
        self._width = width
        self._notes = defaultdict(lambda: defaultdict(dict))
        self.startBar = BAR_TYPES["NORMAL_BAR"]
        self.endBar = BAR_TYPES["NORMAL_BAR"]
        self._callBack = None
        self._isRepeatEnd = False
        self._isRepeatStart = False
        self._isSectionEnd = False
        self.counter = None

    def __len__(self):
        return self._width

    def __iter__(self):
        noteTimes = self._notes.keys()
        noteTimes.sort()
        for noteTime in noteTimes:
            drumIndexes = self._notes[noteTime].keys()
            for drumIndex in drumIndexes:
                yield (NotePosition(noteTime = noteTime,
                                    drumIndex = drumIndex),
                       self._notes[noteTime][drumIndex])

    def _runCallBack(self, position):
        if self._callBack is not None:
            self._callBack(position)

    def setCallBack(self, callBack):
        self._callBack = callBack

    def clearCallBack(self):
        self._callBack = None

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
        else:
            self.endBar &= ~BAR_TYPES["REPEAT_END"]

    def isSectionEnd(self):
        return ((self.endBar & BAR_TYPES["SECTION_END"])
                == BAR_TYPES["SECTION_END"])

    def isRepeatStart(self):
        return ((self.startBar & BAR_TYPES["REPEAT_START"])
                == BAR_TYPES["REPEAT_START"])

    def isRepeatEnd(self):
        return ((self.endBar & BAR_TYPES["REPEAT_END"])
                == BAR_TYPES["REPEAT_END"])

    def getNote(self, position):
        if not(0 <= position.noteTime < len(self)):
            raise BadTimeError(position)
        if (position.noteTime in self._notes and
            position.drumIndex in self._notes[position.noteTime]):
            return self._notes[position.noteTime][position.drumIndex]
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

    def setWidth(self, newWidth):
        assert(newWidth > 0)
        if newWidth == len(self):
            return
        self._width = newWidth
        badTimes = [noteTime for noteTime in self._notes
                    if noteTime >= self._width]
        for badTime in badTimes:
            del self._notes[badTime]

    def setBeatCount(self, beats, counter):
        self._width = beats * counter.beatLength
        self.counter = counter

    def copyMeasure(self):
        notes = list(self)
        return notes

    def count(self):
        if self.counter is None:
            return [" "] * len(self)
        else:
            return list(self.counter.countTicks(len(self)))

    def pasteMeasure(self, position, notes):
        self.clear()
        for pos, head in notes:
            try:
                pos.staffIndex = position.staffIndex
                pos.measureIndex = position.measureIndex
                self.addNote(pos, head)
            except BadTimeError:
                continue

    def write(self, handle):
        print >> handle, "START_BAR %d" % len(self)
        if self.counter is not None:
            print >> handle, "BEATLENGTH %d" % self.counter.beatLength
        startString = [name for name, value in BAR_TYPES.iteritems()
                       if (self.startBar & value) == value]
        print >> handle, "BARLINE %s" % ",".join(startString)
        for pos, head in self:
            print >> handle, "NOTE %d,%d,%s" % (pos.noteTime,
                                                pos.drumIndex,
                                                head)
        endString = [name for name, value in BAR_TYPES.iteritems()
                     if (self.endBar & value) == value ]
        print >> handle, "BARLINE %s" % ",".join(endString)
        print >> handle, "END_BAR"

    def read(self, scoreIterator):
        seenStartLine = False
        seenEndLine = False
        for lineType, lineData in scoreIterator:
            if  lineType == "BARLINE":
                if not seenStartLine:
                    self.startBar = 0
                    for barType in lineData.split(","):
                        self.startBar |= BAR_TYPES[barType]
                    seenStartLine = True
                elif not seenEndLine:
                    self.endBar = 0
                    for barType in lineData.split(","):
                        self.endBar |= BAR_TYPES[barType]
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
                lineData = int(lineData)
                self.counter = TimeCounter.counterMaker(lineData)
            else:
                raise IOError("Unrecognised line type")
