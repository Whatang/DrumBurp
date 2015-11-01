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

from Data import DBConstants
import Data.DefaultKits as DefaultKits

class HeadData(object):
    def __init__(self,  # IGNORE:too-many-arguments
                 midiNote = DefaultKits.DEFAULT_NOTE,
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

class Drum(object):
    def __init__(self, name, abbr, head, locked = False):
        self.name = name
        self.abbr = abbr
        self._head = head
        self._noteHeads = []
        self._headData = {}
        self.locked = locked
        assert len(name) > 0
        assert 1 <= len(abbr) <= DBConstants.DRUM_ABBR_WIDTH
        assert len(head) == 1

    @classmethod
    def makeSimple(cls, name, abbr, head):
        drum = cls(name, abbr, head)
        midiNote = DefaultKits.DEFAULT_NOTE
        notationHead = "default"
        notationLine = 0
        stemDir = DefaultKits.STEM_UP
        headData = HeadData(midiNote, notationHead = notationHead,
                            notationLine = notationLine,
                            stemDirection = stemDir)
        drum.addNoteHead(drum.head, headData)
        guessEffect(drum, drum.head)
        drum.checkShortcuts()
        return drum

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
        if head not in self._noteHeads:
            self._noteHeads.append(head)
        if head in self._headData:
            return
        if headData is None:
            headData = copy.deepcopy(self._headData[self.head])
            headData.shortcut = None
            self._headData[head] = headData
            guessEffect(self, head)
            self.checkShortcuts()
        else:
            assert isinstance(headData, HeadData)
            self._headData[head] = headData

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
def guessEffect(drum, head):
    assert drum.isAllowedHead(head)
    drum.headData(head).effect = _DEFAULTEFFECT.get(head, "normal")

