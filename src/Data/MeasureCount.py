'''
Created on 18 Jan 2011

@author: Mike Thomas

'''

import itertools

_COUNTERS = {}

class MeasureCount(object):
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
        for dummyIndex, count in zip(range(0, numTicks), self.count()):
            yield count

_QUARTERS = MeasureCount(".", "Quarter Notes")
_EIGHTHS = MeasureCount(".+", "Eighth Notes")
_SIXTEENTHS = MeasureCount(".e+a", "Sixteenth Notes")
_TRIPLETS = MeasureCount(".+a", "Triplets")
_SIXTEEN_TRIPLETS = MeasureCount(".ea+ea", "Sixteenth Triplets")

def counterMaker(ticksPerBeat):
    return _COUNTERS[ticksPerBeat]

def getCounters():
    beatLengths = _COUNTERS.keys()
    beatLengths.sort()
    return [(bl, _COUNTERS[bl]) for bl in beatLengths]
