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

from Drum import Drum
from DefaultKits import DEFAULT_KIT
from DBErrors import DuplicateDrumError, NoSuchDrumError

class DrumKit(object):
    '''
    classdocs
    '''

    def __init__(self):
        self._drums = []

    def __len__(self):
        return len(self._drums)

    def __getitem__(self, index):
        return self._drums[index]

    def __iter__(self):
        return iter(self._drums)

    def loadDefaultKit(self):
        for drumData in DEFAULT_KIT:
            self.addDrum(Drum(*drumData))

    def addDrum(self, drum):
        if drum in self._drums:
            raise DuplicateDrumError(drum.name, drum.abbr)
        self._drums.append(drum)

    def deleteDrum(self, name = None, index = None):
        assert(not(index is None and name is None))
        assert(not(index is not None and name is not None))
        if name is not None:
            index = [i for i, dr in enumerate(self._drums)
                     if dr.name == name]
            if len(index) != 1:
                raise NoSuchDrumError(name)
            index = index[0]
        if not (0 <= index < len(self)):
            raise NoSuchDrumError(index)
        self._drums.pop(index)

    def write(self, handle, indenter):
        print >> handle, indenter("KIT_START")
        indenter.increase()
        for drum in self:
            print >> handle, indenter("DRUM %s,%s,%s,%s,%s" % (drum.name,
                                                   drum.abbr,
                                                   drum.head,
                                                   str(drum.locked),
                                                   str(drum.midiNote)))
        indenter.decrease()
        print >> handle, indenter("KIT_END")

    def read(self, scoreIterator):
        for lineType, lineData in scoreIterator:
            if  lineType == "KIT_END":
                break
            elif lineType == "DRUM":
                fields = lineData.split(",")
                if len(fields) > 3:
                    fields[3] = (fields[3] == "True")
                if len(fields) > 4:
                    if fields[4] == "None":
                        fields[4] = None
                    else:
                        fields[4] = int(fields[4])
                drum = Drum(*fields)
                self.addDrum(drum)
            else:
                raise IOError("Unrecognised line type.")
