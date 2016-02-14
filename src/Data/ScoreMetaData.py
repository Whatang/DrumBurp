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

class ScoreMetaData(object):
    def __init__(self):
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
        self.measureCountsVisible = False

    def makeEmpty(self):
        self.title = "Untitled"
        self.artist = "Unknown"
        self.creator = "Nobody"
