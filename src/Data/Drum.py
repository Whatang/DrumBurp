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

from Data.DBConstants import DRUM_ABBR_WIDTH
import Data.DefaultKits as DefaultKits

class HeadData(object):
    def __init__(self, midiNote = DefaultKits.DEFAULT_NOTE,
                 midiVolume = DefaultKits.DEFAULT_VOLUME,
                 effect = "normal",
                 notationHead = "default",
                 notationLine = 0,
                 notationEffect = "none",
                 stemDirection = DefaultKits.STEM_UP,
                 shortcut = ""):
        self.midiNote = midiNote
        self.midiVolume = midiVolume
        self.effect = effect
        self.notationHead = notationHead
        self.notationLine = notationLine
        self.notationEffect = notationEffect
        self.stemDirection = stemDirection
        self.shortcut = shortcut

    def write(self, noteHead, indenter):
        dataString = "%s %d,%d,%s,%s,%d,%s,%d,%s" % (noteHead, self.midiNote,
                                                  self.midiVolume,
                                                  self.effect,
                                                  self.notationHead,
                                                  self.notationLine,
                                                  self.notationEffect,
                                                  self.stemDirection,
                                                  self.shortcut)
        indenter("NOTEHEAD", dataString)

    @classmethod
    def read(cls, abbr, dataString):
        head, data = dataString.split(None, 1)
        fields = data.split(",")
        note, volume, effect = fields[:3]
        note = int(note)
        volume = int(volume)
        shortcut = ""
        if len(fields) > 3:
            nHead, nLine, nEffect, sDir = fields[3:7]
            nLine = int(nLine)
            sDir = int(sDir)
            if len(fields) > 7:
                shortcut = fields[7]
        else:
            nHead, nLine, nEffect, sDir = cls._guessNotation(abbr, head)
        return head, cls(note, volume, effect, nHead,
                         nLine, nEffect, sDir, shortcut)

    @staticmethod
    def _guessNotation(abbr, head):
        for drumInfo in DefaultKits.DEFAULT_KIT:
            if drumInfo[0][1] == abbr:
                nHead, nLine, sDir = drumInfo[-3:]
                nEffect = "none"
                break
        else:
            return ["default", 0, "none", DefaultKits.STEM_UP]
        for headInfo in DefaultKits.DEFAULT_EXTRA_HEADS[abbr]:
            if headInfo[0] == head:
                nHead, nEffect = headInfo[4:6]
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
        assert len(name) > 0
        assert 1 <= len(abbr) <= DRUM_ABBR_WIDTH
        assert len(head) == 1

    @property
    def head(self):
        return self._head

    def setDefaultHead(self, head):
        if head not in self._headData:
            return
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
        if not isinstance(other, Drum):
            return False
        return self.name == other.name or self.abbr == other.abbr

    def headData(self, head):
        if head is None:
            head = self.head
        return self._headData[head]

    def isAllowedHead(self, head):
        return head in self._headData

    def renameHead(self, oldHead, head):
        try:
            index = self._noteHeads.index(oldHead)
        except ValueError:
            return
        self._noteHeads[index] = head
        self._headData[head] = self._headData.pop(oldHead)
        if self._head == oldHead:
            self._head = head

    def addNoteHead(self, head, headData = None):
        self._noteHeads.append(head)
        if headData is None:
            newHead = copy.deepcopy(self._headData[self.head])
            newHead.shortcut = None
            self._headData[head] = newHead
            self._guessEffect(head)
            self.checkShortcuts()
        else:
            assert isinstance(headData, HeadData)
            self._headData[head] = headData

    def _guessEffect(self, head):
        assert head in self._headData
        self._headData[head].effect = _DEFAULTEFFECT.get(head, "normal")

    def guessHeadData(self):
        self._noteHeads = [self._head]
        midiNote = _guessMidiNote(self.abbr)
        for drumInfo in DefaultKits.DEFAULT_KIT:
            if drumInfo[0][1] == self.abbr:
                notationHead, notationLine, stemDir = drumInfo[-3:]
                break
        else:
            notationHead = "default"
            notationLine = 0
            stemDir = DefaultKits.STEM_UP
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
             newNotationEffect,
             shortcut) in DefaultKits.DEFAULT_EXTRA_HEADS.get(self.abbr, []):
            if newMidi is None:
                newMidi = midiNote
            if newMidiVolume is None:
                newMidiVolume = headData.midiVolume
            newData = HeadData(newMidi, newMidiVolume, newEffect,
                               notationHead = newNotationHead,
                               notationLine = notationLine,
                               notationEffect = newNotationEffect,
                               stemDirection = stemDir,
                               shortcut = shortcut)
            self.addNoteHead(extraHead, newData)
        self.checkShortcuts()

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
        except ValueError:
            return
        if idx < 2:
            return
        self._noteHeads[idx - 1:idx + 1] = self._noteHeads[idx:idx - 2:-1]

    def moveHeadDown(self, head):
        try:
            idx = self._noteHeads.index(head)
        except ValueError:
            return
        if idx >= len(self) - 1 or idx == 0:
            return
        self._noteHeads[idx:idx + 2] = self._noteHeads[idx + 1:idx - 1:-1]

    def checkShortcuts(self):
        availableShortcuts = set('abcdefghijklmnopqrstuvwxyz')
        for head, data in self._headData.iteritems():
            if data.shortcut:
                availableShortcuts.remove(data.shortcut)
        for head, data in self._headData.iteritems():
            if not data.shortcut:
                if head in availableShortcuts:
                    data.shortcut = head
                    availableShortcuts.remove(head)
                else:
                    data.shortcut = availableShortcuts.pop()

    def shortcutsAndNoteHeads(self):
        shortcuts = []
        for head in self:
            shortcut = self._headData[head].shortcut
            shortcuts.append((unicode(shortcut), head))
        return shortcuts


    def write(self, indenter):
        indenter("DRUM %s,%s,%s,%s" % (self.name, self.abbr, self.head,
                                       str(self.locked)))
        with indenter:
            for head in self:
                headData = self.headData(head)
                headData.write(head, indenter)



def _guessMidiNote(abbr):
    for drumData, midiNote, x_, y_, z_ in DefaultKits.DEFAULT_KIT:
        if abbr == drumData[1]:
            return midiNote
    return DefaultKits.DEFAULT_NOTE
