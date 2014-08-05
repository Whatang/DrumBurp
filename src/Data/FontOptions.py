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
Created on 5 Sep 2011

@author: Mike Thomas

'''

class FontOptions(object):

    def __init__(self):
        self.noteFontSize = 10
        self.noteFont = "MS Shell Dlg 2"
        self.sectionFontSize = 14
        self.sectionFont = "MS Shell Dlg 2"
        self.metadataFontSize = 16
        self.metadataFont = "MS Shell Dlg 2"

    def write(self, handle, indenter):
        print >> handle, indenter("FONT_OPTIONS_START")
        indenter.increase()
        print >> handle, indenter("NOTEFONT", self.noteFont)
        print >> handle, indenter("NOTEFONTSIZE %d"
                                  % self.noteFontSize)
        print >> handle, indenter("SECTIONFONT", self.sectionFont)
        print >> handle, indenter("SECTIONFONTSIZE %d"
                                  % self.sectionFontSize)
        print >> handle, indenter("METADATAFONT", self.metadataFont)
        print >> handle, indenter("METADATAFONTSIZE %d"
                                  % self.metadataFontSize)
        indenter.decrease()
        print >> handle, indenter("FONT_OPTIONS_END")

    def read(self, scoreIterator):
        for lineType, lineData in scoreIterator:
            if lineType == "FONT_OPTIONS_END":
                break
            elif lineType == "NOTEFONT":
                self.noteFont = lineData
            elif lineType == "NOTEFONTSIZE":
                self.noteFontSize = int(lineData)
            elif lineType == "SECTIONFONT":
                self.sectionFont = lineData
            elif lineType == "SECTIONFONTSIZE":
                self.sectionFontSize = int(lineData)
            elif lineType == "METADATAFONT":
                self.metadataFont = lineData
            elif lineType == "METADATAFONTSIZE":
                self.metadataFontSize = int(lineData)
            else:
                raise IOError("Font information not recognised.")
