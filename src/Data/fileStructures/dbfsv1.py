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

from Data.fileUtils import (FileStructure, PositiveIntegerField,
                            StringField, NonNegativeIntegerField, BooleanField,
                            IntegerField)

import Data.Beat
import Data.MeasureCount
import Data.NotePosition
import Data.Measure
import Data.Drum
import Data.DrumKit
import Data.ScoreMetaData
import Data.FontOptions
import Data.DBConstants
import Data.DefaultKits
import Data.Score
import Data.fileStructures.dbfsv0 as dbfsv0

class BeatStructureV1(FileStructure):
    tag = "BEAT"
    startTag = "BEAT_START"
    endTag = "BEAT_END"

    numTicks = PositiveIntegerField('NUM_TICKS')
    counter = dbfsv0.CounterFieldV0("COUNT")

    def postProcessObject(self, instance):
        return Data.Beat.Beat(instance["counter"], instance.get("numTicks"))

def _beatStructure():
    return BeatStructureV1(singleton = False,
                            setter = lambda count, beat: count.addBeats(beat, 1))

class MeasureCountStructureV1(FileStructure):
    tag = "MEASURE_COUNT"
    targetClass = Data.MeasureCount.MeasureCount

    beats = _beatStructure()

class DefaultMeasureCountStructureV1(FileStructure):
    tag = "DEFAULT_MEASURE_COUNT"
    targetClass = Data.MeasureCount.MeasureCount

    beats = _beatStructure()

class MeasureStructureV1(FileStructure):
    tag = "MEASURE"
    targetClass = Data.Measure.Measure

    counter = MeasureCountStructureV1()
    startBar = NonNegativeIntegerField("STARTBARLINE")
    notes = dbfsv0.NoteFieldV0("NOTE", getter = list, singleton = False)
    endBar = NonNegativeIntegerField("ENDBARLINE")
    repeatCount = PositiveIntegerField("REPEAT_COUNT")
    alternateText = StringField("ALTERNATE")
    simileDistance = NonNegativeIntegerField("SIMILE")
    simileIndex = NonNegativeIntegerField("SIMINDEX")

class NoteHeadStructureV1(FileStructure):
    tag = "NOTEHEAD"
    targetClass = Data.Drum.HeadData

    midiNote = NonNegativeIntegerField("MIDINOTE")
    midiVolume = NonNegativeIntegerField("MIDIVOLUME")
    effect = StringField("EFFECT")
    notationHead = StringField("NOTATIONHEAD")
    notationLine = IntegerField("NOTATIONLINE")
    notationEffect = StringField("NOTATIONEFFECT")
    stemDirection = IntegerField("STEM")
    shortcut = StringField("SHORTCUT")

class DrumStructureV1(FileStructure):
    tag = "DRUM"

    name = StringField("NAME")
    abbr = StringField("ABBR")
    head = StringField("DEFAULT_HEAD")
    locked = BooleanField("LOCKED")
    headlist = StringField("HEADLIST",
                           getter = lambda drum: "".join(list(drum)))
    noteheads = NoteHeadStructureV1(singleton = False)

    def postProcessObject(self, instance):
        drum = Data.Drum.Drum(instance["name"],
                              instance["abbr"],
                              instance["head"],
                              instance["locked"])
        for head, headData in zip(instance["headlist"], instance["noteheads"]):
            drum.addNoteHead(head, headData)
        return drum

class DrumKitStructureV1(FileStructure):
    tag = "KIT"
    targetClass = Data.DrumKit.DrumKit
    drums = DrumStructureV1(singleton = False, getter = list,
                            setter = lambda kit, drum: kit.addDrum(drum))

class ScoreStructureV1(FileStructure):
    tag = "SCORE"
    targetClass = Data.Score.Score

    scoreData = dbfsv0.MetadataStructureV0()
    drumKit = DrumKitStructureV1()
    measures = MeasureStructureV1(singleton = False,
                                  getter = lambda score:list(score.iterMeasures()),
                                  setter = lambda score, msr: score.insertMeasureByIndex(0, measure = msr))
    _sections = StringField("SECTION_TITLE", singleton = False)
    paperSize = StringField("PAPER_SIZE")
    lilysize = PositiveIntegerField("LILYSIZE")
    lilypages = NonNegativeIntegerField("LILYPAGES")
    lilyFill = BooleanField("LILYFILL")
    lilyFormat = NonNegativeIntegerField("LILYFORMAT")
    defaultCount = DefaultMeasureCountStructureV1()
    systemSpacing = NonNegativeIntegerField("SYSTEM_SPACE")
    fontOptions = dbfsv0.FontOptionsStructureV0()

    def postProcessObject(self, instance):
        instance.postReadProcessing()
        return instance
