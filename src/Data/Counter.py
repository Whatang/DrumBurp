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
Created on 16 Apr 2011

@author: Mike Thomas

'''

from collections import OrderedDict
from Data import DBConstants

#thank some other thing I found online
#Author: A.Polino
def is_power2(num):
	return num != 0 and ((num & (num - 1)) == 0)

class Counter(object):
    '''A Counter represents a way of subdividing a single beat.

    A single beat can be counted in many different ways, e.g. as a single
    quarter note, as two 8th notes, as 4 16ths, etc. Counter objects represent
    these different ways to subdivide a beat.

    A Counter has a count string associated with it. This should begin with
    the DBComstants.BEAT_COUNT character. This character represents the count
    at the start of the beat. The following characters represent the count
    for the subdivisions of the beat.

    The alternatives list for a Counter is a list of alternative count strings
    that will also be recognised as matching this Counter. This is to facilitate
    backwards compatibility when the default count string for a Counter changes.
    '''

    def __init__(self, counts, *alternatives):
        if not counts.startswith(DBConstants.BEAT_COUNT):
            counts = DBConstants.BEAT_COUNT + counts
        self._counts = counts
        self._alternatives = [DBConstants.BEAT_COUNT + alt
                              if not alt.startswith(DBConstants.BEAT_COUNT)
                              else alt
                              for alt in alternatives]
        for count in self._alternatives:
            if len(count) != len(counts):
                raise ValueError("All counts for a Counter must be of the "
                                 "same length.")
        self.noteDirectory = {
            True: OrderedDict(),
            False: OrderedDict()
            }
        #add all regular notes
        i = 1
        while len(self._counts) % i == 0:
            self.noteDirectory[False][len(self._counts)/i] = i * 4
            i *= 2

        #If the counter isn't a power of two, it can contain compound notes
        self.supportsCompound = not (len(self._counts) <= 2 or is_power2(len(self._counts)))

        #If the beat is compound, add the compound notes (duh)
        if self.supportsCompound:
            j = 1
            noteType = self.noteDirectory[False].values()[-1] * 2
            while(j < len(self._counts)):
                self.noteDirectory[True][j] = noteType
                noteType /= 2
                j *= 2

    def __iter__(self):
        return iter(self._counts)

    def __len__(self):
        return len(self._counts)

    def __str__(self):
        return self._counts

    def matchesExact(self, beatStr):
        return beatStr == self._counts

    def matchesAlternative(self, beatStr):
        return any(beatStr == alt for alt in self._alternatives)

#1/4
_QUARTER_COUNT = Counter("")
#1/8
_EIGHTH_COUNT = Counter("+", "&")
_TRIPLET_COUNT = Counter("+a", "ea")
_QUINTUPLET_COUNT = Counter("eaea")
_SEPTUPLET_COUNT = Counter("e+ae+a")
#1/16
_SIXTEENTH_COUNT = Counter("e+a")
_SIXTEENTH_COUNT_SPARSE = Counter(" + ")
_SIXTEENTH_TRIPLETS_COUNT = Counter("ea+ea")
_SIXTEENTH_TRIPLETS_COUNT_SPARSE = Counter("  +  ")
_SIXTEENTH_QUINTUPLETS_COUNT = Counter("eaea+eaea")
_SIXTEENTH_SEPTUPLETS_COUNT = Counter("e+ae+a+e+ae+a")
#1/32
_THIRTY_SECONDS_COUNT = Counter(".e.+.a.")
_THIRTY_SECONDS_COUNT_SPARSE = Counter(" e + a ")
_THIRTY_SECONDS_TRIPLET_COUNT = Counter(".e.a.+.e.a.")
_THIRTY_SECONDS_TRIPLET_COUNT_SPARSE = Counter(" e a + e a ")
_THIRTY_SECONDS_QUINTUPLETS_COUNT = Counter(".e.a.e.a.+.e.a.e.a.")
_THIRTY_SECONDS_SEPTUPLETS_COUNT = Counter(".e.+.a.e.+.a.+.e.+.a.e.+.a.")
#1/64
_SIXTY_FOURTH_COUNT = Counter("'.'e'.'+'.'a'.'")
_SIXTY_FOURTH_COUNT_SPARSE = Counter("   e   +   a   ")
_SIXTY_FOURTH_TRIPLET_COUNT = Counter("'.'e'.'a'.'+'.'e'.'a'.'")
_SIXTY_FOURTH_TRIPLET_COUNT_SPARSE = Counter("   e   a   +   e   a   ")
_SIXTY_FOURTH_QUINTUPLETS_COUNT = Counter("'.'e'.'a'.'e'.'a'.'+'.'e'.'a'.'e'.'a'.'")
_SIXTY_FOURTH_SEPTUPLETS_COUNT = Counter("'.'e'.'+'.'a'.'e'.'+'.'a'.'+'.'e'.'+'.'a'.'e'.'+'.'a'.'")

class CounterRegistry(object):
    def __init__(self, defaults=True):
        self._names = []
        self._counts = {}
        if defaults:
            self.restoreDefaults()

    def clear(self):
        self._names = []
        self._counts = {}

    def restoreDefaults(self):
        #1/4
        self.register('Quarter Notes', _QUARTER_COUNT)
        #1/8
        self.register('8ths', _EIGHTH_COUNT)
        self.register('Triplets', _TRIPLET_COUNT)
        self.register('Quintuplets', _QUINTUPLET_COUNT)
        self.register('Septuplets', _SEPTUPLET_COUNT)
        #1/16
        self.register('16ths', _SIXTEENTH_COUNT)
        self.register('Sparse 16ths', _SIXTEENTH_COUNT_SPARSE)
        self.register('16th Triplets', _SIXTEENTH_TRIPLETS_COUNT)
        self.register('Sparse 16th Triplets', _SIXTEENTH_TRIPLETS_COUNT_SPARSE)
        self.register('16th Quintuplets', _SIXTEENTH_QUINTUPLETS_COUNT)
        self.register('16th Septuplets', _SIXTEENTH_SEPTUPLETS_COUNT)
        #1/32
        self.register('32nds', _THIRTY_SECONDS_COUNT)
        self.register('Sparse 32nds', _THIRTY_SECONDS_COUNT_SPARSE)
        self.register('32nd Triplets', _THIRTY_SECONDS_TRIPLET_COUNT)
        self.register('Sparse 32nd Triplets', _THIRTY_SECONDS_TRIPLET_COUNT_SPARSE)
        self.register('32nd Quintuplets', _THIRTY_SECONDS_QUINTUPLETS_COUNT)
        self.register('32nd Septuplets', _THIRTY_SECONDS_SEPTUPLETS_COUNT)
        #1/64
        self.register('64ths', _SIXTY_FOURTH_COUNT)
        self.register('Sparse 64ths', _SIXTY_FOURTH_COUNT_SPARSE)
        self.register('64th Triplets', _SIXTY_FOURTH_TRIPLET_COUNT)
        self.register('Sparse 64th Triplets', _SIXTY_FOURTH_TRIPLET_COUNT_SPARSE)
        self.register('64th Quintuplets', _SIXTY_FOURTH_QUINTUPLETS_COUNT)
        self.register('64th Septuplets', _SIXTY_FOURTH_SEPTUPLETS_COUNT)

    def register(self, name, count):
        if count in self._counts.values():
            raise ValueError("Count %s already exists" % count)
        elif name not in self._counts:
            self._names.append(name)
            self._counts[name] = count
        else:
            raise KeyError('%s already exists' % name)

    def __iter__(self):
        for name in self._names:
            yield (name, self._counts[name])

    def countsByTicks(self, countLength):
        for name, count in self:
            if len(count) == countLength:
                yield name, count

    def getCounterByName(self, name):
        return self._counts[name]

    def getCounterByIndex(self, index):
        return self._counts[self._names[index]]

    def lookupIndex(self, beat):
        beatStr = str(beat)
        for index, (unusedName, count) in enumerate(self):
            if count.matchesExact(beatStr):
                return index
        for index, (unusedName, count) in enumerate(self):
            if count.matchesAlternative(beatStr):
                return index
        return -1

    def findMaster(self, countString):
        index = self.lookupIndex(countString)
        if index == -1:
            raise KeyError("Unrecognised beat!")
        return self._counts[self._names[index]]

    def __getitem__(self, index):
        return self._counts[self._names[index]]


DEFAULT_REGISTRY = CounterRegistry()
