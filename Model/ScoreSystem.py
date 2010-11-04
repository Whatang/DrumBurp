'''
Created on 31 Jul 2010

@author: Mike Thomas

'''
import Data
import bisect
from bisect import bisect_left

class BadMeasureError(StandardError):
    'Could not add this measure to the ScoreSystem'

class BadTimeError(StandardError):
    'The given time does not correspond to any measure in this ScoreSystem'

class ScoreSystem(object):
    '''
    classdocs
    '''


    def __init__(self, score, startTime):
        '''
        Constructor
        '''
        self.score = score
        self._startTime = startTime
        self._lastTime = startTime - 1
        self._timeToMeasure = {}
        self._measures = []
        self._measureLinesOrdered = []
        self._measureLines = set()

    def _getStartTime(self):
        return self._startTime
    startTime = property(fget = _getStartTime)

    def _getLastTime(self):
        return self._lastTime
    lastTime = property(fget = _getLastTime)

    def addMeasure(self, measure):
        if measure.startTime <= self.lastTime:
            print measure.startTime, self.lastTime
            raise BadMeasureError()
        self._measures.append(measure)
        self._measureLinesOrdered.append(measure.lastTime)
        self._measureLines.add(measure.lastTime)
        self._lastTime = measure.lastTime
        mIndex = len(self._measures) - 1
        for t in xrange(measure.startTime, measure.lastTime + 1):
            self._timeToMeasure[t] = (measure, mIndex)

    def _findMeasureAtTime(self, time):
        if time not in self._timeToMeasure:
            raise BadTimeError()
        return self._timeToMeasure[time][0]

    def addNotes(self, iterable):
        for note in iterable:
            self.addNote(note.time, note.lineIndex, note.head)

    def addNote(self, time, lineIndex, head):
        # Quick check to make sure we're not trying to add a note on a measure
        # line
        if time in self._measureLines:
            return
        # Find the measure at this time
        try:
            measure = self._findMeasureAtTime(time)
        except BadTimeError:
            # Not here, just return quietly
            return
        measure.addNewNote(time, lineIndex, head)

    def delNote(self, time, lineIndex):
        # Quick check to make sure we're not trying to delete a note on a measure
        # line
        if time in self._measureLines:
            return
        # Find the measure at this time
        try:
            measure = self._findMeasureAtTime(time)
        except BadTimeError:
            # Not here, just return quietly
            return
        measure.delNote(time, lineIndex)

    def toggleNote(self, time, lineIndex, head):
        # Quick check to make sure we're not trying to toggle a note on a
        # measure line
        if time in self._measureLines:
            return
        # Find the measure at this time
        try:
            measure = self._findMeasureAtTime(time)
        except BadTimeError:
            # Not here, just return quietly
            return
        measure.toggleNote(time, lineIndex, head)

    def getNoteHead(self, time, lineIndex):
        if time in self._measureLines:
            return Data.MEASURE_SPLIT
        else:
            # Find the measure at this time
            try:
                measure = self._findMeasureAtTime(time)
            except BadTimeError:
                # Not here, just return quietly
                return ""
            return measure.getNoteHead(time, lineIndex)
