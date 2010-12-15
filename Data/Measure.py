'''
Created on 12 Dec 2010

@author: Mike Thomas

'''

from collections import defaultdict
from DBConstants import EMPTY_NOTE, BAR_TYPES
from DBErrors import BadTimeError

class Measure(object):
    '''
    classdocs
    '''

    def __init__(self, width = 0):
        self._width = width
        self._notes = defaultdict(lambda: defaultdict(dict))
        self.startBar = BAR_TYPES["NORMAL_BAR"]
        self.endBar = BAR_TYPES["NORMAL_BAR"]
        self._isSectionEnd = False
        self._callBack = None

    def __len__(self):
        return self._width

    def _runCallBack(self, position):
        if self._callBack is not None:
            self._callBack(position)

    def setCallBack(self, callBack):
        self._callBack = callBack

    def clearCallBack(self):
        self._callBack = None

    def setSectionEnd(self, boolean):
        self._isSectionEnd = boolean
        if boolean and self.endBar == BAR_TYPES["NORMAL_BAR"]:
            self.endBar = BAR_TYPES["SECTION_END"]
        if not boolean and self.endBar == BAR_TYPES["SECTION_END"]:
            self.endBar = BAR_TYPES["NORMAL_BAR"]

    def setRepeatStart(self, boolean):
        if boolean:
            self.startBar = BAR_TYPES["REPEAT_START"]
        else:
            self.startBar = BAR_TYPES["NORMAL_BAR"]

    def setRepeatEnd(self, boolean):
        if boolean:
            self.endBar = BAR_TYPES["REPEAT_END"]
        else:
            if self.isSectionEnd():
                self.endBar = BAR_TYPES["SECTION_END"]
            else:
                self.endBar = BAR_TYPES["NORMAL_BAR"]

    def isSectionEnd(self):
        return self._isSectionEnd

    def numNotes(self):
        return sum(len(timeDict) for timeDict in self._notes.values())

    def getNote(self, position):
        if not(0 <= position.noteTime < len(self)):
            raise BadTimeError(position)
        if (position.noteTime in self._notes and
            position.drumIndex in self._notes[position.noteTime]):
            return self._notes[position.noteTime][position.drumIndex]
        return EMPTY_NOTE

    def addNote(self, position, head):
        if not(0 <= position.noteTime < len(self)):
            raise BadTimeError(position)
        if head != self._notes[position.noteTime][position.drumIndex]:
            self._notes[position.noteTime][position.drumIndex] = head
            self._runCallBack(position)

    def deleteNote(self, position):
        if not(0 <= position.noteTime < len(self)):
            raise BadTimeError(position)
        if position.noteTime in self._notes and position.drumIndex in self._notes[position.noteTime]:
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
