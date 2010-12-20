'''
Created on 12 Dec 2010

@author: Mike Thomas
'''
import unittest
from Data.Score import Score
from Data.DBErrors import BadTimeError, OverSizeMeasure
from Data.DBConstants import EMPTY_NOTE
from Data.NotePosition import NotePosition

#pylint: disable-msg=R0904

class TestScoreOneStaff(unittest.TestCase):
    def setUp(self):
        self.score = Score()

    def testEmptyScore(self):
        self.assertEqual(len(self.score), 0)
        self.assertEqual(self.score.numStaffs(), 0)
        self.assertEqual(self.score.numMeasures(), 0)
        self.assertEqual(len(self.score.drumKit), 0)

    def testAddMeasure(self):
        self.score.addMeasure(16)
        self.assertEqual(len(self.score), 16)
        self.assertEqual(self.score.numStaffs(), 1)
        self.assertEqual(self.score.numMeasures(), 1)

    def testGetMeasure(self):
        for i in range(1, 17):
            self.score.addMeasure(i)
        for i in range(1, 17):
            self.assertEqual(len(self.score.getMeasure(i - 1)), i)

    def testGetMeasure_BadIndex(self):
        self.assertRaises(BadTimeError, self.score.getMeasure, 0)
        self.score.addMeasure(16)
        self.score.addMeasure(16)
        self.score.addMeasure(16)
        self.assertRaises(BadTimeError, self.score.getMeasure, -1)
        self.assertRaises(BadTimeError, self.score.getMeasure, 3)

    def testDeleteMeasure(self):
        self.score.addMeasure(16)
        self.score.addMeasure(16)
        self.score.addMeasure(16)
        self.score.deleteMeasure(1)
        self.assertEqual(len(self.score), 32)
        self.assertEqual(self.score.numStaffs(), 1)
        self.assertEqual(self.score.numMeasures(), 2)

    def testDeleteMeasure_EmptySystem(self):
        self.score.addMeasure(16)
        self.score.addMeasure(16)
        self.score.addMeasure(16)
        self.score.deleteMeasure(1)
        self.assertEqual(self.score.numMeasures(), 2)
        self.score.deleteMeasure(1)
        self.assertEqual(self.score.numMeasures(), 1)
        self.score.deleteMeasure(0)
        self.assertEqual(len(self.score), 0)
        self.assertEqual(self.score.numStaffs(), 0)
        self.assertEqual(self.score.numMeasures(), 0)

    def testDeleteMeasure_BadIndex(self):
        self.score.addMeasure(16)
        self.score.addMeasure(16)
        self.score.addMeasure(16)
        self.assertRaises(BadTimeError, self.score.deleteMeasure, -1)
        self.assertRaises(BadTimeError, self.score.deleteMeasure, 3)

    def testInsertMeasure(self):
        self.score.addMeasure(16)
        self.score.addMeasure(16)
        self.score.addMeasure(16)
        self.score.insertMeasure(8, 2)
        self.assertEqual(self.score.numMeasures(), 4)
        self.assertEqual(len(self.score), 56)
        self.assertEqual(len(self.score.getMeasure(2)), 8)
        self.score.insertMeasure(24, 4)
        self.assertEqual(self.score.numMeasures(), 5)
        self.assertEqual(len(self.score), 80)
        self.assertEqual(len(self.score.getMeasure(4)), 24)

    def testInsertMeasure_IntoEmptyScore(self):
        self.score.insertMeasure(16, 0)
        self.assertEqual(self.score.numMeasures(), 1)
        self.assertEqual(len(self.score), 16)
        self.assertEqual(len(self.score.getMeasure(0)), 16)

    def testInsertMeasure_BadIndex(self):
        self.assertRaises(BadTimeError, self.score.insertMeasure, 16, -1)
        self.score.addMeasure(16)
        self.score.addMeasure(16)
        self.score.addMeasure(16)
        self.assertRaises(BadTimeError, self.score.insertMeasure, 16, -1)
        self.assertRaises(BadTimeError, self.score.insertMeasure, 16, 4)

    def testMoveMeasure(self):
        pass

    def testCopyMeasure(self):
        pass

class TestCharacterFormatScore(unittest.TestCase):
    def setUp(self):
        self.score = Score()

    def testTextFormatScore(self):
        for dummy in range(0, 20):
            self.score.addMeasure(16)
        self.score.textFormatScore(80)
        self.assertEqual(self.score.numStaffs(), 5)
        for staff in self.score.iterStaffs():
            self.assertEqual(staff.numMeasures(), 4)
            self.assertEqual(len(staff), 64)
            self.assertEqual(staff.characterWidth(), 69)

    def testTextFormatScoreWithSections(self):
        for dummy in range(0, 20):
            self.score.addMeasure(16)
        self.score.getMeasure(5).setSectionEnd(True)
        self.score.textFormatScore(80)
        self.assertEqual(self.score.numStaffs(), 6)
        self.assertEqual(self.score.getStaff(1).characterWidth(), 36)

    def testTextFormatScore_SectionEndAtScoreEnd(self):
        for dummy in range(0, 20):
            self.score.addMeasure(16)
        self.score.getMeasure(19).setSectionEnd(True)
        self.score.textFormatScore(80)
        self.assertEqual(self.score.numStaffs(), 5)

    def testTextFormatScoreWithSectionsAndRepeat(self):
        for dummy in range(0, 20):
            self.score.addMeasure(16)
        self.score.getMeasure(0).setRepeatStart(True)
        self.score.getMeasure(5).setSectionEnd(True)
        self.score.getMeasure(5).setRepeatEnd(True)
        self.score.textFormatScore(80)
        self.assertEqual(self.score.numStaffs(), 6)
        self.assertEqual(self.score.getStaff(1).characterWidth(), 36)

    def testTextFormatScoreWithLargeBar(self):
        for dummy in range(0, 12):
            self.score.addMeasure(16)
        self.score.addMeasure(70)
        for dummy in range(0, 12):
            self.score.addMeasure(16)
        self.score.textFormatScore(80)
        self.assertEqual(self.score.numStaffs(), 7)
        self.assertEqual(self.score.getStaff(3).characterWidth(), 72)

    def testTextFormatScoreWithOverSizeBar_IgnoreErrors(self):
        for dummy in range(0, 12):
            self.score.addMeasure(16)
        self.score.addMeasure(80)
        for dummy in range(0, 12):
            self.score.addMeasure(16)
        self.score.textFormatScore(80, ignoreErrors = True)
        self.assertEqual(self.score.numStaffs(), 7)
        self.assertEqual(self.score.getStaff(3).characterWidth(), 82)

    def testTextFormatScoreWithOverSizeBar_DontIgnoreErrors(self):
        for dummy in range(0, 12):
            self.score.addMeasure(16)
        self.score.addMeasure(90)
        for dummy in range(0, 12):
            self.score.addMeasure(16)
        self.assertRaises(OverSizeMeasure, self.score.textFormatScore, 80)

    def testTextFormatScore_FewerStaffsAfterDelete(self):
        for dummy in range(0, 9):
            self.score.addMeasure(16)
        self.score.textFormatScore(80)
        self.assertEqual(self.score.numStaffs(), 3)
        self.score.deleteMeasure(6)
        self.score.textFormatScore(80)
        self.assertEqual(self.score.numStaffs(), 2)

    def testTextFormatScore_FewerStaffsOnWiderFormat(self):
        for dummy in range(0, 8):
            self.score.addMeasure(16)
        self.score.textFormatScore(40)
        self.assertEqual(self.score.numStaffs(), 4)
        self.score.textFormatScore(80)
        self.assertEqual(self.score.numStaffs(), 2)


class TestScoreManyStaffs(unittest.TestCase):
    def testAddMeasure(self):
        pass

    def testDeleteMeasure(self):
        pass

    def testDeleteMeasure_EmptyStaff(self):
        pass

class TestNoteControl(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.drumKit.loadDefaultKit()
        for dummy in range(0, 12):
            self.score.addMeasure(16)
        self.score.textFormatScore(80)

    def testGetNote(self):
        self.assertEqual(self.score.getNote(NotePosition(0, 0, 0, 0)),
                         EMPTY_NOTE)

    def testGetNote_BadTime(self):
        self.assertRaises(BadTimeError, self.score.getNote,
                          NotePosition(-1, 0, 0, 0))
        self.assertRaises(BadTimeError, self.score.getNote,
                          NotePosition(20, 0, 0, 0))
        self.assertRaises(BadTimeError, self.score.getNote,
                          NotePosition(0, -1, 0, 0))
        self.assertRaises(BadTimeError, self.score.getNote,
                          NotePosition(0, 20, 0, 0))
        self.assertRaises(BadTimeError, self.score.getNote,
                          NotePosition(0, 0, -1, 0))
        self.assertRaises(BadTimeError, self.score.getNote,
                          NotePosition(0, 0, 20, 0))

    def testGetNote_BadNote(self):
        self.assertRaises(BadTimeError, self.score.getNote,
                          NotePosition(0, 0, 0, -1))
        self.assertRaises(BadTimeError, self.score.getNote,
                          NotePosition(0, 0, 0,
                                       len(self.score.drumKit)))

    def testAddNote(self):
        self.score.addNote(NotePosition(0, 0, 0, 0), "o")
        self.assertEqual(self.score.getNote(NotePosition(0, 0, 0, 0)), "o")

    def testAddNote_BadTime(self):
        self.assertRaises(BadTimeError,
                          self.score.addNote, NotePosition(-1, 0, 0, 0), "x")
        self.assertRaises(BadTimeError,
                          self.score.addNote, NotePosition(20, 0, 0, 0), "x")
        self.assertRaises(BadTimeError,
                          self.score.addNote, NotePosition(0, -1, 0, 0), "x")
        self.assertRaises(BadTimeError,
                          self.score.addNote, NotePosition(0, 20, 0, 0), "x")
        self.assertRaises(BadTimeError,
                          self.score.addNote, NotePosition(0, 0, -1, 0), "x")
        self.assertRaises(BadTimeError,
                          self.score.addNote, NotePosition(0, 0, 20, 0), "x")

    def testAddNote_BadNote(self):
        self.assertRaises(BadTimeError, self.score.addNote,
                          NotePosition(0, 0, 0, -1), "x")
        self.assertRaises(BadTimeError, self.score.addNote,
                          NotePosition(0, 0, 0,
                                       len(self.score.drumKit)), "x")

    def testAddNote_DefaultHead(self):
        self.score.addNote(NotePosition(0, 0, 0, 0))
        defaultHead = self.score.drumKit[0].head
        self.assertEqual(self.score.getNote(NotePosition(0, 0, 0, 0)),
                         defaultHead)

    def testDeleteNote(self):
        self.score.addNote(NotePosition(0, 0, 0, 0), "o")
        self.score.deleteNote(NotePosition(0, 0, 0, 0))
        self.assertEqual(self.score.getNote(NotePosition(0, 0, 0, 0)),
                         EMPTY_NOTE)

    def testDeleteNote_BadTime(self):
        self.assertRaises(BadTimeError, self.score.deleteNote,
                          NotePosition(-1, 0, 0, 0))
        self.assertRaises(BadTimeError, self.score.deleteNote,
                          NotePosition(20, 0, 0, 0))
        self.assertRaises(BadTimeError, self.score.deleteNote,
                          NotePosition(0, -1, 0, 0))
        self.assertRaises(BadTimeError, self.score.deleteNote,
                          NotePosition(0, 20, 0, 0))
        self.assertRaises(BadTimeError, self.score.deleteNote,
                          NotePosition(0, 0, -1, 0))
        self.assertRaises(BadTimeError, self.score.deleteNote,
                          NotePosition(0, 0, 20, 0))

    def testDeleteNote_BadNote(self):
        self.assertRaises(BadTimeError, self.score.deleteNote,
                          NotePosition(0, 0, 0, -1))
        self.assertRaises(BadTimeError, self.score.deleteNote,
                          NotePosition(0, 0, 0,
                                       len(self.score.drumKit)))

    def testToggleNote(self):
        self.score.toggleNote(NotePosition(0, 0, 0, 0), "o")
        self.assertEqual(self.score.getNote(NotePosition(0, 0, 0, 0)), "o")
        self.score.toggleNote(NotePosition(0, 0, 0, 0), "o")
        self.assertEqual(self.score.getNote(NotePosition(0, 0, 0, 0)),
                         EMPTY_NOTE)

    def testToggleNote_BadTime(self):
        self.assertRaises(BadTimeError, self.score.toggleNote,
                          NotePosition(-1, 0, 0, 0), "x")
        self.assertRaises(BadTimeError, self.score.toggleNote,
                          NotePosition(20, 0, 0, 0), "x")
        self.assertRaises(BadTimeError, self.score.toggleNote,
                          NotePosition(0, -1, 0, 0), "x")
        self.assertRaises(BadTimeError, self.score.toggleNote,
                          NotePosition(0, 20, 0, 0), "x")
        self.assertRaises(BadTimeError, self.score.toggleNote,
                          NotePosition(0, 0, -1, 0), "x")
        self.assertRaises(BadTimeError, self.score.toggleNote,
                          NotePosition(0, 0, 20, 0), "x")

    def testToggleNote_BadNote(self):
        self.assertRaises(BadTimeError, self.score.toggleNote,
                          NotePosition(0, 0, 0, -1), "x")
        self.assertRaises(BadTimeError, self.score.toggleNote,
                          NotePosition(0, 0, 0, len(self.score.drumKit)), "x")

    def testToggleNote_DefaultHead(self):
        self.score.toggleNote(NotePosition(0, 0, 0, 0))
        defaultHead = self.score.drumKit[0].head
        self.assertEqual(self.score.getNote(NotePosition(0, 0, 0, 0)),
                         defaultHead)
        self.score.toggleNote(NotePosition(0, 0, 0, 0))
        self.assertEqual(self.score.getNote(NotePosition(0, 0, 0, 0)),
                         EMPTY_NOTE)

class TestCallBack(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.addMeasure(16)
        self.calls = []
        def myCallBack(position):
            self.calls.append((position.staffIndex,
                               position.measureIndex,
                               position.noteTime,
                               position.drumIndex))
        self.score.setCallBack(myCallBack)

    def testAddNote(self):
        pass

if __name__ == "__main__":
    unittest.main()
