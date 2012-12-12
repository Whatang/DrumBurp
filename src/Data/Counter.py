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


from DBConstants import BEAT_COUNT
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
        '''
        Constructor
        '''
        if not counts.startswith(BEAT_COUNT):
            raise ValueError("A Counter must begin with a BEAT_COUNT.")
        for count in alternatives:
            if not count.startswith(BEAT_COUNT):
                raise ValueError("A Counter must begin with a BEAT_COUNT.")
            if len(count) != len(counts):
                raise ValueError("All counts for a Counter must be of the "
                                 "same length.")
        self._counts = counts
        self._alternatives = alternatives

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

    def write(self, handle, indenter):
        print >> handle, indenter("COUNT", "|" + self._counts + "|")

_COUNTER_BEAT = Counter(BEAT_COUNT)
_EIGHTH_COUNT = Counter(BEAT_COUNT + "+", BEAT_COUNT + "&")
_TRIPLET_COUNT = Counter(BEAT_COUNT + "+a", BEAT_COUNT + "ea")
_OLD_TRIPLET_COUNT = Counter(BEAT_COUNT + "ea")
_SIXTEENTH_COUNT = Counter(BEAT_COUNT + "e+a")
_SIXTEENTH_COUNT_SPARSE = Counter(BEAT_COUNT + ' + ')
_SIXTEENTH_TRIPLETS = Counter(BEAT_COUNT + 'ea+ea')
_SIXTEENTH_TRIPLETS_SPARSE = Counter(BEAT_COUNT + '  +  ')
_THIRTY_SECONDS_COUNT = Counter(BEAT_COUNT + '.e.+.a.')
_THIRTY_SECONDS_COUNT_SPARSE = Counter(BEAT_COUNT + ' e + a ')
_THIRTY_SECONDS_TRIPLET_COUNT = Counter(BEAT_COUNT + '.e.a.+.e.a.')
_THIRTY_SECONDS_TRIPLET_COUNT_SPARSE = Counter(BEAT_COUNT + ' e a + e a ')

class CounterRegistry(object):
    def __init__(self, defaults = True):
        self._names = []
        self._counts = {}
        if defaults:
            self.restoreDefaults()

    def clear(self):
        self._names = []
        self._counts = {}

    def restoreDefaults(self):
        self.register('Quarter Notes', _COUNTER_BEAT)
        self.register('8ths', _EIGHTH_COUNT)
        self.register('Triplets', _TRIPLET_COUNT)
        self.register('16ths', _SIXTEENTH_COUNT)
        self.register('Sparse 16ths', _SIXTEENTH_COUNT_SPARSE)
        self.register('16th Triplets', _SIXTEENTH_TRIPLETS)
        self.register('Sparse 16th Triplets', _SIXTEENTH_TRIPLETS_SPARSE)
        self.register('32nds', _THIRTY_SECONDS_COUNT)
        self.register('Sparse 32nds', _THIRTY_SECONDS_COUNT_SPARSE)
        self.register('32nd Triplets', _THIRTY_SECONDS_TRIPLET_COUNT)
        self.register('Sparse 32nd Triplets',
                      _THIRTY_SECONDS_TRIPLET_COUNT_SPARSE)

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
        return(-1)

    def findMaster(self, countString):
        index = self.lookupIndex(countString)
        if index == -1:
            raise KeyError("Unrecognised beat!")
        return self._counts[self._names[index]]

    def __getitem__(self, index):
        return self._counts[self._names[index]]




