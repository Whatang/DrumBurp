'''
Created on 14 Dec 2010

@author: Mike Thomas
'''

from DBErrors import BadNoteSpecification
import copy

class NotePosition(object):
    def __init__(self, staffIndex = None, measureIndex = None,
                 noteTime = None, drumIndex = None):
        if [noteTime, drumIndex].count(None) == 1:
            raise BadNoteSpecification(staffIndex, measureIndex,
                                       noteTime, drumIndex)
        self.staffIndex = staffIndex
        self.measureIndex = measureIndex
        self.noteTime = noteTime
        self.drumIndex = drumIndex

    def __str__(self):
        return ", ".join(str(x) for x in [self.staffIndex, self.measureIndex,
                                          self.noteTime, self.drumIndex])

    @classmethod
    def makeMeasurePosition(cls, np):
        np = copy.copy(np)
        np.noteTime = None
        np.drumIndex = None
        return np

    @classmethod
    def makeStaffPosition(cls, np):
        np = cls.makeMeasurePosition(np)
        np.measureIndex = None
        return np
