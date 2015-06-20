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

from Data.Drum import Drum, HeadData
from Data.DefaultKits import STEM_DOWN, STEM_UP, NAMED_DEFAULTS
from Data.DBErrors import DuplicateDrumError, NoSuchDrumError

class DrumKit(object):
    UP = STEM_UP  # IGNORE:invalid-name
    DOWN = STEM_DOWN

    def __init__(self):
        self._drums = []
        self._lily = {}

    def __len__(self):
        return len(self._drums)

    def __getitem__(self, index):
        return self._drums[index]

    def __iter__(self):
        return iter(self._drums)

    def addDrum(self, drum):
        if drum in self._drums:
            raise DuplicateDrumError(drum.name, drum.abbr)
        self._drums.append(drum)

    def deleteDrum(self, name = None, index = None):
        assert not(index is None and name is None)
        assert not(index is not None and name is not None)
        if name is not None:
            index = [i for i, dr in enumerate(self._drums)
                     if dr.name == name]
            if len(index) != 1:
                raise NoSuchDrumError(name)
            index = index[0]
        if not (0 <= index < len(self)):
            raise NoSuchDrumError(index)
        self._drums.pop(index)

    def allowedNoteHeads(self, drumIndex):
        return list(self._drums[drumIndex])

    def shortcutsAndNoteHeads(self, drumIndex):
        drum = self._drums[drumIndex]
        return drum.shortcutsAndNoteHeads()

    def getDefaultHead(self, index):
        return self[index].head

def _loadDefaultKit(kit, kitInfo = None):
    for (drumData, midiNote, notationHead,
         notationLine, stemDirection) in kitInfo["drums"]:
        drum = Drum(*drumData)
        headData = HeadData(midiNote = midiNote,
                            notationHead = notationHead,
                            notationLine = notationLine,
                            stemDirection = stemDirection)
        drum.addNoteHead(drum.head, headData)
        for (extraHead,
             newMidi,
             newMidiVolume,
             newEffect,
             newNotationHead,
             newNotationEffect,
             shortcut) in kitInfo["heads"].get(drum.abbr, []):
            if newMidi is None:
                newMidi = midiNote
            if newMidiVolume is None:
                newMidiVolume = headData.midiVolume
            newData = HeadData(newMidi, newMidiVolume, newEffect,
                               notationLine = notationLine,
                               notationHead = newNotationHead,
                               notationEffect = newNotationEffect,
                               stemDirection = stemDirection,
                               shortcut = shortcut)
            drum.addNoteHead(extraHead, newData)
        drum.checkShortcuts()
        kit.addDrum(drum)

def getNamedDefaultKit(defaultName = None):
    if defaultName is None:
        defaultName = "Default"
    kitInfo = NAMED_DEFAULTS[defaultName]
    kit = DrumKit()
    _loadDefaultKit(kit, kitInfo)
    return kit

