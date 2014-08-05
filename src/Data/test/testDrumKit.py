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
Created on 12 Dec 2010

@author: Mike Thomas
'''
import unittest
from Data.DrumKit import DrumKit
from Data.DBErrors import DuplicateDrumError, NoSuchDrumError
from Data.Drum import Drum
#pylint: disable-msg=R0904

class TestDrumKit(unittest.TestCase):
    def setUp(self):
        self.kit = DrumKit()

    def testEmptyDrumKit(self):
        self.assertEqual(len(self.kit), 0)

    def testLoadDefault(self):
        self.kit.loadDefaultKit()
        self.assert_(len(self.kit) > 0)
        for drumData, drum in zip(DrumKit.DEFAULT_KIT, self.kit):
            defDrum = Drum(*drumData)
            self.assertEqual(defDrum, drum)

    def testAddDrum(self):
        self.kit.loadDefaultKit()
        numDrums = len(self.kit)
        drum = Drum("test drum", "td", "x")
        self.kit.addDrum(drum)
        self.assertEqual(len(self.kit), numDrums + 1)

    def testAddDuplicate(self):
        self.kit.loadDefaultKit()
        self.assertRaises(DuplicateDrumError,
                          self.kit.addDrum, self.kit[0])

    def testDeleteDrum_NoDrumGiven(self):
        self.assertRaises(AssertionError, self.kit.deleteDrum)

    def testDeleteDrum_OverSpecified(self):
        self.assertRaises(AssertionError, self.kit.deleteDrum)

    def testDeleteDrumByName(self):
        self.kit.loadDefaultKit()
        numDrums = len(self.kit)
        self.assert_(numDrums > 0)
        drum = self.kit[0]
        self.kit.deleteDrum(name = drum.name)
        self.assertEqual(len(self.kit), numDrums - 1)
        for remainingDrum in self.kit:
            self.assertNotEqual(drum, remainingDrum)

    def testDeleteDrumByName_DrumNotFound(self):
        self.kit.loadDefaultKit()
        self.assertRaises(NoSuchDrumError,
                          self.kit.deleteDrum, name = "no such drum")

    def testDeleteDrumByIndex(self):
        self.kit.loadDefaultKit()
        numDrums = len(self.kit)
        self.assert_(numDrums > 0)
        drum = self.kit[0]
        self.kit.deleteDrum(index = 0)
        self.assertEqual(len(self.kit), numDrums - 1)
        for remainingDrum in self.kit:
            self.assertNotEqual(drum, remainingDrum)

    def testDeleteDrumByIndex_BadIndex(self):
        self.kit.loadDefaultKit()
        self.assertRaises(NoSuchDrumError,
                          self.kit.deleteDrum, index = -1)
        self.assertRaises(NoSuchDrumError,
                          self.kit.deleteDrum, index = len(self.kit))



if __name__ == "__main__":
    unittest.main()
