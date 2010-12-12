'''
Created on 31 Jul 2010

@author: Mike Thomas
'''
import unittest
from StringIO import StringIO
from Data.Score import Score, loadScore, makeEmptyScore
from Data.Instrument import Instrument
from Data.Line import Line
import Data.Note

#pylint: disable-msg=R0904
class Test(unittest.TestCase):

    def setUp(self):
        self.score = Score()

    def test_appendInstrument(self):
        instr = Instrument("test")
        self.score.appendInstrument(instr)
        self.assertEqual(self.score.numLines, 1)

    def test_getItem(self):
        instr = Instrument("test")
        self.score.appendInstrument(instr)
        self.assert_(isinstance(self.score[0], Line))
        self.assertEqual(self.score[0].instrument, instr)
        self.assert_(isinstance(self.score[instr.name], Line))
        self.assertEqual(self.score[instr.name].instrument, instr)

    def test_Iterate(self):
        for i in range(0, 5):
            instr = Instrument("drum%d" % i)
            self.score.appendInstrument(instr)
        for i, line in enumerate(self.score):
            self.assertEqual(line.instrument.name, "drum%d" % i)

    def test_SetInstruments(self):
        iList = [Instrument("drum%d" % i) for i in range(0, 5)]
        self.score.setInstruments(iList)
        self.assertEqual(self.score.numLines, 5)
        for i, line in enumerate(self.score):
            self.assertEqual(line.instrument.name, "drum%d" % i)
        iList = [Instrument("drum%d" % i) for i in range(3, 7)]
        self.score.setInstruments(iList)
        self.assertEqual(self.score.numLines, 4)
        for i, line in enumerate(self.score):
            self.assertEqual(line.instrument.name, "drum%d" % (i + 3))

    def test_SongLength_EmptySong(self):
        self.assertEqual(len(self.score), 0)

    def test_addTime(self):
        self.score.addTime(32)
        self.assertEqual(len(self.score), 32)

    def test_lineHead(self):
        iList = [Instrument("drum%d" % i, head = str(i)) for i in range(0, 5)]
        self.score.setInstruments(iList)
        for i in range(0, 5):
            self.assertEqual(self.score.lineHead(i), str(i))

    def test_Notes_LineIndex(self):
        iList = [Instrument("drum%d" % i) for i in range(0, 5)]
        self.score.setInstruments(iList)
        self.score.addTime(17)
        self.score.addNote(0, 0, "x")
        self.assertEqual(self.score.getNote(0, 0), "x")

    def test_Notes_LineName(self):
        iList = [Instrument("drum%d" % i) for i in range(0, 5)]
        self.score.setInstruments(iList)
        self.score.addTime(17)
        self.score.addNote(0, "drum2", "x")
        self.assertEqual(self.score.getNote(0, "drum2"), "x")

    def test_iterNotes(self):
        iList = [Instrument("drum%d" % i, head = "x") for i in range(0, 5)]
        self.score.setInstruments(iList)
        self.score.addTime(17)
        notes = [(0, 0, "o"), (4, 2, "o"), (8, 0, "o"), (12, 2, "o")]
        for i in range(0, 8):
            notes.append((2 * i, 4, "x"))
        notes = [Data.Note.Note(*noteData) for noteData in notes]
        for note in notes:
            self.score.addNote(note.time, note.lineIndex, note.head)
        notes.sort()
        returnedNotes = list(self.score.iterNotes())
        self.assertEqual(returnedNotes[-1].time, 16)
        self.assertEqual(notes, returnedNotes[:-1])

    def test_defaultKit(self):
        self.score.loadDefaultKit()
        self.assertEqual(self.score.numLines, len(self.score.DefaultKit))
        self.assertEqual([l.instrument for l in self.score],
                         self.score.DefaultKit)

    def testSaveLoad(self):
        self.score.loadDefaultKit()
        self.score.addTime(16)
        notes = [(0, 0, "o"), (4, 2, "o"), (8, 0, "o"), (12, 2, "o")]
        for i in range(0, 8):
            notes.append((2 * i, 4, "x"))
        notes = [Data.Note.Note(*noteData) for noteData in notes]
        for note in notes:
            self.score.addNote(note.time, note.lineIndex, note.head)
        scoreString = StringIO("")
        self.score.save(scoreString)
        scoreString.seek(0)
        newScore = loadScore(scoreString)
        for oldNote, newNote in zip(self.score.iterNotes(),
                                    newScore.iterNotes()):
            self.assertEqual(oldNote.time, newNote.time)
            self.assertEqual(oldNote.lineIndex, newNote.lineIndex)
            self.assertEqual(oldNote.head, newNote.head)

class TestStaticFunction(unittest.TestCase):
    def testMakeEmptyScore(self):
        score = makeEmptyScore()
        self.assertEqual(score.numLines, len(Score.DefaultKit))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
