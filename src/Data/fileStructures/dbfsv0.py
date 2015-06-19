# Copyright 2015 Michael Thomas
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

import weakref

from Data import DBErrors
from Data.fileUtils import (FileStructure, PositiveIntegerField,
                            SimpleValueField, Field, StringField,
                            NonNegativeIntegerField, BooleanField)

import Data.Beat
import Data.MeasureCount
import Data.NotePosition
import Data.Measure
import Data.Drum
import Data.DrumKit
import Data.ScoreMetaData
import Data.FontOptions
from Data.Counter import CounterRegistry
import Data.Score


class CounterFieldV0(SimpleValueField):
    registry = CounterRegistry()
    def _processData(self, data):
        if data[0] == "|" and data[-1] == "|":
            data = data[1:-1]
        data = Data.Beat.BEAT_COUNT + data[1:]
        try:
            return self.registry.findMaster(data)
        except KeyError:
            raise DBErrors.BadCount()

    def _toString(self, value):
        return "|" + value + "|"

class BeatStructureV0(FileStructure):
    tag = "BEAT"
    startTag = "BEAT_START"
    endTag = "BEAT_END"

    numTicks = PositiveIntegerField('NUM_TICKS')
    counter = CounterFieldV0("COUNT")

    def postProcessObject(self, instance):
        return Data.Beat.Beat(instance["counter"], instance.get("numTicks"))

class MeasureCountStructureV0(FileStructure):
    tag = "COUNT_INFO"
    startTag = "COUNT_INFO_START"
    endTag = "COUNT_INFO_END"

    beats = BeatStructureV0(singleton = False)
    repeat = PositiveIntegerField('REPEAT_BEATS')

    def postProcessObject(self, instance):
        mCount = Data.MeasureCount.MeasureCount()
        if 'repeat' not in instance:
            instance["repeat"] = 1
        mCount.beats = instance["beats"] * instance["repeat"]
        return mCount

class NoteFieldV0(Field):
    def read(self, target, data):
        noteTime, drumIndex, head = data.split(",")
        pos = Data.NotePosition.NotePosition(noteTime = int(noteTime),
                                             drumIndex = int(drumIndex))
        target.addNote(pos, head)

class BeatLengthFieldV0(Field):
    def read(self, target, data):
        target.counter = Data.MeasureCount.counterMaker(int(data),
                                                        len(target))

class BarlineFieldV0(Field):
    mapping = {"NO_BAR" : lambda x, y: True,
               "NORMAL_BAR" : lambda x, y: True,
               "REPEAT_START": Data.Measure.Measure.setRepeatStart,
               "REPEAT_END": Data.Measure.Measure.setRepeatEnd,
               "SECTION_END": Data.Measure.Measure.setSectionEnd,
               "LINE_BREAK": Data.Measure.Measure.setLineBreak}

    def __init__(self, title, attributeName = None, singleton = True):
        super(BarlineFieldV0, self).__init__(title, attributeName, singleton)
        self.seenStartLine = weakref.WeakSet()
        self.seenEndLine = weakref.WeakSet()

    def read(self, target, lineData):
        if target not in self.seenStartLine:
            target.startBar = 0
            for barType in lineData.split(","):
                self.mapping[barType](target, True)
            self.seenStartLine.add(target)
        elif target not in self.seenEndLine:
            target.endBar = 0
            for barType in lineData.split(","):
                self.mapping[barType](target, True)
            self.seenEndLine.add(target)
        else:
            raise DBErrors.TooManyBarLines()

class MeasureStructureV0(FileStructure):
    tag = "BAR"
    targetClass = Data.Measure.Measure

    counter = MeasureCountStructureV0()
    notes = NoteFieldV0("NOTE")
    barlines = BarlineFieldV0("BARLINE")
    beatLength = BeatLengthFieldV0("BEATLENGTH")
    alternateText = StringField("ALTERNATE")
    repeatCount = PositiveIntegerField("REPEAT_COUNT")
    simileDistance = NonNegativeIntegerField("SIMILE")
    simileIndex = NonNegativeIntegerField("SIMINDEX")

    def makeObject(self, startData):
        return self.targetClass(int(startData))

class MetadataStructureV0(FileStructure):
    tag = "SCORE_METADATA"
    startTag = "SCORE_METADATA"
    targetClass = Data.ScoreMetaData.ScoreMetaData

    title = StringField("TITLE")
    artist = StringField("ARTIST")
    artistVisible = BooleanField("ARTISTVISIBLE")
    creator = StringField("CREATOR")
    creatorVisible = BooleanField("CREATORVISIBLE")
    bpm = PositiveIntegerField("BPM")
    bpmVisible = BooleanField("BPMVISIBLE")
    width = PositiveIntegerField("WIDTH")
    kitDataVisible = BooleanField("KITDATAVISIBLE")
    metadataVisible = BooleanField("METADATAVISIBLE")
    beatCountVisible = BooleanField("BEATCOUNTVISIBLE")
    emptyLinesVisible = BooleanField("EMPTYLINESVISIBLE")
    measureCountsVisible = BooleanField("MEASURECOUNTSVISIBLE")

class DrumField(Field):
    def read(self, target, data):
        fields = data.split(",")
        if len(fields) > 3:
            fields[3] = (fields[3] == "True")
            if len(fields) > 4:
                fields = fields[:3]
        drum = Data.Drum.Drum(*fields)
        target.addDrum(drum)

class NoteHeadField(Field):
    def read(self, target, data):
        lastDrum = target[-1]
        lastDrum.readHeadData(data)

class DrumKitStructureV0(FileStructure):
    tag = "KIT"
    startTag = "KIT_START"
    endTag = "KIT_END"
    targetClass = Data.DrumKit.DrumKit

    drums = DrumField("DRUM")
    noteheads = NoteHeadField("NOTEHEAD")

    def postProcessObject(self, instance):
        for drum in instance:
            if len(drum) == 0:
                drum.guessHeadData()
            drum.checkShortcuts()
        return instance

class FontOptionsStructureV0(FileStructure):
    tag = "FONT_OPTIONS"
    startTag = "FONT_OPTIONS_START"
    endTag = "FONT_OPTIONS_END"
    targetClass = Data.FontOptions.FontOptions

    noteFont = StringField("NOTEFONT")
    noteFontSize = PositiveIntegerField("NOTEFONTSIZE")
    sectionFont = StringField("SECTIONFONT")
    sectionFontSize = PositiveIntegerField("SECTIONFONTSIZE")
    metadataFont = StringField("METADATAFONT")
    metadataFontSize = PositiveIntegerField("METADATAFONTSIZE")

class ScoreStructureV0(FileStructure):
    tag = "SCORE"
    targetClass = Data.Score.Score
    autoMake = True

    scoreData = MetadataStructureV0()
    measures = MeasureStructureV0(singleton = False)
    drumKit = DrumKitStructureV0()
    _sections = StringField("SECTION_TITLE", singleton = False)
    paperSize = StringField("PAPER_SIZE")
    lilySize = PositiveIntegerField("LILYSIZE")
    lilyPages = NonNegativeIntegerField("LILYPAGES")
    lilyFill = BooleanField("LILYFILL")
    lilyFormat = NonNegativeIntegerField("LILYFORMAT")
    defaultCount = MeasureCountStructureV0(singleton = True,
                                           startTag = "DEFAULT_COUNT_INFO_START")
    systemSpacing = NonNegativeIntegerField("SYSTEM_SPACE")
    fontOptions = FontOptionsStructureV0()

    def postProcessObject(self, instance):
        for measure in instance.measures:
            instance.insertMeasureByIndex(0, measure = measure)
        instance.postReadProcessing()
        return instance
