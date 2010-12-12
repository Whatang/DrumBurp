'''
Created on 31 Jul 2010

@author: Mike Thomas

'''
from Line import Line
from Instrument import Instrument
from Constants import MEASURE_SPLIT
from Note import Note
import os
import csv

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
        self._songLength = songLength

    def __iter__(self):
        '''
        Iterate over the Lines in this Score.
        '''
        for index in xrange(0, self.numLines):
            yield self[index]

    def __len__(self):
        '''
        Return the number of Lines in this Score.
        '''
        return self._songLength

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

    def addTime(self, time):
        self._songLength += time

    def addNote(self, noteTime, line, head = None):
        assert(0 <= noteTime < len(self) - 1)
        assert(self[0].noteAtTime(noteTime) != MEASURE_SPLIT)
        if not isinstance(line, Line):
            line = self[line]
        line.addNote(noteTime, head)
        return self.getNote(noteTime, line)

    def delNote(self, noteTime, line):
        assert(self[0].noteAtTime(noteTime) != MEASURE_SPLIT)
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
        for lineIndex in range(0, self.numLines):
            line = self[lineIndex]
            notes.extend(Note(noteTime, lineIndex, noteHead)
                         for noteTime, noteHead in line)
        notes.sort()
        for note in notes:
            yield note
        yield Note(self._songLength - 1, 0, MEASURE_SPLIT)

    def setMeasureLine(self, measureTime):
        line = self[0]
        line.addNote(measureTime, MEASURE_SPLIT)

    def loadDefaultKit(self):
        self.setInstruments(Score.DefaultKit)

    def save(self, handle):
        handle.write("NUM_LINES=%d" % self.numLines)
        handle.write(os.linesep)
        handle.write("SONG_LENGTH=%d" % self._songLength)
        handle.write(os.linesep)
        handle.write("END OF HEADER")
        handle.write(os.linesep)
        writer = csv.writer(handle)
        for line in self:
            instr = line.instrument
            writer.writerow([instr.name, instr.abbr, instr.head])
        handle.write("END OF INSTRUMENTS")
        handle.write(os.linesep)
        for note in self.iterNotes():
            if note.time == len(self) - 1:
                break
            writer.writerow([note.time,
                             note.lineIndex, note.head])

def loadScore(handle):
    songLength = None
    numLines = None
    for line in handle:
        line = line.strip()
        if line == "END OF HEADER":
            break
        fields = line.split("=")
        assert(len(fields) == 2)
        if fields[0] == "NUM_LINES":
            numLines = int(fields[1])
        elif fields[0] == "SONG_LENGTH":
            songLength = int(fields[1])
    assert(numLines is not None and songLength is not None)
    assert(numLines >= 0 and songLength >= 0)
    score = Score(songLength = songLength)
    reader = csv.reader(handle)
    for lineNum, row in enumerate(reader):
        if lineNum == numLines:
            assert(row[0] == "END OF INSTRUMENTS")
            break
        instr = Instrument(name = row[0], abbr = row[1], head = row[2])
        score.appendInstrument(instr)
    for row in reader:
        score.addNote(int(row[0]), int(row[1]), row[2])
    return score

def makeEmptyScore(numBars = 8, barLengths = 16, scoreClass = Score):
    score = scoreClass(numBars * (barLengths + 1))
    score.loadDefaultKit()
    for i in range(1, numBars):
        score.setMeasureLine(i * (barLengths + 1) - 1)
    return score
