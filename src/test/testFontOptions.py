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
Created on 12 Dec 2012

@author: Mike Thomas
'''
import unittest
from cStringIO import StringIO
# pylint: disable-msg=R0904

from Data import FontOptions, fileUtils

class TestFontOptions(unittest.TestCase):
    def testWrite(self):
        options = FontOptions.FontOptions()
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        options.write(indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["FONT_OPTIONS_START",
                          "  NOTEFONT MS Shell Dlg 2",
                          "  NOTEFONTSIZE 10",
                          "  SECTIONFONT MS Shell Dlg 2",
                          "  SECTIONFONTSIZE 14",
                          "  METADATAFONT MS Shell Dlg 2",
                          "  METADATAFONTSIZE 16",
                          "FONT_OPTIONS_END"])

    def testRead(self):
        data = """FONT_OPTIONS_START
                  NOTEFONT mynotefont
                  NOTEFONTSIZE 8
                  SECTIONFONT sectionfont
                  SECTIONFONTSIZE 12
                  METADATAFONT metafont
                  METADATAFONTSIZE 14
                FONT_OPTIONS_END"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        options = fileUtils.FontOptionsStructureV0().read(iterator)
        self.assertEqual(options.noteFont, "mynotefont")
        self.assertEqual(options.noteFontSize, 8)
        self.assertEqual(options.sectionFont, "sectionfont")
        self.assertEqual(options.sectionFontSize, 12)
        self.assertEqual(options.metadataFont, "metafont")
        self.assertEqual(options.metadataFontSize, 14)




if __name__ == "__main__":
    unittest.main()
