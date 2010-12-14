'''
Created on 12 Dec 2010

@author: Mike Thomas

'''

from DrumKit import DrumKit
from Staff import Staff
from Measure import Measure
from DBErrors import BadTimeError, OverSizeMeasure, BadNoteError

class Score(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._staffs = []
        self.drumKit = DrumKit()

    def __len__(self):
        return sum(len(staff) for staff in self._staffs)

    def iterStaffs(self):
        return iter(self._staffs)

    def iterMeasures(self):
        for staff in self.iterStaffs():
            for measure in staff:
                yield measure

    def getMeasure(self, index):
        if not (0 <= index < self.numMeasures()):
            raise BadTimeError()
        staff, index = self._staffContainingMeasure(index)
        return staff[index]

    def getStaff(self, index):
        return self._staffs[index]

    def numStaffs(self):
        return len(self._staffs)

    def numMeasures(self):
        return sum(staff.numMeasures() for staff in self._staffs)

    def addMeasure(self, width):
        newMeasure = Measure(width)
        if self.numStaffs() == 0:
            self._staffs.append(Staff())
        self._staffs[-1].addMeasure(newMeasure)

    def _staffContainingMeasure(self, index):
        measuresSoFar = 0
        for staff in self._staffs:
            if measuresSoFar <= index < measuresSoFar + staff.numMeasures():
                return staff, index - measuresSoFar
            measuresSoFar += staff.numMeasures()
        raise BadTimeError()

    def insertMeasure(self, width, index):
        if not (0 <= index <= self.numMeasures()):
            raise BadTimeError()
        if len(self._staffs) == 0:
            self._staffs.append(Staff())
            staff = self._staffs[0]
        elif index == self.numMeasures():
            staff = self._staffs[-1]
            index = staff.numMeasures()
        else:
            staff, index = self._staffContainingMeasure(index)
        staff.insertMeasure(index, Measure(width))

    def deleteMeasure(self, index):
        if not (0 <= index < self.numMeasures()):
            raise BadTimeError()
        staff, index = self._staffContainingMeasure(index)
        staff.deleteMeasure(index)
        if staff.numMeasures() == 0:
            self._staffs.remove(staff)

    def _formatScore(self, width, widthFunction, ignoreErrors = False):
        measures = list(self.iterMeasures())
        for staff in self.iterStaffs():
            staff.clear()
        staff = self._staffs[0]
        staffIndex = 0
        for measureIndex, measure in enumerate(measures):
            staff.addMeasure(measure)
            while widthFunction(staff) > width:
                if staff.numMeasures() == 1:
                    if ignoreErrors:
                        break
                    else:
                        raise OverSizeMeasure(measure)
                else:
                    staff.deleteMeasure(staff.numMeasures() - 1)
                    staffIndex += 1
                    if staffIndex == self.numStaffs():
                        self._staffs.append(Staff())
                    staff = self._staffs[staffIndex]
                    staff.addMeasure(measure)
            if (measure.isSectionEnd() and
                measureIndex != len(measures) - 1):
                staffIndex += 1
                if staffIndex == self.numStaffs():
                    self._staffs.append(Staff())
                staff = self._staffs[staffIndex]
        self._staffs = self._staffs[:staffIndex + 1]

    def textFormatScore(self, width, ignoreErrors = False):
        self._formatScore(width, Staff.characterWidth, ignoreErrors)

    def gridFormatScore(self, width):
        self._formatScore(width, Staff.gridWidth)

    def getNote(self, staffIndex, measureIndex, timeIndex, noteIndex):
        if not (0 <= staffIndex < self.numMeasures()):
            raise BadTimeError(measureIndex)
        if not (0 <= noteIndex < len(self.drumKit)):
            raise BadNoteError(noteIndex)
        return self.getStaff(staffIndex).getNote(measureIndex,
                                                 timeIndex, noteIndex)

    def addNote(self, staffIndex, measureIndex,
                timeIndex, noteIndex, head = None):
        if not (0 <= staffIndex < self.numMeasures()):
            raise BadTimeError(measureIndex)
        if not (0 <= noteIndex < len(self.drumKit)):
            raise BadNoteError(noteIndex)
        if head is None:
            head = self.drumKit[noteIndex].head
        self.getStaff(staffIndex).addNote(measureIndex, timeIndex,
                                          noteIndex, head)

    def deleteNote(self, staffIndex, measureIndex, timeIndex, noteIndex):
        if not (0 <= staffIndex < self.numMeasures()):
            raise BadTimeError(measureIndex)
        if not (0 <= noteIndex < len(self.drumKit)):
            raise BadNoteError(noteIndex)
        self.getStaff(staffIndex).deleteNote(measureIndex,
                                             timeIndex, noteIndex)

    def toggleNote(self, staffIndex, measureIndex,
                   timeIndex, noteIndex, head = None):
        if not (0 <= staffIndex < self.numMeasures()):
            raise BadTimeError(measureIndex)
        if not (0 <= noteIndex < len(self.drumKit)):
            raise BadNoteError(noteIndex)
        if head is None:
            head = self.drumKit[noteIndex].head
        self.getStaff(staffIndex).toggleNote(measureIndex, timeIndex,
                                             noteIndex, head)
