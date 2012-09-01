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
Created on 12 Dec 2010

@author: Mike Thomas

'''
import copy

from DBConstants import DRUM_ABBR_WIDTH
from DefaultKits import DEFAULT_KIT, DEFAULT_EXTRA_HEADS, STEM_UP

_DEFAULTNOTE = 71
_DEFAULTVOLUME = 96

class HeadData(object):
    def __init__(self, midiNote = _DEFAULTNOTE,
                 midiVolume = _DEFAULTVOLUME,
                 effect = "normal",
                 notationHead = "default",
                 notationLine = 0,
                 notationEffect = "none",
                 stemDirection = STEM_UP):
        self.midiNote = midiNote
        self.midiVolume = midiVolume
        self.effect = effect
        self.notationHead = notationHead
        self.notationLine = notationLine
        self.notationEffect = notationEffect
        self.stemDirection = stemDirection

    def write(self, noteHead, handle, indenter):
        dataString = "%s %d,%d,%s,%s,%d,%s,%d" % (noteHead, self.midiNote,
                                                  self.midiVolume,
                                                  self.effect,
                                                  self.notationHead,
                                                  self.notationLine,
                                                  self.notationEffect,
                                                  self.stemDirection)
        print >> handle, indenter("NOTEHEAD", dataString)

    @staticmethod
    def read(abbr, dataString):
        head, data = dataString.split(None, 1)
        fields = data.split(",")
        note, volume, effect = fields[:3]
        note = int(note)
        volume = int(volume)
        if len(fields) > 3:
            nHead, nLine, nEffect, sDir = fields[3:]
            nLine = int(nLine)
            sDir = int(sDir)
        else:
            nHead, nLine, nEffect, sDir = _guessNotation(abbr, head)
        return head, HeadData(note, volume, effect, nHead, nLine, nEffect, sDir)

def _guessNotation(abbr, head):
    for drumInfo in DEFAULT_KIT:
        if drumInfo[0][1] == abbr:
            nHead, nLine, sDir = drumInfo[-3:]
            nEffect = "none"
            break
    else:
        return ["default", 0, "none", STEM_UP]
    for headInfo in DEFAULT_EXTRA_HEADS[abbr]:
        if headInfo[0] == head:
            nHead, nEffect = headInfo[-2:]
    return nHead, nLine, nEffect, sDir



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
        self._noteHeads = ([head] + self._noteHeads[:index]
                           + self._noteHeads[index + 1:])

    def __iter__(self):
        return iter(self._noteHeads)

    def __len__(self):
        return len(self._noteHeads)

    def __getitem__(self, index):
        return self._noteHeads[index]

    def __eq__(self, other):
        return self.name == other.name or self.abbr == other.abbr

    def headData(self, head):
        if head is None:
            head = self.head
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
        for drumInfo in DEFAULT_KIT:
            if drumInfo[0][1] == self.abbr:
                notationHead, notationLine, stemDir = drumInfo[-3:]
                break
        else:
            notationHead = "default"
            notationLine = 0
            stemDir = STEM_UP
        headData = HeadData(midiNote, notationHead = notationHead,
                            notationLine = notationLine,
                            stemDirection = stemDir)
        self._headData = {self._head: headData}
        self._guessEffect(self._head)
        for (extraHead,
             newMidi,
             newMidiVolume,
             newEffect,
             newNotationHead,
             newNotationEffect) in DEFAULT_EXTRA_HEADS.get(self.abbr, []):
            if newMidi is None:
                newMidi = midiNote
            if newMidiVolume is None:
                newMidiVolume = headData.midiVolume
            newData = HeadData(newMidi, newMidiVolume, newEffect,
                               notationHead = newNotationHead,
                               notationLine = notationLine,
                               notationEffect = newNotationEffect,
                               stemDirection = stemDir)
            self.addNoteHead(extraHead, newData)

    def readHeadData(self, dataString):
        head, data = HeadData.read(self.abbr, dataString)
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
            idx = self._noteHeads.index(head)
        except IndexError:
            return
        assert(idx > 1)
        self._noteHeads[idx - 1:idx + 1] = self._noteHeads[idx:idx - 2:-1]

    def moveHeadDown(self, head):
        try:
            idx = self._noteHeads.index(head)
        except IndexError:
            return
        assert(idx < len(self) - 1)
        self._noteHeads[idx:idx + 2] = self._noteHeads[idx + 1:idx - 1:-1]

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
    for drumData, midiNote, x_, y_, z_ in DEFAULT_KIT:
        if abbr == drumData[1]:
            return midiNote
    return _DEFAULTNOTE
