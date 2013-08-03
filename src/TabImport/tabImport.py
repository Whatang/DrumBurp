'''
Created on Aug 3, 2013

@author: mike_000
'''

from Data.NotePosition import NotePosition
from Data.Score import ScoreFactory
from Data.Drum import Drum, HeadData
from Data.DrumKit import DrumKit
from Data import MeasureCount

import itertools

class DrumStaffGuess(object):
    def __init__(self):
        self._lines = []
        self._barPositions = []

    def num_lines(self):
        return len(self._lines)

    def __iter__(self):
        return iter(self._lines)

    def get_line_by_prefix(self):
        pass

    def add_line(self, line):
        if self._lines:
            thisLineIndexes = [index for index, char in enumerate(line.line)
                               if char == line.BARLINE]
            if thisLineIndexes != self._barPositions:
                return False
        else:
            self._barPositions = [index for index, char in enumerate(line.line)
                                  if char == line.BARLINE]
        self._lines.append(line)
        return True

    def iterMeasures(self):
        bar_iterator = itertools.izip(self._barPositions[:-1], self._barPositions[1:])
        for start, end in bar_iterator:
            yield [DrumLineGuess(line.prefix, line.line[start + 1:end])
                   for line in self]

class DrumLineGuess(object):
    BARLINE = "|"
    EMPTY_NOTE = "-"
    FORBIDDEN = set(" ")
    def __init__(self, prefix, line):
        self.prefix = prefix
        self.line = line
        
    @classmethod
    def recognize(cls, line):
        barCount = line.count(cls.BARLINE)
        if barCount < 2:
            return None
        start = line.index(cls.BARLINE)
        end = line.rindex(cls.BARLINE)
        lineData = line[start:end + 1]
        for char in lineData:
            if char in cls.FORBIDDEN:
                return None
        prefix = line[:start].strip()
        if not prefix:
            return None
        return cls(prefix, lineData)

class DrumKitGuess(object):
    def __init__(self):
        self._heads = {}
        self._order = []

    def __iter__(self):
        return iter(self._order)

    def note_heads(self, prefix):
        return list(self._heads[prefix])

    def add_drum(self, prefix):
        if prefix in self._order:
            return
        self._order.append(prefix)
        self._heads[prefix] = []

    def add_note_head(self, prefix, note_head):
        if note_head not in self._heads[prefix]:
            self._heads[prefix].append(note_head)

    def drumIndex(self, prefix):
        return self._order.index(prefix)

def guess_staffs(lines):
    staffs = []
    currentStaff = None
    for line in itertools.imap(str.strip, lines):
        line = DrumLineGuess.recognize(line)
        if line is None:
            if currentStaff is not None:
                staffs.append(currentStaff)
                currentStaff = None
        else:
            lastStaff = currentStaff
            if currentStaff is None:
                currentStaff = DrumStaffGuess()
            if not currentStaff.add_line(line):
                currentStaff = lastStaff
    if currentStaff is not None:
        staffs.append(currentStaff)
    return staffs

def guess_drums(staff_guesses):
    kit = DrumKitGuess()
    for staff in staff_guesses:
        for line in staff:
            if line.prefix in kit:
                continue
            kit.add_drum(line.prefix)
            for char in line.line:
                if char not in (line.BARLINE, line.EMPTY_NOTE):
                    kit.add_note_head(line.prefix, char)
    return kit

def guess_score(staffs, drums):
    kit = DrumKit()
    for prefix in drums:
        heads = drums.note_heads(prefix)
        print prefix, heads
        default_head = heads[0]
        drum = Drum(prefix, prefix, default_head, False)
        headData = HeadData()
        drum.addNoteHead(default_head, headData)
        for head in heads[1:]:
            drum.addNoteHead(head)
        kit.addDrum(drum)
    score = ScoreFactory.makeEmptyScore(0, None, kit)
    for staff_guess in staffs:
        for measure_lines in staff_guess.iterMeasures():
            if not measure_lines:
                continue
            width = len(measure_lines[0].line)
            measure = score.insertMeasureByIndex(width)
            for line in measure_lines:
                drumIndex = drums.drumIndex(line.prefix)
                for noteTime, head in enumerate(line.line):
                    if head in (line.BARLINE, line.EMPTY_NOTE):
                        continue
                    measure.addNote(NotePosition(noteTime=noteTime, drumIndex=drumIndex),
                                    head)
    return score

def guess_counts(score):
    for measure in score.iterMeasures():
        width = len(measure)
        if width == 4:
            beat_len = 1
        elif width == 8:
            beat_len = 2
        elif width == 16:
            beat_len = 4
        elif width == 6:
            beat_len = 3
        elif width == 12:
            beat_len = 3
        elif width == 24:
            beat_len = 6
        elif width % 4 == 0:
            beat_len = 4
        elif width % 2 == 0:
            beat_len = 2
        else:
            beat_len = 1
        counter = MeasureCount.counterMaker(beat_len, width)
        measure.counter = counter

def main():
    lines = open(r"C:\Users\mike_000\Dropbox\Drum music\Take Me Out.txt").readlines()
    staff_guesses = guess_staffs(lines)
    drums = guess_drums(staff_guesses)
    score = guess_score(staff_guesses, drums)
    guess_counts(score)
    import sys
    score.write(sys.stdout)
    score.write(open(r"C:\Users\mike_000\Dropbox\Drum music\Take Me Out.brp", 'wb'))

if __name__ == '__main__':
    main()
