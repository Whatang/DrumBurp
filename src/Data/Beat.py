'''
Created on 16 Apr 2011

@author: Mike Thomas

'''

import itertools
from Counter import Counter
from DBConstants import BEAT_COUNT

class Beat(object):
    '''
    classdocs
    '''


    def __init__(self, counter, numTicks = None):
        '''
        Constructor
        '''
        self.counter = counter
        if numTicks is None:
            numTicks = self.ticksPerBeat
        self._numTicks = numTicks
        self._beatLength = float(self.numTicks) / self.ticksPerBeat

    def __iter__(self):
        for unusedTickNum, count in itertools.izip(self.iterTicks(),
                                                   self.counter):
            yield count

    def __str__(self):
        return str(self.counter)

    def iterTicks(self):
        return iter(range(0, self.numTicks))

    def numBeats(self):
        return self._beatLength

    @property
    def ticksPerBeat(self):
        return len(self.counter)

    @property
    def numTicks(self):
        return self._numTicks

    def write(self, handle, indenter):
        print >> handle, indenter("BEAT_START")
        indenter.increase()
        if self.numTicks != self.ticksPerBeat:
            print >> handle, indenter("NUM_TICKS", self.numTicks)
        self.counter.write(handle, indenter)
        indenter.decrease()
        print >> handle, indenter("BEAT_END")

    @staticmethod
    def read(scoreIterator):
        numTicks = None
        counter = None
        for lineType, lineData in scoreIterator:
            if lineType == "BEAT_END":
                return Beat(counter, numTicks)
            elif lineType == "NUM_TICKS":
                numTicks = int(lineData)
            elif lineType == "COUNT":
                if lineData[0] == "|" and lineData[-1] == "|":
                    lineData = lineData[1:-1]
                lineData = BEAT_COUNT + lineData[1:]
                counter = Counter(lineData)
            else:
                raise IOError("Unrecognised line type")


