'''
Created on 31 Jul 2010

@author: Mike Thomas

'''

from Constants import MEASURE_SPLIT
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
        self._listeners = {}
        super(ScoreSystem, self).__init__()

    @property
    def numLines(self):
        return self.score.numLines

    @property
    def startTime(self):
        return self._startTime

    @property
    def lastTime(self):
        return self._lastTime

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
        self.dataChanged(time, lineIndex)

    def delNote(self, time, lineIndex):
        # Quick check to make sure we're not trying to delete a note on a
        # measure line
        if time in self._measureLines:
            return
        # Find the measure at this time
        try:
            measure = self._findMeasureAtTime(time)
        except BadTimeError:
            # Not here, just return quietly
            return
        measure.delNote(time, lineIndex)
        self.dataChanged(time, lineIndex)

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
        self.dataChanged(time, lineIndex)

    def getNoteHead(self, time, lineIndex):
        if time in self._measureLines:
            return MEASURE_SPLIT
        else:
            # Find the measure at this time
            try:
                measure = self._findMeasureAtTime(time)
            except BadTimeError:
                # Not here, just return quietly
                return ""
            return measure.getNoteHead(time, lineIndex)

    def registerListener(self, name, listener):
        self._listeners[name] = listener

    def removeListener(self, name):
        if name in self._listeners:
            del self._listeners[name]

    def dataChanged(self, time, lineIndex):
        for listener in self._listeners.itervalues():
            listener(time, lineIndex)

    def scoreTime(self, systemTime):
        return self.startTime + systemTime

    def systemTime(self, scoreTime):
        return scoreTime - self.startTime

    def getLine(self, lineIndex):
        return self.score[lineIndex]
