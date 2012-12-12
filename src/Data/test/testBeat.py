'''
Created on 12 Dec 2012

@author: Mike Thomas
'''
import unittest
from cStringIO import StringIO
from Data import Beat, Counter
from Data import fileUtils

# pylint: disable-msg=R0904

class TestFullBeat(unittest.TestCase):
    beat = Beat.Beat(Counter.Counter(Counter.BEAT_COUNT + "e+a"))

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

    def testWrite(self):
        handle = StringIO()
        indenter = fileUtils.Indenter()
        self.beat.write(handle, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["BEAT_START",
                          "  COUNT |^e+a|",
                          "BEAT_END"])

class TestPartialBeat(unittest.TestCase):
    beat = Beat.Beat(Counter.Counter(Counter.BEAT_COUNT + "e+a"), 2)

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

    def testWrite(self):
        handle = StringIO()
        indenter = fileUtils.Indenter()
        self.beat.write(handle, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["BEAT_START",
                          "  NUM_TICKS 2",
                          "  COUNT |^e+a|",
                          "BEAT_END"])

class TestReadBeats(unittest.TestCase):
    def testReadFull(self):
        handle = StringIO("""BEAT_START
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        beat = Beat.Beat.read(iterator)
        self.assertEqual("".join(beat.count(1)), "1e+a")

    def testReadPartial(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS 2
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        beat = Beat.Beat.read(iterator)
        self.assertEqual("".join(beat.count(1)), "1e")

    def testReadBadCount(self):
        handle = StringIO("""BEAT_START
        COUNT |^e+d|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(IOError, Beat.Beat.read, iterator)

    def testReadBadTicks(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS x
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(IOError, Beat.Beat.read, iterator)

    def testReadBadNegativeTicks(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS -1
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(IOError, Beat.Beat.read, iterator)

    def testReadBadLine(self):
        handle = StringIO("""BEAT_START
        COUNT |^e+a|
        BAD_LINE xxx
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(IOError, Beat.Beat.read, iterator)

if __name__ == "__main__":
    unittest.main()
