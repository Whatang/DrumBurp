'''
Created on Dec 15, 2012

@author: Mike
'''
import unittest
from cStringIO import StringIO
from Data.ASCIISettings import ASCIISettings
from Data import DrumKit, Drum, MeasureCount
from Data.Score import Score
from Data.NotePosition import NotePosition
from Notation.AsciiExport import Exporter, getExportDate
# pylint:disable-msg=C0301

class TestExport(unittest.TestCase):
    exportDate = getExportDate()
    @staticmethod
    def getOutput(score, settings):
        handle = StringIO()
        exporter = Exporter(score, settings)
        exporter.export(handle)
        return handle.getvalue().splitlines()

    def testEmpty(self):
        score = Score()
        settings = ASCIISettings()
        output = self.getOutput(score, settings)
        self.assertEqual(output,
                         ['Tabbed with DrumBurp, a drum tab editor from www.whatang.org',
                          'Title     : ',
                          'Artist    : ',
                          'BPM       : 120',
                          'Tabbed by : ',
                          'Date      : ' + self.exportDate,
                          '',
                          '',
                          '',
                          'Tabbed with DrumBurp, a drum tab editor from www.whatang.org'])

    def testWithKit(self):
        score = Score()
        settings = ASCIISettings()
        score.drumKit = DrumKit.DrumKit()
        score.drumKit.addDrum(Drum.Drum("HiHat", "Hh", "x"))
        score.drumKit.addDrum(Drum.Drum("Crash", "Cr", "x"))
        output = self.getOutput(score, settings)
        self.assertEqual(output,
                         ['Tabbed with DrumBurp, a drum tab editor from www.whatang.org',
                          'Title     : ',
                          'Artist    : ',
                          'BPM       : 120',
                          'Tabbed by : ',
                          'Date      : ' + self.exportDate,
                          '',
                          'Cr - Crash',
                          'Hh - HiHat',
                          '',
                          '',
                          'Tabbed with DrumBurp, a drum tab editor from www.whatang.org'])

    def testSingleMeasure(self):
        score = Score()
        settings = ASCIISettings()
        settings.omitEmpty = False
        score.drumKit = DrumKit.DrumKit()
        score.drumKit.addDrum(Drum.Drum("HiHat", "Hh", "x"))
        score.drumKit.addDrum(Drum.Drum("Crash", "Cr", "x"))
        counter = MeasureCount.counterMaker(4, 16)
        score.insertMeasureByIndex(16, counter = counter)
        output = self.getOutput(score, settings)
        self.assertEqual(output,
                         ['Tabbed with DrumBurp, a drum tab editor from www.whatang.org',
                          'Title     : ',
                          'Artist    : ',
                          'BPM       : 120',
                          'Tabbed by : ',
                          'Date      : ' + self.exportDate,
                          '',
                          'Cr - Crash',
                          'Hh - HiHat',
                          '',
                          'Cr|----------------|',
                          'Hh|----------------|',
                          '   1e+a2e+a3e+a4e+a ',
                          '',
                          'Tabbed with DrumBurp, a drum tab editor from www.whatang.org'])

    def testMultiMeasures(self):
        score = Score()
        settings = ASCIISettings()
        settings.omitEmpty = False
        score.drumKit = DrumKit.DrumKit()
        score.drumKit.addDrum(Drum.Drum("HiHat", "Hh", "x"))
        score.drumKit.addDrum(Drum.Drum("Crash", "Cr", "x"))
        counter = MeasureCount.counterMaker(4, 16)
        score.insertMeasureByIndex(16, counter = counter)
        score.insertMeasureByIndex(16, counter = counter)
        score.insertMeasureByIndex(16, counter = counter)
        score.addNote(NotePosition(0, 0, 0, 0), "x")
        score.addNote(NotePosition(0, 1, 0, 0), "y")
        score.addNote(NotePosition(0, 2, 0, 0), "z")
        output = self.getOutput(score, settings)
        self.assertEqual(output,
                         ['Tabbed with DrumBurp, a drum tab editor from www.whatang.org',
                          'Title     : ',
                          'Artist    : ',
                          'BPM       : 120',
                          'Tabbed by : ',
                          'Date      : ' + self.exportDate,
                          '',
                          'Cr - Crash',
                          'Hh - HiHat',
                          '',
                          'Cr|----------------|----------------|----------------|',
                          'Hh|x---------------|y---------------|z---------------|',
                          '   1e+a2e+a3e+a4e+a 1e+a2e+a3e+a4e+a 1e+a2e+a3e+a4e+a ',
                          '',
                          'Tabbed with DrumBurp, a drum tab editor from www.whatang.org'])

    def testStaffs(self):
        score = Score()
        settings = ASCIISettings()
        settings.omitEmpty = False
        score.drumKit = DrumKit.DrumKit()
        score.drumKit.addDrum(Drum.Drum("HiHat", "Hh", "x"))
        score.drumKit.addDrum(Drum.Drum("Crash", "Cr", "x"))
        counter = MeasureCount.counterMaker(4, 16)
        score.insertMeasureByIndex(16, counter = counter)
        score.insertMeasureByIndex(16, counter = counter)
        score.insertMeasureByIndex(16, counter = counter)
        score.addNote(NotePosition(0, 0, 0, 0), "x")
        score.addNote(NotePosition(0, 1, 0, 0), "y")
        score.addNote(NotePosition(0, 2, 0, 0), "z")
        score.formatScore(40)
        output = self.getOutput(score, settings)
        self.assertEqual(output,
                         ['Tabbed with DrumBurp, a drum tab editor from www.whatang.org',
                          'Title     : ',
                          'Artist    : ',
                          'BPM       : 120',
                          'Tabbed by : ',
                          'Date      : ' + self.exportDate,
                          '',
                          'Cr - Crash',
                          'Hh - HiHat',
                          '',
                          'Cr|----------------|----------------|',
                          'Hh|x---------------|y---------------|',
                          '   1e+a2e+a3e+a4e+a 1e+a2e+a3e+a4e+a ',
                          '',
                          'Cr|----------------|',
                          'Hh|z---------------|',
                          '   1e+a2e+a3e+a4e+a ',
                          '',
                          'Tabbed with DrumBurp, a drum tab editor from www.whatang.org'])

    def testSections(self):
        score = Score()
        settings = ASCIISettings()
        settings.omitEmpty = False
        score.drumKit = DrumKit.DrumKit()
        score.drumKit.addDrum(Drum.Drum("HiHat", "Hh", "x"))
        score.drumKit.addDrum(Drum.Drum("Crash", "Cr", "x"))
        counter = MeasureCount.counterMaker(4, 16)
        score.insertMeasureByIndex(16, counter = counter)
        score.insertMeasureByIndex(16, counter = counter)
        score.insertMeasureByIndex(16, counter = counter)
        score.addNote(NotePosition(0, 0, 0, 0), "x")
        score.addNote(NotePosition(0, 1, 0, 0), "y")
        score.addNote(NotePosition(0, 2, 0, 0), "z")
        score.setSectionEnd(NotePosition(0, 1), True)
        score.setSectionTitle(0, "Section 1")
        score.formatScore(40)
        score.setSectionEnd(NotePosition(1, 0), True)
        score.setSectionTitle(1, "Section 2")
        score.formatScore(40)
        output = self.getOutput(score, settings)
        self.assertEqual(output,
                         ['Tabbed with DrumBurp, a drum tab editor from www.whatang.org',
                          'Title     : ',
                          'Artist    : ',
                          'BPM       : 120',
                          'Tabbed by : ',
                          'Date      : ' + self.exportDate,
                          '',
                          'Cr - Crash',
                          'Hh - HiHat',
                          '',
                          'Section 1',
                          '~~~~~~~~~',
                          '',
                          'Cr|----------------|----------------|',
                          'Hh|x---------------|y---------------|',
                          '   1e+a2e+a3e+a4e+a 1e+a2e+a3e+a4e+a ',
                          '',
                          '',
                          'Section 2',
                          '~~~~~~~~~',
                          '',
                          'Cr|----------------|',
                          'Hh|z---------------|',
                          '   1e+a2e+a3e+a4e+a ',
                          '',
                          'Tabbed with DrumBurp, a drum tab editor from www.whatang.org'])

    def testRepeats(self):
        score = Score()
        settings = ASCIISettings()
        settings.omitEmpty = False
        score.drumKit = DrumKit.DrumKit()
        score.drumKit.addDrum(Drum.Drum("HiHat", "Hh", "x"))
        score.drumKit.addDrum(Drum.Drum("Crash", "Cr", "x"))
        counter = MeasureCount.counterMaker(4, 16)
        score.insertMeasureByIndex(16, counter = counter)
        score.insertMeasureByIndex(16, counter = counter)
        score.insertMeasureByIndex(16, counter = counter)
        score.addNote(NotePosition(0, 0, 0, 0), "x")
        score.addNote(NotePosition(0, 1, 0, 0), "y")
        score.addNote(NotePosition(0, 2, 0, 0), "z")
        score.getMeasure(0).setRepeatStart(True)
        score.getMeasure(0).setRepeatEnd(True)
        score.formatScore(40)
        output = self.getOutput(score, settings)
        self.assertEqual(output,
                         ['Tabbed with DrumBurp, a drum tab editor from www.whatang.org',
                          'Title     : ',
                          'Artist    : ',
                          'BPM       : 120',
                          'Tabbed by : ',
                          'Date      : ' + self.exportDate,
                          '',
                          'Cr - Crash',
                          'Hh - HiHat',
                          '',
                          '  /-------------2x-\                ',
                          'Cr|----------------|----------------|',
                          'Hh|x---------------|y---------------|',
                          '   1e+a2e+a3e+a4e+a 1e+a2e+a3e+a4e+a ',
                          '',
                          'Cr|----------------|',
                          'Hh|z---------------|',
                          '   1e+a2e+a3e+a4e+a ',
                          '',
                          'Tabbed with DrumBurp, a drum tab editor from www.whatang.org'])

    def testAdjacentRepeats(self):
        score = Score()
        settings = ASCIISettings()
        settings.omitEmpty = False
        score.drumKit = DrumKit.DrumKit()
        score.drumKit.addDrum(Drum.Drum("HiHat", "Hh", "x"))
        score.drumKit.addDrum(Drum.Drum("Crash", "Cr", "x"))
        counter = MeasureCount.counterMaker(4, 16)
        score.insertMeasureByIndex(16, counter = counter)
        score.insertMeasureByIndex(16, counter = counter)
        score.insertMeasureByIndex(16, counter = counter)
        score.addNote(NotePosition(0, 0, 0, 0), "x")
        score.addNote(NotePosition(0, 1, 0, 0), "y")
        score.addNote(NotePosition(0, 2, 0, 0), "z")
        score.getMeasure(0).setRepeatStart(True)
        score.getMeasure(0).setRepeatEnd(True)
        score.getMeasure(1).setRepeatStart(True)
        score.getMeasure(1).setRepeatEnd(True)
        score.getMeasure(1).repeatCount = 3
        score.formatScore(40)
        output = self.getOutput(score, settings)
        self.assertEqual(output,
                         ['Tabbed with DrumBurp, a drum tab editor from www.whatang.org',
                          'Title     : ',
                          'Artist    : ',
                          'BPM       : 120',
                          'Tabbed by : ',
                          'Date      : ' + self.exportDate,
                          '',
                          'Cr - Crash',
                          'Hh - HiHat',
                          '',
                          '  /-------------2x-\\/------------3x-\\',
                          'Cr|----------------|----------------|',
                          'Hh|x---------------|y---------------|',
                          '   1e+a2e+a3e+a4e+a 1e+a2e+a3e+a4e+a ',
                          '',
                          'Cr|----------------|',
                          'Hh|z---------------|',
                          '   1e+a2e+a3e+a4e+a ',
                          '',
                          'Tabbed with DrumBurp, a drum tab editor from www.whatang.org'])

    def testAlternates(self):
        score = Score()
        settings = ASCIISettings()
        settings.omitEmpty = False
        score.drumKit = DrumKit.DrumKit()
        score.drumKit.addDrum(Drum.Drum("HiHat", "Hh", "x"))
        score.drumKit.addDrum(Drum.Drum("Crash", "Cr", "x"))
        counter = MeasureCount.counterMaker(4, 16)
        score.insertMeasureByIndex(16, counter = counter)
        score.insertMeasureByIndex(16, counter = counter)
        score.insertMeasureByIndex(16, counter = counter)
        score.addNote(NotePosition(0, 0, 0, 0), "x")
        score.addNote(NotePosition(0, 1, 0, 0), "y")
        score.addNote(NotePosition(0, 2, 0, 0), "z")
        score.getMeasure(0).setRepeatStart(True)
        score.getMeasure(0).setRepeatEnd(True)
        score.getMeasure(0).alternateText = "1."
        score.getMeasure(1).setRepeatEnd(True)
        score.getMeasure(1).alternateText = "2."
        score.formatScore(40)
        output = self.getOutput(score, settings)
        self.assertEqual(output,
                         ['Tabbed with DrumBurp, a drum tab editor from www.whatang.org',
                          'Title     : ',
                          'Artist    : ',
                          'BPM       : 120',
                          'Tabbed by : ',
                          'Date      : ' + self.exportDate,
                          '',
                          'Cr - Crash',
                          'Hh - HiHat',
                          '',
                          '  /1.______________\\2.______________\\',
                          'Cr|----------------|----------------|',
                          'Hh|x---------------|y---------------|',
                          '   1e+a2e+a3e+a4e+a 1e+a2e+a3e+a4e+a ',
                          '',
                          'Cr|----------------|',
                          'Hh|z---------------|',
                          '   1e+a2e+a3e+a4e+a ',
                          '',
                          'Tabbed with DrumBurp, a drum tab editor from www.whatang.org'])

    def testRepeatAcrossStaff(self):
        score = Score()
        settings = ASCIISettings()
        settings.omitEmpty = False
        score.drumKit = DrumKit.DrumKit()
        score.drumKit.addDrum(Drum.Drum("HiHat", "Hh", "x"))
        score.drumKit.addDrum(Drum.Drum("Crash", "Cr", "x"))
        counter = MeasureCount.counterMaker(4, 16)
        score.insertMeasureByIndex(16, counter = counter)
        score.insertMeasureByIndex(16, counter = counter)
        score.insertMeasureByIndex(16, counter = counter)
        score.addNote(NotePosition(0, 0, 0, 0), "x")
        score.addNote(NotePosition(0, 1, 0, 0), "y")
        score.addNote(NotePosition(0, 2, 0, 0), "z")
        score.getMeasure(0).setRepeatStart(True)
        score.getMeasure(2).setRepeatEnd(True)
        score.formatScore(40)
        output = self.getOutput(score, settings)
        self.assertEqual(output,
                         ['Tabbed with DrumBurp, a drum tab editor from www.whatang.org',
                          'Title     : ',
                          'Artist    : ',
                          'BPM       : 120',
                          'Tabbed by : ',
                          'Date      : ' + self.exportDate,
                          '',
                          'Cr - Crash',
                          'Hh - HiHat',
                          '',
                          '  /----------------------------------',
                          'Cr|----------------|----------------|',
                          'Hh|x---------------|y---------------|',
                          '   1e+a2e+a3e+a4e+a 1e+a2e+a3e+a4e+a ',
                          '',
                          '  --------------2x-\\',
                          'Cr|----------------|',
                          'Hh|z---------------|',
                          '   1e+a2e+a3e+a4e+a ',
                          '',
                          'Tabbed with DrumBurp, a drum tab editor from www.whatang.org'])




if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
