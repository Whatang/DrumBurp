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

from Data.Beat import Beat
from Data.Counter import CounterRegistry
from Data import DBConstants

class MeasureCount(object):
    def __init__(self):
        self.beats = []

    def _iterTimeCounter(self, valuePerBeat, swing):
        total = 0
        swing /= 4
        for beat in self.beats:
            beatTicks = beat.ticksPerBeat
            if not swing or beatTicks % 3 == 0 or beatTicks % swing != 0:
                startTotal = total
                perTick = valuePerBeat / beatTicks
                for unusedCount in beat.iterTicks():
                    yield total
                    total += perTick
                total = startTotal + (beat.numTicks * valuePerBeat) / beatTicks
            else:
                ticksPerSwing = beatTicks / swing
                swingCount = 0
                isLong = True
                valuePerLongTick = (valuePerBeat * 2) / (3 * ticksPerSwing)
                valuePerShortTick = valuePerLongTick / 2
                for unusedCount in beat.iterTicks():
                    yield total
                    if isLong:
                        total += valuePerLongTick
                    else:
                        total += valuePerShortTick
                    swingCount += 1
                    if swingCount == ticksPerSwing:
                        swingCount = 0
                        isLong = not isLong
        yield total

    def iterTimesMs(self, msPerBeat, swing):
        for value in self._iterTimeCounter(msPerBeat, swing):
            yield value

    def iterMidiTicks(self, swing):
        for value in self._iterTimeCounter(DBConstants.MIDITICKSPERBEAT, swing):
            yield value

    def timeSig(self):
        lastBeat = self.beats[-1]
        beatTicks = lastBeat.ticksPerBeat
        if beatTicks == lastBeat.numTicks:
            return len(self.beats), 4
        else:
            for i in (12, 8, 6, 4, 3, 2, 1):
                if (beatTicks % i) == 0 and (lastBeat.numTicks % i) == 0:
                    denomPerBeat = beatTicks / i
                    denom = 4 * denomPerBeat
                    num = (len(self.beats) - 1) * denomPerBeat
                    num += lastBeat.numTicks / i
                    return num, denom

    def iterBeatTicks(self):
        for (beatNum, beat) in enumerate(self.beats):
            for tick in beat.iterTicks():
                yield(beatNum, beat, tick)

    def iterBeatTickPositions(self):
        tick = 0
        for beat in self.beats:
            yield tick
            tick += beat.numTicks

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

#     def beatIndexContainingTickIndex(self, tickIndex):
#         totalTicks = 0
#         for beatIndex, beat in enumerate(self.beats):
#             totalTicks += beat.numTicks
#             if totalTicks > tickIndex:
#                 return beatIndex
#         return None

#     def insertBeat(self, beat, index):
#         self.beats.insert(index, beat)

#     def endsWithPartialBeat(self):
#         return self.beats[-1].isPartial()

    def numBeats(self):
        return len(self.beats)

def counterMaker(beatLength, numTicks):
    # Create a MeasureCount from an 'old style' specification, where
    # all we are given is the number of ticks in a beat and the total number
    # of ticks in the bar
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
