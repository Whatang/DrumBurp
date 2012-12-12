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
        for lineType, lineData in scoreIterator:
            if lineData is None:
                lineData = ""
            if lineType == "SCORE_METADATA":
                continue
            if lineType == "TITLE":
                self.title = lineData
            elif lineType == "ARTIST":
                self.artist = lineData
            elif lineType == "ARTISTVISIBLE":
                self.artistVisible = (lineData == "True")
            elif lineType == "CREATOR":
                self.creator = lineData
            elif lineType == "CREATORVISIBLE":
                self.creatorVisible = (lineData == "True")
            elif lineType == "BPM":
                try:
                    self.bpm = int(lineData)
                except (TypeError, ValueError):
                    raise IOError("Bad BPM: " + lineData)
                if self.bpm <= 0:
                    raise IOError("Bad BPM: " + lineData)
            elif lineType == "BPMVISIBLE":
                self.bpmVisible = (lineData == "True")
            elif lineType == "WIDTH":
                try:
                    self.width = int(lineData)
                except (TypeError, ValueError):
                    raise IOError("Bad score width: " + lineData)
                if self.width <= 0:
                    raise IOError("Bad score width: " + lineData)
            elif lineType == "KITDATAVISIBLE":
                self.kitDataVisible = (lineData == "True")
            elif lineType == "METADATAVISIBLE":
                self.metadataVisible = (lineData == "True")
            elif lineType == "BEATCOUNTVISIBLE":
                self.beatCountVisible = (lineData == "True")
            elif lineType == "EMPTYLINESVISIBLE":
                self.emptyLinesVisible = (lineData == "True")
            elif lineType == "END_SCORE_METADATA":
                break
            else:
                raise IOError("Unrecognised line type: " + lineType)

    def save(self, handle, indenter):
        print >> handle, indenter("SCORE_METADATA")
        indenter.increase()
        print >> handle, indenter("TITLE", self.title)
        print >> handle, indenter("ARTIST", self.artist)
        print >> handle, indenter("ARTISTVISIBLE", str(self.artistVisible))
        print >> handle, indenter("CREATOR", self.creator)
        print >> handle, indenter("CREATORVISIBLE", str(self.creatorVisible))
        print >> handle, indenter("BPM", self.bpm)
        print >> handle, indenter("BPMVISIBLE", str(self.bpmVisible))
        print >> handle, indenter("WIDTH", self.width)
        print >> handle, indenter("KITDATAVISIBLE", str(self.kitDataVisible))
        print >> handle, indenter("METADATAVISIBLE", str(self.metadataVisible))
        print >> handle, indenter("BEATCOUNTVISIBLE",
                                  str(self.beatCountVisible))
        print >> handle, indenter("EMPTYLINESVISIBLE",
                                  str(self.emptyLinesVisible))
        indenter.decrease()
        print >> handle, indenter("END_SCORE_METADATA")


    def exportASCII(self):
        metadataString = []
        metadataString.append("Title     : " + self.title)
        if self.artistVisible:
            metadataString.append("Artist    : " + self.artist)
        if self.bpmVisible:
            metadataString.append("BPM       : " + str(self.bpm))
        if self.creatorVisible:
            metadataString.append("Tabbed by : " + self.creator)
        metadataString.append("Date      : " + time.strftime("%d %B %Y"))
        metadataString.append("")
        return metadataString
