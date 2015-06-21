# Copyright 2015 Michael Thomas
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

import unittest
from cStringIO import StringIO
from Data import Beat, Counter, fileUtils, DBErrors, DrumKit, FontOptions, DefaultKits
from Data.Drum import Drum, HeadData
from Data.Counter import CounterRegistry
from Data.Measure import Measure
from Data import MeasureCount, ScoreMetaData
from Data.NotePosition import NotePosition

from Data.fileStructures import dbfsv0

class TestCounter(unittest.TestCase):
    def testWrite(self):
        counter = Counter.Counter("^bcd", "^fgh", "^jkl")
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv0.CounterFieldV0("COUNT",
                              getter = lambda _:counter).write_all(self, indenter)
        self.assertEqual(handle.getvalue(), "COUNT |^bcd|\n")

    def testRead(self):
        target = {}
        dbfsv0.CounterFieldV0("COUNT", attributeName = "counter").read(target, "|^e+a|")
        counter = target["counter"]
        self.assertEqual(str(counter), "^e+a")


class TestBeat(unittest.TestCase):
    def testWriteFullBeat(self):
        beat = Beat.Beat(Counter.Counter("e+a"))
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv0.BeatStructureV0().write(beat, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["BEAT_START",
                          "  COUNT |^e+a|",
                          "BEAT_END"])


    def testWritePartialBeat(self):
        beat = Beat.Beat(Counter.Counter("e+a"), 2)
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv0.BeatStructureV0().write(beat, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["BEAT_START",
                          "  NUM_TICKS 2",
                          "  COUNT |^e+a|",
                          "BEAT_END"])

    def testReadFull(self):
        handle = StringIO("""BEAT_START
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        beat = dbfsv0.BeatStructureV0().read(iterator)
        self.assertEqual("".join(beat.count(1)), "1e+a")

    def testReadPartial(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS 2
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        beat = dbfsv0.BeatStructureV0().read(iterator)
        self.assertEqual("".join(beat.count(1)), "1e")

    def testReadBadCount(self):
        handle = StringIO("""BEAT_START
        COUNT |^e+d|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.BadCount, dbfsv0.BeatStructureV0().read,
                          iterator)

    def testReadBadTicks(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS x
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.InvalidInteger, dbfsv0.BeatStructureV0().read,
                          iterator)

    def testReadBadNegativeTicks(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS -1
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.InvalidPositiveInteger,
                          dbfsv0.BeatStructureV0().read,
                          iterator)

    def testReadBadLine(self):
        handle = StringIO("""BEAT_START
        COUNT |^e+a|
        BAD_LINE xxx
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.UnrecognisedLine,
                          dbfsv0.BeatStructureV0().read, iterator)

class TestMeasureCount(unittest.TestCase):
    def testSimpleWrite(self):
        myCounter = Counter.Counter("e+a")
        count = MeasureCount.makeSimpleCount(myCounter, 4)
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv0.MeasureCountStructureV0().write(count, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["COUNT_INFO_START",
                          "  REPEAT_BEATS 4",
                          "  BEAT_START",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "COUNT_INFO_END"])

    def testComplexWrite(self):
        counter1 = Counter.Counter("e+a")
        counter2 = Counter.Counter("+a")
        counter3 = Counter.Counter("+")
        counter4 = Counter.Counter("e+a")
        count = MeasureCount.MeasureCount()
        count.addBeats(Beat.Beat(counter1), 1)
        count.addBeats(Beat.Beat(counter2), 1)
        count.addBeats(Beat.Beat(counter3), 1)
        count.addBeats(Beat.Beat(counter4, 2), 1)
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv0.MeasureCountStructureV0().write(count, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["COUNT_INFO_START",
                          "  BEAT_START",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    COUNT |^+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    COUNT |^+|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 2",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "COUNT_INFO_END"])

    def testReadSimple(self):
        data = """COUNT_INFO_START
                      REPEAT_BEATS 4
                      BEAT_START
                          COUNT |^e+a|
                      BEAT_END
                  COUNT_INFO_END"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        count = dbfsv0.MeasureCountStructureV0().read(iterator)
        self.assert_(count.isSimpleCount())
        self.assertEqual(len(count), 16)
        self.assertEqual(count.countString(), "1e+a2e+a3e+a4e+a")

    def testReadSimpleDefault(self):
        data = """DEFAULT_COUNT_INFO_START
                      REPEAT_BEATS 4
                      BEAT_START
                          COUNT |^e+a|
                      BEAT_END
                  COUNT_INFO_END"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        count = dbfsv0.MeasureCountStructureV0(startTag = "DEFAULT_COUNT_INFO_START").read(iterator)
        self.assert_(count.isSimpleCount())
        self.assertEqual(len(count), 16)
        self.assertEqual(count.countString(), "1e+a2e+a3e+a4e+a")


    def testReadComplex(self):
        data = """COUNT_INFO_START
                  BEAT_START
                    COUNT |^e+a|
                  BEAT_END
                  BEAT_START
                    COUNT |^+a|
                  BEAT_END
                  BEAT_START
                    COUNT |^+|
                  BEAT_END
                  BEAT_START
                    NUM_TICKS 2
                    COUNT |^e+a|
                  BEAT_END
                COUNT_INFO_END"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        count = dbfsv0.MeasureCountStructureV0().read(iterator)
        self.assertFalse(count.isSimpleCount())
        self.assertEqual(len(count), 11)
        self.assertEqual(count.countString(), "1e+a2+a3+4e")

    def testBadLine(self):
        data = """COUNT_INFO_START
              REPEAT_BEATS 4
              UNRECOGNISED LINE
              BEAT_START
                  COUNT |^e+a|
              BEAT_END
          COUNT_INFO_END"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.UnrecognisedLine,
                          dbfsv0.MeasureCountStructureV0().read,
                          iterator)

    def testBadBeatCount(self):
        data = """COUNT_INFO_START
              REPEAT_BEATS xxx
              UNRECOGNISED LINE
              BEAT_START
                  COUNT |^e+a|
              BEAT_END
          COUNT_INFO_END"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.InvalidInteger,
                          dbfsv0.MeasureCountStructureV0().read, iterator)

    def testNegativeBeatCount(self):
        data = """COUNT_INFO_START
              REPEAT_BEATS -1
              UNRECOGNISED LINE
              BEAT_START
                  COUNT |^e+a|
              BEAT_END
          COUNT_INFO_END"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.InvalidPositiveInteger,
                          dbfsv0.MeasureCountStructureV0().read, iterator)

class TestReadMeasure(unittest.TestCase):
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

    def testReadAlternate(self):
        data = """
        START_BAR 8
          COUNT_INFO_START
            REPEAT_BEATS 4
            BEAT_START
              COUNT |^+|
            BEAT_END
          COUNT_INFO_END
          BARLINE NORMAL_BAR,NO_BAR
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
          BARLINE NORMAL_BAR,NO_BAR,SECTION_END
        END_BAR
        """
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        measure = dbfsv0.MeasureStructureV0().read(iterator)
        self.assert_(measure.isSectionEnd())

    def testReadSimile(self):
        data = """
        START_BAR 8
          COUNT_INFO_START
            REPEAT_BEATS 4
            BEAT_START
              COUNT |^+|
            BEAT_END
          COUNT_INFO_END
          BARLINE NORMAL_BAR,NO_BAR
          BARLINE NORMAL_BAR,NO_BAR
          SIMILE 2
          SIMINDEX 1
        END_BAR
        """
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        measure = dbfsv0.MeasureStructureV0().read(iterator)
        self.assertEqual(measure.simileDistance, 2)
        self.assertEqual(measure.simileIndex, 1)

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

class TestWriteMeasure(unittest.TestCase):
    reg = CounterRegistry()

    def setUp(self):
        self.measure = Measure(16)
        counter = self.reg.getCounterByName("16ths")
        mc = MeasureCount.MeasureCount()
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
        self.measure.simileDistance = 2
        self.measure.simileIndex = 1
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
                          '  SIMILE 2',
                          '  SIMINDEX 1',
                          'END_BAR'])




class TestHeadDataRead(unittest.TestCase):
    def testRead_New(self):
        dataString = "x 72,100,ghost,cross,1,choke,1,c"
        head, data = dbfsv0.NoteHeadFieldV0.readHeadData("Hh", dataString)
        self.assertEqual(head, "x")
        self.assertEqual(data.midiNote, 72)
        self.assertEqual(data.midiVolume, 100)
        self.assertEqual(data.effect, "ghost")
        self.assertEqual(data.notationHead, "cross")
        self.assertEqual(data.notationLine, 1)
        self.assertEqual(data.notationEffect, "choke")
        self.assertEqual(data.stemDirection, 1)
        self.assertEqual(data.shortcut, "c")

    def testRead_Old_Recognised_Drum(self):
        dataString = "g 72,100,ghost"
        head, data = dbfsv0.NoteHeadFieldV0.readHeadData("Sn", dataString)
        self.assertEqual(head, "g")
        self.assertEqual(data.midiNote, 72)
        self.assertEqual(data.midiVolume, 100)
        self.assertEqual(data.effect, "ghost")
        self.assertEqual(data.notationHead, "default")
        self.assertEqual(data.notationLine, 1)
        self.assertEqual(data.notationEffect, "ghost")
        self.assertEqual(data.stemDirection, 1)
        self.assertEqual(data.shortcut, "")

    def testRead_Old_Unrecognised_Drum(self):
        dataString = "g 72,100,ghost"
        head, data = dbfsv0.NoteHeadFieldV0.readHeadData("Xx", dataString)
        self.assertEqual(head, "g")
        self.assertEqual(data.midiNote, 72)
        self.assertEqual(data.midiVolume, 100)
        self.assertEqual(data.effect, "ghost")
        self.assertEqual(data.notationHead, "default")
        self.assertEqual(data.notationLine, 0)
        self.assertEqual(data.notationEffect, "none")
        self.assertEqual(data.stemDirection, 0)
        self.assertEqual(data.shortcut, "")

class TestNoteHeads(unittest.TestCase):
    def testReadHead(self):
        dataString = "x 72,100,ghost,cross,1,choke,1,c"
        drum = Drum("test", "td", "x")
        dbfsv0.NoteHeadFieldV0.readHeadData(drum.abbr, dataString)
        dbfsv0.DrumKitStructureV0.guessHeadData(drum)
        self.assertEqual(len(drum), 1)
        self.assertEqual(drum.head, "x")
        self.assertEqual(drum[0], "x")

    def testGuessHeadData_Unknown(self):
        drum = Drum("test", "td", "x")
        dbfsv0.DrumKitStructureV0.guessHeadData(drum)
        self.assertEqual(len(drum), 1)
        self.assertEqual(drum[0], "x")
        headData = drum.headData(None)
        self.assertEqual(headData.midiNote, DefaultKits.DEFAULT_NOTE)
        self.assertEqual(headData.midiVolume, DefaultKits.DEFAULT_VOLUME)
        self.assertEqual(headData.effect, "normal")
        self.assertEqual(headData.notationHead, "default")
        self.assertEqual(headData.notationLine, 0)
        self.assertEqual(headData.notationEffect, "none")
        self.assertEqual(headData.stemDirection, DefaultKits.STEM_UP)
        self.assertEqual(headData.shortcut, "x")

    def testGuessHeadData_Known(self):
        drum = Drum("HiTom", "HT", "o")
        dbfsv0.DrumKitStructureV0.guessHeadData(drum)
        self.assertEqual(list(drum), ["o", "O", "g", "f", "d"])
        headData = drum.headData(None)
        self.assertEqual(headData.midiNote, 50)


class TestDrum(unittest.TestCase):
    @staticmethod
    def makeDrum():
        drum = Drum("test", "td", "x")
        defaultHead = HeadData(shortcut = "y")
        drum.addNoteHead("x", defaultHead)
        newHead = HeadData(100)
        drum.addNoteHead("y", newHead)
        headData = HeadData(72, 100, "ghost", "cross", 1, "choke", 1, "c")
        drum.addNoteHead("z", headData)
        return drum, defaultHead, newHead

    def testWrite(self):
        drum, first_, second_ = self.makeDrum()
        second_.shortcut = "a"
        outstring = StringIO()
        indenter = fileUtils.Indenter(outstring)
        dbfsv0.DrumFieldV0("DRUM", getter = lambda _:drum).write_all(self, indenter)
        outlines = outstring.getvalue().splitlines()
        self.assertEqual(len(outlines), 4)
        self.assertEqual(outlines[0], "DRUM test,td,x,False")
        self.assertEqual(outlines[1],
                         "  NOTEHEAD x 71,96,normal,default,0,none,0,y")
        self.assertEqual(outlines[2],
                         "  NOTEHEAD y 100,96,normal,default,0,none,0,a")
        self.assertEqual(outlines[3],
                         "  NOTEHEAD z 72,100,ghost,cross,1,choke,1,c")


class TestDrumKit(unittest.TestCase):
    def testRead_NoNoteHeads(self):
        kitData = """KIT_START
        DRUM Snare,Sn,o,True
        DRUM Kick,Bd,o,True
        KIT_END
        """
        handle = StringIO(kitData)
        iterator = fileUtils.dbFileIterator(handle)
        kit = dbfsv0.DrumKitStructureV0().read(iterator)
        self.assertEqual(len(kit), 2)
        self.assertEqual(kit[0].name, "Snare")
        self.assertEqual(len(kit[0]), 6)
        self.assertEqual(kit[1].name, "Kick")
        self.assertEqual(len(kit[1]), 4)

    def testRead_BadLine(self):
        kitData = """KIT_START
        DRUM Snare,Sn,x,True
        NOTEHEAD x 1,100,default
        NOTEHEAD g 1,50,ghost
        DRUM Kick,Bd,o,True
        NOTEHEAD o 2,100,default
        NOTEHEAD O 2,127,accent
        BAD_LINE
        KIT_END
        """
        handle = StringIO(kitData)
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.UnrecognisedLine,
                          dbfsv0.DrumKitStructureV0().read, iterator)

    def testRead_OldNoteHeads(self):
        kitData = """KIT_START
        DRUM Snare,Sn,x,True
        NOTEHEAD x 1,100,default
        NOTEHEAD g 1,50,ghost
        DRUM Kick,Bd,o,True
        NOTEHEAD o 2,100,default
        NOTEHEAD O 2,127,accent
        KIT_END
        """
        handle = StringIO(kitData)
        iterator = fileUtils.dbFileIterator(handle)
        kit = dbfsv0.DrumKitStructureV0().read(iterator)
        self.assertEqual(len(kit), 2)
        self.assertEqual(kit[0].name, "Snare")
        self.assertEqual(len(kit[0]), 2)
        self.assertEqual(kit[1].name, "Kick")
        self.assertEqual(len(kit[1]), 2)

    def testRead_NewNoteHeads(self):
        kitData = """KIT_START
        DRUM Snare,Sn,x,True
        NOTEHEAD x 1,100,normal,default,0,none,0,x
        NOTEHEAD g 1,50,ghost,default,0,ghost,0,g
        DRUM Kick,Bd,o,True
        NOTEHEAD o 2,100,normal,default,-5,none,1,o
        NOTEHEAD O 2,127,accent,default,-5,accent,1,a
        KIT_END
        """
        handle = StringIO(kitData)
        iterator = fileUtils.dbFileIterator(handle)
        kit = dbfsv0.DrumKitStructureV0().read(iterator)
        self.assertEqual(len(kit), 2)
        self.assertEqual(len(kit), 2)
        self.assertEqual(kit[0].name, "Snare")
        self.assertEqual(len(kit[0]), 2)
        self.assertEqual(kit[1].name, "Kick")
        self.assertEqual(len(kit[1]), 2)

    def testNoteHeads(self):
        kitData = """KIT_START
        DRUM Snare,Sn,x,True
        NOTEHEAD x 1,100,default
        NOTEHEAD g 1,50,ghost
        DRUM Kick,Bd,o,True
        NOTEHEAD o 2,100,default
        NOTEHEAD O 2,127,accent
        KIT_END
        """
        handle = StringIO(kitData)
        iterator = fileUtils.dbFileIterator(handle)
        kit = dbfsv0.DrumKitStructureV0().read(iterator)
        self.assertEqual(kit.getDefaultHead(0), "x")
        self.assertEqual(kit.getDefaultHead(1), "o")
        self.assertEqual(kit.allowedNoteHeads(0),
                         ["x", "g"])
        self.assertEqual(kit.shortcutsAndNoteHeads(0), [("x", "x"), ("g", "g")])

    def testWrite(self):
        kit = DrumKit.DrumKit()
        drum = Drum("One", "d1", "x", True)
        drum.addNoteHead("x", HeadData())
        drum.addNoteHead("g",
                         HeadData(effect = "ghost", notationEffect = "ghost"))
        drum.checkShortcuts()
        kit.addDrum(drum)
        drum = Drum("Two", "d2", "o")
        drum.addNoteHead("o", HeadData(notationLine = -5, stemDirection = 1))
        drum.addNoteHead("O", HeadData(effect = "accent",
                                       notationEffect = "accent",
                                       notationLine = -5, stemDirection = 1))
        drum.checkShortcuts()
        kit.addDrum(drum)
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv0.DrumKitStructureV0().write(kit, indenter)
        outlines = handle.getvalue().splitlines()
        self.assertEqual(outlines,
                         ["KIT_START",
                          "  DRUM One,d1,x,True",
                          "    NOTEHEAD x 71,96,normal,default,0,none,0,x",
                          "    NOTEHEAD g 71,96,ghost,default,0,ghost,0,g",
                          "  DRUM Two,d2,o,False",
                          "    NOTEHEAD o 71,96,normal,default,-5,none,1,o",
                          "    NOTEHEAD O 71,96,accent,default,-5,accent,1,a",
                          "KIT_END"])

class TestFontOptions(unittest.TestCase):
    def testWrite(self):
        options = FontOptions.FontOptions()
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv0.FontOptionsStructureV0().write(options, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["FONT_OPTIONS_START",
                          "  NOTEFONT MS Shell Dlg 2",
                          "  NOTEFONTSIZE 10",
                          "  SECTIONFONT MS Shell Dlg 2",
                          "  SECTIONFONTSIZE 14",
                          "  METADATAFONT MS Shell Dlg 2",
                          "  METADATAFONTSIZE 16",
                          "FONT_OPTIONS_END"])

    def testRead(self):
        data = """FONT_OPTIONS_START
                  NOTEFONT mynotefont
                  NOTEFONTSIZE 8
                  SECTIONFONT sectionfont
                  SECTIONFONTSIZE 12
                  METADATAFONT metafont
                  METADATAFONTSIZE 14
                FONT_OPTIONS_END"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        options = dbfsv0.FontOptionsStructureV0().read(iterator)
        self.assertEqual(options.noteFont, "mynotefont")
        self.assertEqual(options.noteFontSize, 8)
        self.assertEqual(options.sectionFont, "sectionfont")
        self.assertEqual(options.sectionFontSize, 12)
        self.assertEqual(options.metadataFont, "metafont")
        self.assertEqual(options.metadataFontSize, 14)

class TestMetaData(unittest.TestCase):
    def testWrite(self):
        meta = ScoreMetaData.ScoreMetaData()
        meta.makeEmpty()
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv0.MetadataStructureV0().write(meta, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["SCORE_METADATA",
                          "  TITLE Untitled",
                          "  ARTIST Unknown",
                          "  ARTISTVISIBLE True",
                          "  CREATOR Nobody",
                          "  CREATORVISIBLE True",
                          "  BPM 120",
                          "  BPMVISIBLE True",
                          "  WIDTH 80",
                          "  KITDATAVISIBLE True",
                          "  METADATAVISIBLE True",
                          "  BEATCOUNTVISIBLE True",
                          "  EMPTYLINESVISIBLE True",
                          "  MEASURECOUNTSVISIBLE False",
                          "END_SCORE_METADATA"])

    def testRead(self):
        data = """SCORE_METADATA
                    TITLE Song
                    ARTIST xxx
                    ARTISTVISIBLE False
                    CREATOR zzz
                    CREATORVISIBLE False
                    BPM 200
                    BPMVISIBLE False
                    WIDTH 100
                    KITDATAVISIBLE False
                    METADATAVISIBLE False
                    BEATCOUNTVISIBLE False
                    EMPTYLINESVISIBLE False
                    MEASURECOUNTSVISIBLE True
                  END_SCORE_METADATA"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        meta = dbfsv0.MetadataStructureV0().read(iterator)
        self.assertEqual(meta.title, "Song")
        self.assertEqual(meta.artist, "xxx")
        self.assertEqual(meta.artistVisible, False)
        self.assertEqual(meta.creator, "zzz")
        self.assertEqual(meta.creatorVisible, False)
        self.assertEqual(meta.bpm, 200)
        self.assertEqual(meta.bpmVisible, False)
        self.assertEqual(meta.width, 100)
        self.assertEqual(meta.kitDataVisible, False)
        self.assertEqual(meta.metadataVisible, False)
        self.assertEqual(meta.beatCountVisible, False)
        self.assertEqual(meta.emptyLinesVisible, False)
        self.assertEqual(meta.measureCountsVisible, True)

    def testBadRead(self):
        data = """SCORE_METADATA
                    TITLE Song
                    ARTIST xxx
                    ARTISTVISIBLE False
                    BAD LINE
                    CREATOR zzz
                    CREATORVISIBLE False
                    BPM 200
                    BPMVISIBLE False
                    WIDTH 100
                    KITDATAVISIBLE False
                    METADATAVISIBLE False
                    BEATCOUNTVISIBLE False
                    EMPTYLINESVISIBLE False
                  END_SCORE_METADATA"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.UnrecognisedLine,
                          dbfsv0.MetadataStructureV0().read, iterator)

    def testBadBpm(self):
        data = """SCORE_METADATA
                    TITLE Song
                    ARTIST xxx
                    ARTISTVISIBLE False
                    CREATOR zzz
                    CREATORVISIBLE False
                    BPM qqq
                    BPMVISIBLE False
                    WIDTH 100
                    KITDATAVISIBLE False
                    METADATAVISIBLE False
                    BEATCOUNTVISIBLE False
                    EMPTYLINESVISIBLE False
                  END_SCORE_METADATA"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.InvalidInteger,
                          dbfsv0.MetadataStructureV0().read, iterator)

    def testNegativeBpm(self):
        data = """SCORE_METADATA
                    TITLE Song
                    ARTIST xxx
                    ARTISTVISIBLE False
                    CREATOR zzz
                    CREATORVISIBLE False
                    BPM -1
                    BPMVISIBLE False
                    WIDTH 100
                    KITDATAVISIBLE False
                    METADATAVISIBLE False
                    BEATCOUNTVISIBLE False
                    EMPTYLINESVISIBLE False
                  END_SCORE_METADATA"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.InvalidPositiveInteger,
                          dbfsv0.MetadataStructureV0().read, iterator)

    def testBadWidth(self):
        data = """SCORE_METADATA
                    TITLE Song
                    ARTIST xxx
                    ARTISTVISIBLE False
                    CREATOR zzz
                    CREATORVISIBLE False
                    BPM 200
                    BPMVISIBLE False
                    WIDTH zzz
                    KITDATAVISIBLE False
                    METADATAVISIBLE False
                    BEATCOUNTVISIBLE False
                    EMPTYLINESVISIBLE False
                  END_SCORE_METADATA"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.InvalidInteger,
                          dbfsv0.MetadataStructureV0().read, iterator)

    def testNegativeWidth(self):
        data = """SCORE_METADATA
                    TITLE Song
                    ARTIST xxx
                    ARTISTVISIBLE False
                    CREATOR zzz
                    CREATORVISIBLE False
                    BPM 200
                    BPMVISIBLE False
                    WIDTH -1
                    KITDATAVISIBLE False
                    METADATAVISIBLE False
                    BEATCOUNTVISIBLE False
                    EMPTYLINESVISIBLE False
                  END_SCORE_METADATA"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.InvalidPositiveInteger,
                         dbfsv0.MetadataStructureV0().read, iterator)



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
