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
class dbFileIterator(object):
    class _Section(object):
        def __init__(self, iterator, startLine, endLine, convertNone = None):
            self._iterator = iterator
            self._startLine = startLine
            self._endLine = endLine
            self._convertNone = convertNone
            self._lines = {}

        def __enter__(self):
            return self

        def process(self):
            for lineType, lineData in self._iterator:
                if lineData == None:
                    lineData = self._convertNone
                if lineType == self._startLine:
                    continue
                elif lineType == self._endLine:
                    break
                elif lineType in self._lines:
                    self._lines[lineType](lineData)
                else:
                    raise IOError("Unrecognised line type: " + lineType)

        @staticmethod
        def _parseInteger(data):
            try:
                data = int(data)
            except (TypeError, ValueError):
                raise IOError("Bad integer value %s" % str(data))
            return data

        @classmethod
        def _parsePositiveInteger(cls, data):
            data = cls._parsePositiveInteger(data)
            if data <= 0:
                raise IOError("Integer value must be positive: %d" % data)
            return data

        def registerInteger(self, lineType, target, attrName):
            self._lines[lineType] = lambda data: setattr(target, attrName,
                                                         self._parseInteger(data))

        def registerPositiveInteger(self, lineType, target, attrName):
            self._lines[lineType] = lambda data: setattr(target, attrName,
                                                         self._parsePositiveInteger(data))

        def registerString(self, lineType, target, attrName):
            self._lines[lineType] = lambda data: setattr(target, attrName, data)

        def registerCallback(self, lineType, callback):
            self._lines[lineType] = callback

        def __exit__(self, excType, excValue, excTraceback):
            return False

    def __init__(self, handle):
        self._handle = handle

    def __iter__(self):
        for line in self._handle:
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

    def section(self, startLine, endLine, convertNone = None):
        return self._Section(self, startLine, endLine, convertNone)


class Indenter(object):
    class Section(object):
        def __init__(self, indenter, sectionStart, sectionEnd):
            self.indenter = indenter
            self.start = sectionStart
            self.end = sectionEnd

        def __enter__(self):
            self.indenter(self.start)
            self.indenter.increase()
            return self

        def __exit__(self, excType, excValue, excTraceback):
            self.indenter.decrease()
            self.indenter(self.end)
            return False

    def __init__(self, handle, indent = "  "):
        self._indent = indent
        self._handle = handle
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
        print >> self._handle, argString

    def __enter__(self):
        self.increase()
        return self

    def __exit__(self, excType, excValue, excTraceback):
        self.decrease()
        return False

    def section(self, sectionStart, sectionEnd):
        return self.Section(self, sectionStart, sectionEnd)
