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
from cStringIO import StringIO
from Data import DrumKit
from Data.DBErrors import DuplicateDrumError, NoSuchDrumError
from Data.Drum import Drum, HeadData
from Data.fileUtils import dbFileIterator, Indenter
# pylint: disable-msg=R0904

class TestDrumKit(unittest.TestCase):
    def setUp(self):
        self.kit = DrumKit.DrumKit()

    def testEmptyDrumKit(self):
        self.assertEqual(len(self.kit), 0)

    def testLoadDefault(self):
        self.kit = DrumKit.getNamedDefaultKit()
        self.assert_(len(self.kit) > 0)

    def testAddDrum(self):
        self.kit = DrumKit.getNamedDefaultKit()
        numDrums = len(self.kit)
        drum = Drum("test drum", "td", "x")
        self.kit.addDrum(drum)
        self.assertEqual(len(self.kit), numDrums + 1)

    def testAddDuplicate(self):
        self.kit = DrumKit.getNamedDefaultKit()
        self.assertRaises(DuplicateDrumError,
                          self.kit.addDrum, self.kit[0])

    def testDeleteDrum_NoDrumGiven(self):
        self.assertRaises(AssertionError, self.kit.deleteDrum)

    def testDeleteDrum_OverSpecified(self):
        self.assertRaises(AssertionError, self.kit.deleteDrum)

    def testDeleteDrumByName(self):
        self.kit = DrumKit.getNamedDefaultKit()
        numDrums = len(self.kit)
        self.assert_(numDrums > 0)
        drum = self.kit[0]
        self.kit.deleteDrum(name = drum.name)
        self.assertEqual(len(self.kit), numDrums - 1)
        for remainingDrum in self.kit:
            self.assertNotEqual(drum, remainingDrum)

    def testDeleteDrumByName_DrumNotFound(self):
        self.kit = DrumKit.getNamedDefaultKit()
        self.assertRaises(NoSuchDrumError,
                          self.kit.deleteDrum, name = "no such drum")

    def testDeleteDrumByIndex(self):
        self.kit = DrumKit.getNamedDefaultKit()
        numDrums = len(self.kit)
        self.assert_(numDrums > 0)
        drum = self.kit[0]
        self.kit.deleteDrum(index = 0)
        self.assertEqual(len(self.kit), numDrums - 1)
        for remainingDrum in self.kit:
            self.assertNotEqual(drum, remainingDrum)

    def testDeleteDrumByIndex_BadIndex(self):
        self.kit = DrumKit.getNamedDefaultKit()
        self.assertRaises(NoSuchDrumError,
                          self.kit.deleteDrum, index = -1)
        self.assertRaises(NoSuchDrumError,
                          self.kit.deleteDrum, index = len(self.kit))

    def testRead_NoNoteHeads(self):
        kitData = """KIT_START
        DRUM Snare,Sn,x,True
        DRUM Kick,Bd,o,True
        KIT_END
        """
        handle = StringIO(kitData)
        iterator = dbFileIterator(handle)
        kit = DrumKit.DrumKit()
        kit.read(iterator)
        self.assertEqual(len(kit), 2)
        self.assertEqual(kit[0].name, "Snare")
        self.assertEqual(len(kit[0]), 6)
        self.assertEqual(kit[1].name, "Kick")
        self.assertEqual(len(kit[1]), 4)

    def testRead_BadLine(self):
        kitData = """KIT_START
        DRUM Snare,Sn,x,True
        NOTEHEAD x 1,100,default
        NOTEHEAD g 1,50,ghost
        DRUM Kick,Bd,o,True
        NOTEHEAD o 2,100,default
        NOTEHEAD O 2,127,accent
        BAD_LINE
        KIT_END
        """
        handle = StringIO(kitData)
        iterator = dbFileIterator(handle)
        kit = DrumKit.DrumKit()
        self.assertRaises(IOError, kit.read, iterator)

    def testRead_OldNoteHeads(self):
        kitData = """KIT_START
        DRUM Snare,Sn,x,True
        NOTEHEAD x 1,100,default
        NOTEHEAD g 1,50,ghost
        DRUM Kick,Bd,o,True
        NOTEHEAD o 2,100,default
        NOTEHEAD O 2,127,accent
        KIT_END
        """
        handle = StringIO(kitData)
        iterator = dbFileIterator(handle)
        kit = DrumKit.DrumKit()
        kit.read(iterator)
        self.assertEqual(len(kit), 2)
        self.assertEqual(len(kit), 2)
        self.assertEqual(kit[0].name, "Snare")
        self.assertEqual(len(kit[0]), 2)
        self.assertEqual(kit[1].name, "Kick")
        self.assertEqual(len(kit[1]), 2)

    def testRead_NewNoteHeads(self):
        kitData = """KIT_START
        DRUM Snare,Sn,x,True
        NOTEHEAD x 1,100,normal,default,0,none,0,x
        NOTEHEAD g 1,50,ghost,default,0,ghost,0,g
        DRUM Kick,Bd,o,True
        NOTEHEAD o 2,100,normal,default,-5,none,1,o
        NOTEHEAD O 2,127,accent,default,-5,accent,1,a
        KIT_END
        """
        handle = StringIO(kitData)
        iterator = dbFileIterator(handle)
        kit = DrumKit.DrumKit()
        kit.read(iterator)
        self.assertEqual(len(kit), 2)
        self.assertEqual(len(kit), 2)
        self.assertEqual(kit[0].name, "Snare")
        self.assertEqual(len(kit[0]), 2)
        self.assertEqual(kit[1].name, "Kick")
        self.assertEqual(len(kit[1]), 2)

    def testNoteHeads(self):
        kitData = """KIT_START
        DRUM Snare,Sn,x,True
        NOTEHEAD x 1,100,default
        NOTEHEAD g 1,50,ghost
        DRUM Kick,Bd,o,True
        NOTEHEAD o 2,100,default
        NOTEHEAD O 2,127,accent
        KIT_END
        """
        handle = StringIO(kitData)
        iterator = dbFileIterator(handle)
        kit = DrumKit.DrumKit()
        kit.read(iterator)
        self.assertEqual(kit.getDefaultHead(0), "x")
        self.assertEqual(kit.getDefaultHead(1), "o")
        self.assertEqual(kit.allowedNoteHeads(0),
                         ["x", "g"])
        self.assertEqual(kit.shortcutsAndNoteHeads(0), [("x", "x"), ("g", "g")])

    def testWrite(self):
        kit = DrumKit.DrumKit()
        drum = Drum("One", "d1", "x", True)
        drum.addNoteHead("x", HeadData())
        drum.addNoteHead("g",
                         HeadData(effect = "ghost", notationEffect = "ghost"))
        drum.checkShortcuts()
        kit.addDrum(drum)
        drum = Drum("Two", "d2", "o")
        drum.addNoteHead("o", HeadData(notationLine = -5, stemDirection = 1))
        drum.addNoteHead("O", HeadData(effect = "accent",
                                       notationEffect = "accent",
                                       notationLine = -5, stemDirection = 1))
        drum.checkShortcuts()
        kit.addDrum(drum)
        handle = StringIO()
        indenter = Indenter()
        kit.write(handle, indenter)
        outlines = handle.getvalue().splitlines()
        self.assertEqual(len(outlines), 8)
        self.assertEqual(outlines[0],
                         "KIT_START")
        self.assertEqual(outlines[1],
                         "  DRUM One,d1,x,True")
        self.assertEqual(outlines[2],
                         "    NOTEHEAD x 71,96,normal,default,0,none,0,x")
        self.assertEqual(outlines[3],
                         "    NOTEHEAD g 71,96,ghost,default,0,ghost,0,g")
        self.assertEqual(outlines[4],
                         "  DRUM Two,d2,o,False")
        self.assertEqual(outlines[5],
                         "    NOTEHEAD o 71,96,normal,default,-5,none,1,o")
        self.assertEqual(outlines[6],
                         "    NOTEHEAD O 71,96,accent,default,-5,accent,1,a")
        self.assertEqual(outlines[7],
                         "KIT_END")
if __name__ == "__main__":
    unittest.main()
