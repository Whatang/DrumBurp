'''
Created on 31 Jul 2010

@author: Mike Thomas
'''
import unittest
from Data.Score import Score
from Data.Instrument import Instrument
from Data.Line import Line
import Data.Note

SCORE = None
class Test(unittest.TestCase):


    def setUp(self):
        global SCORE
        SCORE = Score()

    def test_appendInstrument(self):
        instr = Instrument("test")
        SCORE.appendInstrument(instr)
        self.assertEqual(len(SCORE), 1)

    def test_getItem(self):
        instr = Instrument("test")
        SCORE.appendInstrument(instr)
        self.assert_(isinstance(SCORE[0], Line))
        self.assertEqual(SCORE[0].instrument, instr)
        self.assert_(isinstance(SCORE[instr.name], Line))
        self.assertEqual(SCORE[instr.name].instrument, instr)

    def test_Iterate(self):
        for i in range(0, 5):
            instr = Instrument("drum%d" % i)
            SCORE.appendInstrument(instr)
        for i, line in enumerate(SCORE):
            self.assertEqual(line.instrument.name, "drum%d" % i)

    def test_SetInstruments(self):
        iList = [Instrument("drum%d" % i) for i in range(0, 5)]
        SCORE.setInstruments(iList)
        self.assertEqual(len(SCORE), 5)
        for i, line in enumerate(SCORE):
            self.assertEqual(line.instrument.name, "drum%d" % i)
        iList = [Instrument("drum%d" % i) for i in range(3, 7)]
        SCORE.setInstruments(iList)
        self.assertEqual(len(SCORE), 4)
        for i, line in enumerate(SCORE):
            self.assertEqual(line.instrument.name, "drum%d" % (i + 3))

    def test_SongLength_EmptySong(self):
        self.assertEqual(SCORE.songLength, 0)

    def test_Notes_LineIndex(self):
        iList = [Instrument("drum%d" % i) for i in range(0, 5)]
        SCORE.setInstruments(iList)
        SCORE.addNote(0, 0, "x")
        self.assertEqual(SCORE.getNote(0, 0), "x")

    def test_Notes_LineName(self):
        iList = [Instrument("drum%d" % i) for i in range(0, 5)]
        SCORE.setInstruments(iList)
        SCORE.addNote(0, "drum2", "x")
        self.assertEqual(SCORE.getNote(0, "drum2"), "x")

    def test_iterNotes(self):
        iList = [Instrument("drum%d" % i, head = "x") for i in range(0, 5)]
        SCORE.setInstruments(iList)
        SCORE.songLength = 17
        notes = [(0, 0, "o"), (4, 2, "o"), (8, 0, "o"), (12, 2, "o")]
        for i in range(0, 8):
            notes.append((2 * i, 4, "x"))
        notes = [Data.Note.Note(*noteData) for noteData in notes]
        for note in notes:
            SCORE.addNote(note.time, note.lineIndex, note.head)
        notes.sort()
        returnedNotes = list(SCORE.iterNotes())
        self.assertEqual(returnedNotes[-1].time, 16)
        self.assertEqual(notes, returnedNotes[:-1])

    def test_defaultKit(self):
        SCORE.loadDefaultKit()
        self.assertEqual(len(SCORE), len(SCORE.DefaultKit))
        self.assertEqual([l.instrument for l in SCORE],
                         SCORE.DefaultKit)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
