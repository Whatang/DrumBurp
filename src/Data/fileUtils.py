# Copyright 2012 Michael Thomas
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
Created on 7 Oct 2012

@author: Mike Thomas
'''
def dbFileIterator(handle):
    for line in handle:
        line = line.strip()
        fields = line.split(None, 1)
        if len(fields) == 1:
            fields.append(None)
        elif len(fields) == 0:
            # Blank line
            continue
        lineType, lineData = fields
        lineType = lineType.upper()
        yield lineType, lineData


class Indenter(object):
    def __init__(self, indent = "  "):
        self._indent = indent
        self._level = 0
    def increase(self):
        self._level += 1
    def decrease(self):
        self._level -= 1
        self._level = max(0, self._level)
    def __call__(self, *args):
        argString = " ".join(str(ar) for ar in args)
        if self._level != 0:
            argString = (self._indent * self._level) + argString
        return argString
