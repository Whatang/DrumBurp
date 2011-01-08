'''
Created on 12 Dec 2010

@author: Mike Thomas

'''

from DrumKit import DrumKit
from Staff import Staff
from Measure import Measure
from DBErrors import BadTimeError, OverSizeMeasure
from Data.NotePosition import NotePosition

#pylint: disable-msg=R0904

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
        self._callBack = None

    def __len__(self):
        return sum(len(staff) for staff in self._staffs)

    def _runCallBack(self, position):
        if self._callBack is not None:
            self._callBack(position)

    def setCallBack(self, callBack):
        self._callBack = callBack

    def clearCallBack(self):
        self._callBack = None

    def _setStaffCallBack(self, staff, staffIndex):
        def wrappedCallBack(position):
            position.staffindex = staffIndex
            self._runCallBack(position)
        staff.setCallBack(wrappedCallBack)

    def iterStaffs(self):
        return iter(self._staffs)

    def iterMeasures(self):
        for staff in self.iterStaffs():
            for measure in staff:
                yield measure

    def iterNotes(self):
        for sIndex, staff in enumerate(self.iterStaffs()):
            for np, head in staff.iterNotes():
                np.staffIndex = sIndex
                yield np, head

    def getMeasure(self, index):
        if not (0 <= index < self.numMeasures()):
            raise BadTimeError()
        staff, index = self._staffContainingMeasure(index)
        return staff[index]

    def getStaff(self, index):
        return self._staffs[index]

    def numStaffs(self):
        return len(self._staffs)

    def addStaff(self):
        newStaff = Staff()
        self._staffs.append(newStaff)
        self._setStaffCallBack(newStaff, self.numStaffs() - 1)

    def deleteLastStaff(self):
        staff = self._staffs.pop()
        staff.clearCallBack()

    def deleteStaffByIndex(self, index):
        if not (0 <= index < self.numStaffs()):
            raise BadTimeError(index)
        staff = self._staffs.pop(index)
        staff.clearCallBack()
        for offset, nextStaff in enumerate(self._staffs[index:]):
            self._setStaffCallBack(nextStaff, index + offset)

    def deleteStaff(self, position):
        self.deleteStaffByIndex(position.staffIndex)

    def insertStaffByIndex(self, index):
        if not (0 <= index <= self.numStaffs()):
            raise BadTimeError(index)
        newStaff = Staff()
        self._staffs.insert(index, newStaff)
        for offset, nextStaff in enumerate(self._staffs[index:]):
            self._setStaffCallBack(nextStaff, index + offset)

    def insertStaff(self, position):
        self.insertStaffByIndex(position.staffIndex)

    def numMeasures(self):
        return sum(staff.numMeasures() for staff in self.iterStaffs())

    def addEmptyMeasure(self, width):
        newMeasure = Measure(width)
        if self.numStaffs() == 0:
            self.addStaff()
        self.getStaff(-1).addMeasure(newMeasure)

    def _staffContainingMeasure(self, index):
        measuresSoFar = 0
        for staff in self.iterStaffs():
            if measuresSoFar <= index < measuresSoFar + staff.numMeasures():
                return staff, index - measuresSoFar
            measuresSoFar += staff.numMeasures()
        raise BadTimeError()

    def insertMeasureByIndex(self, width, index):
        if not (0 <= index <= self.numMeasures()):
            raise BadTimeError()
        if self.numStaffs() == 0:
            self.addStaff()
            staff = self.getStaff(0)
        elif index == self.numMeasures():
            staff = self.getStaff(-1)
            index = staff.numMeasures()
        else:
            staff, index = self._staffContainingMeasure(index)
        staff.insertMeasure(NotePosition(measureIndex = index),
                            Measure(width))

    def insertMeasureByPosition(self, width, position):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        staff = self.getStaff(position.staffIndex)
        staff.insertMeasure(position, Measure(width))

    def deleteMeasureByIndex(self, index):
        if not (0 <= index < self.numMeasures()):
            raise BadTimeError()
        staff, index = self._staffContainingMeasure(index)
        staff.deleteMeasure(NotePosition(measureIndex = index))

    def deleteMeasureByPosition(self, position):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        staff = self.getStaff(position.staffIndex)
        staff.deleteMeasure(position)

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

    def _formatScore(self, width,
                     widthFunction, ignoreErrors = False):
        measures = list(self.iterMeasures())
        oldNumMeasures = [staff.numMeasures() for staff in self.iterStaffs()]
        for staff in self.iterStaffs():
            staff.clear()
        staff = self.getStaff(0)
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
                    staff.deleteLastMeasure()
                    staffIndex += 1
                    if staffIndex == self.numStaffs():
                        self.addStaff()
                    staff = self.getStaff(staffIndex)
                    staff.addMeasure(measure)
            if (measure.isSectionEnd() and
                measureIndex != len(measures) - 1):
                staffIndex += 1
                if staffIndex == self.numStaffs():
                    self.addStaff()
                staff = self.getStaff(staffIndex)
        while self.numStaffs() > staffIndex + 1:
            self.deleteLastStaff()
        newNumMeasures = [staff.numMeasures() for staff in self.iterStaffs()]
        return newNumMeasures != oldNumMeasures

    def textFormatScore(self, width, ignoreErrors = False):
        return self._formatScore(width, Staff.characterWidth, ignoreErrors)

    def gridFormatScore(self, width):
        return self._formatScore(width,
                                 Staff.gridWidth,
                                 True)

def makeEmptyScore(numMeasures, measureWidth):
    score = Score()
    score.drumKit.loadDefaultKit()
    for dummy in range(0, numMeasures):
        score.addEmptyMeasure(measureWidth)
    return score

class ScoreFactory(object):
    def __call__(self, filename):
        if filename is not None:
            pass
        else:
            score = makeEmptyScore(32, 16)
        return score
