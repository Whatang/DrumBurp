'''
Created on 18 Jan 2011

@author: Mike Thomas

'''

import itertools

_COUNTERS = {}

class TimeCounter(object):
    '''
    classdocs
    '''


    def __init__(self, counts = None, name = None):
        '''
        Constructor
        '''
        self.name = name
        if counts is None:
            counts = ["."]
        self._ticksPerBeat = 1
        self._counts = list(counts)
        self.beatLength = len(self._counts)
        _COUNTERS[self.beatLength] = self

    def description(self):
        return "%s: %s" % (self.name, "".join(self.countTicks(4)))

    def count(self):
        for beat in itertools.count(1):
            yield str(beat)
            for count in self._counts[1:]:
                yield count

    def countBeats(self, numBeats):
        for beat in range(1, numBeats + 1):
            yield str(beat)
            for count in self._counts[1:]:
                yield count

    def countTicks(self, numTicks):
        beat = 1
        count = 0
        ticks = 0
        while ticks < numTicks:
            if count == 0:
                yield str(beat)
            else:
                yield self._counts[count]
            ticks += 1
            count += 1
            if count == self.beatLength:
                count = 0
                beat += 1

_QUARTERS = TimeCounter(".", "Quarter Notes")
_EIGHTHS = TimeCounter(".+", "Eighth Notes")
_SIXTEENTHS = TimeCounter(".e+a", "Sixteenth Notes")
_TRIPLETS = TimeCounter(".+a", "Triplets")
_SIXTEEN_TRIPLETS = TimeCounter(".ea+ea", "Sixteenth Triplets")

def counterMaker(ticksPerBeat):
    return _COUNTERS[ticksPerBeat]

def getCounters():
    beatLengths = _COUNTERS.keys()
    beatLengths.sort()
    return [(bl, _COUNTERS[bl]) for bl in beatLengths]
