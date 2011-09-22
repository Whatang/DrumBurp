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
import copy

from DBConstants import DRUM_ABBR_WIDTH
from DefaultKits import DEFAULT_KIT, DEFAULT_EXTRA_HEADS

_DEFAULTNOTE = 71
_DEFAULTVOLUME = 96

class HeadData(object):
    def __init__(self, midiNote = _DEFAULTNOTE,
                 midiVolume = _DEFAULTVOLUME,
                 effect = "normal"):
        self.midiNote = midiNote
        self.midiVolume = midiVolume
        self.effect = effect

    def write(self, noteHead, handle, indenter):
        dataString = "%s %d,%d,%s" % (noteHead, self.midiNote,
                                      self.midiVolume,
                                      self.effect)
        print >> handle, indenter("NOTEHEAD", dataString)

    @staticmethod
    def read(dataString):
        head, data = dataString.split()
        note, volume, effect = data.split(",")
        note = int(note)
        volume = int(volume)
        return head, HeadData(note, volume, effect)


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
    def __init__(self, name, abbr, head, locked = False):
        self.name = name
        self.abbr = abbr
        self._head = head
        self._noteHeads = []
        self._headData = {}
        self.locked = locked
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

    def addNoteHead(self, head, headData = None):
        self._noteHeads.append(head)
        if headData is None:
            self._headData[head] = copy.deepcopy(self._headData[self.head])
            self._guessEffect(head)
        else:
            self._headData[head] = headData

    def _guessEffect(self, head):
        assert(head in self._headData)
        self._headData[head].effect = _DEFAULTEFFECT.get(head, "normal")

    def guessHeadData(self):
        self._noteHeads = [self._head]
        midiNote = _guessMidiNote(self.abbr)
        headData = HeadData(midiNote)
        self._headData = {self._head: headData}
        self._guessEffect(self._head)
        for extraHead, newMidi, newMidiVolume, newEffect in DEFAULT_EXTRA_HEADS.get(self.abbr, []):
            if newMidi is None:
                newMidi = midiNote
            if newMidiVolume is None:
                newMidiVolume = headData.midiVolume
            newData = HeadData(newMidi, newMidiVolume, newEffect)
            self.addNoteHead(extraHead, newData)

    def readHeadData(self, dataString):
        head, data = HeadData.read(dataString)
        self._noteHeads.append(head)
        self._headData[head] = data

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

    def write(self, handle, indenter):
        print >> handle, indenter("DRUM %s,%s,%s,%s" % (self.name,
                                                        self.abbr,
                                                        self.head,
                                                        str(self.locked)))
        for head in self:
            headData = self.headData(head)
            indenter.increase()
            headData.write(head, handle, indenter)
            indenter.decrease()



def _guessMidiNote(abbr):
    for drumData, midiNote in DEFAULT_KIT:
        if abbr == drumData[1]:
            return midiNote
    return _DEFAULTNOTE
