'''
Created on 4 Apr 2012

@author: Mike Thomas

'''
from __future__ import print_function
from contextlib import contextmanager

import sys

class Indenter(object):
    def __init__(self, spaces = 2):
        self._spaces = spaces
        self._level = 0
        self._handle = sys.stdout

    def __call__(self, *args, **kwargs):
        self.write(*args, **kwargs)

    def increase(self):
        self._level += self._spaces

    def decrease(self):
        self._level -= self._spaces

    def setHandle(self, handle):
        self._handle = handle

    def write(self, *args, **kwargs):
        print(" " * self._level, end = '', file = self._handle)
        print(*args, **kwargs)

def makeLilyContext(opener, closer):
    def myLilyContext(indenter, context):
        indenter.write(" ".join(x for x in [context, opener] if x))
        indenter.increase()
        yield
        indenter.decrease()
        indenter.write(closer)
    return myLilyContext

LilyContext = contextmanager(makeLilyContext("{", "}"))
VoiceContext = contextmanager(makeLilyContext("<<", ">>"))

def lilyString(inString):
    return '"%s"' % inString

class LilyMeasure(object):
    def __init__(self, score, measure):
        self.measure = measure
        self.score = score

    def voiceOne(self, indenter):
        indenter("bd1")

    def voiceTwo(self, indenter):
        indenter("sn1")

class LilypondScore(object):
    def __init__(self, score):
        self.score = score
        self.kit = score.drumKit
        self.scoreData = score.scoreData
        self.indenter = Indenter()

    def write(self, handle):
        self.indenter.setHandle(handle)
        self.indenter(r'\version "2.12.3"')
        with LilyContext(self.indenter, '\header'):
            self._writeHeader()
        with LilyContext(self.indenter, '\score'):
            self._writeScore()

    def _writeHeader(self):
        self.indenter('title = %s' % lilyString(self.scoreData.title))
        if self.scoreData.artistVisible:
            self.indenter('composer = %s' % lilyString(self.scoreData.artist))
        if self.scoreData.creatorVisible:
            self.indenter('arranger = %s' % lilyString(self.scoreData.creator))

    def _writeScore(self):
        with VoiceContext(self.indenter, r'\new DrumStaff'):
            self._writeDrumStaffInfo()
            with LilyContext(self.indenter, r'\drummode'):
                self._writeMusic()
        self.indenter(r'\layout {}')

    def _writeDrumStaffInfo(self):
        self.indenter(r'\set Staff.instrumentName = #"Drums"')
        if self.scoreData.bpmVisible:
            self.indenter(r'\tempo 4 = %d' % self.scoreData.bpm)
        #self.indenter(r'\set DrumStaff.drumStyleTable = #(alist->hash-table mydrums)')
        self.indenter(r"\override Score.RehearsalMark #'self-alignment-X = #LEFT")

    def _writeMusic(self):
        measureIterator = self.score.iterMeasures()
        sectionTitle = self.score.getSectionTitle(0)
        sectionIndex = 0
        repeatCommands = []
        try:
            measure = measureIterator.next()
            hasAlternate = False
            while True:
                if sectionTitle:
                    self.indenter(r'\mark %s' % lilyString(sectionTitle))
                if measure.isRepeatStart():
                    repeatCommands.append("start-repeat")
                if measure.alternateText is not None:
                    if hasAlternate:
                        repeatCommands.append("(volta #f)")
                    repeatCommands.append("(volta %s)" % lilyString(measure.alternateText))
                    hasAlternate = True
                if repeatCommands:
                    self.indenter(r"\set Score.repeatCommands = #'(%s)" % " ".join(repeatCommands))
                    repeatCommands = []
                with VoiceContext(self.indenter, ""):
                    self._writeMeasure(measure)
                if measure.isRepeatEnd():
                    if measure.repeatCount > 2:
                        self.indenter(r"\once \override Score.RehearsalMark #'self-alignment-X = #right")
                        self.indenter(r'\mark %s' % lilyString("x%d" % measure.repeatCount))
                    repeatCommands.append("end-repeat")
                if measure.isSectionEnd():
                    sectionIndex += 1
                    if sectionIndex < self.score.numSections():
                        sectionTitle = self.score.getSectionTitle(sectionIndex)
                else:
                    sectionTitle = None
                if hasAlternate and (measure.isSectionEnd() or measure.isRepeatEnd()):
                    repeatCommands.append("(volta #f)")
                    hasAlternate = False
                if measure.isLineEnd() or measure.isSectionEnd():
                    self.indenter(r'\break')
                measure = measureIterator.next()
        except StopIteration:
            if repeatCommands:
                self.indenter(r"\set Score.repeatCommands = #'(%s)" % " ".join(repeatCommands))

    def _writeMeasure(self, measure):
        parsed = LilyMeasure(self.score, measure)
        with LilyContext(self.indenter, r'\new DrumVoice'):
            self.indenter(r'\voiceOne')
            parsed.voiceOne(self.indenter)
        with LilyContext(self.indenter, r'\new DrumVoice'):
            self.indenter(r'\voiceTwo')
            parsed.voiceTwo(self.indenter)


def test():
    import Data.Score
    score = Data.Score.ScoreFactory.loadScore('C:\Users\Mike_2\Dropbox\Drum music\Breakout.brp')
    lyScore = LilypondScore(score)
    lyScore.write(sys.stdout)

if __name__ == "__main__":
    test()

