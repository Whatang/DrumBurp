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
import unittest

#pylint: disable-msg=R0904
from Data.Drum import Drum
class TestDrum(unittest.TestCase):


    def testDrum(self):
        drum = Drum("test drum", "td", "x")
        self.assertEqual(drum.name, "test drum")
        self.assertEqual(drum.abbr, "td")
        self.assertEqual(drum.head, "x")

    def testEquality(self):
        drum1 = Drum("test drum", "td", "x")
        drum2 = Drum("test drum", "td", "x")
        drum3 = Drum("test drum", "d2", "x")
        drum4 = Drum("test drum2", "td", "x")
        drum5 = Drum("test drum2", "d2", "x")
        self.assertEqual(drum1, drum2)
        self.assertEqual(drum1, drum3)
        self.assertEqual(drum1, drum4)
        self.assertNotEqual(drum1, drum5)



if __name__ == "__main__":
    unittest.main()
