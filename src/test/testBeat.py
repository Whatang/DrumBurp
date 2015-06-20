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
from Data import Beat, Counter


# pylint: disable-msg=R0904

class TestFullBeat(unittest.TestCase):
    beat = Beat.Beat(Counter.Counter("e+a"))

    def testStr(self):
        self.assertEqual(str(self.beat), "^e+a")

    def testTicksPerBeat(self):
        self.assertEqual(self.beat.ticksPerBeat, 4)

    def testNumTicks(self):
        self.assertEqual(self.beat.numTicks, 4)

    def testNumBeats(self):
        self.assertEqual(self.beat.numBeats(), 1.0)

    def testIter(self):
        count = list(self.beat)
        self.assertEqual(count, ["^", "e", "+", "a"])

    def testIterTicks(self):
        ticks = list(self.beat.iterTicks())
        self.assertEqual(ticks, [0, 1, 2, 3])

    def testCount(self):
        count = list(self.beat.count(2))
        self.assertEqual(count, ["2", "e", "+", "a"])

class TestPartialBeat(unittest.TestCase):
    beat = Beat.Beat(Counter.Counter("e+a"), 2)

    def testStr(self):
        self.assertEqual(str(self.beat), "^e+a")

    def testTicksPerBeat(self):
        self.assertEqual(self.beat.ticksPerBeat, 4)

    def testNumTicks(self):
        self.assertEqual(self.beat.numTicks, 2)

    def testNumBeats(self):
        self.assertEqual(self.beat.numBeats(), 0.5)

    def testIter(self):
        count = list(self.beat)
        self.assertEqual(count, ["^", "e"])

    def testIterTicks(self):
        ticks = list(self.beat.iterTicks())
        self.assertEqual(ticks, [0, 1])

    def testCount(self):
        count = list(self.beat.count(2))
        self.assertEqual(count, ["2", "e"])

if __name__ == "__main__":
    unittest.main()
