'''
Created on 12 Dec 2010

@author: Mike Thomas
'''
import unittest
from Data.Staff import Staff
from Data.Measure import Measure
from Data.DBConstants import BAR_TYPES, EMPTY_NOTE
from Data.DBErrors import BadTimeError

#pylint: disable-msg=R0904

class TestStaff(unittest.TestCase):
    def setUp(self):
        self.staff = Staff()

    def testEmptyStaff(self):
        self.assertEqual(self.staff.numMeasures(), 0)
        self.assertEqual(len(self.staff), 0)

    def testAddMeasure(self):
        self.staff.addMeasure(Measure(1))
        self.assertEqual(self.staff.numMeasures(), 1)
        self.assertEqual(len(self.staff), 1)
        self.staff.addMeasure(Measure(2))
        self.assertEqual(self.staff.numMeasures(), 2)
        self.assertEqual(len(self.staff), 3)

    def testIterateOverMeasures(self):
        for i in range(1, 16):
            self.staff.addMeasure(Measure(i))
        for i, measure in enumerate(self.staff):
            self.assertEqual(len(measure), i + 1)

    def testGetMeasureByIndex(self):
        for i in range(1, 16):
            self.staff.addMeasure(Measure(i))
        for i in range(1, 16):
            self.assertEqual(len(self.staff[i - 1]), i)

    def testDeleteMeasure(self):
        self.staff.addMeasure(Measure(1))
        self.staff.addMeasure(Measure(2))
        self.staff.deleteMeasure(0)
        self.assertEqual(self.staff.numMeasures(), 1)
        self.assertEqual(len(self.staff), 2)

    def testDeleteMeasure_BadIndex(self):
        self.staff.addMeasure(Measure(1))
        self.staff.addMeasure(Measure(2))
        self.assertRaises(BadTimeError, self.staff.deleteMeasure, -1)
        self.assertRaises(BadTimeError, self.staff.deleteMeasure, 2)

    def testInsertMeasure(self):
        self.staff.addMeasure(Measure(1))
        self.staff.addMeasure(Measure(3))
        self.staff.insertMeasure(1, Measure(2))
        for i, measure in enumerate(self.staff):
            self.assertEqual(len(measure), i + 1)

    def testInsertMeasureAtStart(self):
        self.staff.addMeasure(Measure(2))
        self.staff.insertMeasure(0, Measure(1))
        for i, measure in enumerate(self.staff):
            self.assertEqual(len(measure), i + 1)

    def testInsertMeasureAtEnd(self):
        self.staff.addMeasure(Measure(1))
        self.staff.insertMeasure(1, Measure(2))
        for i, measure in enumerate(self.staff):
            self.assertEqual(len(measure), i + 1)

    def testInsertMeasure_BadIndex(self):
        self.staff.addMeasure(Measure(1))
        self.staff.addMeasure(Measure(2))
        m = Measure(3)
        self.assertRaises(BadTimeError, self.staff.insertMeasure, -1, m)
        self.assertRaises(BadTimeError, self.staff.insertMeasure, 3, m)

    def testClearStaff(self):
        self.staff.addMeasure(Measure(16))
        self.staff.addMeasure(Measure(16))
        self.staff.addMeasure(Measure(16))
        self.staff.addMeasure(Measure(16))
        self.staff.clear()
        self.assertEqual(len(self.staff), 0)
        self.assertEqual(self.staff.numMeasures(), 0)

    def testCharacterWidth_EmptyStaff(self):
        self.assertEqual(self.staff.characterWidth(), 0)

    def testCharacterWidth(self):
        self.staff.addMeasure(Measure(16))
        self.staff.addMeasure(Measure(16))
        self.staff.addMeasure(Measure(16))
        self.assertEqual(self.staff.characterWidth(), 52)
        endMeasure = Measure(16)
        endMeasure.endBar = BAR_TYPES["SECTION_END"]
        self.staff.addMeasure(endMeasure)
        self.assertEqual(self.staff.characterWidth(), 70)

    def testGridWidth_EmptyStaff(self):
        self.assertEqual(self.staff.gridWidth(), 0)

    def testGridWidth(self):
        self.staff.addMeasure(Measure(16))
        self.staff.addMeasure(Measure(16))
        self.staff.addMeasure(Measure(16))
        self.assertEqual(self.staff.gridWidth(), 52)
        endMeasure = Measure(16)
        endMeasure.endBar = BAR_TYPES["SECTION_END"]
        self.staff.addMeasure(endMeasure)
        self.assertEqual(self.staff.gridWidth(), 69)


class TestNoteControl(unittest.TestCase):
    def setUp(self):
        self.staff = Staff()
        self.staff.addMeasure(Measure(16))
        self.staff.addMeasure(Measure(16))
        self.staff.addMeasure(Measure(16))
        self.staff.addMeasure(Measure(16))

    def testGetNote(self):
        self.assertEqual(self.staff.getNote(0, 0, 0), EMPTY_NOTE)

    def testGetNote_BadTime(self):
        self.assertRaises(BadTimeError, self.staff.getNote, -1, 0, 0)
        self.assertRaises(BadTimeError, self.staff.getNote, 20, 0, 0)
        self.assertRaises(BadTimeError, self.staff.getNote, 0, -1, 0)
        self.assertRaises(BadTimeError, self.staff.getNote, 0, 20, 0)

    def testAddNote(self):
        self.staff.addNote(0, 0, 0, "o")
        self.assertEqual(self.staff.getNote(0, 0, 0), "o")

    def testAddNote_BadTime(self):
        self.assertRaises(BadTimeError, self.staff.addNote, -1, 0, 0, "x")
        self.assertRaises(BadTimeError, self.staff.addNote, 4, 0, 0, "x")
        self.assertRaises(BadTimeError, self.staff.addNote, 0, -1, 0, "x")
        self.assertRaises(BadTimeError, self.staff.addNote, 0, 20, 0, "x")

    def testDeleteNote(self):
        self.staff.addNote(0, 0, 0, "o")
        self.staff.deleteNote(0, 0, 0)
        self.assertEqual(self.staff.getNote(0, 0, 0), EMPTY_NOTE)

    def testDeleteNote_BadTime(self):
        self.assertRaises(BadTimeError, self.staff.deleteNote, -1, 0, 0)
        self.assertRaises(BadTimeError, self.staff.deleteNote, 20, 0, 0)
        self.assertRaises(BadTimeError, self.staff.deleteNote, 0, -1, 0)
        self.assertRaises(BadTimeError, self.staff.deleteNote, 0, 20, 0)

    def testToggleNote(self):
        self.staff.toggleNote(0, 0, 0, "o")
        self.assertEqual(self.staff.getNote(0, 0, 0), "o")
        self.staff.toggleNote(0, 0, 0, "o")
        self.assertEqual(self.staff.getNote(0, 0, 0), EMPTY_NOTE)

    def testToggleNote_BadTime(self):
        self.assertRaises(BadTimeError, self.staff.toggleNote, -1, 0, 0, "x")
        self.assertRaises(BadTimeError, self.staff.toggleNote, 20, 0, 0, "x")
        self.assertRaises(BadTimeError, self.staff.toggleNote, 0, -1, 0, "x")
        self.assertRaises(BadTimeError, self.staff.toggleNote, 0, 20, 0, "x")

class TestCallBack(unittest.TestCase):
    def setUp(self):
        self.staff = Staff()
        self.staff.addMeasure(Measure(16))
        self.calls = []
        self.staff.setCallBack(lambda m, t, d: self.calls.append((m, t, d)))

    def testAddNoteCallBack(self):
        self.staff.addNote(0, 0, 0, "x")
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0], (0, 0, 0))
        self.staff.addNote(0, 0, 0, "x")
        self.assertEqual(len(self.calls), 1)
        self.staff.addNote(0, 0, 0, "o")
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[1], (0, 0, 0))

    def testDeleteNoteCallBack(self):
        self.staff.deleteNote(0, 0, 0)
        self.assertEqual(len(self.calls), 0)
        self.staff.addNote(0, 0, 0, "x")
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0], (0, 0, 0))
        self.staff.deleteNote(0, 0, 0)
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[1], (0, 0, 0))

    def testToggleNoteCallBack(self):
        self.staff.toggleNote(0, 0, 0, "x")
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0], (0, 0, 0))
        self.staff.toggleNote(0, 0, 0, "x")
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[1], (0, 0, 0))
        self.staff.toggleNote(0, 0, 0, "x")
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(self.calls[2], (0, 0, 0))
        self.staff.toggleNote(0, 0, 0, "o")
        self.assertEqual(len(self.calls), 4)
        self.assertEqual(self.calls[2], (0, 0, 0))

    def testClearCallBack(self):
        self.staff.clearCallBack()
        self.staff.addNote(0, 0, 0, "x")
        self.assertEqual(len(self.calls), 0)

    def testAddMeasureCallBack(self):
        self.staff.addMeasure(Measure(16))
        self.staff.addNote(1, 0, 0, "x")
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0], (1, 0, 0))

    def testDeleteMeasureCallBack(self):
        self.staff.addMeasure(Measure(16))
        self.staff.addMeasure(Measure(16))
        self.staff.addNote(1, 0, 0, "x")
        self.staff.deleteMeasure(0)
        self.staff.deleteNote(0, 0, 0)
        self.staff.addNote(1, 0, 0, "x")
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(self.calls[0], (1, 0, 0))
        self.assertEqual(self.calls[1], (0, 0, 0))
        self.assertEqual(self.calls[2], (1, 0, 0))

    def testInsertMeasureCallBack(self):
        self.staff.addNote(0, 0, 0, "x")
        self.staff.insertMeasure(0, Measure(8))
        self.staff.addNote(0, 0, 0, "x")
        self.staff.deleteNote(1, 0, 0)
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(self.calls[0], (0, 0, 0))
        self.assertEqual(self.calls[1], (0, 0, 0))
        self.assertEqual(self.calls[2], (1, 0, 0))



if __name__ == "__main__":
    unittest.main()
