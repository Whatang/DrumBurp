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

import itertools
from Data import DBConstants


class Beat(object):
    '''A Beat is a measured instance of a Counter.

    A Beat may be less than the full length of the corresponding Counter to
    reflect partial beats at the end of a Measure. A sequence of Beats makes
    up a MeasureCount.
    '''

    def __init__(self, counter, numTicks=None):
        self.counter = counter
        if numTicks is None:
            numTicks = self.ticksPerBeat
        self._numTicks = numTicks
        self._beatLength = float(self.numTicks) / self.ticksPerBeat

    def __iter__(self):
        for unusedTickNum, count in zip(self.iterTicks(),
                                                   self.counter):
            yield count

    def count(self, beatNum):
        for count in self:
            if count == DBConstants.BEAT_COUNT:
                yield str(beatNum)
            else:
                yield count

    def __str__(self):
        return str(self.counter)

    def iterTicks(self):
        return range(self.numTicks)

    def numBeats(self):
        return self._beatLength

    @property
    def ticksPerBeat(self):
        return len(self.counter)

    @property
    def numTicks(self):
        return self._numTicks

    def isPartial(self):
        return self._numTicks < len(self.counter)
