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
from cStringIO import StringIO
from Data.Score import Score, InconsistentRepeats, ScoreFactory
from Data import DrumKit, Drum, DBErrors
from Data.DBErrors import BadTimeError, OverSizeMeasure
from Data.DBConstants import EMPTY_NOTE
from Data.NotePosition import NotePosition
from Data import fileUtils
from Data.fileStructures import dbfsv0

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

    def testInsertMeasureByPosition(self):
        self.score.insertMeasureByPosition(16)
        self.score.insertMeasureByPosition(16)
        self.score.insertMeasureByPosition(16)
        self.score.insertMeasureByPosition(8, NotePosition(0, 2))
        self.assertEqual(self.score.numMeasures(), 4)
        self.assertEqual(len(self.score), 56)
        self.assertEqual(len(self.score.getMeasure(2)), 8)
        self.score.insertMeasureByPosition(24, NotePosition(0, 4))
        self.assertEqual(self.score.numMeasures(), 5)
        self.assertEqual(len(self.score), 80)
        self.assertEqual(len(self.score.getMeasure(4)), 24)

    def testInsertMeasureByPosition_IntoEmptyScore(self):
        self.score.insertMeasureByPosition(16)
        self.assertEqual(self.score.numMeasures(), 1)
        self.assertEqual(len(self.score), 16)
        self.assertEqual(len(self.score.getMeasure(0)), 16)

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
        self.score.drumKit = DrumKit.getNamedDefaultKit()
        for dummy in range(0, 12):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(80)

    def testgetItemAtPosition(self):
        self.assertEqual(self.score.getItemAtPosition(NotePosition(0, 0, 0, 0)),
                         EMPTY_NOTE)
        self.assertEqual(self.score.getItemAtPosition(NotePosition(0, 0)),
                         self.score.getMeasure(0))
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
        self.score.getMeasure(5).setSectionEnd(True)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 6)

    def testFormatScore_SectionEndAtScoreEnd(self):
        for dummy in range(0, 20):
            self.score.insertMeasureByIndex(16)
        self.score.getMeasure(19).setSectionEnd(True)
        self.score.formatScore(80)
        self.assertEqual(self.score.numStaffs(), 5)

    def testFormatScoreWithSectionsAndRepeat(self):
        for dummy in range(0, 20):
            self.score.insertMeasureByIndex(16)
        self.score.getMeasure(0).setRepeatStart(True)
        self.score.getMeasure(5).setSectionEnd(True)
        self.score.getMeasure(5).setRepeatEnd(True)
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

    def testGetMeasurePosition(self):
        for dummy in range(0, 8):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(40)
        self.assertEqual(self.score.getMeasurePosition(0),
                         NotePosition(0, 0))
        self.assertEqual(self.score.getMeasurePosition(1),
                         NotePosition(0, 1))
        self.assertEqual(self.score.getMeasurePosition(2),
                         NotePosition(1, 0))
        self.assertEqual(self.score.getMeasurePosition(3),
                         NotePosition(1, 1))
        self.assertEqual(self.score.getMeasurePosition(4),
                         NotePosition(2, 0))
        self.assertEqual(self.score.getMeasurePosition(5),
                         NotePosition(2, 1))
        self.assertEqual(self.score.getMeasurePosition(6),
                         NotePosition(3, 0))
        self.assertEqual(self.score.getMeasurePosition(7),
                         NotePosition(3, 1))
        self.assertRaises(BadTimeError, self.score.getMeasurePosition, 8)

    def testGetMeasureIndex(self):
        for dummy in range(0, 8):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(40)
        self.assertEqual(self.score.getMeasureIndex(NotePosition(0, 0)), 0)
        self.assertEqual(self.score.getMeasureIndex(NotePosition(0, 1)), 1)
        self.assertEqual(self.score.getMeasureIndex(NotePosition(1, 0)), 2)
        self.assertEqual(self.score.getMeasureIndex(NotePosition(1, 1)), 3)
        self.assertEqual(self.score.getMeasureIndex(NotePosition(2, 0)), 4)
        self.assertEqual(self.score.getMeasureIndex(NotePosition(2, 1)), 5)
        self.assertEqual(self.score.getMeasureIndex(NotePosition(3, 0)), 6)
        self.assertEqual(self.score.getMeasureIndex(NotePosition(3, 1)), 7)
        self.assertRaises(BadTimeError,
                          self.score.getMeasureIndex, NotePosition(4, 4))

    def testTrailingMeasures(self):
        self.score.drumKit = DrumKit.getNamedDefaultKit()
        for dummy in range(0, 8):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(40)
        self.score.addNote(NotePosition(0, 1, 0, 0), "x")
        trailing = self.score.trailingEmptyMeasures()
        self.assertEqual(trailing,
                         [self.score.getMeasurePosition(i)
                          for i in xrange(7, 1, -1)])

    def testTrailingMeasuresEmptyScore(self):
        for dummy in range(0, 8):
            self.score.insertMeasureByIndex(16)
        self.score.formatScore(40)
        trailing = self.score.trailingEmptyMeasures()
        self.assertEqual(trailing,
                         [self.score.getMeasurePosition(i)
                          for i in xrange(7, 0, -1)])

class TestCopyPaste(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.kit = DrumKit.getNamedDefaultKit()
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

    def testAlternatesNoEnd(self):
        self.score.getMeasure(0).setRepeatStart(True)
        self.score.getMeasure(1).setRepeatEnd(True)
        self.score.getMeasure(1).alternateText = "1,3-5."
        self.score.getMeasure(2).setRepeatEnd(True)
        self.score.getMeasure(2).alternateText = "2,6."
        self.score.getMeasure(3).alternateText = "7."
        measures = list(self.score.iterMeasuresWithRepeats())
        self.assertEqual([m[1] for m in measures[0:14]],
                         [0, 1, 0, 2, 0, 1, 0, 1, 0, 1, 0, 2, 0, 3])
        self.assertEqual([m[1] for m in measures[14:]],
                         range(4, 26))
        for measure, index in measures:
            self.assertEqual(measure, self.score.getMeasure(index))

    def testInconsistentAlternates(self):
        self.score.getMeasure(0).setRepeatStart(True)
        self.score.getMeasure(1).setRepeatEnd(True)
        self.score.getMeasure(1).alternateText = "1,3-5."
        self.score.getMeasure(2).setRepeatEnd(True)
        self.score.getMeasure(2).alternateText = "2,6."
        self.score.getMeasure(3).setRepeatEnd(True)
        self.score.getMeasure(3).alternateText = "12."
        self.assertRaises(InconsistentRepeats, list,
                          self.score.iterMeasuresWithRepeats())


class TestSections(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.drumKit = DrumKit.getNamedDefaultKit()
        for index in range(0, 26):
            self.score.insertMeasureByIndex(16)
            measure = self.score.getMeasure(index)
            measure.addNote(NotePosition(noteTime = 0, drumIndex = 0),
                            chr(ord("a") + index))
        self.score.formatScore(80)

    def testNoSections(self):
        self.assertEqual(self.score.numSections(), 0)

    def testAddSection(self):
        np = self.score.getMeasurePosition(3)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 1)
        self.assertEqual(self.score.getSectionTitle(0), "New Section")

    def testSetSectionTitle(self):
        np = self.score.getMeasurePosition(3)
        self.score.setSectionEnd(np, True)
        self.score.setSectionTitle(0, "Section 1")
        np = self.score.getMeasurePosition(15)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 2)
        self.score.setSectionTitle(1, "Section 2")
        self.assertEqual(self.score.getSectionTitle(0), "Section 1")
        self.assertEqual(self.score.getSectionTitle(1), "Section 2")
        self.assertEqual(list(self.score.iterSections()),
                         ["Section 1", "Section 2"])

    def testRemoveSection(self):
        np = self.score.getMeasurePosition(3)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 1)
        self.score.setSectionTitle(0, "Section 1")
        np = self.score.getMeasurePosition(15)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 2)
        self.score.setSectionTitle(1, "Section 2")
        np = self.score.getMeasurePosition(3)
        self.score.setSectionEnd(np, False)
        self.assertEqual(self.score.numSections(), 1)
        self.assertEqual(self.score.getSectionTitle(0), "Section 2")

    def testGetSectionIndex(self):
        np = self.score.getMeasurePosition(3)
        self.score.setSectionEnd(np, True)
        np = self.score.getMeasurePosition(19)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 2)
        np = self.score.getMeasurePosition(2)
        self.assertEqual(self.score.getSectionIndex(np), 0)
        np = self.score.getMeasurePosition(10)
        self.assertEqual(self.score.getSectionIndex(np), 1)

    def testGetSectionStartStaffIndex(self):
        np = self.score.getMeasurePosition(3)
        self.score.setSectionEnd(np, True)
        np = self.score.getMeasurePosition(19)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 2)
        np = self.score.getMeasurePosition(2)
        self.assertEqual(self.score.getSectionStartStaffIndex(np), 0)
        np = self.score.getMeasurePosition(10)
        self.assertEqual(self.score.getSectionStartStaffIndex(np), 1)

    def testIterMeasuresInSection(self):
        np = self.score.getMeasurePosition(3)
        self.score.setSectionEnd(np, True)
        np = self.score.getMeasurePosition(19)
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
        np = self.score.getMeasurePosition(3)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 1)
        self.score.setSectionTitle(0, "Section 1")
        np = self.score.getMeasurePosition(15)
        self.score.setSectionEnd(np, True)
        self.score.setSectionTitle(1, "Section 2")
        self.assertEqual(self.score.numSections(), 2)
        self.score.deleteSection(NotePosition(0, 1))
        self.assertEqual(self.score.numSections(), 1)
        self.assertEqual(self.score.numStaffs(), 6)
        self.assertEqual(self.score.numMeasures(), 22)
        self.assertEqual(self.score.getSectionTitle(0), "Section 2")

    def testDeleteSection_MiddleSection(self):
        np = self.score.getMeasurePosition(3)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 1)
        self.score.setSectionTitle(0, "Section 1")
        np = self.score.getMeasurePosition(15)
        self.score.setSectionEnd(np, True)
        self.score.setSectionTitle(1, "Section 2")
        np = self.score.getMeasurePosition(23)
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
        np = self.score.getMeasurePosition(3)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 1)
        self.score.setSectionTitle(0, "Section 1")
        np = self.score.getMeasurePosition(15)
        self.score.setSectionEnd(np, True)
        self.score.setSectionTitle(1, "Section 2")
        np = self.score.getMeasurePosition(23)
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
        np = self.score.getMeasurePosition(3)
        self.score.setSectionEnd(np, True)
        self.assertEqual(self.score.numSections(), 1)
        self.score.setSectionTitle(0, "Section 1")
        np = self.score.getMeasurePosition(15)
        self.score.setSectionEnd(np, True)
        self.score.setSectionTitle(1, "Section 2")
        np = self.score.getMeasurePosition(23)
        self.score.setSectionEnd(np, True)
        self.score.setSectionTitle(2, "Section 3")
        self.assertEqual(self.score.numSections(), 3)
        self.score.deleteSection(NotePosition(6, 0))
        self.assertEqual(self.score.numSections(), 3)

class TestRelativePositions(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.drumKit = DrumKit.getNamedDefaultKit()
        for index in range(0, 26):
            self.score.insertMeasureByIndex(16)
            measure = self.score.getMeasure(index)
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

class TestWrite(unittest.TestCase):
    @staticmethod
    def getOutput(score):
        handle = StringIO()
        score.write(handle)
        return handle.getvalue().splitlines()

    def testWrite(self):
        score = Score()
        score.insertMeasureByIndex(16)
        score.setSectionEnd(NotePosition(0, 0), True)
        score.lilyFill = True
        self.assertEqual(self.getOutput(score),
                        ['DB_FILE_FORMAT 0',
                         'SCORE_METADATA',
                         '  TITLE ',
                         '  ARTIST ',
                         '  ARTISTVISIBLE True',
                         '  CREATOR ',
                         '  CREATORVISIBLE True',
                         '  BPM 120',
                         '  BPMVISIBLE True',
                         '  WIDTH 80',
                         '  KITDATAVISIBLE True',
                         '  METADATAVISIBLE True',
                         '  BEATCOUNTVISIBLE True',
                         '  EMPTYLINESVISIBLE True',
                         '  MEASURECOUNTSVISIBLE False',
                         'END_SCORE_METADATA',
                         'KIT_START',
                         'KIT_END',
                         'START_BAR 16',
                         '  BARLINE NORMAL_BAR,NO_BAR',
                         '  BARLINE NORMAL_BAR,NO_BAR,SECTION_END',
                         'END_BAR',
                         'SECTION_TITLE New Section',
                         'PAPER_SIZE Letter',
                         'LILYSIZE 20',
                         'LILYPAGES 0',
                         'LILYFILL YES',
                         'LILYFORMAT 0',
                         'DEFAULT_COUNT_INFO_START',
                         '  REPEAT_BEATS 4',
                         '  BEAT_START',
                         '    COUNT |^|',
                         '  BEAT_END',
                         'COUNT_INFO_END',
                         'SYSTEM_SPACE 25',
                         'FONT_OPTIONS_START',
                         '  NOTEFONT MS Shell Dlg 2',
                         '  NOTEFONTSIZE 10',
                         '  SECTIONFONT MS Shell Dlg 2',
                         '  SECTIONFONTSIZE 14',
                         '  METADATAFONT MS Shell Dlg 2',
                         '  METADATAFONTSIZE 16',
                         'FONT_OPTIONS_END'])



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

class TestHash(unittest.TestCase):
    def setUp(self):
        self.score = Score()
        self.score.drumKit = DrumKit.getNamedDefaultKit()
        for dummy in range(0, 16):
            self.score.insertMeasureByIndex(16)

    def testEmpty(self):
        hash_val = self.score.hashScore()
        self.assertEqual(hash_val.encode("hex"),
                         "0bc1a56ea6085a688c4c46e538645bab")

class TestRead(unittest.TestCase):
    ff_zero_data = """
    SCORE_METADATA
      TITLE Sample
    END_SCORE_METADATA
    KIT_START
      DRUM Foot pedal,Hf,x,False
        NOTEHEAD x 44,96,normal,cross,-5,none,1,x
      DRUM Kick,Bd,o,True
        NOTEHEAD o 36,96,normal,default,-3,none,1,a
        NOTEHEAD O 36,127,accent,default,-3,accent,1,o
        NOTEHEAD g 36,50,ghost,default,-3,ghost,1,g
        NOTEHEAD d 36,96,drag,default,-3,drag,1,d
      DRUM Floor Tom,FT,o,False
        NOTEHEAD o 43,96,normal,default,-1,none,1,a
        NOTEHEAD O 43,127,accent,default,-1,accent,1,o
        NOTEHEAD g 43,50,ghost,default,-1,ghost,1,g
        NOTEHEAD f 43,96,flam,default,-1,flam,1,f
        NOTEHEAD d 43,96,drag,default,-1,drag,1,d
      DRUM Snare,Sn,o,True
        NOTEHEAD o 38,96,normal,default,1,none,1,a
        NOTEHEAD O 38,127,accent,default,1,accent,1,o
        NOTEHEAD g 38,50,ghost,default,1,ghost,1,g
        NOTEHEAD x 37,96,normal,cross,1,none,1,x
        NOTEHEAD f 38,96,flam,default,1,flam,1,f
        NOTEHEAD d 38,96,drag,default,1,drag,1,d
      DRUM Mid Tom,MT,o,False
        NOTEHEAD o 47,96,normal,default,2,none,1,a
        NOTEHEAD O 47,127,accent,default,2,accent,1,o
        NOTEHEAD g 47,50,ghost,default,2,ghost,1,g
        NOTEHEAD f 47,96,flam,default,2,flam,1,f
        NOTEHEAD d 47,96,drag,default,2,drag,1,d
      DRUM High Tom,HT,o,False
        NOTEHEAD o 50,96,normal,default,3,none,1,a
        NOTEHEAD O 50,127,accent,default,3,accent,1,o
        NOTEHEAD g 50,50,ghost,default,3,ghost,1,g
        NOTEHEAD f 50,96,flam,default,3,flam,1,f
        NOTEHEAD d 50,96,drag,default,3,drag,1,d
      DRUM Ride,Ri,x,False
        NOTEHEAD x 51,96,normal,cross,4,none,0,a
        NOTEHEAD X 51,127,accent,cross,4,accent,0,x
        NOTEHEAD b 53,96,normal,triangle,4,none,0,b
        NOTEHEAD d 51,96,drag,cross,4,drag,0,d
      DRUM HiHat,Hh,x,False
        NOTEHEAD x 42,96,normal,cross,5,none,0,b
        NOTEHEAD X 42,127,accent,cross,5,accent,0,x
        NOTEHEAD o 46,96,normal,cross,5,open,0,o
        NOTEHEAD O 46,127,accent,cross,5,accent,0,a
        NOTEHEAD d 42,96,drag,cross,5,drag,0,d
        NOTEHEAD + 42,96,choke,cross,5,stopped,0,s
        NOTEHEAD # 42,96,choke,cross,5,choke,0,c
      DRUM Crash,Cr,x,False
        NOTEHEAD x 49,96,normal,cross,6,none,0,a
        NOTEHEAD X 49,127,accent,cross,6,accent,0,x
        NOTEHEAD # 49,96,choke,cross,6,stopped,0,c
    KIT_END
    START_BAR 8
      COUNT_INFO_START
        REPEAT_BEATS 4
        BEAT_START
          COUNT |^+|
        BEAT_END
      COUNT_INFO_END
      BARLINE NORMAL_BAR,REPEAT_START,NO_BAR
      BARLINE NORMAL_BAR,NO_BAR,REPEAT_END
      REPEAT_COUNT 3
    END_BAR
    START_BAR 8
      COUNT_INFO_START
        REPEAT_BEATS 4
        BEAT_START
          COUNT |^+|
        BEAT_END
      COUNT_INFO_END
      BARLINE NORMAL_BAR,NO_BAR
      NOTE 5,3,o
      NOTE 6,3,o
      BARLINE NORMAL_BAR,NO_BAR
    END_BAR
    START_BAR 8
      COUNT_INFO_START
        REPEAT_BEATS 4
        BEAT_START
          COUNT |^+|
        BEAT_END
      COUNT_INFO_END
      BARLINE NORMAL_BAR,REPEAT_START,NO_BAR
      NOTE 0,1,q
      NOTE 0,7,x
      NOTE 2,3,o
      NOTE 2,7,x
      NOTE 4,1,o
      NOTE 4,7,x
      NOTE 6,3,o
      NOTE 6,7,x
      BARLINE NORMAL_BAR,NO_BAR
    END_BAR
    START_BAR 8
      COUNT_INFO_START
        REPEAT_BEATS 4
        BEAT_START
          COUNT |^+|
        BEAT_END
      COUNT_INFO_END
      BARLINE NORMAL_BAR,NO_BAR
      NOTE 0,1,o
      NOTE 0,7,x
      NOTE 2,3,o
      NOTE 2,7,x
      NOTE 3,1,o
      NOTE 4,7,x
      NOTE 5,1,o
      NOTE 6,3,o
      NOTE 6,7,x
      BARLINE NORMAL_BAR,NO_BAR,REPEAT_END
      REPEAT_COUNT 10
    END_BAR
    START_BAR 8
      COUNT_INFO_START
        REPEAT_BEATS 4
        BEAT_START
          COUNT |^+|
        BEAT_END
      COUNT_INFO_END
      BARLINE NORMAL_BAR,REPEAT_START,NO_BAR
      NOTE 0,1,o
      NOTE 0,6,x
      NOTE 2,3,o
      NOTE 2,6,x
      NOTE 4,1,o
      NOTE 4,6,x
      NOTE 6,3,o
      NOTE 6,6,x
      NOTE 7,1,o
      BARLINE NORMAL_BAR,NO_BAR
    END_BAR
    START_BAR 8
      COUNT_INFO_START
        REPEAT_BEATS 4
        BEAT_START
          COUNT |^+|
        BEAT_END
      COUNT_INFO_END
      BARLINE NORMAL_BAR,NO_BAR
      NOTE 0,6,x
      NOTE 1,1,o
      NOTE 2,3,o
      NOTE 2,6,x
      NOTE 4,1,o
      NOTE 4,6,x
      NOTE 6,3,o
      NOTE 6,6,x
      BARLINE NORMAL_BAR,NO_BAR,REPEAT_END
      REPEAT_COUNT 2
      ALTERNATE 1-14.
    END_BAR
    START_BAR 8
      COUNT_INFO_START
        REPEAT_BEATS 4
        BEAT_START
          COUNT |^+|
        BEAT_END
      COUNT_INFO_END
      BARLINE NORMAL_BAR,NO_BAR
      NOTE 0,6,x
      NOTE 1,1,o
      NOTE 2,3,o
      NOTE 2,6,x
      NOTE 4,6,x
      NOTE 5,1,o
      NOTE 6,3,f
      BARLINE NORMAL_BAR,NO_BAR,SECTION_END
      ALTERNATE 15.
    END_BAR
    SECTION_TITLE A title
    SECTION_TITLE Bridge
    SECTION_TITLE Chorus 1
    SECTION_TITLE Middle
    SECTION_TITLE Bridge & Chorus 2
    SECTION_TITLE Outro
    PAPER_SIZE Letter
    LILYSIZE 20
    LILYPAGES 0
    LILYFILL YES
    DEFAULT_COUNT_INFO_START
      REPEAT_BEATS 4
      BEAT_START
        COUNT |^+|
      BEAT_END
    COUNT_INFO_END
    SYSTEM_SPACE 25
    FONT_OPTIONS_START
      NOTEFONT MS Shell Dlg 2
      NOTEFONTSIZE 10
      SECTIONFONT MS Shell Dlg 2
      SECTIONFONTSIZE 14
      METADATAFONT MS Shell Dlg 2
      METADATAFONTSIZE 16
    FONT_OPTIONS_END
    """

    def testReadVersionZeroNoFileFormatNumber(self):
        handle = StringIO(self.ff_zero_data)
        iterator = fileUtils.dbFileIterator(handle)
        score = dbfsv0.ScoreStructureV0().read(iterator, ("START_SCORE", ""))
        self.assert_(score.lilyFill)
        self.assertEqual(score.lilypages, 0)
        self.assertEqual(score.lilysize, 20)
        self.assertEqual(score.scoreData.title, "Sample")
        self.assertEqual(score.getSectionTitle(0), "A title")
        self.assert_(score.drumKit[1].isAllowedHead('q'))

    def testReadVersionZeroWithFileFormatNumber(self):
        handle = StringIO("""DB_FILE_FORMAT 0
        """ + self.ff_zero_data)
        score = Score()
        score.read(handle)
        self.assert_(score.lilyFill)
        self.assertEqual(score.lilypages, 0)
        self.assertEqual(score.lilysize, 20)
        self.assertEqual(score.scoreData.title, "Sample")
        self.assertEqual(score.getSectionTitle(0), "A title")
        self.assert_(score.drumKit[1].isAllowedHead('q'))

    def testReadTooHighVersionNumber(self):
        data = """DB_FILE_FORMAT 10000
        """ + self.ff_zero_data
        handle = StringIO(data)
        score = Score()
        self.assertRaises(DBErrors.DBVersionError, score.read, handle)

class TestScoreFactory(unittest.TestCase):
    def testMakeEmptyDefault(self):
        score = ScoreFactory.makeEmptyScore(16, None, None)
        self.assertEqual(score.numMeasures(), 16)

    def testFactory(self):
        factory = ScoreFactory()
        score = factory()
        self.assertEqual(score.numMeasures(), 32)

if __name__ == "__main__":
    unittest.main()
