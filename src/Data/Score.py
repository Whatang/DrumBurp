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

import Data.DrumKit as DrumKit
from Data.Staff import Staff
from Data.Measure import Measure
from Data.Counter import CounterRegistry
from Data.MeasureCount import makeSimpleCount
from Data.DBErrors import BadTimeError, OverSizeMeasure, DBVersionError
from Data.NotePosition import NotePosition
from Data.ScoreMetaData import ScoreMetaData
from Data.FontOptions import FontOptions
import Data.fileUtils as fileUtils
import bisect
import hashlib
import gzip
import itertools
import codecs
from StringIO import StringIO

CURRENT_FILE_FORMAT = 0

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
        self.drumKit = DrumKit.DrumKit()
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
        self.lilyFormat = 0

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

    def _checkStaffIndex(self, index):
        if not (0 <= index < self.numStaffs()):
            raise BadTimeError()

    def _checkDrumIndex(self, index):
        if not(0 <= index < len(self.drumKit)):
            raise BadTimeError()

    def _checkMeasureIndex(self, index, endOk = False):
        if not(0 <= index < self.numMeasures()):
            if not (endOk and index == self.numMeasures()):
                raise BadTimeError()

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
            realMeasure = measure
            if measure.simileDistance:
                realMeasure = self.getReferredMeasure(index)
            yield realMeasure, index
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
        self._checkMeasureIndex(index)
        staff, index = self._staffContainingMeasure(index)
        return staff[index]

    def getReferredMeasure(self, index):
        self._checkMeasureIndex(index)
        measure = self.getMeasure(index)
        while index > 0 and measure.simileDistance > 0:
            index -= measure.simileDistance
            if index <= 0:
                index = 0
            measure = self.getMeasure(index)
        return measure

    def getItemAtPosition(self, position):
        if position.staffIndex is None:
            return self
        self._checkStaffIndex(position.staffIndex)
        staff = self.getStaff(position.staffIndex)
        if position.measureIndex is None:
            return staff
        if position.drumIndex is not None:
            self._checkDrumIndex(position.drumIndex)
        return staff.getItemAtPosition(position)

    def getStaff(self, index):
        return self._staffs[index]

    def numStaffs(self):
        return len(self._staffs)

    def _addStaff(self):
        newStaff = Staff()
        self._staffs.append(newStaff)
        self._setStaffCallBack(newStaff, self.numStaffs() - 1)

    def _deleteStaffByIndex(self, index):
        self._checkStaffIndex(index)
        staff = self._staffs[index]
        staff.clearCallBack()
        if staff.isSectionEnd():
            if index == 0 or self.getStaff(index - 1).isSectionEnd():
                position = NotePosition(staffIndex = index)
                sectionIndex = self.getSectionIndex(position)
                self._deleteSectionTitle(sectionIndex)
            else:
                prevStaff = self.getStaff(index - 1)
                position = NotePosition(staffIndex = index - 1,
                                        measureIndex =
                                        prevStaff.numMeasures() - 1)
                prevStaff.setSectionEnd(position, True)
        self._staffs.pop(index)
        for offset, nextStaff in enumerate(self._staffs[index:]):
            self._setStaffCallBack(nextStaff, index + offset)

    def numMeasures(self):
        return sum(staff.numMeasures() for staff in self.iterStaffs())

    def _staffContainingMeasure(self, index):
        measuresSoFar = 0
        for staff in self.iterStaffs():
            if measuresSoFar <= index < measuresSoFar + staff.numMeasures():
                return staff, index - measuresSoFar
            measuresSoFar += staff.numMeasures()
        raise BadTimeError()

    def getMeasureIndex(self, position):
        self._checkStaffIndex(position.staffIndex)
        index = 0
        for staffIndex in xrange(0, position.staffIndex):
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


    def insertMeasureByIndex(self, width, index = None, counter = None):
        if index is None:
            index = self.numMeasures()
        if self.numStaffs() == 0:
            self._addStaff()
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

    def insertMeasureByPosition(self, width, position = None, counter = None):
        if position is None:
            if self.numStaffs() == 0:
                self._addStaff()
            position = NotePosition(self.numStaffs() - 1)
            staff = self.getStaff(self.numStaffs() - 1)
            position.measureIndex = staff.numMeasures()
        self._checkStaffIndex(position.staffIndex)
        newMeasure = Measure(width)
        newMeasure.counter = counter
        staff = self.getStaff(position.staffIndex)
        staff.insertMeasure(position, newMeasure)
        return newMeasure

    def deleteMeasureByIndex(self, index):
        self._checkMeasureIndex(index)
        np = self.getMeasurePosition(index)
        self.deleteMeasureByPosition(np)

    def deleteMeasureByPosition(self, position):
        self._checkStaffIndex(position.staffIndex)
        staff = self.getStaff(position.staffIndex)
        if (staff.isSectionEnd()
            and position.measureIndex == staff.numMeasures() - 1):
            sectionIndex = self.getSectionIndex(position)
            self._deleteSectionTitle(sectionIndex)
        staff.deleteMeasure(position)

    def deleteMeasuresAtPosition(self, position, numToDelete):
        position = position.makeMeasurePosition()
        staff = self.getStaff(position.staffIndex)
        for dummyIndex in xrange(numToDelete):
            if position.measureIndex == staff.numMeasures():
                if staff.numMeasures() == 0:
                    self._deleteStaffByIndex(position.staffIndex)
                else:
                    position.staffIndex += 1
                    position.measureIndex = 0
                staff = self.getStaff(position.staffIndex)
            staff.deleteMeasure(position)

    def trailingEmptyMeasures(self):
        emptyMeasures = []
        np = NotePosition(staffIndex = self.numStaffs() - 1)
        staff = self.getItemAtPosition(np)
        np.measureIndex = staff.numMeasures() - 1
        measure = self.getItemAtPosition(np)
        while ((np.staffIndex > 0 or np.measureIndex > 0)
               and measure.isEmpty()):  # pylint:disable-msg=E1103
            emptyMeasures.append(np.makeMeasurePosition())
            if np.measureIndex == 0:
                np.staffIndex -= 1
                staff = self.getStaff(np.staffIndex)
                np.measureIndex = staff.numMeasures()
            np.measureIndex -= 1
            measure = self.getItemAtPosition(np)
        return emptyMeasures

    def copyMeasure(self, position):
        self._checkStaffIndex(position.staffIndex)
        staff = self.getStaff(position.staffIndex)
        return staff.copyMeasure(position)

    def pasteMeasure(self, position, notes, copyMeasureDecorations = False):
        self._checkStaffIndex(position.staffIndex)
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
        assert(len(ends) == self.numSections())
        return bisect.bisect_left(ends, position.staffIndex)

    def getSectionTitle(self, index):
        return self._sections[index]

    def setSectionTitle(self, index, title):
        self._sections[index] = title

    def _deleteSectionTitle(self, index):
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
            self._deleteStaffByIndex(startIndex)
        self._deleteStaffByIndex(startIndex)

    def iterSections(self):
        return iter(self._sections)

    def setSectionEnd(self, position, onOff, title = None):
        self._checkStaffIndex(position.staffIndex)
        staff = self.getStaff(position.staffIndex)
        sectionIndex = self.getSectionIndex(position)
        if onOff:
            if title is None:
                title = "New Section"
            self._sections.insert(sectionIndex, title)
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
        self._checkStaffIndex(position.staffIndex)
        staff = self.getStaff(position.staffIndex)
        if not (0 <= position.measureIndex < staff.numMeasures()):
            raise BadTimeError()
        position = position.makeMeasurePosition()
        position.measureIndex += 1
        if position.measureIndex == staff.numMeasures():
            position.staffIndex += 1
            if position.staffIndex == self.numStaffs():
                position.staffIndex = None
                position.measureIndex = None
            else:
                position.measureIndex = 0
        return position

    @staticmethod
    def _getPrefixAndDigitSuffix(targetString):
        withoutDigitSuffix = targetString.rstrip("0123456789")
        if withoutDigitSuffix == targetString:
            return targetString, None
        suffix = targetString[len(withoutDigitSuffix):]
        suffix = int(suffix)
        return withoutDigitSuffix, suffix

    def _makeNewSectionTitle(self, startTitle):
        stem, suffix = self._getPrefixAndDigitSuffix(startTitle)
        if suffix is None:
            return
        for section in self.iterSections():
            sectionStem, sectionSuffix = self._getPrefixAndDigitSuffix(section)
            if sectionStem == stem:
                suffix = max(suffix, sectionSuffix)
        return "%s %d" % (stem, suffix + 1)

    def insertSectionCopy(self, position, sectionIndex):
        self.turnOffCallBacks()
        position = position.makeMeasurePosition()
        try:
            self._checkStaffIndex(position.staffIndex)
            sectionMeasures = list(self.iterMeasuresInSection(sectionIndex))
            sectionTitle = self._makeNewSectionTitle(self.getSectionTitle(sectionIndex))
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

    def addNote(self, position, head = None):
        self._checkStaffIndex(position.staffIndex)
        self._checkDrumIndex(position.drumIndex)
        if head is None:
            head = self.drumKit[position.drumIndex].head
        self.getStaff(position.staffIndex).addNote(position, head)

    def deleteNote(self, position):
        self._checkStaffIndex(position.staffIndex)
        self._checkDrumIndex(position.drumIndex)
        self.getStaff(position.staffIndex).deleteNote(position)

    def toggleNote(self, position, head = None):
        self._checkStaffIndex(position.staffIndex)
        self._checkDrumIndex(position.drumIndex)
        if head is None:
            head = self.drumKit[position.drumIndex].head
        self.getStaff(position.staffIndex).toggleNote(position, head)

    def notePlus(self, pos, ticks):
        self._checkStaffIndex(pos.staffIndex)
        self._checkDrumIndex(pos.drumIndex)
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
        current = first.makeMeasurePosition()
        end = second.makeMeasurePosition()
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

    def formatScore(self, width = None, ignoreErrors = True):
        if width is None:
            width = self.scoreData.width
        measures = list(self.iterMeasures())
        if not self._formatState:
            self.saveFormatState()
        for staff in self.iterStaffs():
            staff.clear()
        staff = self.getStaff(0)
        staffIndex = 0
        staffWidth = 0
        for measureIndex, measure in enumerate(measures):
            staff.addMeasure(measure)
            if staffWidth == 0:
                staffWidth = 2
            if measure.simileDistance > 0:
                referredMeasure = measure
                refIndex = measureIndex
                while refIndex > 0 and referredMeasure.simileDistance > 0:
                    refIndex -= referredMeasure.simileDistance
                    if refIndex < 0:
                        refIndex = 0
                    referredMeasure = measures[refIndex]
                measureWidth = referredMeasure.numBeats()
            else:
                measureWidth = len(measure)
            staffWidth += measureWidth + 1
            while staffWidth > width:
                if staff.numMeasures() == 1:
                    if ignoreErrors:
                        break
                    else:
                        raise OverSizeMeasure(measure)
                else:
                    staff.deleteLastMeasure()
                    staffIndex += 1
                    if staffIndex == self.numStaffs():
                        self._addStaff()
                    staff = self.getStaff(staffIndex)
                    staff.addMeasure(measure)
                    staffWidth = 2 + measureWidth
            if (measure.isLineEnd() and
                measureIndex != len(measures) - 1):
                staffIndex += 1
                if staffIndex == self.numStaffs():
                    self._addStaff()
                staff = self.getStaff(staffIndex)
                staffWidth = 0
        while self.numStaffs() > staffIndex + 1:
            staff = self._staffs.pop()
            staff.clearCallBack()
        return self._formatState != self._getFormatState()

    def changeKit(self, newKit, changes):
        for measure in self.iterMeasures():
            measure.changeKit(newKit, changes)
        self.drumKit = newKit

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
            if (drum.locked or self.scoreData.emptyLinesVisible
                or staff.lineIsVisible(lineNum)):
                count += 1
                if count == lineIndex:
                    return lineNum
        if count == -1 and lineIndex == 0:
            return 0
        raise BadTimeError(staffIndex)

    def _iterLinesLockedOrWithNotes(self, staffIndex):
        staff = self.getStaff(staffIndex)
        count = 0
        for lineNum, drum in enumerate(self.drumKit):
            if (drum.locked
                or staff.lineIsVisible(lineNum)):
                count += 1
                yield drum
        if count == 0:
            yield self.drumKit[0]

    def iterVisibleLines(self, staffIndex, forceIgnoreEmpty = False):
        if self.scoreData.emptyLinesVisible and not forceIgnoreEmpty:
            return iter(self.drumKit)
        else:
            return self._iterLinesLockedOrWithNotes(staffIndex)

    def write(self, handle):
        indenter = fileUtils.Indenter(handle)
        indenter("DB_FILE_FORMAT", CURRENT_FILE_FORMAT)
        self.scoreData.save(indenter)
        self.drumKit.write(indenter)
        for measure in self.iterMeasures():
            measure.write(indenter)
        for title in self._sections:
            indenter("SECTION_TITLE", title)
        indenter("PAPER_SIZE", self.paperSize)
        indenter("LILYSIZE", self.lilysize)
        indenter("LILYPAGES", self.lilypages)
        if self.lilyFill:
            indenter("LILYFILL", "YES")
        indenter("LILYFORMAT", self.lilyFormat)
        self.defaultCount.write(indenter, True)
        indenter("SYSTEM_SPACE", self.systemSpacing)
        self.fontOptions.write(indenter)


    def read(self, handle):
        # Check the file format version
        handle, handleCopy = itertools.tee(handle)
        firstline = handleCopy.next()
        del handleCopy
        scoreIterator = fileUtils.dbFileIterator(handle)
        if firstline.startswith("DB_FILE_FORMAT"):
            versionDict = {}
            with scoreIterator.section(None, None, readLines = 1) as section:
                section.readNonNegativeInteger("DB_FILE_FORMAT", versionDict, "fileVersion")
            fileVersion = versionDict.get("fileVersion", 0)
        else:
            fileVersion = 0
        if fileVersion > CURRENT_FILE_FORMAT:
            raise DBVersionError(scoreIterator)
        # Read from the input file
        self.lilyFill = False
        self.lilyFormat = 0
        def _readMeasure(lineData):
            measureWidth = int(lineData)
            measure = self.insertMeasureByIndex(measureWidth)
            measure.read(scoreIterator)
        with scoreIterator.section(None, None) as section:
            section.readSubsection("SCORE_METADATA", self.scoreData.load)
            section.readCallback("START_BAR", _readMeasure)
            section.readSubsection("KIT_START", self.drumKit.read)
            section.readCallback("SECTION_TITLE",
                                 self._sections.append)
            section.readString("PAPER_SIZE", self, "paperSize")
            section.readPositiveInteger("LILYSIZE", self, "lilySize")
            section.readNonNegativeInteger("LILYPAGES", self, "lilyPages")
            section.readBoolean("LILYFILL", self, "lilyFill")
            section.readNonNegativeInteger("LILYFORMAT", self, "lilyFormat")
            section.readSubsection("DEFAULT_COUNT_INFO_START",
                                   lambda i: self.defaultCount.read(i, True))
            section.readNonNegativeInteger("SYSTEM_SPACE", self,
                                           "systemSpacing")
            section.readSubsection("FONT_OPTIONS_START", self.fontOptions.read)
        # Check that all the note heads are valid
        for measure in self.iterMeasures():
            for np, head in measure:
                if not self.drumKit[np.drumIndex].isAllowedHead(head):
                    self.drumKit[np.drumIndex].addNoteHead(head)
        # Format the score appropriately
        self.formatScore(self.scoreData.width)
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
        scoreString = scoreString.getvalue()
        return hashlib.md5(scoreString.encode('utf-8')).digest()  # pylint:disable-msg=E1121

class ScoreFactory(object):
    def __call__(self, filename = None,
                 numMeasures = 32,
                 counter = None,
                 kit = None):
        if filename is not None:
            score = self.loadScore(filename)
        else:
            score = self.makeEmptyScore(numMeasures, counter, kit)
        return score

    @classmethod
    def makeEmptyScore(cls, numMeasures, counter, kit):
        score = Score()
        if kit is None:
            kit = DrumKit.getNamedDefaultKit()
        score.drumKit = kit
        if counter is None:
            registry = CounterRegistry()
            counter = list(registry.countsByTicks(2))
            counter = counter[0][1]
            counter = makeSimpleCount(counter, 4)
        for dummy in xrange(numMeasures):
            score.insertMeasureByIndex(len(counter), counter = counter)
        score.scoreData.makeEmpty()
        return score

    @classmethod
    def loadScore(cls, filename):
        score = Score()
        try:
            with gzip.open(filename, 'rb') as handle:
                with codecs.getreader('utf-8')(handle) as reader:
                    score.read(reader)
        except IOError:
            score = Score()
            with open(filename, 'rU') as handle:
                score.read(handle)
        return score

    @classmethod
    def saveScore(cls, score, filename):
        scoreBuffer = StringIO()
        score.write(scoreBuffer)
        with gzip.open(filename, 'wb') as handle:
            with codecs.getwriter('utf-8')(handle) as writer:
                writer.write(scoreBuffer.getvalue())
