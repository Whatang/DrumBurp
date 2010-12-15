'''
Created on 12 Dec 2010

@author: Mike Thomas

'''

from DrumKit import DrumKit
from Staff import Staff
from Measure import Measure
from DBErrors import BadTimeError, OverSizeMeasure
from Data.NotePosition import NotePosition

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
        staff.insertMeasure(NotePosition(measureIndex = index),
                            Measure(width))

    def deleteMeasure(self, index):
        if not (0 <= index < self.numMeasures()):
            raise BadTimeError()
        staff, index = self._staffContainingMeasure(index)
        staff.deleteMeasure(NotePosition(measureIndex = index))
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
                    staff.deleteMeasure(NotePosition(measureIndex = staff.numMeasures() - 1))
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

    def getNote(self, position):
        if not (0 <= position.staffIndex < self.numMeasures()):
            raise BadTimeError(position)
        if not (0 <= position.drumIndex < len(self.drumKit)):
            raise BadTimeError(position)
        return self.getStaff(position.staffIndex).getNote(position)

    def addNote(self, position, head = None):
        if not (0 <= position.staffIndex < self.numMeasures()):
            raise BadTimeError(position)
        if not (0 <= position.drumIndex < len(self.drumKit)):
            raise BadTimeError(position)
        if head is None:
            head = self.drumKit[position.drumIndex].head
        self.getStaff(position.staffIndex).addNote(position, head)

    def deleteNote(self, position):
        if not (0 <= position.staffIndex < self.numMeasures()):
            raise BadTimeError(position)
        if not (0 <= position.drumIndex < len(self.drumKit)):
            raise BadTimeError(position)
        self.getStaff(position.staffIndex).deleteNote(position)

    def toggleNote(self, position, head = None):
        if not (0 <= position.staffIndex < self.numMeasures()):
            raise BadTimeError(position)
        if not (0 <= position.drumIndex < len(self.drumKit)):
            raise BadTimeError(position)
        if head is None:
            head = self.drumKit[position.drumIndex].head
        self.getStaff(position.staffIndex).toggleNote(position, head)
