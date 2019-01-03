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
import Data.ASCIISettings as ASCIISettings
# pylint: disable-msg=R0904


class TestAsciiSettings(unittest.TestCase):
    def testNames(self):
        settings = ASCIISettings.ASCIISettings()
        names = settings.checkNames()
        self.assertEqual(names,
                         ['metadata', 'kitKey', 'omitEmpty',
                          'sectionBrackets', 'underline',
                          'printCounts', 'emptyLineBeforeSection',
                          'emptyLineAfterSection'])
        false_settings = set(['sectionBrackets'])
        for name in names:
            self.assertEqual(getattr(settings, name), name not in false_settings,
                             "Default value for AsciiSettings.'%s' is wrong"
                             % name)


if __name__ == "__main__":
    unittest.main()
