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

    def _runCallBack(self, noteTime, drumIndex):
        if self._callBack is not None:
            self._callBack(noteTime, drumIndex)

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

    def getNote(self, noteTime, drumIndex):
        if not(0 <= noteTime < len(self)):
            raise BadTimeError(noteTime)
        if noteTime in self._notes and drumIndex in self._notes[noteTime]:
            return self._notes[noteTime][drumIndex]
        return EMPTY_NOTE

    def addNote(self, noteTime, drumIndex, head):
        if not(0 <= noteTime < len(self)):
            raise BadTimeError(noteTime)
        if head != self._notes[noteTime][drumIndex]:
            self._notes[noteTime][drumIndex] = head
            self._runCallBack(noteTime, drumIndex)

    def deleteNote(self, noteTime, drumIndex):
        if not(0 <= noteTime < len(self)):
            raise BadTimeError(noteTime)
        if noteTime in self._notes and drumIndex in self._notes[noteTime]:
            del self._notes[noteTime][drumIndex]
            if len(self._notes[noteTime]) == 0:
                del self._notes[noteTime]
            self._runCallBack(noteTime, drumIndex)


    def toggleNote(self, noteTime, drumIndex, head):
        if not(0 <= noteTime < len(self)):
            raise BadTimeError(noteTime)
        if (noteTime in self._notes
            and drumIndex in self._notes[noteTime]
            and self.getNote(noteTime, drumIndex) == head):
            self.deleteNote(noteTime, drumIndex)
        else:
            self.addNote(noteTime, drumIndex, head)

    def setWidth(self, newWidth):
        assert(newWidth > 0)
        if newWidth == len(self):
            return
        self._width = newWidth
        badTimes = [noteTime for noteTime in self._notes
                    if noteTime >= self._width]
        for badTime in badTimes:
            del self._notes[badTime]
