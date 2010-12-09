'''
Created on 31 Jul 2010

@author: Mike Thomas

'''
from Line import Line
from Instrument import Instrument
from Constants import MEASURE_SPLIT
from Note import Note

class Score(object):
    '''
    classdocs
    '''

    DefaultKit = [Instrument("Foot Hat", "x", "Fo"),
                   Instrument("Bass", "o", "Bd"),
                   Instrument("Low Tom", "o", "LT"),
                   Instrument("Snare", "o"),
                   Instrument("Mid Tom", "o", "MT"),
                   Instrument("High Tom", "o", "HT"),
                   Instrument("Ride", "x"),
                   Instrument("HiHat", "x", "hh"),
                   Instrument("Crash", "x")
                   ]

    def __init__(self, songLength = 0):
        '''
        Constructor
       
        >>> score= Score()
        >>> len(score)
        0
        '''
        self._lines = {}
        self._instrumentOrder = []
        self.songLength = songLength

    def __iter__(self):
        '''
        Iterate over the Lines in this Score.
        '''
        for index in xrange(0, len(self)):
            yield self[index]

    def __len__(self):
        '''
        Return the number of Lines in this Score.
        '''
        return len(self._lines)

    def __getitem__(self, subscript):
        '''
        Return a given Line from this Score. 
        '''
        if isinstance(subscript, int):
            return self._lines[self._instrumentOrder[subscript]]
        else:
            return self._lines[subscript]

    @property
    def numLines(self):
        return len(self._lines)

    def addNote(self, noteTime, line, head = None):
        '''
        
        '''
        if not isinstance(line, Line):
            line = self[line]
        line.addNote(noteTime, head)
        return self.getNote(noteTime, line)

    def delNote(self, noteTime, line):
        if not isinstance(line, Line):
            line = self[line]
        line.delNote(noteTime)

    def getNote(self, noteTime, line):
        if not isinstance(line, Line):
            line = self[line]
        return line.noteAtTime(noteTime)

    def appendInstrument(self, instr):
        '''
        Append an Instrument to this score.
        
        @type instr: Data.Instrument.Instrument
        '''
        self._lines[instr.name] = Line(instr)
        self._instrumentOrder.append(instr.name)

    def setInstruments(self, instrumentList):
        '''
        Set the instruments in the score, and their order in the systems.
        
        @type instrumentList: list        
        '''
        self._instrumentOrder = [instr.name for instr in instrumentList]
        for instr in instrumentList:
            if instr.name not in self._lines:
                self._lines[instr.name] = Line(instr)
        iSet = set(instr.name for instr in instrumentList)
        badLines = [line for line in self._lines.itervalues()
                    if line.instrument.name not in iSet]
        for line in badLines:
            self._lines.pop(line.instrument.name)

    def lineHead(self, line):
        return self[line].defaultHead()

    def iterNotes(self):
        '''
        Iterate over the notes in this Score, in time order.
        
        Each note returned is a Note object.
        '''
        notes = []
        for lineIndex in range(0, len(self)):
            line = self[lineIndex]
            notes.extend(Note(noteTime, lineIndex, noteHead)
                         for noteTime, noteHead in line)
        notes.sort()
        for note in notes:
            if note.time < self.songLength - 1:
                yield note
            else:
                break
        yield Note(self.songLength - 1, 0, MEASURE_SPLIT)

    def setMeasureLine(self, measureTime):
        line = self[0]
        line.addNote(measureTime, MEASURE_SPLIT)

    def loadDefaultKit(self):
        self.setInstruments(Score.DefaultKit)

def makeEmptyScore(numBars = 8, barLengths = 16, scoreClass = Score):
    score = scoreClass(numBars * (barLengths + 1))
    score.loadDefaultKit()
    for i in range(0, numBars):
        score.setMeasureLine((i + 1) * (barLengths + 1) - 1)
    return score
