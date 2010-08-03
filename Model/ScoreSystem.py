'''
Created on 31 Jul 2010

@author: Mike Thomas

'''
import Data

class ScoreSystem(object):
    '''
    classdocs
    '''


    def __init__(self, startTime = 0):
        '''
        Constructor
        '''
        self.startTime = startTime
        self.lastTime = self.startTime
        self._notes = {}
        self._measureLines = set()

    def addNotes(self, iterable):
        for note in iterable:
            if note.time > self.lastTime:
                self.lastTime = note.time
            if note.head == Data.MEASURE_SPLIT:
                self._measureLines.add(note.time)
            else:
                self._notes[(note.time, note.lineIndex)] = note.head

    def delNote(self, time, lineIndex):
        if ((not (self.startTime <= time <= self.lastTime))
             or
             (time in self._measureLines)):
            return
        self._notes.pop((time, lineIndex), None)

    def getNoteHead(self, time, lineIndex):
        if not (self.startTime <= time <= self.lastTime):
            return ""
        if time in self._measureLines:
            return Data.MEASURE_SPLIT
        else:
            return self._notes.get((time, lineIndex), Data.EMPTY_NOTE)
