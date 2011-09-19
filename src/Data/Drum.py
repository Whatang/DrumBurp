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
Created on 12 Dec 2010

@author: Mike Thomas

'''

from DBConstants import DRUM_ABBR_WIDTH
from DefaultKits import DEFAULT_KIT

class HeadData(object):
    def __init__(self, midiNote = 36, midiVolume = 64, effect = "normal"):
        self.midiNote = midiNote
        self.midiVolume = midiVolume
        self.effect = effect

_DEFAULTEFFECT = {"x":"normal",
                  "X":"accent",
                  "o":"normal",
                  "O":"accent",
                  "g":"ghost",
                  "f":"flam",
                  "d":"drag",
                  "+":"choke",
                  "#":"choke",
                  "b":"normal"}

class Drum(object):
    '''
    classdocs
    '''
    def __init__(self, name, abbr, head, locked = False, midiNote = None):
        self.name = name
        self.abbr = abbr
        self.head = head
        if midiNote is None:
            midiNote = _guessMidiNote(abbr)
        self.midiNote = midiNote
        self.noteHeads = ["x", "X", "o", "O", "g", "f", "d", "+", "#", "b"]
        self.headData = {}
        for h in self.noteHeads:
            self.headData[h] = HeadData(midiNote = midiNote,
                                        effect = _DEFAULTEFFECT[h])
        self.locked = locked
        assert(len(name) > 0)
        assert(1 <= len(abbr) <= DRUM_ABBR_WIDTH)
        assert(len(head) == 1)

    def __eq__(self, other):
        return self.name == other.name or self.abbr == other.abbr

    def exportASCII(self):
        return "%2s - %s" % (self.abbr, self.name)

    def renameHead(self, oldHead, head):
        try:
            index = self.noteHeads.index(oldHead)
        except IndexError:
            return
        self.noteHeads[index] = head
        self.headData[head] = self.headData.pop(oldHead)
        if self.head == oldHead:
            self.head = head


def _guessMidiNote(abbr):
    for drumData in DEFAULT_KIT:
        if abbr == drumData[1]:
            return drumData[4]
    return 71
