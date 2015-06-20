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
Created on 12 Dec 2012

@author: Mike Thomas
'''
import unittest

# pylint: disable-msg=R0904

from Data import MeasureCount, Counter, Beat


class TestSimple(unittest.TestCase):
    my_counter = Counter.Counter("e+a")
    count = MeasureCount.makeSimpleCount(my_counter, 4)

    def testLength(self):
        self.assertEqual(len(self.count), 16)

    def testNumBeats(self):
        self.assertEqual(self.count.numBeats(), 4)

    def testIsSimple(self):
        self.assert_(self.count.isSimpleCount())

    def testCount(self):
        self.assertEqual(list(self.count.count()),
                         ["1", "e", "+", "a",
                          "2", "e", "+", "a",
                          "3", "e", "+", "a",
                          "4", "e", "+", "a"])

    def testCountString(self):
        self.assertEqual(self.count.countString(),
                         "1e+a2e+a3e+a4e+a")

    def testGetItem(self):
        beat = self.count[1]
        self.assert_(isinstance(beat, Beat.Beat))
        self.assertEqual(beat.numTicks, 4)
        self.assertEqual(beat.ticksPerBeat, 4)
        self.assertRaises(IndexError, self.count.__getitem__, 4)

    def testIterTimesMs(self):
        times = list(self.count.iterTimesMs(100))
        self.assertEqual(times, [0, 25, 50, 75,
                                 100, 125, 150, 175,
                                 200, 225, 250, 275,
                                 300, 325, 350, 375, 400])

    def testTimeSig(self):
        self.assertEqual(self.count.timeSig(), (4, 4))

    def testIterBeatTicks(self):
        ticks = list(self.count.iterBeatTicks())
        beat = self.count[0]
        self.assertEqual(ticks,
                         [(0, beat, 0), (0, beat, 1),
                          (0, beat, 2), (0, beat, 3),
                          (1, beat, 0), (1, beat, 1),
                          (1, beat, 2), (1, beat, 3),
                          (2, beat, 0), (2, beat, 1),
                          (2, beat, 2), (2, beat, 3),
                          (3, beat, 0), (3, beat, 1),
                          (3, beat, 2), (3, beat, 3)])

    def testIterBeatTickPositions(self):
        ticks = list(self.count.iterBeatTickPositions())
        self.assertEqual(ticks, [0, 4, 8, 12])

    def testIterMidiTicks(self):
        ticks = list(self.count.iterMidiTicks())
        self.assertEqual(ticks, [0, 48, 96, 144,
                                 192, 240, 288, 336,
                                 384, 432, 480, 528,
                                 576, 624, 672, 720, 768])

    def testIterTime(self):
        ticks = list(self.count.iterTime())
        self.assertEqual(ticks,
                         [(0, 0, 4), (0, 1, 4), (0, 2, 4), (0, 3, 4),
                          (1, 0, 4), (1, 1, 4), (1, 2, 4), (1, 3, 4),
                          (2, 0, 4), (2, 1, 4), (2, 2, 4), (2, 3, 4),
                          (3, 0, 4), (3, 1, 4), (3, 2, 4), (3, 3, 4)])

class TestComplex(unittest.TestCase):
    counter1 = Counter.Counter("e+a")
    counter2 = Counter.Counter("+a")
    counter3 = Counter.Counter("+")
    counter4 = Counter.Counter("e+a")
    count = MeasureCount.MeasureCount()
    count.addBeats(Beat.Beat(counter1), 1)
    count.addBeats(Beat.Beat(counter2), 1)
    count.addBeats(Beat.Beat(counter3), 1)
    count.addBeats(Beat.Beat(counter4, 2), 1)

    def testLength(self):
        self.assertEqual(len(self.count), 11)

    def testNumBeats(self):
        self.assertEqual(self.count.numBeats(), 4)

    def testIsSimple(self):
        self.assertFalse(self.count.isSimpleCount())

    def testCount(self):
        self.assertEqual(list(self.count.count()),
                         ["1", "e", "+", "a",
                          "2", "+", "a",
                          "3", "+",
                          "4", "e", ])

    def testCountString(self):
        self.assertEqual(self.count.countString(),
                         "1e+a2+a3+4e")

    def testGetItem(self):
        beat = self.count[1]
        self.assert_(isinstance(beat, Beat.Beat))
        self.assertEqual(beat.numTicks, 3)
        self.assertEqual(beat.ticksPerBeat, 3)
        self.assertRaises(IndexError, self.count.__getitem__, 4)

    def testIterTimesMs(self):
        times = list(self.count.iterTimesMs(120))
        self.assertEqual(times, [0, 30, 60, 90,
                                 120, 160, 200,
                                 240, 300,
                                 360, 390, 420])

    def testTimeSig(self):
        self.assertEqual(self.count.timeSig(), (7, 8))

    def testIterBeatTicks(self):
        ticks = list(self.count.iterBeatTicks())
        beat1 = self.count[0]
        beat2 = self.count[1]
        beat3 = self.count[2]
        beat4 = self.count[3]
        self.assertEqual(ticks,
                         [(0, beat1, 0), (0, beat1, 1),
                          (0, beat1, 2), (0, beat1, 3),
                          (1, beat2, 0), (1, beat2, 1),
                          (1, beat2, 2),
                          (2, beat3, 0), (2, beat3, 1),
                          (3, beat4, 0), (3, beat4, 1)])

    def testIterBeatTickPositions(self):
        ticks = list(self.count.iterBeatTickPositions())
        self.assertEqual(ticks, [0, 4, 7, 9])

    def testIterMidiTicks(self):
        ticks = list(self.count.iterMidiTicks())
        self.assertEqual(ticks, [0, 48, 96, 144,
                                 192, 256, 320,
                                 384, 480,
                                 576, 624, 672])

    def testIterTime(self):
        ticks = list(self.count.iterTime())
        self.assertEqual(ticks,
                         [(0, 0, 4), (0, 1, 4), (0, 2, 4), (0, 3, 4),
                          (1, 0, 3), (1, 1, 3), (1, 2, 3),
                          (2, 0, 2), (2, 1, 2),
                          (3, 0, 4), (3, 1, 4)])

class TestCounterMaker(unittest.TestCase):
    def testMake(self):
        count = MeasureCount.counterMaker(4, 16)
        self.assert_(isinstance(count, MeasureCount.MeasureCount))
        self.assert_(count.isSimpleCount())
        self.assertEqual(len(count), 16)

class TestTimeSigs(unittest.TestCase):
    sixteenths = Counter.Counter("e+a")
    triplets = Counter.Counter("+a")
    eighths = Counter.Counter("+")

    def testTwoFour(self):
        count = MeasureCount.makeSimpleCount(self.eighths, 2)
        self.assertEqual(count.timeSig(), (2, 4))
        count = MeasureCount.makeSimpleCount(self.triplets, 2)
        self.assertEqual(count.timeSig(), (2, 4))
        count = MeasureCount.makeSimpleCount(self.sixteenths, 2)
        self.assertEqual(count.timeSig(), (2, 4))

    def testThreeFour(self):
        count = MeasureCount.makeSimpleCount(self.eighths, 3)
        self.assertEqual(count.timeSig(), (3, 4))
        count = MeasureCount.makeSimpleCount(self.triplets, 3)
        self.assertEqual(count.timeSig(), (3, 4))
        count = MeasureCount.makeSimpleCount(self.sixteenths, 3)
        self.assertEqual(count.timeSig(), (3, 4))

    def testFourFour(self):
        count = MeasureCount.makeSimpleCount(self.eighths, 4)
        self.assertEqual(count.timeSig(), (4, 4))
        count = MeasureCount.makeSimpleCount(self.triplets, 4)
        self.assertEqual(count.timeSig(), (4, 4))
        count = MeasureCount.makeSimpleCount(self.sixteenths, 4)
        self.assertEqual(count.timeSig(), (4, 4))

    def testFiveFour(self):
        count = MeasureCount.makeSimpleCount(self.eighths, 5)
        self.assertEqual(count.timeSig(), (5, 4))
        count = MeasureCount.makeSimpleCount(self.triplets, 5)
        self.assertEqual(count.timeSig(), (5, 4))
        count = MeasureCount.makeSimpleCount(self.sixteenths, 5)
        self.assertEqual(count.timeSig(), (5, 4))

    def testSixFour(self):
        count = MeasureCount.makeSimpleCount(self.eighths, 6)
        self.assertEqual(count.timeSig(), (6, 4))
        count = MeasureCount.makeSimpleCount(self.triplets, 6)
        self.assertEqual(count.timeSig(), (6, 4))
        count = MeasureCount.makeSimpleCount(self.sixteenths, 6)
        self.assertEqual(count.timeSig(), (6, 4))

    def testSevenFour(self):
        count = MeasureCount.makeSimpleCount(self.eighths, 7)
        self.assertEqual(count.timeSig(), (7, 4))
        count = MeasureCount.makeSimpleCount(self.triplets, 7)
        self.assertEqual(count.timeSig(), (7, 4))
        count = MeasureCount.makeSimpleCount(self.sixteenths, 7)
        self.assertEqual(count.timeSig(), (7, 4))

    def testThreeEight(self):
        count = MeasureCount.makeSimpleCount(self.eighths, 1)
        count.addBeats(Beat.Beat(self.eighths, 1), 1)
        self.assertEqual(count.timeSig(), (3, 8))
        count = MeasureCount.makeSimpleCount(self.sixteenths, 1)
        count.addBeats(Beat.Beat(self.sixteenths, 2), 1)
        self.assertEqual(count.timeSig(), (3, 8))

    def testFiveEight(self):
        count = MeasureCount.makeSimpleCount(self.eighths, 2)
        count.addBeats(Beat.Beat(self.eighths, 1), 1)
        self.assertEqual(count.timeSig(), (5, 8))
        count = MeasureCount.makeSimpleCount(self.sixteenths, 2)
        count.addBeats(Beat.Beat(self.sixteenths, 2), 1)
        self.assertEqual(count.timeSig(), (5, 8))

    def testSevenEight(self):
        count = MeasureCount.makeSimpleCount(self.eighths, 3)
        count.addBeats(Beat.Beat(self.eighths, 1), 1)
        self.assertEqual(count.timeSig(), (7, 8))
        count = MeasureCount.makeSimpleCount(self.sixteenths, 3)
        count.addBeats(Beat.Beat(self.sixteenths, 2), 1)
        self.assertEqual(count.timeSig(), (7, 8))

    def testNineEight(self):
        count = MeasureCount.makeSimpleCount(self.eighths, 4)
        count.addBeats(Beat.Beat(self.eighths, 1), 1)
        self.assertEqual(count.timeSig(), (9, 8))
        count = MeasureCount.makeSimpleCount(self.sixteenths, 4)
        count.addBeats(Beat.Beat(self.sixteenths, 2), 1)
        self.assertEqual(count.timeSig(), (9, 8))

    def testThirteenSixteen(self):
        count = MeasureCount.makeSimpleCount(self.sixteenths, 3)
        count.addBeats(Beat.Beat(self.sixteenths, 1), 1)
        self.assertEqual(count.timeSig(), (13, 16))

    def testFifteenSixteen(self):
        count = MeasureCount.makeSimpleCount(self.sixteenths, 3)
        count.addBeats(Beat.Beat(self.sixteenths, 3), 1)
        self.assertEqual(count.timeSig(), (15, 16))

    def testSeventeenSixteen(self):
        count = MeasureCount.makeSimpleCount(self.sixteenths, 4)
        count.addBeats(Beat.Beat(self.sixteenths, 1), 1)
        self.assertEqual(count.timeSig(), (17, 16))


if __name__ == "__main__":
    unittest.main()
