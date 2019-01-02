# Copyright 2015 Michael Thomas
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
Created on Jun 20, 2015

@author: Mike Thomas
'''
from Data.Drum import Drum, HeadData, Drum
from Data.DefaultKits import NAMED_DEFAULTS
from Data import DrumKit


def _loadDefaultKit(kit, kitInfo=None):
    for (drumData, midiNote, notationHead,
         notationLine, stemDirection) in kitInfo["drums"]:
        drum = Drum(*drumData)
        headData = HeadData(midiNote=midiNote,
                            notationHead=notationHead,
                            notationLine=notationLine,
                            stemDirection=stemDirection)
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
                               notationLine=notationLine,
                               notationHead=newNotationHead,
                               notationEffect=newNotationEffect,
                               stemDirection=stemDirection,
                               shortcut=shortcut)
            drum.addNoteHead(extraHead, newData)
        drum.checkShortcuts()
        kit.addDrum(drum)


class DrumKitFactory(object):
    @staticmethod
    def emptyKit():
        return DrumKit.DrumKit()

    @staticmethod
    def getNamedDefaultKit(defaultName=None):
        if defaultName is None:
            defaultName = "Default"
        kitInfo = NAMED_DEFAULTS[defaultName]
        kit = DrumKitFactory.emptyKit()
        _loadDefaultKit(kit, kitInfo)
        return kit
