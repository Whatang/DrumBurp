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
Created on 23 Jan 2011

@author: Mike Thomas

'''
import time

class ScoreMetaData(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.title = ""
        self.artist = ""
        self.artistVisible = True
        self.bpm = 120
        self.bpmVisible = True
        self.creator = ""
        self.creatorVisible = True
        self.width = 80
        self.kitDataVisible = True
        self.metadataVisible = True
        self.beatCountVisible = True
        self.emptyLinesVisible = True

    def makeEmpty(self):
        self.title = "Untitled"
        self.artist = "Unknown"
        self.creator = "Nobody"

    def load(self, scoreIterator):
        with scoreIterator.section("SCORE_METADATA",
                                   "END_SCORE_METADATA") as section:
            section.readString("TITLE", self, "title")
            section.readString("ARTIST", self, "artist")
            section.readBoolean("ARTISTVISIBLE", self, "artistVisible")
            section.readString("CREATOR", self, "creator")
            section.readBoolean("CREATORVISIBLE", self, "creatorVisible")
            section.readPositiveInteger("BPM", self, "bpm")
            section.readBoolean("BPMVISIBLE", self, "bpmVisible")
            section.readPositiveInteger("WIDTH", self, "width")
            section.readBoolean("KITDATAVISIBLE", self, "kitDataVisible")
            section.readBoolean("METADATAVISIBLE", self, "metadataVisible")
            section.readBoolean("BEATCOUNTVISIBLE", self, "beatCountVisible")
            section.readBoolean("EMPTYLINESVISIBLE", self, "emptyLinesVisible")

    def save(self, indenter):
        with indenter.section("SCORE_METADATA", "END_SCORE_METADATA"):
            indenter("TITLE", self.title)
            indenter("ARTIST", self.artist)
            indenter("ARTISTVISIBLE", str(self.artistVisible))
            indenter("CREATOR", self.creator)
            indenter("CREATORVISIBLE", str(self.creatorVisible))
            indenter("BPM", self.bpm)
            indenter("BPMVISIBLE", str(self.bpmVisible))
            indenter("WIDTH", self.width)
            indenter("KITDATAVISIBLE", str(self.kitDataVisible))
            indenter("METADATAVISIBLE", str(self.metadataVisible))
            indenter("BEATCOUNTVISIBLE",
                                      str(self.beatCountVisible))
            indenter("EMPTYLINESVISIBLE",
                                      str(self.emptyLinesVisible))
