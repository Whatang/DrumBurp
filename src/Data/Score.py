'''
Created on 12 Dec 2010

@author: Mike Thomas

'''

from DrumKit import DrumKit
from Staff import Staff
from Measure import Measure
from DBErrors import BadTimeError, OverSizeMeasure
from NotePosition import NotePosition
from ScoreMetaData import ScoreMetaData
import os
import bisect
import time

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
        self.scoreData = ScoreMetaData()
        self._sections = []

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
            position.staffIndex = staffIndex
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

    def addEmptyMeasure(self, width, counter = None):
        newMeasure = Measure(width)
        newMeasure.counter = counter
        if self.numStaffs() == 0:
            self.addStaff()
        self.getStaff(-1).addMeasure(newMeasure)
        return newMeasure

    def _staffContainingMeasure(self, index):
        measuresSoFar = 0
        for staff in self.iterStaffs():
            if measuresSoFar <= index < measuresSoFar + staff.numMeasures():
                return staff, index - measuresSoFar
            measuresSoFar += staff.numMeasures()
        raise BadTimeError()

    def insertMeasureByIndex(self, width, index, counter = None):
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
        newMeasure = Measure(width)
        newMeasure.counter = counter
        staff.insertMeasure(NotePosition(measureIndex = index),
                            newMeasure)

    def insertMeasureByPosition(self, width, position, counter = None):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        newMeasure = Measure(width)
        newMeasure.counter = counter
        staff = self.getStaff(position.staffIndex)
        staff.insertMeasure(position, newMeasure)

    def deleteMeasureByIndex(self, index):
        if not (0 <= index < self.numMeasures()):
            raise BadTimeError()
        staff, index = self._staffContainingMeasure(index)
        np = NotePosition(staffIndex = self._staffs.index(staff),
                          measureIndex = index)
        self.deleteMeasureByPosition(np)

    def deleteMeasureByPosition(self, position):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        staff = self.getStaff(position.staffIndex)
        if (staff.isSectionEnd()
            and position.measureIndex == staff.numMeasures() - 1):
            sectionIndex = self.getSectionIndex(position)
            self.deleteSectionTitle(sectionIndex)
        staff.deleteMeasure(position)

    def deleteEmptyMeasures(self):
        while self.numMeasures() > 1:
            index = self.numMeasures() - 1
            measure = self.getMeasure(index)
            if measure.isEmpty():
                self.deleteMeasureByIndex(index)
            else:
                break

    def copyMeasure(self, position):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        staff = self.getStaff(position.staffIndex)
        return staff.copyMeasure(position)

    def pasteMeasure(self, position, notes):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        staff = self.getStaff(position.staffIndex)
        staff.pasteMeasure(position, notes)

    def setMeasureBeatCount(self, position, beats, counter):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        staff = self.getStaff(position.staffIndex)
        staff.setMeasureBeatCount(position, beats, counter)

    def numSections(self):
        return len(self._sections)

    def getSectionIndex(self, position):
        ends = []
        for staffIndex, staff in enumerate(self.iterStaffs()):
            assert(staff.isConsistent())
            if staff.isSectionEnd():
                ends.append(staffIndex)
        assert(len(ends) == self.numSections())
        return bisect.bisect_left(ends, position.staffIndex)

    def getSectionTitle(self, index):
        return self._sections[index]

    def setSectionTitle(self, index, title):
        self._sections[index] = title

    def deleteSectionTitle(self, index):
        self._sections.pop(index)

    def iterSections(self):
        return iter(self._sections)

    def setSectionEnd(self, position, onOff):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        staff = self.getStaff(position.staffIndex)
        sectionIndex = self.getSectionIndex(position)
        if onOff:
            self._sections.insert(sectionIndex, "Section Title")
        else:
            if sectionIndex < self.numSections():
                self._sections.pop(sectionIndex)
        staff.setSectionEnd(position, onOff)

    def setLineBreak(self, position, onOff):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        staff = self.getStaff(position.staffIndex)
        staff.setLineBreak(position, onOff)

    def setRepeatEnd(self, position, onOff):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        staff = self.getStaff(position.staffIndex)
        staff.setRepeatEnd(position, onOff)

    def setRepeatStart(self, position, onOff):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        staff = self.getStaff(position.staffIndex)
        staff.setRepeatStart(position, onOff)

    def getNote(self, position):
        if not (0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError(position)
        if not (0 <= position.drumIndex < len(self.drumKit)):
            raise BadTimeError(position)
        return self.getStaff(position.staffIndex).getNote(position)

    def addNote(self, position, head = None):
        if not (0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError(position)
        if not (0 <= position.drumIndex < len(self.drumKit)):
            raise BadTimeError(position)
        if head is None:
            head = self.drumKit[position.drumIndex].head
        self.getStaff(position.staffIndex).addNote(position, head)

    def deleteNote(self, position):
        if not (0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError(position)
        if not (0 <= position.drumIndex < len(self.drumKit)):
            raise BadTimeError(position)
        self.getStaff(position.staffIndex).deleteNote(position)

    def toggleNote(self, position, head = None):
        if not (0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError(position)
        if not (0 <= position.drumIndex < len(self.drumKit)):
            raise BadTimeError(position)
        if head is None:
            head = self.drumKit[position.drumIndex].head
        self.getStaff(position.staffIndex).toggleNote(position, head)

    def notePlus(self, pos, ticks):
        if not (0 <= pos.staffIndex < self.numStaffs()):
            raise BadTimeError(pos)
        if not (0 <= pos.drumIndex < len(self.drumKit)):
            raise BadTimeError(pos)
        staff = self.getStaff(pos.staffIndex)
        measure = staff[pos.measureIndex]
        pos.noteTime += ticks
        while pos.noteTime >= len(measure):
            pos.noteTime -= len(measure)
            pos.measureIndex += 1
            if pos.measureIndex >= staff.numMeasures():
                pos.measureIndex = 0
                pos.staffIndex += 1
                if pos.staffIndex == self.numStaffs():
                    return None
                staff = self.getStaff(pos.staffIndex)
            measure = staff[pos.measureIndex]
        return pos

    def _formatScore(self, width,
                     widthFunction, ignoreErrors = False):
        if width is None:
            width = self.scoreData.width
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
            if (measure.isLineEnd() and
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

    def changeKit(self, newKit, changes):
        for measure in self.iterMeasures():
            measure.changeKit(changes)
        self.drumKit = newKit

    def write(self, handle):
        self.scoreData.save(handle)
        self.drumKit.write(handle)
        for measure in self.iterMeasures():
            measure.write(handle)
        for title in self._sections:
            print >> handle, "SECTION_TITLE", title

    def read(self, handle):
        def scoreHandle():
            for line in handle:
                line = line.rstrip()
                fields = line.split(None, 1)
                if len(fields) == 1:
                    fields.append(None)
                elif len(fields) == 0:
                    # Blank line
                    continue
                lineType, lineData = fields
                lineType = lineType.upper()
                yield lineType, lineData
        scoreIterator = scoreHandle()
        for lineType, lineData in scoreIterator:
            if lineType == "SCORE_METADATA":
                self.scoreData.load(scoreIterator)
            elif lineType == "START_BAR":
                measureWidth = int(lineData)
                measure = self.addEmptyMeasure(measureWidth)
                measure.read(scoreIterator)
            elif lineType == "KIT_START":
                self.drumKit.read(scoreIterator)
            elif lineType == "SECTION_TITLE":
                self._sections.append(lineData)
            else:
                raise IOError("Unrecognised line type.")
        # Format the score appropriately
        self.gridFormatScore(self.scoreData.width)
        # Make sure we've got the right number of section titles
        assert(all(staff.isConsistent() for staff in self.iterStaffs()))
        numSections = len([staff for staff in self.iterStaffs()
                           if staff.isSectionEnd()])
        if numSections > self.numSections():
            self._sections += ["Section Title"] * (numSections
                                                   - self.numSections())
        elif numSections < self.numSections():
            self._sections = self._sections[:numSections]


    def exportASCII(self, handle, settings):
        metadataString = self.scoreData.exportASCII()
        asciiString = []
        newSection = True
        sectionIndex = 0
        isRepeating = False
        for staff in self.iterStaffs():
            assert(staff.isConsistent())
            if newSection:
                newSection = False
                if sectionIndex < self.numSections():
                    if len(asciiString) > 0 and settings.emptyLineBeforeSection:
                        asciiString.append("")
                    title = self.getSectionTitle(sectionIndex)
                    asciiString.append(title)
                    if settings.underline:
                        asciiString.append("".join(["~"] * len(title)))
                    if settings.emptyLineAfterSection:
                        asciiString.append("")
                    sectionIndex += 1
            newSection = staff.isSectionEnd()
            staffString, isRepeating = staff.exportASCII(self.drumKit,
                                                       settings,
                                                       isRepeating)
            asciiString.extend(staffString)
            asciiString.append("")
        asciiString = asciiString[:-1]
        kitString = []
        for instr in self.drumKit:
            kitString.append(instr.exportASCII())
        kitString.reverse()
        kitString.append("")
        if settings.metadata:
            handle.writelines(mString + os.linesep
                              for mString in metadataString)
        if settings.kitKey:
            handle.writelines(iString + os.linesep
                              for iString in kitString)
        handle.writelines(sString + os.linesep for sString in asciiString)

class ScoreFactory(object):
    def __call__(self, filename = None,
                 numMeasures = 32 , measureWidth = 16,
                 counter = None):
        if filename is not None:
            score = self.loadScore(filename)
        else:
            score = self.makeEmptyScore(numMeasures, measureWidth, counter)
        return score

    @classmethod
    def makeEmptyScore(cls, numMeasures, measureWidth, counter):
        score = Score()
        score.drumKit.loadDefaultKit()
        for dummy in range(0, numMeasures):
            score.addEmptyMeasure(measureWidth, counter = counter)
        return score

    @classmethod
    def loadScore(cls, filename):
        score = Score()
        with open(filename, 'rU') as handle:
            score.read(handle)
        return score

    @classmethod
    def saveScore(cls, score, filename):
        with open(filename, 'w') as handle:
            score.write(handle)
