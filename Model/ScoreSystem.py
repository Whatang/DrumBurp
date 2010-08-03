'''
Created on 31 Jul 2010

@author: Mike Thomas

'''
import Data

class ScoreSystem(object):
    '''
    classdocs
    '''


    def __init__(self, score, startTime):
        '''
        Constructor
        '''
        self.score = score
        self.startTime = startTime
        self.lastTime = self.startTime
        self._notes = {}
        self._measureLines = set()

    def addNotes(self, iterable):
        for note in iterable:
            self.addNote(note.time, note.lineIndex, note.head)

    def addNote(self, time, lineIndex, head):
        if time > self.lastTime:
            self.lastTime = time
        if time < self.startTime:
            return
        if time in self._measureLines:
            return
        if head == Data.MEASURE_SPLIT:
            self._measureLines.add(time)
            self.score.addNote(time, 0, head)
        else:
            head = self.score.addNote(time, lineIndex, head)
            self._notes[(time, lineIndex)] = head

    def delNote(self, time, lineIndex):
        if ((not (self.startTime <= time <= self.lastTime))
             or
             (time in self._measureLines)):
            return
        if time in self._measureLines:
            return
        self._notes.pop((time, lineIndex), None)
        self.score.delNote(time, lineIndex)

    def toggleNote(self, time, lineIndex, head):
        if ((not (self.startTime <= time <= self.lastTime))
             or
             (time in self._measureLines)):
            return
        if (time, lineIndex) in self._notes:
            self.delNote(time, lineIndex)
        elif time in self._measureLines:
            return
        else:
            self.addNote(time, lineIndex, head)

    def getNoteHead(self, time, lineIndex):
        if not (self.startTime <= time <= self.lastTime):
            return ""
        if time in self._measureLines:
            return Data.MEASURE_SPLIT
        else:
            return self._notes.get((time, lineIndex), Data.EMPTY_NOTE)
