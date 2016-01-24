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
from Data import DrumKit, Drum, DrumKitFactory
from Data.DBErrors import BadTimeError, OverSizeMeasure, InconsistentRepeats
from Data.DBConstants import EMPTY_NOTE
from Data.NotePosition import NotePosition

# pylint:disable=too-many-lines

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
            self.assertEqual(len(self.score.getMeasureByIndex(i - 1)), i)

    def testGetMeasure_BadIndex(self):
        self.assertRaises(BadTimeError, self.score.getMeasureByIndex, 0)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.assertRaises(BadTimeError, self.score.getMeasureByIndex, -1)
        self.assertRaises(BadTimeError, self.score.getMeasureByIndex, 3)

    def testDeleteMeasureByIndex(self):
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.deleteMeasureByIndex(1)
        self.assertEqual(len(self.score), 32)
        self.assertEqual(self.score.numStaffs(), 1)
        self.assertEqual(self.score.numMeasures(), 2)

    def testDeleteMeasureByIndex_EmptySystem(self):
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

    def testDeleteMeasureByIndex_BadIndex(self):
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.assertRaises(BadTimeError, self.score.deleteMeasureByIndex, -1)
        self.assertRaises(BadTimeError, self.score.deleteMeasureByIndex, 3)

    def testDeleteMeasureByPosition(self):
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.deleteMeasureByPosition(NotePosition(0, 1))
        self.assertEqual(len(self.score), 32)
        self.assertEqual(self.score.numStaffs(), 1)
        self.assertEqual(self.score.numMeasures(), 2)

    def testDeleteMeasureByPosition_EmptySystem(self):
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.deleteMeasureByPosition(NotePosition(0, 1))
        self.assertEqual(self.score.numMeasures(), 2)
        self.score.deleteMeasureByPosition(NotePosition(0, 1))
        self.assertEqual(self.score.numMeasures(), 1)
        self.score.deleteMeasureByPosition(NotePosition(0, 0))
        self.assertEqual(len(self.score), 0)
        self.assertEqual(self.score.numStaffs(), 1)
        self.assertEqual(self.score.numMeasures(), 0)

    def testDeleteMeasureByPosition_BadPosition(self):
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.assertRaises(BadTimeError, self.score.deleteMeasureByPosition,
                          NotePosition(0, 3))
        self.assertRaises(BadTimeError, self.score.deleteMeasureByPosition,
                          NotePosition(1, 1))

    def testDeleteMeasuresAtPosition_SingleStaff(self):
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.assertEqual(self.score.numMeasures(), 6)
        self.assertEqual(self.score.numStaffs(), 1)
        self.score.deleteMeasuresAtPosition(NotePosition(0, 1), 3)
        self.assertEqual(self.score.numMeasures(), 3)
        self.assertEqual(self.score.numStaffs(), 1)

    def testDeleteMeasuresAtPosition_MultipleStaffs(self):
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.formatScore(60)
        self.assertEqual(self.score.numMeasures(), 6)
        self.assertEqual(self.score.numStaffs(), 2)
        self.score.deleteMeasuresAtPosition(NotePosition(0, 1), 3)
        self.assertEqual(self.score.numMeasures(), 3)
        self.assertEqual(self.score.numStaffs(), 2)

    def testDeleteMeasuresAtPosition_MultipleStaffs_EmptyStaff(self):
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.formatScore(60)
        self.assertEqual(self.score.numMeasures(), 6)
        self.assertEqual(self.score.numStaffs(), 2)
        self.score.deleteMeasuresAtPosition(NotePosition(0, 0), 4)
        self.assertEqual(self.score.numMeasures(), 2)
        self.assertEqual(self.score.numStaffs(), 1)

    def testInsertMeasure(self):
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(8, 2)
        self.assertEqual(self.score.numMeasures(), 4)
        self.assertEqual(len(self.score), 56)
        self.assertEqual(len(self.score.getMeasureByIndex(2)), 8)
        self.score.insertMeasureByIndex(24, 4)
        self.assertEqual(self.score.numMeasures(), 5)
        self.assertEqual(len(self.score), 80)
        self.assertEqual(len(self.score.getMeasureByIndex(4)), 24)

    def testInsertMeasure_IntoEmptyScore(self):
        self.score.insertMeasureByIndex(16, 0)
        self.assertEqual(self.score.numMeasures(), 1)
        self.assertEqual(len(self.score), 16)
        self.assertEqual(len(self.score.getMeasureByIndex(0)), 16)

    def testInsertMeasure_BadIndex(self):
        self.assertRaises(BadTimeError, self.score.insertMeasureByIndex, 16, -1)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(16)
        self.assertRaises(BadTimeError, self.score.insertMeasureByIndex, 16, -1)
        self.assertRaises(BadTimeError, self.score.insertMeasureByIndex, 16, 4)

    def testInsertMeasureByPosition(self):
        self.score.insertMeasureByPosition(16)
        self.score.insertMeasureByPosition(16)
        self.score.insertMeasureByPosition(16)
        self.score.insertMeasureByPosition(8, NotePosition(0, 2))
        self.assertEqual(self.score.numMeasures(), 4)
        self.assertEqual(len(self.score), 56)
        self.assertEqual(len(self.score.getMeasureByIndex(2)), 8)
        self.score.insertMeasureByPosition(24, NotePosition(0, 4))
        self.assertEqual(self.score.numMeasures(), 5)
        self.assertEqual(len(self.score), 80)
        self.assertEqual(len(self.score.getMeasureByIndex(4)), 24)

    def testInsertMeasureByPosition_IntoEmptyScore(self):
        self.score.insertMeasureByPosition(16)
        self.assertEqual(self.score.numMeasures(), 1)
        self.assertEqual(len(self.score), 16)
        self.assertEqual(len(self.score.getMeasureByIndex(0)), 16)

    def testInsertMeasureByPosition_BadIndex(self):
        self.assertRaises(BadTimeError, self.score.insertMeasureByPosition, 16,
                          NotePosition(0, -1))
        self.score.insertMeasureByPosition(16)
        self.score.insertMeasureByPosition(16)
        self.score.insertMeasureByPosition(16)
        self.assertRaises(BadTimeError, self.score.insertMeasureByPosition,
                          16, NotePosition(1, 0))
        self.assertRaises(BadTimeError, self.score.insertMeasureByPosition,
                          16, NotePosition(0, 4))

class TestNoteControl(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.drumKit = DrumKitFactory.DrumKitFactory.getNamedDefaultKit()
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(80)

    def testgetItemAtPosition(self):
        self.assertEqual(self.score.getItemAtPosition(NotePosition(0, 0, 0, 0)),
                         EMPTY_NOTE)
        self.assertEqual(self.score.getItemAtPosition(NotePosition(0, 0)),
                         self.score.getMeasureByIndex(0))
        self.assertEqual(self.score.getItemAtPosition(NotePosition(0)),
                         self.score.getStaff(0))
        self.assertEqual(self.score.getItemAtPosition(NotePosition()),
                         self.score)

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

class TestFormatScore(unittest.TestCase):
    def setUp(self):
        self.score = Score()

    def testFormatScoreDefaultWidth(self):
        for dummy in range(0, 20):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore()
        self.assertEqual(self.score.numStaffs(), 5)
        for staff in self.score.iterStaffs():
            self.assertEqual(staff.numMeasures(), 4)
            self.assertEqual(len(staff), 64)

    def testFormatScore(self):
        for dummy in range(0, 20):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 5)
        for staff in self.score.iterStaffs():
            self.assertEqual(staff.numMeasures(), 4)
            self.assertEqual(len(staff), 64)

    def testFormatScoreWithSections(self):
        for dummy in range(0, 20):
            self.score.insertMeasureByIndex(16)
        self.score.getMeasureByIndex(5).setSectionEnd(True)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 6)

    def testFormatScore_SectionEndAtScoreEnd(self):
        for dummy in range(0, 20):
            self.score.insertMeasureByIndex(16)
        self.score.getMeasureByIndex(19).setSectionEnd(True)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 5)

    def testFormatScoreWithSectionsAndRepeat(self):
        for dummy in range(0, 20):
            self.score.insertMeasureByIndex(16)
        self.score.getMeasureByIndex(0).setRepeatStart(True)
        self.score.getMeasureByIndex(5).setSectionEnd(True)
        self.score.getMeasureByIndex(5).setRepeatEnd(True)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 6)

    def testFormatScoreWithLargeBar(self):
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(70)
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 7)

    def testFormatScoreWithOverSizeBar_IgnoreErrors(self):
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(80)
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(80, ignoreErrors = True)
        self.assertEqual(self.score.numStaffs(), 7)

    def testFormatScoreWithOverSizeBar_DontIgnoreErrors(self):
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.score.insertMeasureByIndex(90)
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.assertRaises(OverSizeMeasure, self.score.formatScore, 80,
                          ignoreErrors = False)

    def testFormatScore_FewerStaffsAfterDelete(self):
        for dummy in range(0, 9):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 3)
        self.score.deleteMeasureByIndex(6)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 2)

    def testFormatScore_FewerStaffsOnWiderFormat(self):
        for dummy in range(0, 8):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(40)
        self.assertEqual(self.score.numStaffs(), 4)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 2)

    def testMeasureIndexToPosition(self):
        for dummy in range(0, 8):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(40)
        self.assertEqual(self.score.measureIndexToPosition(0),
                         NotePosition(0, 0))
        self.assertEqual(self.score.measureIndexToPosition(1),
                         NotePosition(0, 1))
        self.assertEqual(self.score.measureIndexToPosition(2),
                         NotePosition(1, 0))
        self.assertEqual(self.score.measureIndexToPosition(3),
                         NotePosition(1, 1))
        self.assertEqual(self.score.measureIndexToPosition(4),
                         NotePosition(2, 0))
        self.assertEqual(self.score.measureIndexToPosition(5),
                         NotePosition(2, 1))
        self.assertEqual(self.score.measureIndexToPosition(6),
                         NotePosition(3, 0))
        self.assertEqual(self.score.measureIndexToPosition(7),
                         NotePosition(3, 1))
        self.assertRaises(BadTimeError, self.score.measureIndexToPosition, 8)

    def testMeasurePositionToIndex(self):
        for dummy in range(0, 8):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(40)
        self.assertEqual(self.score.measurePositionToIndex(NotePosition(0, 0)), 0)
        self.assertEqual(self.score.measurePositionToIndex(NotePosition(0, 1)), 1)
        self.assertEqual(self.score.measurePositionToIndex(NotePosition(1, 0)), 2)
        self.assertEqual(self.score.measurePositionToIndex(NotePosition(1, 1)), 3)
        self.assertEqual(self.score.measurePositionToIndex(NotePosition(2, 0)), 4)
        self.assertEqual(self.score.measurePositionToIndex(NotePosition(2, 1)), 5)
        self.assertEqual(self.score.measurePositionToIndex(NotePosition(3, 0)), 6)
        self.assertEqual(self.score.measurePositionToIndex(NotePosition(3, 1)), 7)
        self.assertRaises(BadTimeError,
                          self.score.measurePositionToIndex, NotePosition(4, 4))

    def testTrailingMeasures(self):
        self.score.drumKit = DrumKitFactory.DrumKitFactory.getNamedDefaultKit()
        for dummy in range(0, 8):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(40)
        self.score.addNote(NotePosition(0, 1, 0, 0), "x")
        trailing = self.score.trailingEmptyMeasures()
        self.assertEqual(trailing,
                         [self.score.measureIndexToPosition(i)
                          for i in xrange(7, 1, -1)])

    def testTrailingMeasuresEmptyScore(self):
        for dummy in range(0, 8):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(40)
        trailing = self.score.trailingEmptyMeasures()
        self.assertEqual(trailing,
                         [self.score.measureIndexToPosition(i)
                          for i in xrange(7, 0, -1)])

class TestCopyPaste(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.kit = DrumKitFactory.DrumKitFactory.getNamedDefaultKit()
        for width in range(0, 8):
            self.score.insertMeasureByIndex(width + 8)
        self.score.formatScore(40)

    def testCopyPasteByPosition(self):
        copied = self.score.copyMeasure(NotePosition(0, 0))
        self.score.pasteMeasure(NotePosition(0, 2), copied)
        self.assertEqual(len(self.score.getItemAtPosition(NotePosition(0, 2))), 8)

    def testCopyPasteByIndex(self):
        copied = self.score.copyMeasure(NotePosition(0, 0))
        self.score.pasteMeasureByIndex(2, copied)
        self.assertEqual(len(self.score.getItemAtPosition(NotePosition(0, 2))), 8)


class TestIteration(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.drumKit = DrumKitFactory.DrumKitFactory.getNamedDefaultKit()
        for index in range(0, 26):
            self.score.insertMeasureByIndex(16)
            measure = self.score.getMeasureByIndex(index)
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
        self.score.getMeasureByIndex(0).setRepeatStart(True)
        self.score.getMeasureByIndex(3).setRepeatEnd(True)
        self.score.getMeasureByIndex(3).repeatCount = 3
        measures = list(self.score.iterMeasuresWithRepeats())
        self.assertEqual([m[1] for m in measures[0:12]],
                         [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3])
        self.assertEqual([m[1] for m in measures[12:]],
                         range(4, 26))
        for measure, index in measures:
            self.assertEqual(measure, self.score.getMeasureByIndex(index))

    def testAlternates(self):
        self.score.getMeasureByIndex(0).setRepeatStart(True)
        self.score.getMeasureByIndex(1).setRepeatEnd(True)
        self.score.getMeasureByIndex(1).alternateText = "1,3-5."
        self.score.getMeasureByIndex(2).setRepeatEnd(True)
        self.score.getMeasureByIndex(2).alternateText = "2,6."
        self.score.getMeasureByIndex(3).setRepeatEnd(True)
        self.score.getMeasureByIndex(3).alternateText = "7."
        measures = list(self.score.iterMeasuresWithRepeats())
        self.assertEqual([m[1] for m in measures[0:14]],
                         [0, 1, 0, 2, 0, 1, 0, 1, 0, 1, 0, 2, 0, 3])
        self.assertEqual([m[1] for m in measures[14:]],
                         range(4, 26))
        for measure, index in measures:
            self.assertEqual(measure, self.score.getMeasureByIndex(index))

    def testAlternatesSectionEnd(self):
        self.score.getMeasureByIndex(0).setRepeatStart(True)
        self.score.getMeasureByIndex(1).setRepeatEnd(True)
        self.score.getMeasureByIndex(1).alternateText = "1,3-5."
        self.score.getMeasureByIndex(2).setRepeatEnd(True)
        self.score.getMeasureByIndex(2).alternateText = "2,6."
        self.score.getMeasureByIndex(3).setSectionEnd(True)
        self.score.getMeasureByIndex(3).alternateText = "7."
        measures = list(self.score.iterMeasuresWithRepeats())
        self.assertEqual([m[1] for m in measures[0:14]],
                         [0, 1, 0, 2, 0, 1, 0, 1, 0, 1, 0, 2, 0, 3])
        self.assertEqual([m[1] for m in measures[14:]],
                         range(4, 26))
        for measure, index in measures:
            self.assertEqual(measure, self.score.getMeasureByIndex(index))

    def testAlternatesNoEnd(self):
        self.score.getMeasureByIndex(0).setRepeatStart(True)
        self.score.getMeasureByIndex(1).setRepeatEnd(True)
        self.score.getMeasureByIndex(1).alternateText = "1,3-5."
        self.score.getMeasureByIndex(2).setRepeatEnd(True)
        self.score.getMeasureByIndex(2).alternateText = "2,6."
        self.score.getMeasureByIndex(3).alternateText = "7."
        measures = list(self.score.iterMeasuresWithRepeats())
        self.assertEqual([m[1] for m in measures[0:14]],
                         [0, 1, 0, 2, 0, 1, 0, 1, 0, 1, 0, 2, 0, 3])
        self.assertEqual([m[1] for m in measures[14:]],
                         range(4, 26))
        for measure, index in measures:
            self.assertEqual(measure, self.score.getMeasureByIndex(index))

    def testInconsistentAlternates(self):
        self.score.getMeasureByIndex(0).setRepeatStart(True)
        self.score.getMeasureByIndex(1).setRepeatEnd(True)
        self.score.getMeasureByIndex(1).alternateText = "1,3-5."
        self.score.getMeasureByIndex(2).setRepeatEnd(True)
        self.score.getMeasureByIndex(2).alternateText = "2,6."
        self.score.getMeasureByIndex(3).setRepeatEnd(True)
        self.score.getMeasureByIndex(3).alternateText = "12."
        self.assertRaises(InconsistentRepeats, list,
                          self.score.iterMeasuresWithRepeats())


class TestSections(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.drumKit = DrumKitFactory.DrumKitFactory.getNamedDefaultKit()
        for index in range(0, 26):
            self.score.insertMeasureByIndex(16)
            measure = self.score.getMeasureByIndex(index)
            measure.addNote(NotePosition(noteTime = 0, drumIndex = 0),
                            chr(ord("a") + index))
        self.score.formatScore(80)

    def testNoSections(self):
        self.assertEqual(self.score.numSections(), 0)

    def testAddSection(self):
        np = self.score.measureIndexToPosition(3)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 1)
        self.assertEqual(self.score.getSectionTitle(0), "New Section")

    def testSetSectionTitle(self):
        np = self.score.measureIndexToPosition(3)
        self.score.setSectionEnd(np, True)
        self.score.setSectionTitle(0, "Section 1")
        np = self.score.measureIndexToPosition(15)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 2)
        self.score.setSectionTitle(1, "Section 2")
        self.assertEqual(self.score.getSectionTitle(0), "Section 1")
        self.assertEqual(self.score.getSectionTitle(1), "Section 2")
        self.assertEqual(list(self.score.iterSections()),
                         ["Section 1", "Section 2"])

    def testRemoveSection(self):
        np = self.score.measureIndexToPosition(3)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 1)
        self.score.setSectionTitle(0, "Section 1")
        np = self.score.measureIndexToPosition(15)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 2)
        self.score.setSectionTitle(1, "Section 2")
        np = self.score.measureIndexToPosition(3)
        self.score.setSectionEnd(np, False)
        self.assertEqual(self.score.numSections(), 1)
        self.assertEqual(self.score.getSectionTitle(0), "Section 2")

    def testGetSectionIndex(self):
        np = self.score.measureIndexToPosition(3)
        self.score.setSectionEnd(np, True)
        np = self.score.measureIndexToPosition(19)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 2)
        np = self.score.measureIndexToPosition(2)
        self.assertEqual(self.score.getSectionIndex(np), 0)
        np = self.score.measureIndexToPosition(10)
        self.assertEqual(self.score.getSectionIndex(np), 1)

    def testGetSectionStartStaffIndex(self):
        np = self.score.measureIndexToPosition(3)
        self.score.setSectionEnd(np, True)
        np = self.score.measureIndexToPosition(19)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 2)
        np = self.score.measureIndexToPosition(2)
        self.assertEqual(self.score.getSectionStartStaffIndex(np), 0)
        np = self.score.measureIndexToPosition(10)
        self.assertEqual(self.score.getSectionStartStaffIndex(np), 1)

    def testIterMeasuresInSection(self):
        np = self.score.measureIndexToPosition(3)
        self.score.setSectionEnd(np, True)
        np = self.score.measureIndexToPosition(19)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 2)
        measureIndexes = [ord(measure.noteAt(0, 0)) - ord('a') for measure
                          in self.score.iterMeasuresInSection(0)]
        self.assertEqual(measureIndexes, [0, 1, 2, 3])
        measureIndexes = [ord(measure.noteAt(0, 0)) - ord('a') for measure
                          in self.score.iterMeasuresInSection(1)]
        self.assertEqual(measureIndexes, range(4, 20))
        self.assertRaises(BadTimeError, list,
                          self.score.iterMeasuresInSection(3))

    def testDeleteSection_FirstSection(self):
        np = self.score.measureIndexToPosition(3)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 1)
        self.score.setSectionTitle(0, "Section 1")
        np = self.score.measureIndexToPosition(15)
        self.score.setSectionEnd(np, True)
        self.score.setSectionTitle(1, "Section 2")
        self.assertEqual(self.score.numSections(), 2)
        self.score.deleteSection(NotePosition(0, 1))
        self.assertEqual(self.score.numSections(), 1)
        self.assertEqual(self.score.numStaffs(), 6)
        self.assertEqual(self.score.numMeasures(), 22)
        self.assertEqual(self.score.getSectionTitle(0), "Section 2")

    def testDeleteSection_MiddleSection(self):
        np = self.score.measureIndexToPosition(3)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 1)
        self.score.setSectionTitle(0, "Section 1")
        np = self.score.measureIndexToPosition(15)
        self.score.setSectionEnd(np, True)
        self.score.setSectionTitle(1, "Section 2")
        np = self.score.measureIndexToPosition(23)
        self.score.setSectionEnd(np, True)
        self.score.setSectionTitle(2, "Section 3")
        self.assertEqual(self.score.numSections(), 3)
        self.score.deleteSection(NotePosition(2, 2))
        self.assertEqual(self.score.numSections(), 2)
        self.assertEqual(self.score.numStaffs(), 4)
        self.assertEqual(self.score.numMeasures(), 14)
        self.assertEqual(self.score.getSectionTitle(0), "Section 1")
        self.assertEqual(self.score.getSectionTitle(1), "Section 3")

    def testDeleteSection_EndSection(self):
        np = self.score.measureIndexToPosition(3)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 1)
        self.score.setSectionTitle(0, "Section 1")
        np = self.score.measureIndexToPosition(15)
        self.score.setSectionEnd(np, True)
        self.score.setSectionTitle(1, "Section 2")
        np = self.score.measureIndexToPosition(23)
        self.score.setSectionEnd(np, True)
        self.score.setSectionTitle(2, "Section 3")
        self.assertEqual(self.score.numSections(), 3)
        self.score.deleteSection(NotePosition(5, 0))
        self.assertEqual(self.score.numSections(), 2)
        self.assertEqual(self.score.numStaffs(), 5)
        self.assertEqual(self.score.numMeasures(), 18)
        self.assertEqual(self.score.getSectionTitle(0), "Section 1")
        self.assertEqual(self.score.getSectionTitle(1), "Section 2")

    def testDeleteSection_BadPosition(self):
        np = self.score.measureIndexToPosition(3)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 1)
        self.score.setSectionTitle(0, "Section 1")
        np = self.score.measureIndexToPosition(15)
        self.score.setSectionEnd(np, True)
        self.score.setSectionTitle(1, "Section 2")
        np = self.score.measureIndexToPosition(23)
        self.score.setSectionEnd(np, True)
        self.score.setSectionTitle(2, "Section 3")
        self.assertEqual(self.score.numSections(), 3)
        self.score.deleteSection(NotePosition(6, 0))
        self.assertEqual(self.score.numSections(), 3)

class TestRelativePositions(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.drumKit = DrumKitFactory.DrumKitFactory.getNamedDefaultKit()
        for index in range(0, 26):
            self.score.insertMeasureByIndex(16)
            measure = self.score.getMeasureByIndex(index)
            measure.addNote(NotePosition(noteTime = 0, drumIndex = 0),
                            chr(ord("a") + index))
        self.score.formatScore(80)

    def testNotePlus(self):
        # Within measure
        nextNote = self.score.notePlus(NotePosition(0, 0, 0, 0), 1)
        self.assertEqual(nextNote, NotePosition(0, 0, 1, 0))
        nextNote = self.score.notePlus(NotePosition(0, 0, 3, 0), 8)
        self.assertEqual(nextNote, NotePosition(0, 0, 11, 0))
        # Next measure
        nextNote = self.score.notePlus(NotePosition(0, 0, 0, 0), 20)
        self.assertEqual(nextNote, NotePosition(0, 1, 4, 0))
        # Across multiple measures
        nextNote = self.score.notePlus(NotePosition(0, 0, 0, 0), 40)
        self.assertEqual(nextNote, NotePosition(0, 2, 8, 0))
        # Across staffs
        nextNote = self.score.notePlus(NotePosition(0, 0, 0, 0), 250)
        self.assertEqual(nextNote, NotePosition(3, 3, 10, 0))
        # Too far
        nextNote = self.score.notePlus(NotePosition(0, 0, 0, 0), 10000)
        self.assertEqual(nextNote, None)

    def testTickDifference(self):
        # Within measure
        np1 = NotePosition(0, 0, 0, 0)
        np2 = NotePosition(0, 0, 8, 2)
        self.assertEqual(self.score.tickDifference(np2, np1), 8)
        self.assertEqual(self.score.tickDifference(np1, np2), -8)
        # Next measure
        np1 = NotePosition(0, 0, 0, 0)
        np2 = NotePosition(0, 1, 8, 2)
        self.assertEqual(self.score.tickDifference(np2, np1), 24)
        self.assertEqual(self.score.tickDifference(np1, np2), -24)
        # Across multiple measures
        np1 = NotePosition(0, 0, 0, 0)
        np2 = NotePosition(0, 2, 8, 2)
        self.assertEqual(self.score.tickDifference(np2, np1), 40)
        self.assertEqual(self.score.tickDifference(np1, np2), -40)
        # Across staffs
        np1 = NotePosition(0, 0, 0, 0)
        np2 = NotePosition(3, 2, 8, 2)
        self.assertEqual(self.score.tickDifference(np2, np1), 232)
        self.assertEqual(self.score.tickDifference(np1, np2), -232)

    def testNextMeasure(self):
        # Within staff
        nextPos = self.score.nextMeasure(NotePosition(0, 0))
        self.assertEqual(nextPos, NotePosition(0, 1))
        # Next staff
        nextPos = self.score.nextMeasure(NotePosition(0, 3))
        self.assertEqual(nextPos, NotePosition(1, 0))
        # At end of score
        nextPos = self.score.nextMeasure(NotePosition(6, 1))
        self.assertEqual(nextPos, NotePosition())
        # Bad input
        self.assertRaises(BadTimeError, self.score.nextMeasure,
                          NotePosition(6, 2))
        self.assertRaises(BadTimeError, self.score.nextMeasure,
                          NotePosition(8, 3))

class TestVisibleLines(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        kit = DrumKit.DrumKit()
        kit.addDrum(Drum.Drum("d1", "d1", "x", True))
        kit.addDrum(Drum.Drum("d2", "d2", "x", False))
        kit.addDrum(Drum.Drum("d3", "d3", "x", False))
        kit.addDrum(Drum.Drum("d4", "d4", "x", True))
        kit.addDrum(Drum.Drum("d5", "d5", "x", False))
        self.score.drumKit = kit
        self.score.scoreData.emptyLinesVisible = False
        for unused in range(0, 16):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(80)
        self.score.addNote(NotePosition(1, 0, 0, 0), "x")
        self.score.addNote(NotePosition(2, 0, 0, 1), "x")
        self.score.addNote(NotePosition(3, 0, 0, 0), "x")
        self.score.addNote(NotePosition(3, 0, 0, 1), "x")
        self.score.addNote(NotePosition(3, 0, 0, 2), "x")
        self.score.addNote(NotePosition(3, 0, 0, 3), "x")
        self.score.addNote(NotePosition(3, 0, 0, 4), "x")

    def testNoLockedOrVisible(self):
        self.score = Score()
        kit = DrumKit.DrumKit()
        kit.addDrum(Drum.Drum("d1", "d1", "x", False))
        kit.addDrum(Drum.Drum("d2", "d2", "x", False))
        kit.addDrum(Drum.Drum("d3", "d3", "x", False))
        kit.addDrum(Drum.Drum("d4", "d4", "x", False))
        kit.addDrum(Drum.Drum("d5", "d5", "x", False))
        self.score.drumKit = kit
        self.score.scoreData.emptyLinesVisible = False
        for unused in range(0, 16):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(80)
        self.assertEqual(self.score.numVisibleLines(0), 1)
        self.assertEqual(self.score.nthVisibleLineIndex(0, 0), 0)
        self.assertRaises(BadTimeError, self.score.nthVisibleLineIndex, 0, 1)
        self.assertEqual(list(self.score.iterVisibleLines(0)), [kit[0]])
        self.assertEqual(list(self.score.iterVisibleLines(0, True)), [kit[0]])

    def testNumVisibleLines(self):
        self.score.scoreData.emptyLinesVisible = False
        self.assertEqual(self.score.numVisibleLines(0), 2)
        self.assertEqual(self.score.numVisibleLines(1), 2)
        self.assertEqual(self.score.numVisibleLines(2), 3)
        self.assertEqual(self.score.numVisibleLines(3), 5)
        self.score.scoreData.emptyLinesVisible = True
        self.assertEqual(self.score.numVisibleLines(0), 5)
        self.assertEqual(self.score.numVisibleLines(1), 5)
        self.assertEqual(self.score.numVisibleLines(2), 5)
        self.assertEqual(self.score.numVisibleLines(3), 5)

    def testNthVisibleLineIndex(self):
        self.score.scoreData.emptyLinesVisible = False
        self.assertEqual(self.score.nthVisibleLineIndex(0, 0), 0)
        self.assertEqual(self.score.nthVisibleLineIndex(0, 1), 3)
        self.assertRaises(BadTimeError, self.score.nthVisibleLineIndex, 0, 2)
        self.assertEqual(self.score.nthVisibleLineIndex(1, 0), 0)
        self.assertEqual(self.score.nthVisibleLineIndex(1, 1), 3)
        self.assertRaises(BadTimeError, self.score.nthVisibleLineIndex, 1, 2)
        self.assertEqual(self.score.nthVisibleLineIndex(2, 0), 0)
        self.assertEqual(self.score.nthVisibleLineIndex(2, 1), 1)
        self.assertEqual(self.score.nthVisibleLineIndex(2, 2), 3)
        self.assertRaises(BadTimeError, self.score.nthVisibleLineIndex, 2, 3)
        self.assertEqual(self.score.nthVisibleLineIndex(3, 0), 0)
        self.assertEqual(self.score.nthVisibleLineIndex(3, 1), 1)
        self.assertEqual(self.score.nthVisibleLineIndex(3, 2), 2)
        self.assertEqual(self.score.nthVisibleLineIndex(3, 3), 3)
        self.assertEqual(self.score.nthVisibleLineIndex(3, 4), 4)
        self.assertRaises(BadTimeError, self.score.nthVisibleLineIndex, 3, 5)
        self.score.scoreData.emptyLinesVisible = True
        self.assertEqual(self.score.nthVisibleLineIndex(0, 0), 0)
        self.assertEqual(self.score.nthVisibleLineIndex(0, 1), 1)
        self.assertEqual(self.score.nthVisibleLineIndex(0, 2), 2)
        self.assertEqual(self.score.nthVisibleLineIndex(0, 3), 3)
        self.assertEqual(self.score.nthVisibleLineIndex(0, 4), 4)
        self.assertRaises(BadTimeError, self.score.nthVisibleLineIndex, 0, 5)
        self.assertEqual(self.score.nthVisibleLineIndex(1, 0), 0)
        self.assertEqual(self.score.nthVisibleLineIndex(1, 1), 1)
        self.assertEqual(self.score.nthVisibleLineIndex(1, 2), 2)
        self.assertEqual(self.score.nthVisibleLineIndex(1, 3), 3)
        self.assertEqual(self.score.nthVisibleLineIndex(1, 4), 4)
        self.assertRaises(BadTimeError, self.score.nthVisibleLineIndex, 1, 5)
        self.assertEqual(self.score.nthVisibleLineIndex(2, 0), 0)
        self.assertEqual(self.score.nthVisibleLineIndex(2, 1), 1)
        self.assertEqual(self.score.nthVisibleLineIndex(2, 2), 2)
        self.assertEqual(self.score.nthVisibleLineIndex(2, 3), 3)
        self.assertEqual(self.score.nthVisibleLineIndex(2, 4), 4)
        self.assertRaises(BadTimeError, self.score.nthVisibleLineIndex, 2, 5)
        self.assertEqual(self.score.nthVisibleLineIndex(3, 0), 0)
        self.assertEqual(self.score.nthVisibleLineIndex(3, 1), 1)
        self.assertEqual(self.score.nthVisibleLineIndex(3, 2), 2)
        self.assertEqual(self.score.nthVisibleLineIndex(3, 3), 3)
        self.assertEqual(self.score.nthVisibleLineIndex(3, 4), 4)
        self.assertRaises(BadTimeError, self.score.nthVisibleLineIndex, 3, 5)

    def testIterVisibleLines(self):
        self.score.scoreData.emptyLinesVisible = False
        self.assertEqual(list(self.score.iterVisibleLines(0)),
                         [self.score.drumKit[0], self.score.drumKit[3]])
        self.assertEqual(list(self.score.iterVisibleLines(1)),
                         [self.score.drumKit[0], self.score.drumKit[3]])
        self.assertEqual(list(self.score.iterVisibleLines(2)),
                         [self.score.drumKit[0],
                          self.score.drumKit[1],
                          self.score.drumKit[3]])
        self.assertEqual(list(self.score.iterVisibleLines(3)),
                         [self.score.drumKit[0],
                          self.score.drumKit[1],
                          self.score.drumKit[2],
                          self.score.drumKit[3],
                          self.score.drumKit[4]])
        self.score.scoreData.emptyLinesVisible = True
        self.assertEqual(list(self.score.iterVisibleLines(0)),
                         [self.score.drumKit[0],
                          self.score.drumKit[1],
                          self.score.drumKit[2],
                          self.score.drumKit[3],
                          self.score.drumKit[4]])
        self.assertEqual(list(self.score.iterVisibleLines(1)),
                         [self.score.drumKit[0],
                          self.score.drumKit[1],
                          self.score.drumKit[2],
                          self.score.drumKit[3],
                          self.score.drumKit[4]])
        self.assertEqual(list(self.score.iterVisibleLines(2)),
                         [self.score.drumKit[0],
                          self.score.drumKit[1],
                          self.score.drumKit[2],
                          self.score.drumKit[3],
                          self.score.drumKit[4]])
        self.assertEqual(list(self.score.iterVisibleLines(3)),
                         [self.score.drumKit[0],
                          self.score.drumKit[1],
                          self.score.drumKit[2],
                          self.score.drumKit[3],
                          self.score.drumKit[4]])

    def testIterVisibleLinesForceIgnoreEmpty(self):
        self.score.scoreData.emptyLinesVisible = False
        self.assertEqual(list(self.score.iterVisibleLines(0, True)),
                         [self.score.drumKit[0], self.score.drumKit[3]])
        self.assertEqual(list(self.score.iterVisibleLines(1, True)),
                         [self.score.drumKit[0], self.score.drumKit[3]])
        self.assertEqual(list(self.score.iterVisibleLines(2, True)),
                         [self.score.drumKit[0],
                          self.score.drumKit[1],
                          self.score.drumKit[3]])
        self.assertEqual(list(self.score.iterVisibleLines(3, True)),
                         [self.score.drumKit[0],
                          self.score.drumKit[1],
                          self.score.drumKit[2],
                          self.score.drumKit[3],
                          self.score.drumKit[4]])
        self.score.scoreData.emptyLinesVisible = True
        self.assertEqual(list(self.score.iterVisibleLines(0, True)),
                         [self.score.drumKit[0], self.score.drumKit[3]])
        self.assertEqual(list(self.score.iterVisibleLines(1, True)),
                         [self.score.drumKit[0], self.score.drumKit[3]])
        self.assertEqual(list(self.score.iterVisibleLines(2, True)),
                         [self.score.drumKit[0], self.score.drumKit[1],
                          self.score.drumKit[3]])
        self.assertEqual(list(self.score.iterVisibleLines(3, True)),
                         [self.score.drumKit[0],
                          self.score.drumKit[1],
                          self.score.drumKit[2],
                          self.score.drumKit[3],
                          self.score.drumKit[4]])

class TestCallBack(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.drumKit = DrumKitFactory.DrumKitFactory.getNamedDefaultKit()
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

class TestHash(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.drumKit = DrumKitFactory.DrumKitFactory.getNamedDefaultKit()
        for dummy in range(0, 16):
            self.score.insertMeasureByIndex(16)

    def testEmpty(self):
        hashVal = self.score.hashScore()
        self.assertEqual(hashVal.encode("hex"),
                         "95b319c82f934d9abfce950b58a7c3bd")

if __name__ == "__main__":
    unittest.main()
