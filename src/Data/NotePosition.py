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
Created on 14 Dec 2010

@author: Mike Thomas
'''

from DBErrors import BadNoteSpecification
import copy

class NotePosition(object):
    def __init__(self, staffIndex = None, measureIndex = None,
                 noteTime = None, drumIndex = None):
        if [noteTime, drumIndex].count(None) == 1:
            raise BadNoteSpecification(staffIndex, measureIndex,
                                       noteTime, drumIndex)
        self.staffIndex = staffIndex
        self.measureIndex = measureIndex
        self.noteTime = noteTime
        self.drumIndex = drumIndex

    def __str__(self):
        return ", ".join(str(x) for x in [self.staffIndex, self.measureIndex,
                                          self.noteTime, self.drumIndex])

    def makeMeasurePosition(self):
        np = copy.copy(self)
        np.noteTime = None
        np.drumIndex = None
        return np

    def makeStaffPosition(self):
        np = self.makeMeasurePosition()
        np.measureIndex = None
        return np
