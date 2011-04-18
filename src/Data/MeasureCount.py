'''
Created on 18 Jan 2011

@author: Mike Thomas

'''

from DBConstants import BEAT_COUNT
from Beat import Beat
from Counter import CounterRegistry

class MeasureCount(object):
    def __init__(self):
        self.beats = []

    def count(self):
        for beatNum, beat in enumerate(self.beats):
            for count in beat.count(beatNum + 1):
                yield count

    def isSimpleCount(self):
        firstBeat = "".join(self.beats[0])
        return all("".join(beat) == firstBeat for beat in self.beats)

    def __len__(self):
        return sum(beat.numTicks for beat in self.beats)

    def __getitem__(self, index):
        return self.beats[index]

    def countString(self):
        return "".join(self.count())

    def addSimpleBeats(self, counter, numBeats):
        beat = Beat(counter)
        self.addBeats(beat, numBeats)

    def addBeats(self, beat, numBeats):
        self.beats.extend([beat] * numBeats)

    def numBeats(self):
        return len(self.beats)

    def write(self, handle, indenter):
        print >> handle, indenter("COUNT_INFO_START")
        indenter.increase()
        if self.isSimpleCount():
            # All beats are the same
            print >> handle, indenter("REPEAT_BEATS %d" % len(self.beats))
            self.beats[0].write(handle, indenter)
        else:
            for beat in self.beats:
                beat.write(handle, indenter)
        indenter.decrease()
        print >> handle, indenter("COUNT_INFO_END")

    def read(self, scoreIterator):
        repeat = False
        for lineType, lineData in scoreIterator:
            if lineType == "COUNT_INFO_END":
                break
            elif lineType == "REPEAT_BEATS":
                repeat = int(lineData)
            elif lineType == "BEAT_START":
                beat = Beat.read(scoreIterator)
                if repeat:
                    self.beats.extend([beat] * repeat)
                else:
                    self.beats.append(beat)
            else:
                raise IOError("Unrecognised line type")

def counterMaker(beatLength, numTicks = None):
    # Create a MeasureCount from an 'old style' specification, where
    # all we are given is the number of ticks in a beat.
    if numTicks is None:
        numTicks = beatLength
    defaultRegistry = CounterRegistry()
    counts = [count[1] for count in
              defaultRegistry.countsByTicks(beatLength)]
    count = counts[0]
    mc = MeasureCount()
    mc.addSimpleBeats(count, numTicks / beatLength)
    return mc

def makeSimpleCount(counter, numBeats):
    mc = MeasureCount()
    mc.addSimpleBeats(counter, numBeats)
    return mc
