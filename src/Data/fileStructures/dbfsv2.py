# Copyright 2017 Michael Thomas
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
                            StringField, NonNegativeIntegerField, BooleanField)

import Data.ScoreMetaData
import Data.Score

from Data.fileStructures.dbfsv1 import DrumKitStructureV1, MeasureStructureV1, DefaultMeasureCountStructureV1
from Data.fileStructures.dbfsv0 import FontOptionsStructureV0


class MetadataStructureV2(FileStructure):
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
    swing = NonNegativeIntegerField("SWING")


class ScoreStructureV2(FileStructure):
    tag = "SCORE"
    targetClass = Data.Score.Score

    scoreData = MetadataStructureV2()
    drumKit = DrumKitStructureV1()
    measures = MeasureStructureV1(singleton=False,
                                  getter=lambda score: list(
                                      score.iterMeasures()),
                                  setter=lambda score, msr: score.insertMeasureByIndex(0, measure=msr))
    _sections = StringField("SECTION_TITLE", singleton=False)
    paperSize = StringField("PAPER_SIZE")
    lilysize = PositiveIntegerField("LILYSIZE")
    lilypages = NonNegativeIntegerField("LILYPAGES")
    lilyFill = BooleanField("LILYFILL")
    lilyFormat = NonNegativeIntegerField("LILYFORMAT")
    defaultCount = DefaultMeasureCountStructureV1()
    systemSpacing = NonNegativeIntegerField("SYSTEM_SPACE")
    fontOptions = FontOptionsStructureV0()

    def postProcessObject(self, instance):
        instance.postReadProcessing()
        return instance
