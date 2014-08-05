# Copyright 2011 Michael Thomas
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
Created on 12 Dec 2010

@author: Mike Thomas
'''
import unittest
from Data.Measure import Measure
from Data.DBErrors import BadTimeError
from Data.DBConstants  import EMPTY_NOTE
from Data.NotePosition import NotePosition
#pylint: disable-msg=R0904

class TestMeasure(unittest.TestCase):
    def setUp(self):
        self.measure = Measure(16)

    def testEmptyMeasure(self):
        self.assertEqual(len(self.measure), 16)
        self.assertEqual(self.measure.numNotes(), 0)
        self.assertEqual(self.measure.getNote(NotePosition(noteTime = 0,
                                                           drumIndex = 0)),
                         EMPTY_NOTE)
        self.assertFalse(self.measure.isSectionEnd())
        self.assertFalse(self.measure.isRepeatEnd())
        self.assertFalse(self.measure.isRepeatStart())

    def testGetNote_BadTime(self):
        self.assertRaises(BadTimeError, self.measure.getNote,
                          NotePosition(noteTime = -1, drumIndex = 0))
        self.assertRaises(BadTimeError, self.measure.getNote,
                          NotePosition(noteTime = 20, drumIndex = 0))

    def testNumNotes(self):
        for i in range(0, 16):
            self.measure.addNote(NotePosition(noteTime = i, drumIndex = 0), "o")
        self.assertEqual(self.measure.numNotes(), 16)

    def testAddNote(self):
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "o")
        notePos = NotePosition(noteTime = 0, drumIndex = 0)
        self.assertEqual(self.measure.getNote(notePos), "o")

    def testAddNote_BadTime(self):
        self.assertRaises(BadTimeError, self.measure.addNote,
                          NotePosition(noteTime = -1, drumIndex = 0), "x")
        self.assertRaises(BadTimeError, self.measure.addNote,
                          NotePosition(noteTime = 20, drumIndex = 0), "x")

    def testIterNotes(self):
        for i in range(0, 4):
            self.measure.addNote(NotePosition(noteTime = 4 * i,
                                              drumIndex = i), str(i))
        for i, (np, head) in enumerate(self.measure):
            self.assertEqual(head, str(i))
            self.assertEqual(np.noteTime, 4 * i)
            self.assertEqual(np.drumIndex, i)


    def testDeleteNote(self):
        np = NotePosition(noteTime = 0, drumIndex = 0)
        self.measure.addNote(np, "o")
        self.measure.deleteNote(np)
        self.assertEqual(self.measure.numNotes(), 0)
        self.assertEqual(self.measure.getNote(np), EMPTY_NOTE)

    def testDeleteNote_BadTime(self):
        self.assertRaises(BadTimeError, self.measure.deleteNote,
                          NotePosition(noteTime = -1, drumIndex = 0))
        self.assertRaises(BadTimeError, self.measure.deleteNote,
                          NotePosition(noteTime = 20, drumIndex = 0))

    def testToggleNote(self):
        np = NotePosition(noteTime = 0, drumIndex = 0)
        self.measure.toggleNote(np, "o")
        self.assertEqual(self.measure.getNote(np), "o")
        self.assertEqual(self.measure.numNotes(), 1)
        self.measure.toggleNote(np, "o")
        self.assertEqual(self.measure.numNotes(), 0)
        self.assertEqual(self.measure.getNote(np), EMPTY_NOTE)

    def testToggleNote_ChangeNote(self):
        np = NotePosition(noteTime = 0, drumIndex = 0)
        self.measure.toggleNote(np, "o")
        self.measure.toggleNote(np, "x")
        self.assertEqual(self.measure.getNote(np), "x")

    def testToggleNote_BadTime(self):
        self.assertRaises(BadTimeError, self.measure.toggleNote,
                          NotePosition(noteTime = -1, drumIndex = 0), "x")
        self.assertRaises(BadTimeError, self.measure.toggleNote,
                          NotePosition(noteTime = 20, drumIndex = 0), "x")

    def testSetWidth_BadWidth(self):
        self.assertRaises(AssertionError, self.measure.setWidth, -1)

    def testSetWidth_MakeEmptyMeasureBigger(self):
        self.measure.setWidth(32)
        self.assertEqual(len(self.measure), 32)

    def testSetWidth_MakeEmptyMeasureSmaller(self):
        self.measure.setWidth(8)
        self.assertEqual(len(self.measure), 8)

    def testSetWidth_MakeNonEmptyMeasureBigger(self):
        self.measure.addNote(NotePosition(noteTime = 7, drumIndex = 1), "x")
        self.measure.setWidth(32)
        self.assertEqual(len(self.measure), 32)
        notePos = NotePosition(noteTime = 7, drumIndex = 1)
        self.assertEqual(self.measure.getNote(notePos), "x")

    def testSetWidth_MakeNonEmptyMeasureSmaller(self):
        self.measure.addNote(NotePosition(noteTime = 7, drumIndex = 1), "x")
        self.measure.addNote(NotePosition(noteTime = 12, drumIndex = 1), "x")
        self.measure.setWidth(8)
        self.assertEqual(len(self.measure), 8)
        notePos = NotePosition(noteTime = 7, drumIndex = 1)
        self.assertEqual(self.measure.getNote(notePos), "x")
        self.assertEqual(self.measure.numNotes(), 1)

    def testSetWidth_NoEffect(self):
        notePos1 = NotePosition(noteTime = 7, drumIndex = 1)
        notePos2 = NotePosition(noteTime = 12, drumIndex = 1)
        self.measure.addNote(notePos1, "x")
        self.measure.addNote(notePos2, "x")
        self.measure.setWidth(16)
        self.assertEqual(len(self.measure), 16)
        self.assertEqual(self.measure.getNote(notePos1), "x")
        self.assertEqual(self.measure.getNote(notePos2), "x")
        self.assertEqual(self.measure.numNotes(), 2)

    def testSetSectionEnd_NoRepeat(self):
        self.assertFalse(self.measure.isSectionEnd())
        self.measure.setSectionEnd(True)
        self.assert_(self.measure.isSectionEnd())
        self.measure.setSectionEnd(False)
        self.assertFalse(self.measure.isSectionEnd())

    def testSetSectionEnd_Repeat(self):
        self.measure.setRepeatEnd(True)
        self.assertFalse(self.measure.isSectionEnd())
        self.measure.setSectionEnd(True)
        self.assert_(self.measure.isSectionEnd())
        self.assert_(self.measure.isRepeatEnd())
        self.measure.setSectionEnd(False)
        self.assertFalse(self.measure.isSectionEnd())
        self.assert_(self.measure.isRepeatEnd())
        self.measure.setRepeatEnd(False)
        self.assertFalse(self.measure.isSectionEnd())
        self.assertFalse(self.measure.isRepeatEnd())

    def testSetRepeatStart(self):
        self.measure.setRepeatStart(True)
        self.assert_(self.measure.isRepeatStart())
        self.measure.setRepeatStart(False)
        self.assertFalse(self.measure.isRepeatStart())

    def testSetRepeatEnd_NotSectionEnd(self):
        self.measure.setRepeatEnd(True)
        self.assert_(self.measure.isRepeatEnd())
        self.measure.setRepeatEnd(False)
        self.assertFalse(self.measure.isRepeatEnd())

    def testSetRepeatEnd_IsSectionEnd(self):
        self.measure.setSectionEnd(True)
        self.measure.setRepeatEnd(True)
        self.assert_(self.measure.isRepeatEnd())
        self.measure.setRepeatEnd(False)
        self.assertFalse(self.measure.isRepeatEnd())

class TestCallBack(unittest.TestCase):
    def setUp(self):
        self.measure = Measure(16)
        self.calls = []
        def myCallBack(position):
            self.calls.append((position.noteTime, position.drumIndex))
        self.measure.setCallBack(myCallBack)

    def testAddNoteCallBack(self):
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "x")
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0], (0, 0))
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "x")
        self.assertEqual(len(self.calls), 1)
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "o")
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[1], (0, 0))

    def testDeleteNoteCallBack(self):
        self.measure.deleteNote(NotePosition(noteTime = 0, drumIndex = 0))
        self.assertEqual(len(self.calls), 0)
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "x")
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0], (0, 0))
        self.measure.deleteNote(NotePosition(noteTime = 0, drumIndex = 0))
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[1], (0, 0))

    def testToggleNoteCallBack(self):
        np = NotePosition(noteTime = 0, drumIndex = 0)
        self.measure.toggleNote(np, "x")
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0], (0, 0))
        self.measure.toggleNote(np, "x")
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[1], (0, 0))
        self.measure.toggleNote(np, "x")
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(self.calls[2], (0, 0))
        self.measure.toggleNote(np, "o")
        self.assertEqual(len(self.calls), 4)
        self.assertEqual(self.calls[2], (0, 0))

    def testClearCallBack(self):
        self.measure.clearCallBack()
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "x")
        self.assertEqual(len(self.calls), 0)

if __name__ == "__main__":
    unittest.main()
