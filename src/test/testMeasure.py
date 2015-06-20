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
from Data.Measure import Measure
from Data.Counter import CounterRegistry
from Data.MeasureCount import MeasureCount
from Data.DBErrors import BadTimeError
from Data.DBConstants  import EMPTY_NOTE
from Data.NotePosition import NotePosition
from Data import fileUtils
from Data.fileStructures import dbfsv0
# pylint: disable-msg=R0904

class TestMeasure(unittest.TestCase):
    reg = CounterRegistry()

    def setUp(self):
        self.measure = Measure(16)
        counter = self.reg.getCounterByName("16ths")
        mc = MeasureCount()
        mc.addSimpleBeats(counter, 4)
        self.measure.setBeatCount(mc)

    def testCount(self):
        count = self.measure.count()
        self.assertEqual(count,
                         ["1", "e", "+", "a",
                          "2", "e", "+", "a",
                          "3", "e", "+", "a",
                          "4", "e", "+", "a"])
        measure = Measure(16)
        self.assertEqual(measure.count(), [" "] * 16)

    def testEmptyMeasure(self):
        self.assertEqual(len(self.measure), 16)
        self.assertEqual(self.measure.numNotes(), 0)
        self.assertEqual(self.measure.getNote(NotePosition(noteTime = 0,
                                                           drumIndex = 0)),
                         EMPTY_NOTE)
        self.assertFalse(self.measure.isSectionEnd())
        self.assertFalse(self.measure.isRepeatEnd())
        self.assertFalse(self.measure.isRepeatStart())

    def testIsEmpty_True(self):
        self.assert_(self.measure.isEmpty())

    def testIsEmpty_False(self):
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "o")
        self.assertFalse(self.measure.isEmpty())

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

    def testSetSectionEnd_NoRepeat(self):
        self.assertFalse(self.measure.isSectionEnd())
        self.assertFalse(self.measure.isLineEnd())
        self.measure.setSectionEnd(True)
        self.assert_(self.measure.isSectionEnd())
        self.assert_(self.measure.isLineEnd())
        self.measure.setSectionEnd(False)
        self.assertFalse(self.measure.isSectionEnd())
        self.assertFalse(self.measure.isLineEnd())

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

    def testLineBreak(self):
        self.assertFalse(self.measure.isLineBreak())
        self.assertFalse(self.measure.isLineEnd())
        self.measure.setLineBreak(True)
        self.assert_(self.measure.isLineBreak())
        self.assert_(self.measure.isLineEnd())
        self.measure.setLineBreak(False)
        self.assertFalse(self.measure.isLineBreak())
        self.assertFalse(self.measure.isLineEnd())

    def testClearMeasure(self):
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "x")
        self.measure.addNote(NotePosition(noteTime = 1, drumIndex = 1), "o")
        self.assertEqual(self.measure.numNotes(), 2)
        self.assertFalse(self.measure.isEmpty())
        self.measure.clear()
        self.assert_(self.measure.isEmpty())

    def testCopyPaste(self):
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "x")
        self.measure.addNote(NotePosition(noteTime = 1, drumIndex = 1), "o")
        measure2 = Measure(8)
        copied = self.measure.copyMeasure()
        measure2.pasteMeasure(copied)
        self.assertEqual(len(measure2), 16)
        self.assertEqual(measure2.numNotes(), 2)
        self.assertEqual(measure2.getNote(NotePosition(None, None, 0, 0)), "x")
        self.assertEqual(measure2.getNote(NotePosition(None, None, 1, 1)), "o")

    def testCopyPasteWithDecorations(self):
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "x")
        self.measure.addNote(NotePosition(noteTime = 1, drumIndex = 1), "o")
        self.measure.setRepeatEnd(True)
        self.measure.setRepeatStart(True)
        self.measure.setLineBreak(True)
        self.measure.setSectionEnd(True)
        measure2 = Measure(8)
        self.assertFalse(measure2.isRepeatEnd())
        self.assertFalse(measure2.isRepeatStart())
        self.assertFalse(measure2.isLineBreak())
        self.assertFalse(measure2.isSectionEnd())
        copied = self.measure.copyMeasure()
        measure2.pasteMeasure(copied, True)
        self.assertEqual(len(measure2), 16)
        self.assertEqual(measure2.numNotes(), 2)
        self.assertEqual(measure2.getNote(NotePosition(None, None, 0, 0)), "x")
        self.assertEqual(measure2.getNote(NotePosition(None, None, 1, 1)), "o")
        self.assertTrue(measure2.isRepeatEnd())
        self.assertTrue(measure2.isRepeatStart())
        self.assertTrue(measure2.isLineBreak())
        self.assertTrue(measure2.isSectionEnd())

    def testChangeCount_Shorter(self):
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "a")
        self.measure.addNote(NotePosition(noteTime = 1, drumIndex = 1), "b")
        self.measure.addNote(NotePosition(noteTime = 2, drumIndex = 0), "c")
        self.measure.addNote(NotePosition(noteTime = 3, drumIndex = 1), "d")
        self.measure.addNote(NotePosition(noteTime = 4, drumIndex = 0), "e")
        self.measure.addNote(NotePosition(noteTime = 5, drumIndex = 1), "f")
        self.measure.addNote(NotePosition(noteTime = 6, drumIndex = 0), "g")
        self.measure.addNote(NotePosition(noteTime = 7, drumIndex = 1), "h")
        self.measure.addNote(NotePosition(noteTime = 8, drumIndex = 0), "i")
        self.measure.addNote(NotePosition(noteTime = 9, drumIndex = 1), "j")
        self.measure.addNote(NotePosition(noteTime = 10, drumIndex = 0), "k")
        self.measure.addNote(NotePosition(noteTime = 11, drumIndex = 1), "l")
        self.measure.addNote(NotePosition(noteTime = 12, drumIndex = 0), "m")
        self.measure.addNote(NotePosition(noteTime = 13, drumIndex = 1), "n")
        self.measure.addNote(NotePosition(noteTime = 14, drumIndex = 0), "o")
        self.measure.addNote(NotePosition(noteTime = 15, drumIndex = 1), "p")
        counter = self.reg.getCounterByName("8ths")
        mc = MeasureCount()
        mc.addSimpleBeats(counter, 3)
        self.measure.setBeatCount(mc)
        self.assertEqual(len(self.measure), 6)
        self.assertEqual(self.measure.numNotes(), 6)
        self.assertEqual(self.measure.noteAt(noteTime = 0, drumIndex = 0), "a")
        self.assertEqual(self.measure.noteAt(noteTime = 1, drumIndex = 0), "c")
        self.assertEqual(self.measure.noteAt(noteTime = 2, drumIndex = 0), "e")
        self.assertEqual(self.measure.noteAt(noteTime = 3, drumIndex = 0), "g")
        self.assertEqual(self.measure.noteAt(noteTime = 4, drumIndex = 0), "i")
        self.assertEqual(self.measure.noteAt(noteTime = 5, drumIndex = 0), "k")


    def testChangeCount_Longer(self):
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "a")
        self.measure.addNote(NotePosition(noteTime = 1, drumIndex = 1), "b")
        self.measure.addNote(NotePosition(noteTime = 2, drumIndex = 0), "c")
        self.measure.addNote(NotePosition(noteTime = 3, drumIndex = 1), "d")
        self.measure.addNote(NotePosition(noteTime = 4, drumIndex = 0), "e")
        self.measure.addNote(NotePosition(noteTime = 5, drumIndex = 1), "f")
        self.measure.addNote(NotePosition(noteTime = 6, drumIndex = 0), "g")
        self.measure.addNote(NotePosition(noteTime = 7, drumIndex = 1), "h")
        self.measure.addNote(NotePosition(noteTime = 8, drumIndex = 0), "i")
        self.measure.addNote(NotePosition(noteTime = 9, drumIndex = 1), "j")
        self.measure.addNote(NotePosition(noteTime = 10, drumIndex = 0), "k")
        self.measure.addNote(NotePosition(noteTime = 11, drumIndex = 1), "l")
        self.measure.addNote(NotePosition(noteTime = 12, drumIndex = 0), "m")
        self.measure.addNote(NotePosition(noteTime = 13, drumIndex = 1), "n")
        self.measure.addNote(NotePosition(noteTime = 14, drumIndex = 0), "o")
        self.measure.addNote(NotePosition(noteTime = 15, drumIndex = 1), "p")
        counter = self.reg.getCounterByName("32nds")
        mc = MeasureCount()
        mc.addSimpleBeats(counter, 5)
        self.measure.setBeatCount(mc)
        self.assertEqual(len(self.measure), 40)
        self.assertEqual(self.measure.numNotes(), 16)
        self.assertEqual(self.measure.noteAt(noteTime = 0, drumIndex = 0), "a")
        self.assertEqual(self.measure.noteAt(noteTime = 2, drumIndex = 1), "b")
        self.assertEqual(self.measure.noteAt(noteTime = 4, drumIndex = 0), "c")
        self.assertEqual(self.measure.noteAt(noteTime = 6, drumIndex = 1), "d")
        self.assertEqual(self.measure.noteAt(noteTime = 8, drumIndex = 0), "e")
        self.assertEqual(self.measure.noteAt(noteTime = 10, drumIndex = 1), "f")
        self.assertEqual(self.measure.noteAt(noteTime = 12, drumIndex = 0), "g")
        self.assertEqual(self.measure.noteAt(noteTime = 14, drumIndex = 1), "h")
        self.assertEqual(self.measure.noteAt(noteTime = 16, drumIndex = 0), "i")
        self.assertEqual(self.measure.noteAt(noteTime = 18, drumIndex = 1), "j")
        self.assertEqual(self.measure.noteAt(noteTime = 20, drumIndex = 0), "k")
        self.assertEqual(self.measure.noteAt(noteTime = 22, drumIndex = 1), "l")
        self.assertEqual(self.measure.noteAt(noteTime = 24, drumIndex = 0), "m")
        self.assertEqual(self.measure.noteAt(noteTime = 26, drumIndex = 1), "n")
        self.assertEqual(self.measure.noteAt(noteTime = 28, drumIndex = 0), "o")
        self.assertEqual(self.measure.noteAt(noteTime = 30, drumIndex = 1), "p")

    def testLineIsVisible(self):
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "a")
        self.measure.addNote(NotePosition(noteTime = 2, drumIndex = 2), "a")
        self.measure.addNote(NotePosition(noteTime = 3, drumIndex = 7), "a")
        self.assert_(self.measure.lineIsVisible(0))
        self.assert_(self.measure.lineIsVisible(2))
        self.assert_(self.measure.lineIsVisible(7))
        self.assertFalse(self.measure.lineIsVisible(1))
        self.assertFalse(self.measure.lineIsVisible(3))
        self.assertFalse(self.measure.lineIsVisible(4))
        self.assertFalse(self.measure.lineIsVisible(5))
        self.assertFalse(self.measure.lineIsVisible(6))
        self.assertFalse(self.measure.lineIsVisible(8))


class TestRead(unittest.TestCase):
    def testReadMeasure(self):
        data = """START_BAR 12
                  COUNT_INFO_START
                    REPEAT_BEATS 4
                    BEAT_START
                      COUNT |^+|
                    BEAT_END
                  COUNT_INFO_END
                  BARLINE NORMAL_BAR,NO_BAR
                  NOTE 0,1,o
                  NOTE 0,2,o
                  NOTE 1,2,o
                  NOTE 2,2,o
                  NOTE 2,3,o
                  NOTE 3,2,o
                  NOTE 3,3,o
                  NOTE 4,1,o
                  NOTE 4,2,o
                  NOTE 5,2,o
                  NOTE 6,2,o
                  NOTE 6,3,o
                  NOTE 7,2,x
                  BARLINE NORMAL_BAR,NO_BAR
                END_BAR"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        measure = dbfsv0.MeasureStructureV0().read(iterator)
        self.assertEqual(len(measure), 8)
        self.assertEqual(measure.numNotes(), 13)
        self.assertEqual(measure.noteAt(0, 1), "o")
        self.assertEqual(measure.noteAt(0, 2), "o")
        self.assertEqual(measure.noteAt(1, 2), "o")
        self.assertEqual(measure.noteAt(2, 2), "o")
        self.assertEqual(measure.noteAt(2, 3), "o")
        self.assertEqual(measure.noteAt(3, 2), "o")
        self.assertEqual(measure.noteAt(3, 3), "o")
        self.assertEqual(measure.noteAt(4, 1), "o")
        self.assertEqual(measure.noteAt(4, 2), "o")
        self.assertEqual(measure.noteAt(5, 2), "o")
        self.assertEqual(measure.noteAt(6, 2), "o")
        self.assertEqual(measure.noteAt(6, 3), "o")
        self.assertEqual(measure.noteAt(7, 2), "x")
        self.assertFalse(measure.isRepeatStart())
        self.assertFalse(measure.isRepeatEnd())
        self.assertFalse(measure.isSectionEnd())
        self.assertFalse(measure.isLineBreak())
        self.assertEqual(measure.alternateText, None)
        self.assertEqual(measure.repeatCount, 1)

    def testReadRepeatBar(self):
        data = """START_BAR 8
                    COUNT_INFO_START
                      REPEAT_BEATS 4
                      BEAT_START
                        COUNT |^+|
                      BEAT_END
                    COUNT_INFO_END
                    BARLINE NORMAL_BAR,REPEAT_START,NO_BAR
                    BARLINE NORMAL_BAR,NO_BAR,REPEAT_END
                    REPEAT_COUNT 6
                  END_BAR"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        measure = dbfsv0.MeasureStructureV0().read(iterator)
        self.assertEqual(measure.repeatCount, 6)
        self.assert_(measure.isRepeatStart())
        self.assert_(measure.isRepeatEnd())

    def testReadAlterate(self):
        data = """
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
          NOTE 1,6,x
          NOTE 2,3,o
          NOTE 2,6,x
          NOTE 3,6,x
          NOTE 4,1,o
          NOTE 4,6,x
          NOTE 5,1,o
          NOTE 5,6,x
          NOTE 6,8,x
          NOTE 6,3,o
          BARLINE NORMAL_BAR,NO_BAR,SECTION_END,REPEAT_END
          REPEAT_COUNT 2
          ALTERNATE 2.
        END_BAR
        """
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        measure = dbfsv0.MeasureStructureV0().read(iterator)
        self.assert_(measure.isRepeatEnd())
        self.assertEqual(measure.alternateText, "2.")

    def testReadLineBreak(self):
        data = """
        START_BAR 15
          COUNT_INFO_START
            BEAT_START
              COUNT |^+a|
            BEAT_END
            BEAT_START
              COUNT |^+a|
            BEAT_END
            BEAT_START
              COUNT |^ea+ea|
            BEAT_END
            BEAT_START
              COUNT |^+a|
            BEAT_END
          COUNT_INFO_END
          BARLINE NORMAL_BAR,NO_BAR
          NOTE 10,1,o
          NOTE 11,1,o
          NOTE 12,1,O
          BARLINE NORMAL_BAR,LINE_BREAK,NO_BAR
        END_BAR
        """
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        measure = dbfsv0.MeasureStructureV0().read(iterator)
        self.assert_(measure.isLineBreak())

    def testReadSectionEnd(self):
        data = """
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
          NOTE 1,1,o
          NOTE 1,7,x
          NOTE 2,3,o
          NOTE 2,7,x
          NOTE 3,7,x
          NOTE 4,1,o
          NOTE 4,7,x
          NOTE 5,1,o
          NOTE 5,7,x
          NOTE 6,8,x
          NOTE 6,3,o
          BARLINE NORMAL_BAR,NO_BAR,SECTION_END
        END_BAR
        """
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        measure = dbfsv0.MeasureStructureV0().read(iterator)
        self.assert_(measure.isSectionEnd())

    def testReadOldMeasure(self):
        data = """START_BAR 8
                  BEATLENGTH 2
                  BARLINE NORMAL_BAR,NO_BAR
                  NOTE 0,1,o
                  NOTE 0,2,o
                  NOTE 1,2,o
                  NOTE 2,2,o
                  NOTE 2,3,o
                  NOTE 3,2,o
                  NOTE 3,3,o
                  NOTE 4,1,o
                  NOTE 4,2,o
                  NOTE 5,2,o
                  NOTE 6,2,o
                  NOTE 6,3,o
                  NOTE 7,2,o
                  BARLINE NORMAL_BAR,NO_BAR
                END_BAR"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        measure = dbfsv0.MeasureStructureV0().read(iterator)
        self.assertEqual(len(measure), 8)
        self.assertEqual(measure.numNotes(), 13)
        self.assertEqual(measure.noteAt(0, 1), "o")
        self.assertEqual(measure.noteAt(0, 2), "o")
        self.assertEqual(measure.noteAt(1, 2), "o")
        self.assertEqual(measure.noteAt(2, 2), "o")
        self.assertEqual(measure.noteAt(2, 3), "o")
        self.assertEqual(measure.noteAt(3, 2), "o")
        self.assertEqual(measure.noteAt(3, 3), "o")
        self.assertEqual(measure.noteAt(4, 1), "o")
        self.assertEqual(measure.noteAt(4, 2), "o")
        self.assertEqual(measure.noteAt(5, 2), "o")
        self.assertEqual(measure.noteAt(6, 2), "o")
        self.assertEqual(measure.noteAt(6, 3), "o")
        self.assertEqual(measure.noteAt(7, 2), "o")
        self.assertFalse(measure.isRepeatStart())
        self.assertFalse(measure.isRepeatEnd())
        self.assertFalse(measure.isSectionEnd())
        self.assertFalse(measure.isLineBreak())
        self.assertEqual(measure.alternateText, None)
        self.assertEqual(measure.repeatCount, 1)

class TestWrite(unittest.TestCase):
    reg = CounterRegistry()

    def setUp(self):
        self.measure = Measure(16)
        counter = self.reg.getCounterByName("16ths")
        mc = MeasureCount()
        mc.addSimpleBeats(counter, 4)
        self.measure.setBeatCount(mc)

    def get_output(self):
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv0.MeasureStructureV0().write(self.measure, indenter)
        return handle.getvalue().splitlines()

    def testWriteEmpty(self):
        output = self.get_output()
        self.assertEqual(output,
                         ['START_BAR 16',
                          '  COUNT_INFO_START',
                          '    REPEAT_BEATS 4',
                          '    BEAT_START',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '  COUNT_INFO_END',
                          '  BARLINE NORMAL_BAR,NO_BAR',
                          '  BARLINE NORMAL_BAR,NO_BAR',
                          'END_BAR'])

    def testWriteSimple(self):
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "a")
        self.measure.addNote(NotePosition(noteTime = 1, drumIndex = 1), "b")
        self.measure.addNote(NotePosition(noteTime = 2, drumIndex = 0), "c")
        self.measure.addNote(NotePosition(noteTime = 3, drumIndex = 1), "d")
        self.measure.addNote(NotePosition(noteTime = 4, drumIndex = 0), "e")
        self.measure.addNote(NotePosition(noteTime = 5, drumIndex = 1), "f")
        self.measure.addNote(NotePosition(noteTime = 6, drumIndex = 0), "g")
        self.measure.addNote(NotePosition(noteTime = 7, drumIndex = 1), "h")
        self.measure.addNote(NotePosition(noteTime = 8, drumIndex = 0), "i")
        self.measure.addNote(NotePosition(noteTime = 9, drumIndex = 1), "j")
        self.measure.addNote(NotePosition(noteTime = 10, drumIndex = 0), "k")
        self.measure.addNote(NotePosition(noteTime = 11, drumIndex = 1), "l")
        self.measure.addNote(NotePosition(noteTime = 12, drumIndex = 0), "m")
        self.measure.addNote(NotePosition(noteTime = 13, drumIndex = 1), "n")
        self.measure.addNote(NotePosition(noteTime = 14, drumIndex = 0), "o")
        self.measure.addNote(NotePosition(noteTime = 15, drumIndex = 1), "p")
        output = self.get_output()
        self.assertEqual(output,
                         ['START_BAR 16',
                          '  COUNT_INFO_START',
                          '    REPEAT_BEATS 4',
                          '    BEAT_START',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '  COUNT_INFO_END',
                          '  BARLINE NORMAL_BAR,NO_BAR',
                          '  NOTE 0,0,a',
                          '  NOTE 1,1,b',
                          '  NOTE 2,0,c',
                          '  NOTE 3,1,d',
                          '  NOTE 4,0,e',
                          '  NOTE 5,1,f',
                          '  NOTE 6,0,g',
                          '  NOTE 7,1,h',
                          '  NOTE 8,0,i',
                          '  NOTE 9,1,j',
                          '  NOTE 10,0,k',
                          '  NOTE 11,1,l',
                          '  NOTE 12,0,m',
                          '  NOTE 13,1,n',
                          '  NOTE 14,0,o',
                          '  NOTE 15,1,p',
                          '  BARLINE NORMAL_BAR,NO_BAR',
                          'END_BAR'])

    def testWriteDecorations(self):
        self.measure.setLineBreak(True)
        self.measure.setSectionEnd(True)
        self.measure.setRepeatEnd(True)
        self.measure.setRepeatStart(True)
        self.measure.alternateText = "xxx"
        self.measure.repeatCount = 10
        output = self.get_output()
        self.assertEqual(output,
                         ['START_BAR 16',
                          '  COUNT_INFO_START',
                          '    REPEAT_BEATS 4',
                          '    BEAT_START',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '  COUNT_INFO_END',
                          '  BARLINE NORMAL_BAR,REPEAT_START,NO_BAR',
                          ('  BARLINE NORMAL_BAR,LINE_BREAK,NO_BAR,' +
                           'SECTION_END,REPEAT_END'),
                          '  REPEAT_COUNT 10',
                          '  ALTERNATE xxx',
                          'END_BAR'])

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
        self.measure.addNote(NotePosition(noteTime = 1, drumIndex = 1), "o")
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[1], (1, 1))

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

    def testClearMeasureCallback(self):
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "x")
        self.measure.addNote(NotePosition(noteTime = 1, drumIndex = 1), "o")
        self.assertEqual(len(self.calls), 2)
        self.measure.clear()
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(self.calls[2], (None, None))

    def testClearCallBack(self):
        self.measure.clearCallBack()
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "x")
        self.assertEqual(len(self.calls), 0)

if __name__ == "__main__":
    unittest.main()
