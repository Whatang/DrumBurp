'''
Created on Apr 9, 2016

@author: mike_000
'''
import unittest
from io import StringIO
from Notation import lilypond
from Data.DrumKitFactory import DrumKitFactory
from Data.Counter import CounterRegistry
from Data.Measure import Measure
from Data.MeasureCount import MeasureCount

_REG = CounterRegistry()


class TestCompoundSticking(unittest.TestCase):
    def setUp(self):
        self.kit = DrumKitFactory.getNamedDefaultKit()
        self.lilykit = lilypond.LilyKit(self.kit)
        self.indenter = lilypond.LilyIndenter()
        self.output = StringIO.StringIO()
        self.indenter.setHandle(self.output)
        self.measure = Measure()
        counter = _REG.getCounterByName("Triplets")
        mc = MeasureCount()
        mc.addSimpleBeats(counter, 4)
        self.measure.setBeatCount(mc)

    def testCompoundSticking(self):
        self.measure.setAbove(0, "L")
        self.measure.setAbove(1, "R")
        self.measure.setAbove(2, "L")
        lilyMeasure = lilypond.LilyMeasure(self.measure, self.lilykit)
        lilyMeasure.sticking(self.indenter)
        output = self.output.getvalue().strip()
        self.assertEqual(output,
                         r'\new Lyrics \with { alignAboveContext = #"main" } \lyricmode { \times 2/3 { L8 R8 L8 } " "4 " "4 " "4 }')

    def testCompoundStickingAtEndOfMeasure(self):
        self.measure.setAbove(9, "L")
        self.measure.setAbove(10, "R")
        self.measure.setAbove(11, "L")
        lilyMeasure = lilypond.LilyMeasure(self.measure, self.lilykit)
        lilyMeasure.sticking(self.indenter)
        output = self.output.getvalue().strip()
        self.assertEqual(output,
                         r'\new Lyrics \with { alignAboveContext = #"main" } \lyricmode { " "4 " "4 " "4 \times 2/3 { L8 R8 L8 } }')


if __name__ == "__main__":
    unittest.main()
