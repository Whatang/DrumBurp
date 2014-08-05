# Copyright 2011 Michael Thomas
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
        self.bpm = 120
        self.creator = ""
        self.width = 80

    def makeEmpty(self):
        self.title = "Untitled"
        self.artist = "Unknown"
        self.creator = "Nobody"

    def load(self, scoreIterator):
        for lineType, lineData in scoreIterator:
            if lineData is None:
                lineData = ""
            if lineType == "TITLE":
                self.title = lineData
            elif lineType == "ARTIST":
                self.artist = lineData
            elif lineType == "CREATOR":
                self.creator = lineData
            elif lineType == "BPM":
                self.bpm = int(lineData)
            elif lineType == "WIDTH":
                self.width = int(lineData)
            elif lineType == "END_SCORE_METADATA":
                break

    def save(self, handle, indenter):
        print >> handle, indenter("SCORE_METADATA")
        indenter.increase()
        print >> handle, indenter("TITLE", self.title)
        print >> handle, indenter("ARTIST", self.artist)
        print >> handle, indenter("CREATOR", self.creator)
        print >> handle, indenter("BPM", self.bpm)
        print >> handle, indenter("WIDTH", self.width)
        indenter.decrease()
        print >> handle, indenter("END_SCORE_METADATA")


    def exportASCII(self):
        metadataString = []
        metadataString.append("Title     : " + self.title)
        metadataString.append("Artist    : " + self.artist)
        metadataString.append("BPM       : " + str(self.bpm))
        metadataString.append("Tabbed by : " + self.creator)
        metadataString.append("Date      : " + time.strftime("%d %B %Y"))
        metadataString.append("")
        return metadataString
