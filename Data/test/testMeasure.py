'''
Created on 12 Dec 2010

@author: Mike Thomas
'''
import unittest
from Data.Measure import Measure
from Data.DBErrors import BadTimeError
from Data.DBConstants  import EMPTY_NOTE, BAR_TYPES

#pylint: disable-msg=R0904

class TestMeasure(unittest.TestCase):
    def setUp(self):
        self.measure = Measure(16)

    def testEmptyMeasure(self):
        self.assertEqual(len(self.measure), 16)
        self.assertEqual(self.measure.numNotes(), 0)
        self.assertEqual(self.measure.getNote(0, 0),
                         EMPTY_NOTE)
        self.assertEqual(self.measure.startBar,
                         BAR_TYPES["NORMAL_BAR"])
        self.assertEqual(self.measure.endBar,
                         BAR_TYPES["NORMAL_BAR"])

    def testGetNote_BadTime(self):
        self.assertRaises(BadTimeError, self.measure.getNote, -1, 0)
        self.assertRaises(BadTimeError, self.measure.getNote, 20, 0)

    def testNumNotes(self):
        for i in range(0, 16):
            self.measure.addNote(i, 0, "o")
        self.assertEqual(self.measure.numNotes(), 16)

    def testAddNote(self):
        self.measure.addNote(0, 0, "o")
        self.assertEqual(self.measure.getNote(0, 0), "o")

    def testAddNote_BadTime(self):
        self.assertRaises(BadTimeError, self.measure.addNote, -1, 0, "x")
        self.assertRaises(BadTimeError, self.measure.addNote, 20, 0, "x")

    def testDeleteNote(self):
        self.measure.addNote(0, 0, "o")
        self.measure.deleteNote(0, 0)
        self.assertEqual(self.measure.numNotes(), 0)
        self.assertEqual(self.measure.getNote(0, 0), EMPTY_NOTE)

    def testDeleteNote_BadTime(self):
        self.assertRaises(BadTimeError, self.measure.deleteNote, -1, 0)
        self.assertRaises(BadTimeError, self.measure.deleteNote, 20, 0)

    def testToggleNote(self):
        self.measure.toggleNote(0, 0, "o")
        self.assertEqual(self.measure.getNote(0, 0), "o")
        self.assertEqual(self.measure.numNotes(), 1)
        self.measure.toggleNote(0, 0, "o")
        self.assertEqual(self.measure.numNotes(), 0)
        self.assertEqual(self.measure.getNote(0, 0), EMPTY_NOTE)

    def testToggleNote_ChangeNote(self):
        self.measure.toggleNote(0, 0, "o")
        self.measure.toggleNote(0, 0, "x")
        self.assertEqual(self.measure.getNote(0, 0), "x")

    def testToggleNote_BadTime(self):
        self.assertRaises(BadTimeError, self.measure.toggleNote, -1, 0, "x")
        self.assertRaises(BadTimeError, self.measure.toggleNote, 20, 0, "x")

    def testSetWidth_BadWidth(self):
        self.assertRaises(AssertionError, self.measure.setWidth, -1)

    def testSetWidth_MakeEmptyMeasureBigger(self):
        self.measure.setWidth(32)
        self.assertEqual(len(self.measure), 32)

    def testSetWidth_MakeEmptyMeasureSmaller(self):
        self.measure.setWidth(8)
        self.assertEqual(len(self.measure), 8)

    def testSetWidth_MakeNonEmptyMeasureBigger(self):
        self.measure.addNote(7, 1, "x")
        self.measure.setWidth(32)
        self.assertEqual(len(self.measure), 32)
        self.assertEqual(self.measure.getNote(7, 1), "x")

    def testSetWidth_MakeNonEmptyMeasureSmaller(self):
        self.measure.addNote(7, 1, "x")
        self.measure.addNote(12, 1, "x")
        self.measure.setWidth(8)
        self.assertEqual(len(self.measure), 8)
        self.assertEqual(self.measure.getNote(7, 1), "x")
        self.assertEqual(self.measure.numNotes(), 1)

    def testSetWidth_NoEffect(self):
        self.measure.addNote(7, 1, "x")
        self.measure.addNote(12, 1, "x")
        self.measure.setWidth(16)
        self.assertEqual(len(self.measure), 16)
        self.assertEqual(self.measure.getNote(7, 1), "x")
        self.assertEqual(self.measure.getNote(12, 1), "x")
        self.assertEqual(self.measure.numNotes(), 2)

    def testSetSectionEnd_NoRepeat(self):
        self.assertFalse(self.measure.isSectionEnd())
        self.measure.setSectionEnd(True)
        self.assert_(self.measure.isSectionEnd())
        self.assertEqual(self.measure.endBar, BAR_TYPES["SECTION_END"])
        self.measure.setSectionEnd(True)
        self.assert_(self.measure.isSectionEnd())
        self.assertEqual(self.measure.endBar, BAR_TYPES["SECTION_END"])
        self.measure.setSectionEnd(False)
        self.assertFalse(self.measure.isSectionEnd())
        self.assertEqual(self.measure.endBar, BAR_TYPES["NORMAL_BAR"])
        self.measure.setSectionEnd(False)
        self.assertFalse(self.measure.isSectionEnd())
        self.assertEqual(self.measure.endBar, BAR_TYPES["NORMAL_BAR"])

    def testSetSectionEnd_Repeat(self):
        self.measure.setRepeatEnd(True)
        self.assertFalse(self.measure.isSectionEnd())
        self.measure.setSectionEnd(True)
        self.assert_(self.measure.isSectionEnd())
        self.assertEqual(self.measure.endBar, BAR_TYPES["REPEAT_END"])
        self.measure.setSectionEnd(True)
        self.assert_(self.measure.isSectionEnd())
        self.assertEqual(self.measure.endBar, BAR_TYPES["REPEAT_END"])
        self.measure.setSectionEnd(False)
        self.assertFalse(self.measure.isSectionEnd())
        self.assertEqual(self.measure.endBar, BAR_TYPES["REPEAT_END"])
        self.measure.setSectionEnd(False)
        self.assertFalse(self.measure.isSectionEnd())
        self.assertEqual(self.measure.endBar, BAR_TYPES["REPEAT_END"])

    def testSetRepeatStart(self):
        self.assertEqual(self.measure.startBar, BAR_TYPES["NORMAL_BAR"])
        self.measure.setRepeatStart(True)
        self.assertEqual(self.measure.startBar, BAR_TYPES["REPEAT_START"])
        self.measure.setRepeatStart(False)
        self.assertEqual(self.measure.startBar, BAR_TYPES["NORMAL_BAR"])

    def testSetRepeatEnd_NotSectionEnd(self):
        self.assertEqual(self.measure.endBar, BAR_TYPES["NORMAL_BAR"])
        self.measure.setRepeatEnd(True)
        self.assertEqual(self.measure.endBar, BAR_TYPES["REPEAT_END"])
        self.measure.setRepeatEnd(False)
        self.assertEqual(self.measure.endBar, BAR_TYPES["NORMAL_BAR"])

    def testSetRepeatEnd_IsSectionEnd(self):
        self.measure.setSectionEnd(True)
        self.assertEqual(self.measure.endBar, BAR_TYPES["SECTION_END"])
        self.measure.setRepeatEnd(True)
        self.assertEqual(self.measure.endBar, BAR_TYPES["REPEAT_END"])
        self.measure.setRepeatEnd(False)
        self.assertEqual(self.measure.endBar, BAR_TYPES["SECTION_END"])

class TestCallBack(unittest.TestCase):
    def setUp(self):
        self.measure = Measure(16)
        self.calls = []
        def myCallBack(noteIndex, drumIndex):
            self.calls.append((noteIndex, drumIndex))
        self.measure.setCallBack(myCallBack)

    def testAddNoteCallBack(self):
        self.measure.addNote(0, 0, "x")
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0], (0, 0))
        self.measure.addNote(0, 0, "x")
        self.assertEqual(len(self.calls), 1)
        self.measure.addNote(0, 0, "o")
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[1], (0, 0))

    def testDeleteNoteCallBack(self):
        self.measure.deleteNote(0, 0)
        self.assertEqual(len(self.calls), 0)
        self.measure.addNote(0, 0, "x")
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0], (0, 0))
        self.measure.deleteNote(0, 0)
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[1], (0, 0))

    def testToggleNoteCallBack(self):
        self.measure.toggleNote(0, 0, "x")
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0], (0, 0))
        self.measure.toggleNote(0, 0, "x")
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[1], (0, 0))
        self.measure.toggleNote(0, 0, "x")
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(self.calls[2], (0, 0))
        self.measure.toggleNote(0, 0, "o")
        self.assertEqual(len(self.calls), 4)
        self.assertEqual(self.calls[2], (0, 0))

    def testClearCallBack(self):
        self.measure.clearCallBack()
        self.measure.addNote(0, 0, "x")
        self.assertEqual(len(self.calls), 0)

if __name__ == "__main__":
    unittest.main()
