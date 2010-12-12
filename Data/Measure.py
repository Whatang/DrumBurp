'''
Created on 6 Oct 2010

@author: Mike Thomas

'''
from Constants import MEASURE_SPLIT, EMPTY_NOTE

class BadNoteTimeError(StandardError):
    'Bad time for this note'

class Measure(object):
    '''
    classdocs
    '''


    def __init__(self, score, startTime):
        '''
        Constructor
        '''
        self._startTime = startTime
        self._lastTime = startTime
        self.score = score
        self._notes = {}

    def __cmp__(self, other):
        return cmp(self.startTime, other.startTime)

    def _getStartTime(self):
        return self._startTime
    startTime = property(fget = _getStartTime)

    def _getLastTime(self):
        return self._lastTime
    lastTime = property(fget = _getLastTime)

    def _getWidth(self):
        return self.lastTime - self.startTime
    width = property(fget = _getWidth)

    def recordNote(self, note):
        if note.time < self.startTime:
            raise BadNoteTimeError(note.time, self.startTime)
        if note.time > self.lastTime:
            self._lastTime = note.time
        self._notes[(note.time, note.lineIndex)] = note.head

    def addNewNote(self, time, lineIndex, head):
        if not (self.startTime <= time < self.lastTime):
            raise BadNoteTimeError()
        head = self.score.addNote(time, lineIndex, head)
        self._notes[(time, lineIndex)] = head

    def delNote(self, time, lineIndex):
        self._notes.pop((time, lineIndex), None)
        self.score.delNote(time, lineIndex)

    def toggleNote(self, time, lineIndex, head):
        if head is None:
            head = self.score.lineHead(lineIndex)
        if (time, lineIndex) in self._notes and self._notes[(time, lineIndex)] == head:
            self.delNote(time, lineIndex)
        else:
            self.addNewNote(time, lineIndex, head)

    def getNoteHead(self, time, lineIndex):
        if time == self.lastTime:
            return MEASURE_SPLIT
        return self._notes.get((time, lineIndex), EMPTY_NOTE)
