# Copyright 2011-12 Michael Thomas
#
# See www.whatang.org for more information.
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DrumBurp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DrumBurp.  If not, see <http://www.gnu.org/licenses/>
'''
Created on 18 Jan 2011

@author: Mike Thomas

'''

from Beat import Beat
from Counter import CounterRegistry

MIDITICKSPERBEAT = 48

class MeasureCount(object):
    def __init__(self):
        self.beats = []

    def iterTimesMs(self, msPerBeat):
        total = 0
        for beat in self.beats:
            beatTicks = beat.ticksPerBeat
            startTotal = total
            for unusedCount in beat.iterTicks():
                yield total
                total += msPerBeat / beatTicks
            total = startTotal + (beat.numTicks * msPerBeat) / beatTicks
        yield total

    def floatBeats(self):
        lastBeat = self.beats[-1]
        beatTicks = lastBeat.ticksPerBeat
        return ((len(self.beats) - 1) +
                float(lastBeat.numTicks) / beatTicks)

    def timeSig(self):
        lastBeat = self.beats[-1]
        beatTicks = lastBeat.ticksPerBeat
        if beatTicks == lastBeat.numTicks:
            return len(self.beats), 4
        else:
            for i in (6, 4, 3, 2, 1):
                if (beatTicks % i) == 0 and (lastBeat.numTicks % i) == 0:
                    denomPerBeat = (lastBeat.numTicks / i)
                    denom = 4 * denomPerBeat
                    num = (len(self.beats) - 1) * denomPerBeat
                    num += beatTicks / i
                    return num, denom

    def iterBeatTicks(self):
        for (beatNum, beat) in enumerate(self.beats):
            for tick in beat.iterTicks():
                yield(beatNum, beat, tick)

    def iterBeatTimes(self):
        tick = 0
        for beat in self.beats:
            yield tick
            tick += beat.numTicks

    def iterMidiTicks(self):
        total = 0
        for beat in self.beats:
            midiTicks = MIDITICKSPERBEAT / beat.ticksPerBeat
            for unused in beat.iterTicks():
                yield total
                total += midiTicks
        yield total

    def count(self):
        for beatNum, beat in enumerate(self.beats):
            for count in beat.count(beatNum + 1):
                yield count

    def iterTime(self):
        for beatNum, beat in enumerate(self.beats):
            for timeIndex, unusedCount in enumerate(beat.count(beatNum + 1)):
                yield (beatNum, timeIndex, beat.ticksPerBeat)

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

    def write(self, handle, indenter, title = "COUNT_INFO_START"):
        print >> handle, indenter(title)
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
