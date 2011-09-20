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
        self._head = head
        if midiNote is None:
            midiNote = _guessMidiNote(abbr)
        self.midiNote = midiNote
        self._noteHeads = ["x", "X", "o", "O", "g", "f", "d", "+", "#", "b"]
        self._headData = {}
        for h in self._noteHeads:
            self._headData[h] = HeadData(midiNote = midiNote,
                                         effect = _DEFAULTEFFECT[h])
        self.locked = locked
        self.setDefaultHead(head)
        assert(len(name) > 0)
        assert(1 <= len(abbr) <= DRUM_ABBR_WIDTH)
        assert(len(head) == 1)

    @property
    def head(self):
        return self._head

    def setDefaultHead(self, head):
        assert(head in self._headData)
        self._head = head
        index = self._noteHeads.index(head)
        self._noteHeads = [head] + self._noteHeads[:index] + self._noteHeads[index + 1:]

    def __iter__(self):
        return iter(self._noteHeads)

    def __len__(self):
        return len(self._noteHeads)

    def __getitem__(self, index):
        return self._noteHeads[index]

    def __eq__(self, other):
        return self.name == other.name or self.abbr == other.abbr

    def headData(self, head):
        return self._headData[head]

    def exportASCII(self):
        return "%2s - %s" % (self.abbr, self.name)

    def isAllowedHead(self, head):
        return head in self._headData

    def renameHead(self, oldHead, head):
        try:
            index = self._noteHeads.index(oldHead)
        except IndexError:
            return
        self._noteHeads[index] = head
        self._headData[head] = self._headData.pop(oldHead)
        if self._head == oldHead:
            self._head = head

    def addNoteHead(self, head):
        self._noteHeads.append(head)
        self._headData[head] = HeadData(midiNote = self.midiNote)

    def removeNoteHead(self, head):
        try:
            self._noteHeads.remove(head)
        except ValueError:
            return
        self._headData.pop(head)

    def moveHeadUp(self, head):
        try:
            index = self._noteHeads.index(head)
        except IndexError:
            return
        assert(index > 1)
        self._noteHeads[index - 1:index + 1] = reversed(self._noteHeads[index - 1:index + 1])

    def moveHeadDown(self, head):
        try:
            index = self._noteHeads.index(head)
        except IndexError:
            return
        assert(index < len(self) - 1)
        self._noteHeads[index:index + 2] = reversed(self._noteHeads[index:index + 2])



def _guessMidiNote(abbr):
    for drumData in DEFAULT_KIT:
        if abbr == drumData[1]:
            return drumData[4]
    return 71
