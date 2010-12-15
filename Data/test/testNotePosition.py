'''
Created on 14 Dec 2010

@author: Mike Thomas
'''
import unittest

from Data.NotePosition import NotePosition
from Data.DBErrors import BadNoteSpecification

#pylint: disable-msg=R0904



class TestNotePosition(unittest.TestCase):
    def testBadNoteSpecification(self):
        self.assertRaises(BadNoteSpecification, NotePosition,
                          staffIndex = 1, measureIndex = 2, noteTime = 3)
        self.assertRaises(BadNoteSpecification, NotePosition,
                          staffIndex = 1, measureIndex = 2, drumIndex = 4)
        self.assertRaises(BadNoteSpecification, NotePosition,
                          measureIndex = 1, drumIndex = 3)
        self.assertRaises(BadNoteSpecification, NotePosition,
                          measureIndex = 1, noteTime = 2)
        self.assertRaises(BadNoteSpecification, NotePosition,
                          staffIndex = 1, drumIndex = 3)
        self.assertRaises(BadNoteSpecification, NotePosition,
                          staffIndex = 1, noteTime = 2)
        self.assertRaises(BadNoteSpecification, NotePosition,
                          drumIndex = 3)
        self.assertRaises(BadNoteSpecification, NotePosition,
                          noteTime = 2)

    def testInitAll(self):
        np = NotePosition(1, 2, 3, 4)
        self.assertEqual(np.staffIndex, 1)
        self.assertEqual(np.measureIndex, 2)
        self.assertEqual(np.noteTime, 3)
        self.assertEqual(np.drumIndex, 4)

    def testInitAllByName(self):
        np = NotePosition(staffIndex = 1, measureIndex = 2,
                          noteTime = 3, drumIndex = 4)
        self.assertEqual(np.staffIndex, 1)
        self.assertEqual(np.measureIndex, 2)
        self.assertEqual(np.noteTime, 3)
        self.assertEqual(np.drumIndex, 4)

    def testOnlyNote(self):
        np = NotePosition(noteTime = 2, drumIndex = 3)
        self.assertEqual(np.staffIndex, None)
        self.assertEqual(np.measureIndex, None)
        self.assertEqual(np.noteTime, 2)
        self.assertEqual(np.drumIndex, 3)

    def testMeasureAndNote(self):
        np = NotePosition(measureIndex = 1, noteTime = 2, drumIndex = 3)
        self.assertEqual(np.staffIndex, None)
        self.assertEqual(np.measureIndex, 1)
        self.assertEqual(np.noteTime, 2)
        self.assertEqual(np.drumIndex, 3)

    def testStaffAndMeasure(self):
        np = NotePosition(1, 2)
        self.assertEqual(np.staffIndex, 1)
        self.assertEqual(np.measureIndex, 2)
        self.assertEqual(np.noteTime, None)
        self.assertEqual(np.drumIndex, None)

    def testOnlyMeasure(self):
        np = NotePosition(measureIndex = 1)
        self.assertEqual(np.staffIndex, None)
        self.assertEqual(np.measureIndex, 1)
        self.assertEqual(np.noteTime, None)
        self.assertEqual(np.drumIndex, None)

    def testStaffAndNote(self):
        np = NotePosition(staffIndex = 1, noteTime = 2, drumIndex = 3)
        self.assertEqual(np.staffIndex, 1)
        self.assertEqual(np.measureIndex, None)
        self.assertEqual(np.noteTime, 2)
        self.assertEqual(np.drumIndex, 3)

    def testOnlyStaff(self):
        np = NotePosition(1)
        self.assertEqual(np.staffIndex, 1)
        self.assertEqual(np.measureIndex, None)
        self.assertEqual(np.noteTime, None)
        self.assertEqual(np.drumIndex, None)

    def testWholeSong(self):
        np = NotePosition()
        self.assertEqual(np.staffIndex, None)
        self.assertEqual(np.measureIndex, None)
        self.assertEqual(np.noteTime, None)
        self.assertEqual(np.drumIndex, None)

    def testString(self):
        np = NotePosition(1, 2, 3, 4)
        self.assertEqual(str(np), "1, 2, 3, 4")





if __name__ == "__main__":
    unittest.main()
