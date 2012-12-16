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
Created on 12 Dec 2010

@author: Mike Thomas
'''
import unittest
from Data.Score import Score
from Data import DrumKit
from Data.DBErrors import BadTimeError, OverSizeMeasure
from Data.DBConstants import EMPTY_NOTE
from Data.NotePosition import NotePosition

# pylint: disable-msg=R0904

class TestMeasureControl(unittest.TestCase):
    def setUp(self):
        self.score = Score()

    def testEmptyScore(self):
        self.assertEqual(len(self.score), 0)
        self.assertEqual(self.score.numStaffs(), 0)
        self.assertEqual(self.score.numMeasures(), 0)
        self.assertEqual(len(self.score.drumKit), 0)

    def testAddMeasure(self):
        self.score.insertMeasureByIndex(16)
        self.assertEqual(len(self.score), 16)
        self.assertEqual(self.score.numStaffs(), 1)
        self.assertEqual(self.score.numMeasures(), 1)

    def testGetMeasure(self):
        for i in range(1, 17):
            self.score.insertMeasureByIndex(i)
        for i in range(1, 17):
            self.assertEqual(len(self.score.getMeasure(i - 1)), i)

    def testGetMeasure_BadIndex(self):
        self.assertRaises(BadTimeError, self.score.getMeasure, 0)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.assertRaises(BadTimeError, self.score.getMeasure, -1)
        self.assertRaises(BadTimeError, self.score.getMeasure, 3)

    def testDeleteMeasure(self):
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.deleteMeasureByIndex(1)
        self.assertEqual(len(self.score), 32)
        self.assertEqual(self.score.numStaffs(), 1)
        self.assertEqual(self.score.numMeasures(), 2)

    def testDeleteMeasure_EmptySystem(self):
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.deleteMeasureByIndex(1)
        self.assertEqual(self.score.numMeasures(), 2)
        self.score.deleteMeasureByIndex(1)
        self.assertEqual(self.score.numMeasures(), 1)
        self.score.deleteMeasureByIndex(0)
        self.assertEqual(len(self.score), 0)
        self.assertEqual(self.score.numStaffs(), 1)
        self.assertEqual(self.score.numMeasures(), 0)

    def testDeleteMeasure_BadIndex(self):
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.assertRaises(BadTimeError, self.score.deleteMeasureByIndex, -1)
        self.assertRaises(BadTimeError, self.score.deleteMeasureByIndex, 3)

    def testInsertMeasure(self):
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(8, 2)
        self.assertEqual(self.score.numMeasures(), 4)
        self.assertEqual(len(self.score), 56)
        self.assertEqual(len(self.score.getMeasure(2)), 8)
        self.score.insertMeasureByIndex(24, 4)
        self.assertEqual(self.score.numMeasures(), 5)
        self.assertEqual(len(self.score), 80)
        self.assertEqual(len(self.score.getMeasure(4)), 24)

    def testInsertMeasure_IntoEmptyScore(self):
        self.score.insertMeasureByIndex(16, 0)
        self.assertEqual(self.score.numMeasures(), 1)
        self.assertEqual(len(self.score), 16)
        self.assertEqual(len(self.score.getMeasure(0)), 16)

    def testInsertMeasure_BadIndex(self):
        self.assertRaises(BadTimeError, self.score.insertMeasureByIndex, 16, -1)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.assertRaises(BadTimeError, self.score.insertMeasureByIndex, 16, -1)
        self.assertRaises(BadTimeError, self.score.insertMeasureByIndex, 16, 4)

class TestNoteControl(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.drumKit = DrumKit.getNamedDefaultKit()
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(80)

    def testgetItemAtPosition(self):
        self.assertEqual(self.score.getItemAtPosition(NotePosition(0, 0, 0, 0)),
                         EMPTY_NOTE)

    def testgetItemAtPosition_BadTime(self):
        self.assertRaises(BadTimeError, self.score.getItemAtPosition,
                          NotePosition(-1, 0, 0, 0))
        self.assertRaises(BadTimeError, self.score.getItemAtPosition,
                          NotePosition(20, 0, 0, 0))
        self.assertRaises(BadTimeError, self.score.getItemAtPosition,
                          NotePosition(0, -1, 0, 0))
        self.assertRaises(BadTimeError, self.score.getItemAtPosition,
                          NotePosition(0, 20, 0, 0))
        self.assertRaises(BadTimeError, self.score.getItemAtPosition,
                          NotePosition(0, 0, -1, 0))
        self.assertRaises(BadTimeError, self.score.getItemAtPosition,
                          NotePosition(0, 0, 20, 0))

    def testgetItemAtPosition_BadNote(self):
        self.assertRaises(BadTimeError, self.score.getItemAtPosition,
                          NotePosition(0, 0, 0, -1))
        self.assertRaises(BadTimeError, self.score.getItemAtPosition,
                          NotePosition(0, 0, 0,
                                       len(self.score.drumKit)))

    def testAddNote(self):
        self.score.addNote(NotePosition(0, 0, 0, 0), "o")
        self.assertEqual(self.score.getItemAtPosition(NotePosition(0, 0, 0, 0)),
                         "o")

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
        self.assertEqual(self.score.getItemAtPosition(NotePosition(0, 0, 0, 0)),
                         defaultHead)

    def testDeleteNote(self):
        self.score.addNote(NotePosition(0, 0, 0, 0), "o")
        self.score.deleteNote(NotePosition(0, 0, 0, 0))
        self.assertEqual(self.score.getItemAtPosition(NotePosition(0, 0, 0, 0)),
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
        self.assertEqual(self.score.getItemAtPosition(NotePosition(0, 0, 0, 0)),
                         "o")
        self.score.toggleNote(NotePosition(0, 0, 0, 0), "o")
        self.assertEqual(self.score.getItemAtPosition(NotePosition(0, 0, 0, 0)),
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
        self.assertEqual(self.score.getItemAtPosition(NotePosition(0, 0, 0, 0)),
                         defaultHead)
        self.score.toggleNote(NotePosition(0, 0, 0, 0))
        self.assertEqual(self.score.getItemAtPosition(NotePosition(0, 0, 0, 0)),
                         EMPTY_NOTE)

class TestCharacterFormatScore(unittest.TestCase):
    def setUp(self):
        self.score = Score()

    def testgridFormatScore(self):
        for dummy in range(0, 20):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 5)
        for staff in self.score.iterStaffs():
            self.assertEqual(staff.numMeasures(), 4)
            self.assertEqual(len(staff), 64)
            self.assertEqual(staff.gridWidth(), 69)

    def testgridFormatScoreWithSections(self):
        for dummy in range(0, 20):
            self.score.insertMeasureByIndex(16)
        self.score.getMeasure(5).setSectionEnd(True)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 6)
        self.assertEqual(self.score.getStaff(1).gridWidth(), 35)

    def testgridFormatScore_SectionEndAtScoreEnd(self):
        for dummy in range(0, 20):
            self.score.insertMeasureByIndex(16)
        self.score.getMeasure(19).setSectionEnd(True)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 5)

    def testgridFormatScoreWithSectionsAndRepeat(self):
        for dummy in range(0, 20):
            self.score.insertMeasureByIndex(16)
        self.score.getMeasure(0).setRepeatStart(True)
        self.score.getMeasure(5).setSectionEnd(True)
        self.score.getMeasure(5).setRepeatEnd(True)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 6)
        self.assertEqual(self.score.getStaff(1).gridWidth(), 35)

    def testgridFormatScoreWithLargeBar(self):
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(70)
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 7)
        self.assertEqual(self.score.getStaff(3).gridWidth(), 72)

    def testgridFormatScoreWithOverSizeBar_IgnoreErrors(self):
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(80)
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(80, ignoreErrors = True)
        self.assertEqual(self.score.numStaffs(), 7)
        self.assertEqual(self.score.getStaff(3).gridWidth(), 82)

    def testgridFormatScoreWithOverSizeBar_DontIgnoreErrors(self):
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(90)
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.assertRaises(OverSizeMeasure, self.score.formatScore, 80,
                          ignoreErrors = False)

    def testgridFormatScore_FewerStaffsAfterDelete(self):
        for dummy in range(0, 9):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 3)
        self.score.deleteMeasureByIndex(6)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 2)

    def testgridFormatScore_FewerStaffsOnWiderFormat(self):
        for dummy in range(0, 8):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(40)
        self.assertEqual(self.score.numStaffs(), 4)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 2)

class TestIteration(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.drumKit = DrumKit.getNamedDefaultKit()
        for index in range(0, 26):
            self.score.insertMeasureByIndex(16)
            measure = self.score.getMeasure(index)
            measure.addNote(NotePosition(noteTime = 0, drumIndex = 0),
                            chr(ord("a") + index))
        self.score.formatScore(80)

    def testIterMeasures(self):
        mcount = 0
        for index, measure in enumerate(self.score.iterMeasures()):
            self.assertEqual(measure.noteAt(0, 0), chr(ord("a") + index))
            mcount += 1
        self.assertEqual(mcount, 26)

    def testIterMeasuresBetween(self):
        start = NotePosition(0, 3)
        end = NotePosition(3, 2)
        mcount = 0
        for measure, index, np in self.score.iterMeasuresBetween(start, end):
            self.assertEqual(measure.noteAt(0, 0), chr(ord("a") + index))
            self.assertEqual(measure, self.score.getItemAtPosition(np))
            mcount += 1
        self.assertEqual(mcount, 12)

    def testIterMeasuresBetweenReversed(self):
        start = NotePosition(0, 3)
        end = NotePosition(3, 2)
        mcount = 0
        for measure, index, np in self.score.iterMeasuresBetween(end, start):
            self.assertEqual(measure.noteAt(0, 0), chr(ord("a") + index))
            self.assertEqual(measure, self.score.getItemAtPosition(np))
            mcount += 1
        self.assertEqual(mcount, 12)

    def testIterSimpleRepeat(self):
        self.score.getMeasure(0).setRepeatStart(True)
        self.score.getMeasure(3).setRepeatEnd(True)
        self.score.getMeasure(3).repeatCount = 3
        measures = list(self.score.iterMeasuresWithRepeats())
        self.assertEqual([m[1] for m in measures[0:12]],
                         [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3])
        self.assertEqual([m[1] for m in measures[12:]],
                         range(4, 26))
        for measure, index in measures:
            self.assertEqual(measure, self.score.getMeasure(index))

    def testAlternates(self):
        self.score.getMeasure(0).setRepeatStart(True)
        self.score.getMeasure(1).setRepeatEnd(True)
        self.score.getMeasure(1).alternateText = "1,3-5."
        self.score.getMeasure(2).setRepeatEnd(True)
        self.score.getMeasure(2).alternateText = "2,6."
        self.score.getMeasure(3).setRepeatEnd(True)
        self.score.getMeasure(3).alternateText = "7."
        measures = list(self.score.iterMeasuresWithRepeats())
        self.assertEqual([m[1] for m in measures[0:14]],
                         [0, 1, 0, 2, 0, 1, 0, 1, 0, 1, 0, 2, 0, 3])
        self.assertEqual([m[1] for m in measures[14:]],
                         range(4, 26))
        for measure, index in measures:
            self.assertEqual(measure, self.score.getMeasure(index))

    def testAlternatesSectionEnd(self):
        self.score.getMeasure(0).setRepeatStart(True)
        self.score.getMeasure(1).setRepeatEnd(True)
        self.score.getMeasure(1).alternateText = "1,3-5."
        self.score.getMeasure(2).setRepeatEnd(True)
        self.score.getMeasure(2).alternateText = "2,6."
        self.score.getMeasure(3).setSectionEnd(True)
        self.score.getMeasure(3).alternateText = "7."
        measures = list(self.score.iterMeasuresWithRepeats())
        self.assertEqual([m[1] for m in measures[0:14]],
                         [0, 1, 0, 2, 0, 1, 0, 1, 0, 1, 0, 2, 0, 3])
        self.assertEqual([m[1] for m in measures[14:]],
                         range(4, 26))
        for measure, index in measures:
            self.assertEqual(measure, self.score.getMeasure(index))

class TestCallBack(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.drumKit = DrumKit.getNamedDefaultKit()
        for dummy in range(0, 16):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(80)
        self.calls = []
        def myCallBack(position):
            self.calls.append((position.staffIndex,
                               position.measureIndex,
                               position.noteTime,
                               position.drumIndex))
        self.score.setCallBack(myCallBack)

    def testAddNoteCallBack(self):
        notePos = NotePosition(1, 0, 0, 4)
        self.score.addNote(notePos, "x")
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0], (1, 0, 0, 4))
        self.score.addNote(notePos, "x")
        self.assertEqual(len(self.calls), 1)
        self.score.addNote(notePos, "o")
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[1], (1, 0, 0, 4))

    def testDeleteNoteCallBack(self):
        np = NotePosition(1, 0, 0, 4)
        self.score.deleteNote(np)
        self.assertEqual(len(self.calls), 0)
        self.score.addNote(np, "x")
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0], (1, 0, 0, 4))
        self.score.deleteNote(np)
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[1], (1, 0, 0, 4))

    def testToggleNoteCallBack(self):
        np = NotePosition(1, 0, 0, 0)
        self.score.toggleNote(np, "x")
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0], (1, 0, 0, 0))
        self.score.toggleNote(np, "x")
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[1], (1, 0, 0, 0))
        self.score.toggleNote(np, "x")
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(self.calls[2], (1, 0, 0, 0))
        self.score.toggleNote(np, "o")
        self.assertEqual(len(self.calls), 4)
        self.assertEqual(self.calls[2], (1, 0, 0, 0))

    def testClearCallBack(self):
        self.score.clearCallBack()
        self.score.addNote(NotePosition(staffIndex = 0,
                                        measureIndex = 0,
                                        noteTime = 0,
                                        drumIndex = 0), "x")
        self.assertEqual(len(self.calls), 0)

    def testTurnOnOff(self):
        np = NotePosition(1, 0, 0, 0)
        self.score.toggleNote(np, "x")
        self.assertEqual(len(self.calls), 1)
        self.score.turnOffCallBacks()
        np = NotePosition(1, 0, 0, 0)
        self.score.toggleNote(np, "x")
        self.assertEqual(len(self.calls), 1)
        self.score.turnOnCallBacks()
        np = NotePosition(1, 0, 0, 0)
        self.score.toggleNote(np, "x")
        self.assertEqual(len(self.calls), 2)

if __name__ == "__main__":
    unittest.main()
