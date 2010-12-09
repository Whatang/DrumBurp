'''
Created on 5 Dec 2010

@author: Mike Thomas
'''

from Score import Score
from ScoreSystem import ScoreSystem
from Measure import Measure
from Constants import MEASURE_SPLIT

class FormattedScore(Score):
    def __init__(self, songLength = 0):
        super(FormattedScore, self).__init__(songLength)
        self._desiredWidth = 80
        self._actualWidth = 80
        self._systems = []
        self._measures = []
        self.calculateMeasures()
        self._calculateSystems()

    def _setWidth(self, value):
        if value != self._desiredWidth:
            self._desiredWidth = value
            self._calculateSystems()
    def _getWidth(self):
        return self._desiredWidth
    width = property(fget = _getWidth, fset = _setWidth)

    def iterSystems(self):
        return iter(self._systems)

    @property
    def numSystems(self):
        return len(self._systems)

    def setMeasureLine(self, measureTime):
        Score.setMeasureLine(self, measureTime)
        self.calculateMeasures()


    def calculateMeasures(self):
        self._measures = []
        thisMeasure = Measure(score = self, startTime = 0)
        for note in self.iterNotes():
            thisMeasure.recordNote(note)
            if note.head == MEASURE_SPLIT:
                self._measures.append(thisMeasure)
                thisMeasure = Measure(score = self,
                                      startTime = thisMeasure.lastTime + 1)
        self._calculateSystems()

    def _calculateSystems(self):
        self._systems = []
        startTime = 0
        thisSystem = ScoreSystem(self, startTime)
        self._actualWidth = self.width
        for measure in self._measures:
            endTime = measure.lastTime
            if endTime - startTime < self.width:
                thisSystem.addMeasure(measure)
            else:
                if thisSystem.lastTime != thisSystem.startTime:
                    # i.e. there is at least one measure on this line
                    # already, so end the line and start a new one
                    self._systems.append(thisSystem)
                    startTime = thisSystem.lastTime + 1
                    thisSystem = ScoreSystem(self, startTime)
                    thisSystem.addMeasure(measure)
                else:
                    # Just stick the measure on this line, and make the width 
                    # of the table bigger to accommodate it if necessary
                    thisSystem.addMeasure(measure)
                    startTime = thisSystem.lastTime + 1
                    thisSystem = ScoreSystem(self, startTime)
                    self._actualWidth = max(self._actualWidth, measure.width)
        if thisSystem.lastTime != thisSystem.startTime:
            self._systems.append(thisSystem)
