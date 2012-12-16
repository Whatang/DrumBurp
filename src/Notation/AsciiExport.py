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
Created on Dec 15, 2012

@author: Mike Thomas
'''
from Data.DBConstants import REPEAT_EXTENDER, BARLINE, DRUM_ABBR_WIDTH, EMPTY_NOTE, REPEAT_END, REPEAT_STARTER, ALTERNATE_EXTENDER
from Data.NotePosition import NotePosition
import time

def getExportDate():
    return time.strftime("%d %B %Y")

class Exporter(object):
    def __init__(self, score, settings):
        self.score = score
        self.settings = settings
        self._isRepeating = False
        self._repeatExtender = None

    def _exportScoreData(self):
        scoreData = self.score.scoreData
        metadataString = []
        metadataString.append("Title     : " + scoreData.title)
        if scoreData.artistVisible:
            metadataString.append("Artist    : " + scoreData.artist)
        if scoreData.bpmVisible:
            metadataString.append("BPM       : " + str(scoreData.bpm))
        if scoreData.creatorVisible:
            metadataString.append("Tabbed by : " + scoreData.creator)
        metadataString.append("Date      : " + getExportDate())
        metadataString.append("")
        return metadataString

    @staticmethod
    def _barString(first, second):
        if first is None and second is None:
            return ""
        else:
            return BARLINE

    def _getDrumLine(self, staff, drum, position, drumIndex):
        position.drumIndex = drumIndex
        lastBar = None
        lineString = "%*s" % (DRUM_ABBR_WIDTH, drum.abbr)
        lineOk = False
        for measureIndex, measure in enumerate(staff):
            position.measureIndex = measureIndex
            barString = self._barString(lastBar, measure)
            lineString += barString
            lastBar = measure
            for noteTime in range(len(measure)):
                position.noteTime = noteTime
                note = measure.getNote(position)
                lineString += note
                lineOk = lineOk or note != EMPTY_NOTE
        barString = self._barString(lastBar, None)
        lineString += barString
        return lineString, lineOk

    def _getCountLine(self, staff):
        countString = "  "
        lastBar = None
        for measure in staff:
            barString = self._barString(lastBar, measure)
            lastBar = measure
            countString += " " * len(barString)
            countString += "".join(measure.count())
        barString = self._barString(lastBar, None)
        countString += " " * len(barString)
        return countString



    def _measureBegin(self, repeatString, measure, lastMeasure, delta):
        if not self._isRepeating:
            if measure and measure.isRepeatStart():
                if (lastMeasure and lastMeasure.isRepeatEnd()):
                    repeatString += REPEAT_END
                    delta = 1
                self._isRepeating = True
                self._repeatExtender = REPEAT_EXTENDER
                repeatString += REPEAT_STARTER
            elif (lastMeasure and
                lastMeasure.isRepeatEnd()):
                repeatString += REPEAT_END
            elif measure:
                repeatString += " "
        else:
            repeatString += self._repeatExtender
        return repeatString, delta


    def _measureMiddle(self, repeatString, measure, delta):
        if measure is not None:
            if measure.alternateText:
                repeatString += measure.alternateText
                delta += len(measure.alternateText)
                self._repeatExtender = ALTERNATE_EXTENDER
                self._isRepeating = True
            if self._isRepeating:
                repeatString += self._repeatExtender * (len(measure) - delta)
                delta = 0
            else:
                repeatString += " " * len(measure)
        return repeatString, delta


    def _measureEnd(self, measure, repeatString):
        if self._isRepeating and measure and measure.isRepeatEnd():
            self._isRepeating = False
            if self._repeatExtender == REPEAT_EXTENDER:
                repeatCount = "%dx" % measure.repeatCount
                repeatCountLength = len(repeatCount)
                repeatString = (repeatString[:-(repeatCountLength + 1)]
                                + repeatCount + repeatString[-1:])
        return repeatString

    def _getRepeatString(self, staff):
        staffString = []
        hasRepeat = (self._isRepeating or
                     any(measure.isRepeatStart() for measure in staff) or
                     any(measure.alternateText for measure in staff))
        if not hasRepeat:
            return staffString
        repeatString = "  "
        lastMeasure = None
        delta = 0
        for measure in list(staff) + [None]:
            repeatString, delta = self._measureBegin(repeatString,
                                                     measure, lastMeasure,
                                                     delta)
            repeatString, delta = self._measureMiddle(repeatString,
                                                      measure, delta)
            repeatString = self._measureEnd(measure, repeatString)
            lastMeasure = measure
        staffString = [repeatString]
        return staffString

    def _exportStaff(self, staff):
        kit = self.score.drumKit
        kitSize = len(kit)
        indices = range(0, kitSize)
        indices.reverse()
        position = NotePosition()
        staffString = self._getRepeatString(staff)
        for drumIndex in indices:
            drum = kit[drumIndex]
            lineString, lineOk = self._getDrumLine(staff,
                                                   drum,
                                                   position,
                                                   drumIndex)
            if lineOk or drum.locked or not self.settings.omitEmpty:
                staffString.append(lineString)
        if self.settings.printCounts:
            countString = self._getCountLine(staff)
            staffString.append(countString)
        return staffString

    def _exportKit(self):
        kitString = []
        for instr in self.score.drumKit:
            kitString.append("%2s - %s" % (instr.abbr, instr.name))
        kitString.reverse()
        kitString.append("")
        return kitString


    def _exportMusic(self, asciiString):
        newSection = True
        sectionIndex = 0
        self._isRepeating = False
        self._repeatExtender = REPEAT_EXTENDER
        for staff in self.score.iterStaffs():
            assert staff.isConsistent()
            if newSection:
                self._isRepeating = False
                newSection = False
                if sectionIndex < self.score.numSections():
                    if (len(asciiString) > 0 and
                        self.settings.emptyLineBeforeSection):
                        asciiString.append("")
                    title = self.score.getSectionTitle(sectionIndex)
                    asciiString.append(title)
                    if self.settings.underline:
                        asciiString.append("".join(["~"] * len(title)))
                    if self.settings.emptyLineAfterSection:
                        asciiString.append("")
                    sectionIndex += 1
            newSection = staff.isSectionEnd()
            staffString = self._exportStaff(staff)
            asciiString.extend(staffString)
            asciiString.append("")

        asciiString = asciiString[:-1]
        return asciiString

    def export(self, handle):
        metadataString = self._exportScoreData()
        asciiString = []
        asciiString = self._exportMusic(asciiString)
        kitString = self._exportKit()
        print >> handle, ("Tabbed with DrumBurp, "
                          "a drum tab editor from www.whatang.org")
        if self.settings.metadata:
            for mString in metadataString:
                print >> handle, mString
        if self.settings.kitKey:
            for iString in kitString:
                print >> handle, iString
        for sString in asciiString:
            print >> handle, sString
        print >> handle, ""
        print >> handle, ("Tabbed with DrumBurp, "
                          "a drum tab editor from www.whatang.org")

