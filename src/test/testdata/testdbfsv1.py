# Copyright 2015 Michael Thomas
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
Created on Jun 21, 2015

@author: Mike Thomas
'''

import unittest
from cStringIO import StringIO
from Data import Beat, Counter, fileUtils, DBErrors, DrumKit, FontOptions, DefaultKits
from Data.Drum import Drum, HeadData
from Data.Counter import CounterRegistry
from Data.Measure import Measure
from Data import MeasureCount, ScoreMetaData
from Data.NotePosition import NotePosition

from Data.fileStructures import dbfsv1

class TestBeat(unittest.TestCase):
    def testWriteFullBeat(self):
        beat = Beat.Beat(Counter.Counter("e+a"))
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv1.BeatStructureV1().write(beat, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["BEAT_START",
                          "  NUM_TICKS 4",
                          "  COUNT |^e+a|",
                          "BEAT_END"])


    def testWritePartialBeat(self):
        beat = Beat.Beat(Counter.Counter("e+a"), 2)
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv1.BeatStructureV1().write(beat, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["BEAT_START",
                          "  NUM_TICKS 2",
                          "  COUNT |^e+a|",
                          "BEAT_END"])

    def testReadFull(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS 4
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        beat = dbfsv1.BeatStructureV1().read(iterator)
        self.assertEqual("".join(beat.count(1)), "1e+a")

    def testReadPartial(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS 2
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        beat = dbfsv1.BeatStructureV1().read(iterator)
        self.assertEqual("".join(beat.count(1)), "1e")

    def testReadBadCount(self):
        handle = StringIO("""BEAT_START
        COUNT |^e+d|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.BadCount, dbfsv1.BeatStructureV1().read,
                          iterator)

    def testReadBadTicks(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS x
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.InvalidInteger, dbfsv1.BeatStructureV1().read,
                          iterator)

    def testReadBadNegativeTicks(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS -1
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.InvalidPositiveInteger,
                          dbfsv1.BeatStructureV1().read,
                          iterator)

    def testReadBadLine(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS 4
        COUNT |^e+a|
        BAD_LINE xxx
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.UnrecognisedLine,
                          dbfsv1.BeatStructureV1().read, iterator)

class TestMeasureCount(unittest.TestCase):
    def testSimpleWrite(self):
        myCounter = Counter.Counter("e+a")
        count = MeasureCount.makeSimpleCount(myCounter, 4)
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv1.MeasureCountStructureV1().write(count, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["COUNT_INFO_START",
                          "  BEAT_START",
                          "    NUM_TICKS 4",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 4",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 4",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 4",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "COUNT_INFO_END"])

    def testComplexWrite(self):
        counter1 = Counter.Counter("e+a")
        counter2 = Counter.Counter("+a")
        counter3 = Counter.Counter("+")
        counter4 = Counter.Counter("e+a")
        count = MeasureCount.MeasureCount()
        count.addBeats(Beat.Beat(counter1), 1)
        count.addBeats(Beat.Beat(counter2), 1)
        count.addBeats(Beat.Beat(counter3), 1)
        count.addBeats(Beat.Beat(counter4, 2), 1)
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv1.MeasureCountStructureV1().write(count, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["COUNT_INFO_START",
                          "  BEAT_START",
                          "    NUM_TICKS 4",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 3",
                          "    COUNT |^+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 2",
                          "    COUNT |^+|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 2",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "COUNT_INFO_END"])

    def testReadSimple(self):
        data = """COUNT_INFO_START
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                  COUNT_INFO_END"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        count = dbfsv1.MeasureCountStructureV1().read(iterator)
        self.assert_(count.isSimpleCount())
        self.assertEqual(len(count), 16)
        self.assertEqual(count.countString(), "1e+a2e+a3e+a4e+a")

    def testReadSimpleDefault(self):
        data = """DEFAULT_COUNT_INFO_START
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                  COUNT_INFO_END"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        count = dbfsv1.MeasureCountStructureV1(startTag = "DEFAULT_COUNT_INFO_START").read(iterator)
        self.assert_(count.isSimpleCount())
        self.assertEqual(len(count), 16)
        self.assertEqual(count.countString(), "1e+a2e+a3e+a4e+a")


    def testReadComplex(self):
        data = """COUNT_INFO_START
                  BEAT_START
                    COUNT |^e+a|
                  BEAT_END
                  BEAT_START
                    COUNT |^+a|
                  BEAT_END
                  BEAT_START
                    COUNT |^+|
                  BEAT_END
                  BEAT_START
                    NUM_TICKS 2
                    COUNT |^e+a|
                  BEAT_END
                COUNT_INFO_END"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        count = dbfsv1.MeasureCountStructureV1().read(iterator)
        self.assertFalse(count.isSimpleCount())
        self.assertEqual(len(count), 11)
        self.assertEqual(count.countString(), "1e+a2+a3+4e")

    def testBadLine(self):
        data = """COUNT_INFO_START
              UNRECOGNISED LINE
              BEAT_START
                  COUNT |^e+a|
              BEAT_END
          COUNT_INFO_END"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.UnrecognisedLine,
                          dbfsv1.MeasureCountStructureV1().read,
                          iterator)

    def testRepeatBeats(self):
        data = """COUNT_INFO_START
              REPEAT_BEATS 3
              BEAT_START
                  COUNT |^e+a|
              BEAT_END
          COUNT_INFO_END"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.UnrecognisedLine,
                          dbfsv1.MeasureCountStructureV1().read, iterator)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
