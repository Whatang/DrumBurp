# Copyright 2011-12 Michael Thomas
#
# See www.whatang.org for more information.
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DrumBurp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DrumBurp.  If not, see <http://www.gnu.org/licenses/>
'''
Created on 12 Dec 2010

@author: Mike Thomas

'''

from DrumKit import DrumKit
from Staff import Staff
from Measure import Measure
from Counter import CounterRegistry
from MeasureCount import makeSimpleCount, MeasureCount
from DBErrors import BadTimeError, OverSizeMeasure
from DBConstants import REPEAT_EXTENDER
from NotePosition import NotePosition
from ScoreMetaData import ScoreMetaData
from FontOptions import FontOptions
import os
import bisect
import copy
import hashlib
from StringIO import StringIO


class InconsistentRepeats(StandardError):
    "Bad repeat data"

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
        self._callBacksEnabled = True
        self.scoreData = ScoreMetaData()
        self._sections = []
        self._formatState = None
        self.paperSize = "Letter"
        counter = CounterRegistry().getCounterByIndex(0)
        self.defaultCount = makeSimpleCount(counter, 4)
        self.systemSpacing = 25
        self.fontOptions = FontOptions()
        self.lilysize = 20
        self.lilypages = 0
        self.lilyFill = False

    def __len__(self):
        return sum(len(staff) for staff in self._staffs)

    def _runCallBack(self, position):
        if self._callBack is not None and self._callBacksEnabled:
            self._callBack(position)

    def turnOnCallBacks(self):
        self._callBacksEnabled = True

    def turnOffCallBacks(self):
        self._callBacksEnabled = False

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

    def iterMeasuresBetween(self, start, end):
        if self.getMeasureIndex(end) < self.getMeasureIndex(start):
            start, end = end, start
        staffIndex = start.staffIndex
        measureIndex = start.measureIndex
        absIndex = self.getMeasureIndex(start)
        while staffIndex < end.staffIndex:
            staff = self.getStaff(staffIndex)
            while measureIndex < staff.numMeasures():
                yield (staff[measureIndex], absIndex,
                       NotePosition(staffIndex, measureIndex))
                measureIndex += 1
                absIndex += 1
            measureIndex = 0
            staffIndex += 1
        staff = self.getStaff(staffIndex)
        while measureIndex <= end.measureIndex:
            yield (staff[measureIndex], absIndex,
                   NotePosition(staffIndex, measureIndex))
            absIndex += 1
            measureIndex += 1

    @staticmethod
    def _readAlternates(text):
        alternates = [t.strip() for t in
                      text.split(",")]
        theseAlternates = set()
        for aText in alternates:
            if "-" in aText:
                aStart, aEnd = aText.split("-")
                for aVal in xrange(int(aStart), int(aEnd.rstrip(".")) + 1):
                    theseAlternates.add(aVal)
            else:
                theseAlternates.add(int(aText.rstrip(".")))
        return theseAlternates

    @staticmethod
    def _findRepeatData(measures, index, alternateIndexes):
        start = index
        numMeasures = len(measures)
        numRepeats = 0
        alternates = set()
        while index < numMeasures:
            measure = measures[index]
            if index in alternateIndexes:
                numRepeats += len(alternateIndexes[index])
                alternates.update(alternateIndexes[index])
            if (measure.isRepeatEnd() or measure.isSectionEnd()):
                if alternates:
                    if (index + 1 == numMeasures or
                        not measures[index + 1].alternateText
                        or measures[index + 1].isRepeatStart()
                        or measure.isSectionEnd()):
                        if alternates != set(xrange(1, numRepeats + 1)):
                            raise InconsistentRepeats(start, index)
                        return index + 1, numRepeats
                else:
                    numRepeats = measure.repeatCount
                    return index + 1, numRepeats
            index += 1
        return index, numRepeats


    def iterMeasuresWithRepeats(self):
        measures = list(self.iterMeasures())
        alternates = {}
        repeatData = {}
        repeatStart = -1
        for index, measure in enumerate(measures):
            if measure.alternateText:
                alternates[index] = self._readAlternates(measure.alternateText)
        for index, measure in enumerate(measures):
            if measure.isRepeatStart():
                repeatData[index] = self._findRepeatData(measures, index,
                                                         alternates)
        index = 0
        repeatStart = 0
        repeatNum = -1
        afterRepeat = -1
        latestRepeatEnd = -1
        numMeasures = len(measures)
        alternateStarts = {}
        while index < numMeasures:
            measure = measures[index]
            if measure.isRepeatStart():
                repeatStart = index
                afterRepeat, numRepeats = repeatData[index]
                repeatNum += 1
            if index in alternates and repeatNum > -1:
                theseAlternates = alternates[index]
                alternateStarts.update((aStart, index) for aStart
                                       in theseAlternates)
                if repeatNum + 1 not in theseAlternates:
                    index = alternateStarts.get(repeatNum + 1,
                                                latestRepeatEnd + 1)
                    continue
            yield measure, index
            if measure.isRepeatEnd() and repeatNum > -1:
                if alternateStarts:
                    if repeatNum < numRepeats - 1:
                        if index > latestRepeatEnd:
                            latestRepeatEnd = index
                        index = repeatStart
                    else:
                        index = afterRepeat
                        repeatNum = -1
                        alternateStarts = {}
                elif repeatNum < numRepeats - 1:
                    index = repeatStart
                else:
                    index += 1
                    repeatNum = -1
            elif measure.isSectionEnd():
                repeatNum = -1
                index += 1
                alternateStarts = {}
            else:
                index += 1

    def getMeasure(self, index):
        if not (0 <= index < self.numMeasures()):
            raise BadTimeError()
        staff, index = self._staffContainingMeasure(index)
        return staff[index]

    def getItemAtPosition(self, position):
        if position.staffIndex is None:
            return self
        if not (0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        staff = self.getStaff(position.staffIndex)
        if position.measureIndex is None:
            return staff
        return staff.getItemAtPosition(position)

    def getStaff(self, index):
        return self._staffs[index]

    def numStaffs(self):
        return len(self._staffs)

    def addStaff(self):
        newStaff = Staff()
        self._staffs.append(newStaff)
        self._setStaffCallBack(newStaff, self.numStaffs() - 1)


    def deleteStaffByIndex(self, index):
        if not (0 <= index < self.numStaffs()):
            raise BadTimeError(index)
        staff = self._staffs[index]
        staff.clearCallBack()
        if staff.isSectionEnd():
            if index == 0 or self.getStaff(index - 1).isSectionEnd():
                position = NotePosition(staffIndex = index)
                sectionIndex = self.getSectionIndex(position)
                self.deleteSectionTitle(sectionIndex)
            else:
                prevStaff = self.getStaff(index - 1)
                position = NotePosition(staffIndex = index - 1,
                                        measureIndex =
                                        prevStaff.numMeasures() - 1)
                prevStaff.setSectionEnd(position, True)
        self._staffs.pop(index)
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

    def getMeasureIndex(self, position):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        index = 0
        for staffIndex in range(0, position.staffIndex):
            index += self.getStaff(staffIndex).numMeasures()
        index += position.measureIndex
        return index

    def getMeasurePosition(self, index):
        staffIndex = 0
        staff = self.getStaff(0)
        while index >= staff.numMeasures():
            index -= staff.numMeasures()
            staffIndex += 1
            if staffIndex == self.numStaffs():
                break
            staff = self.getStaff(staffIndex)
        if staffIndex == self.numStaffs():
            raise BadTimeError(index)
        return NotePosition(staffIndex = staffIndex,
                            measureIndex = index)


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
        return newMeasure

    def insertMeasureByPosition(self, width, position, counter = None):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        newMeasure = Measure(width)
        newMeasure.counter = counter
        staff = self.getStaff(position.staffIndex)
        staff.insertMeasure(position, newMeasure)
        return newMeasure

    def deleteMeasureByIndex(self, index):
        if not (0 <= index < self.numMeasures()):
            raise BadTimeError()
        np = self.getMeasurePosition(index)
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

    def deleteMeasuresAtPosition(self, position, numToDelete):
        position = copy.copy(position)
        staff = self.getStaff(position.staffIndex)
        for dummyIndex in xrange(numToDelete):
            if position.measureIndex == staff.numMeasures():
                if staff.numMeasures() == 0:
                    self.deleteStaff(position)
                else:
                    position.staffIndex += 1
                    position.measureIndex = 0
                staff = self.getStaff(position.staffIndex)
            staff.deleteMeasure(position)

    def clearMeasure(self, position):
        measure = self.getItemAtPosition(position.makeMeasurePosition())
        measure.clear() #IGNORE:E1103

    def trailingEmptyMeasures(self):
        emptyMeasures = []
        np = NotePosition(staffIndex = self.numStaffs() - 1)
        staff = self.getItemAtPosition(np)
        np.measureIndex = staff.numMeasures() - 1
        measure = self.getItemAtPosition(np)
        while ((np.staffIndex > 0 or np.measureIndex > 0)
               and measure.isEmpty()): #pylint:disable-msg=E1103
            emptyMeasures.append(copy.copy(np))
            if np.measureIndex == 0:
                np.staffIndex -= 1
                staff = self.getStaff(np.staffIndex)
                np.measureIndex = staff.numMeasures()
            np.measureIndex -= 1
            measure = self.getItemAtPosition(np)
        return emptyMeasures


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

    def pasteMeasure(self, position, notes, copyMeasureDecorations = False):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        staff = self.getStaff(position.staffIndex)
        return staff.pasteMeasure(position, notes, copyMeasureDecorations)

    def pasteMeasureByIndex(self, index, notes, copyMeasureDecorations = False):
        position = self.getMeasurePosition(index)
        self.pasteMeasure(position, notes, copyMeasureDecorations)

    def numSections(self):
        return len(self._sections)

    def getSectionIndex(self, position):
        ends = []
        for staffIndex, staff in enumerate(self.iterStaffs()):
            assert(staff.isConsistent())
            if staff.isSectionEnd():
                ends.append(staffIndex)
        try:
            assert(len(ends) == self.numSections())
        except:
            print len(ends), self.numSections()
            raise
        return bisect.bisect_left(ends, position.staffIndex)

    def getSectionTitle(self, index):
        return self._sections[index]

    def setSectionTitle(self, index, title):
        self._sections[index] = title

    def deleteSectionTitle(self, index):
        self._sections.pop(index)

    def getSectionStartStaffIndex(self, position):
        startIndex = position.staffIndex
        while (startIndex > 0 and
               not self.getStaff(startIndex - 1).isSectionEnd()):
            startIndex -= 1
        return startIndex

    def deleteSection(self, position):
        sectionIndex = self.getSectionIndex(position)
        if sectionIndex == self.numSections():
            return
        startIndex = position.staffIndex
        while (startIndex > 0 and
               not self.getStaff(startIndex - 1).isSectionEnd()):
            startIndex -= 1
        while not self.getStaff(startIndex).isSectionEnd():
            self.deleteStaffByIndex(startIndex)
        self.deleteStaffByIndex(startIndex)

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

    def iterMeasuresInSection(self, sectionIndex):
        if not(0 <= sectionIndex < self.numSections()):
            raise BadTimeError()
        thisSection = 0
        inSection = (thisSection == sectionIndex)
        for measure in self.iterMeasures():
            if inSection:
                yield measure
                if measure.isSectionEnd():
                    break
            if measure.isSectionEnd():
                thisSection += 1
                inSection = (thisSection == sectionIndex)

    def nextMeasure(self, position):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        staff = self.getStaff(position.staffIndex)
        if not (0 <= position.measureIndex < staff.numMeasures()):
            raise BadTimeError()
        position = NotePosition(position.staffIndex, position.measureIndex)
        position.measureIndex += 1
        if position.measureIndex == staff.numMeasures():
            position.staffIndex += 1
            if position.staffIndex == self.numStaffs():
                position.staffIndex = None
                position.measureIndex = None
            else:
                position.measureIndex = 0
        return position

    def nextMeasurePositionInSection(self, position):
        if not(0 <= position.staffIndex < self.numStaffs()):
            raise BadTimeError()
        staff = self.getStaff(position.staffIndex)
        if not (0 <= position.measureIndex < staff.numMeasures()):
            raise BadTimeError()
        position = NotePosition(position.staffIndex, position.measureIndex)
        if staff[position.measureIndex].isSectionEnd():
            position.staffIndex = None
            position.measureIndex = None
        else:
            position.measureIndex += 1
            if position.measureIndex == staff.numMeasures:
                position.staffIndex += 1
                if position.staffIndex == self.numStaffs():
                    position.staffIndex = None
                    position.measureIndex = None
                else:
                    position.measureIndex = 0
        return position

    def insertSectionCopy(self, position, sectionIndex):
        self.turnOffCallBacks()
        position = copy.copy(position)
        try:
            if not(0 <= position.staffIndex < self.numStaffs()):
                raise BadTimeError()
            sectionMeasures = list(self.iterMeasuresInSection(sectionIndex))
            sectionTitle = "Copy of " + self.getSectionTitle(sectionIndex)
            newIndex = self.getSectionIndex(position)
            self._sections.insert(newIndex, sectionTitle)
            for measure in sectionMeasures:
                newMeasure = self.insertMeasureByPosition(len(measure),
                                                          position,
                                                          measure.counter)
                newMeasure.pasteMeasure(measure, True)
                position.measureIndex += 1
        finally:
            self.turnOnCallBacks()

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

    def tickDifference(self, second, first):
        """Calculate the difference in ticks between NotePositions first and 
        second.
        """
        current = copy.copy(first)
        current.noteTime = None
        current.drumIndex = None
        end = copy.copy(second)
        end.noteTime = None
        end.drumIndex = None
        ticks = 0
        direction = 1
        offset = first.noteTime
        if end < current:
            current, end = end, current
            direction = -1
            offset = second.noteTime
        while current < end:
            ticks += len(self.getItemAtPosition(current)) - offset
            current = self.nextMeasure(current)
            offset = 0
        if direction == 1:
            ticks += second.noteTime - offset
        else:
            ticks += first.noteTime - offset
        ticks *= direction
        return ticks


    def _getFormatState(self):
        return [(staff.numMeasures(), self.numVisibleLines(index))
                for index, staff in enumerate(self.iterStaffs())]

    def saveFormatState(self):
        self._formatState = self._getFormatState()

    def _formatScore(self, width,
                     widthFunction, ignoreErrors = False):
        if width is None:
            width = self.scoreData.width
        measures = list(self.iterMeasures())
        if not self._formatState:
            self.saveFormatState()
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
            staff = self._staffs.pop()
            staff.clearCallBack()
        return self._formatState != self._getFormatState()

    def textFormatScore(self, width = None, ignoreErrors = False):
        return self._formatScore(width, Staff.characterWidth, ignoreErrors)

    def gridFormatScore(self, width = None):
        return self._formatScore(width,
                                 Staff.gridWidth,
                                 True)

    def changeKit(self, newKit, changes):
        for measure in self.iterMeasures():
            measure.changeKit(newKit, changes)
        self.drumKit = newKit

    def getDefaultHead(self, drumIndex):
        return self.drumKit.getDefaultHead(drumIndex)

    def numVisibleLines(self, index):
        if self.scoreData.emptyLinesVisible:
            return len(self.drumKit)
        else:
            staff = self.getStaff(index)
            count = sum(drum.locked or staff.lineIsVisible(index)
                        for index, drum in enumerate(self.drumKit))
            if count == 0:
                return 1
            else:
                return count

    def nthVisibleLineIndex(self, staffIndex, lineIndex):
        count = -1
        staff = self.getStaff(staffIndex)
        for lineNum, drum in enumerate(self.drumKit):
            if drum.locked or staff.lineIsVisible(lineNum):
                count += 1
                if count == lineIndex:
                    return lineNum
        if count == -1:
            return 0
        raise BadTimeError(staffIndex)

    def iterVisibleLines(self, staffIndex):
        staff = self.getStaff(staffIndex)
        count = 0
        for lineNum, drum in enumerate(self.drumKit):
            if drum.locked or staff.lineIsVisible(lineNum):
                count += 1
                yield drum
        if count == 0:
            yield self.drumKit[0]

    def emptyDrums(self):
        emptyDrums = set(self.drumKit)
        for staffIndex in xrange(self.numStaffs()):
            emptyDrums.difference_update(set(self.iterVisibleLines(staffIndex)))
            if not emptyDrums:
                break
        return emptyDrums

    def write(self, handle):
        indenter = Indenter()
        self.scoreData.save(handle, indenter)
        self.drumKit.write(handle, indenter)
        for measure in self.iterMeasures():
            measure.write(handle, indenter)
        for title in self._sections:
            print >> handle, indenter("SECTION_TITLE", title)
        print >> handle, "PAPER_SIZE", self.paperSize
        print >> handle, "LILYSIZE", self.lilysize
        print >> handle, "LILYPAGES", self.lilypages
        if self.lilyFill:
            print >> handle, "LILYFILL", "YES"
        self.defaultCount.write(handle, indenter,
                                title = "DEFAULT_COUNT_INFO_START")
        print >> handle, "SYSTEM_SPACE", self.systemSpacing
        self.fontOptions.write(handle, indenter)


    def read(self, handle):
        def scoreHandle():
            for line in handle:
                line = line.strip()
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
        self.lilyFill = False
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
            elif lineType == "PAPER_SIZE":
                self.paperSize = lineData
            elif lineType == "LILYSIZE":
                self.lilysize = int(lineData)
            elif lineType == "LILYPAGES":
                self.lilypages = int(lineData)
            elif lineType == "LILYFILL":
                self.lilyFill = True
            elif lineType == "DEFAULT_COUNT_INFO_START":
                self.defaultCount = MeasureCount()
                self.defaultCount.read(scoreIterator)
            elif lineType == "SYSTEM_SPACE":
                self.systemSpacing = int(lineData)
            elif lineType == "FONT_OPTIONS_START":
                self.fontOptions = FontOptions()
                self.fontOptions.read(scoreIterator)
            else:
                raise IOError("Unrecognised line type: " + lineType)
        for measure in self.iterMeasures():
            for np, head in measure:
                if not self.drumKit[np.drumIndex].isAllowedHead(head):
                    self.drumKit[np.drumIndex].addNoteHead(head)
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

    def hashScore(self):
        scoreString = StringIO()
        self.write(scoreString)
        scoreString.seek(0, 0)
        scoreString = "".join(scoreString)
        return hashlib.md5(str(scoreString)).digest() #pylint:disable-msg=E1101

    def exportASCII(self, handle, settings):
        metadataString = self.scoreData.exportASCII()
        asciiString = []
        newSection = True
        sectionIndex = 0
        isRepeating = False
        repeatExtender = REPEAT_EXTENDER
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
            (staffString,
             isRepeating,
             repeatExtender) = staff.exportASCII(self.drumKit,
                                                 settings,
                                                 isRepeating,
                                                 repeatExtender)
            asciiString.extend(staffString)
            asciiString.append("")
        asciiString = asciiString[:-1]
        kitString = []
        for instr in self.drumKit:
            kitString.append(instr.exportASCII())
        kitString.reverse()
        kitString.append("")
        print >> handle, ("Tabbed with DrumBurp, "
                          "a drum tab editor from www.whatang.org")
        if settings.metadata:
            handle.writelines(mString + os.linesep
                              for mString in metadataString)
        if settings.kitKey:
            handle.writelines(iString + os.linesep
                              for iString in kitString)
        handle.writelines(sString + os.linesep for sString in asciiString)

class ScoreFactory(object):
    def __call__(self, filename = None,
                 numMeasures = 32,
                 counter = None):
        if filename is not None:
            score = self.loadScore(filename)
        else:
            score = self.makeEmptyScore(numMeasures, counter)
        return score

    @classmethod
    def makeEmptyScore(cls, numMeasures, counter):
        score = Score()
        score.drumKit.loadDefaultKit()
        if counter is None:
            registry = CounterRegistry()
            counter = list(registry.countsByTicks(2))
            counter = counter[0][1]
            counter = makeSimpleCount(counter, 4)
        for dummy in range(0, numMeasures):
            score.addEmptyMeasure(len(counter), counter = counter)
        score.scoreData.makeEmpty()
        return score

    @classmethod
    def loadScore(cls, filename):
        score = Score()
        with open(filename, 'rU') as handle:
            score.read(handle)
        return score

    @classmethod
    def saveScore(cls, score, filename):
        scoreBuffer = StringIO()
        score.write(scoreBuffer)
        with open(filename, 'w') as handle:
            handle.write(scoreBuffer.getvalue())

class Indenter(object):
    def __init__(self, indent = "  "):
        self._indent = indent
        self._level = 0
    def increase(self):
        self._level += 1
    def decrease(self):
        self._level -= 1
        self._level = max(0, self._level)
    def __call__(self, *args):
        argString = " ".join(str(ar) for ar in args)
        if self._level != 0:
            argString = (self._indent * self._level) + argString
        return argString
