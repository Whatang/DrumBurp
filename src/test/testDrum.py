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
import inspect

# pylint: disable-msg=R0904
from Data.Drum import Drum, HeadData
from Data import DefaultKits

class TestHeadData(unittest.TestCase):
    def testRead_New(self):
        dataString = "x 72,100,ghost,cross,1,choke,1,c"
        head, data = HeadData.read("Hh", dataString)
        self.assertEqual(head, "x")
        self.assertEqual(data.midiNote, 72)
        self.assertEqual(data.midiVolume, 100)
        self.assertEqual(data.effect, "ghost")
        self.assertEqual(data.notationHead, "cross")
        self.assertEqual(data.notationLine, 1)
        self.assertEqual(data.notationEffect, "choke")
        self.assertEqual(data.stemDirection, 1)
        self.assertEqual(data.shortcut, "c")

    def testRead_Old_Recognised_Drum(self):
        dataString = "g 72,100,ghost"
        head, data = HeadData.read("Sn", dataString)
        self.assertEqual(head, "g")
        self.assertEqual(data.midiNote, 72)
        self.assertEqual(data.midiVolume, 100)
        self.assertEqual(data.effect, "ghost")
        self.assertEqual(data.notationHead, "default")
        self.assertEqual(data.notationLine, 1)
        self.assertEqual(data.notationEffect, "ghost")
        self.assertEqual(data.stemDirection, 1)
        self.assertEqual(data.shortcut, "")

    def testRead_Old_Unrecognised_Drum(self):
        dataString = "g 72,100,ghost"
        head, data = HeadData.read("Xx", dataString)
        self.assertEqual(head, "g")
        self.assertEqual(data.midiNote, 72)
        self.assertEqual(data.midiVolume, 100)
        self.assertEqual(data.effect, "ghost")
        self.assertEqual(data.notationHead, "default")
        self.assertEqual(data.notationLine, 0)
        self.assertEqual(data.notationEffect, "none")
        self.assertEqual(data.stemDirection, 0)
        self.assertEqual(data.shortcut, "")


class TestDrum(unittest.TestCase):


    def testDrum(self):
        drum = Drum("test drum", "td", "x")
        self.assertEqual(drum.name, "test drum")
        self.assertEqual(drum.abbr, "td")
        self.assertEqual(drum.head, "x")
        self.assertFalse(drum.locked)

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

    def testDefaultHead(self):
        drum = Drum("test drum", "td", "x")
        self.assertEqual(len(drum), 0)
        self.assertEqual(drum.head, "x")
        self.assertFalse(drum.isAllowedHead("x"))
        self.assertRaises(KeyError, drum.headData , None)

    @staticmethod
    def makeDrum():
        drum = Drum("test", "td", "x")
        defaultHead = HeadData(shortcut = "y")
        drum.addNoteHead("x", defaultHead)
        newHead = HeadData(100)
        drum.addNoteHead("y", newHead)
        drum.addNoteHead("z", None)
        return drum, defaultHead, newHead

    def testAddNoteHead(self):
        drum, defaultHead, newHead = self.makeDrum()
        self.assertEqual(len(drum), 3)
        self.assert_(drum.isAllowedHead("x"))
        self.assert_(drum.isAllowedHead("y"))
        self.assert_(drum.isAllowedHead("z"))
        self.assertFalse(drum.isAllowedHead("a"))
        self.assertEqual(drum.headData("x"), defaultHead)
        self.assertEqual(drum.headData("y"), newHead)
        self.assertEqual(drum.headData(None), defaultHead)

    def testCopyDefaultHead(self):
        drum, defaultHead, second_ = self.makeDrum()
        thirdHead = drum.headData("z")
        for attr in dir(thirdHead):
            if (attr.startswith("_")
                or inspect.ismethod(getattr(defaultHead, attr))):
                continue
            if attr == "shortcut":
                self.assertNotEqual(defaultHead.shortcut, thirdHead.shortcut)
            else:
                self.assertEqual(getattr(defaultHead, attr),
                                 getattr(thirdHead, attr),
                                 "%s does not match" % attr)

    def testIterDrum(self):
        drum, first_, second_ = self.makeDrum()
        observed = list(drum)
        self.assertEqual(observed, ["x", "y", "z"])
        self.assertEqual(drum[0], "x")
        self.assertEqual(drum[1], "y")
        self.assertEqual(drum[2], "z")

    def testRenameHead(self):
        drum, first_, second_ = self.makeDrum()
        self.assert_(drum.isAllowedHead("x"))
        self.assertFalse(drum.isAllowedHead("a"))
        self.assertEqual(drum.head, "x")
        self.assertEqual(drum[0], "x")
        drum.renameHead("x", "a")
        self.assert_(drum.isAllowedHead("a"))
        self.assertFalse(drum.isAllowedHead("x"))
        self.assertEqual(drum.head, "a")
        self.assertEqual(drum[0], "a")
        drum.renameHead("q", "v")
        self.assertFalse(drum.isAllowedHead("q"))
        self.assertFalse(drum.isAllowedHead("v"))

    def testRemoveHead(self):
        drum, first_, second_ = self.makeDrum()
        self.assert_(drum.isAllowedHead("y"))
        self.assertEqual(len(drum), 3)
        drum.removeNoteHead("y")
        self.assertFalse(drum.isAllowedHead("y"))
        self.assertEqual(len(drum), 2)
        drum.removeNoteHead("q")
        self.assertEqual(len(drum), 2)

    def testMoveUp(self):
        drum, first_, second_ = self.makeDrum()
        self.assertEqual(list(drum), ["x", "y", "z"])
        drum.moveHeadUp("x")
        self.assertEqual(list(drum), ["x", "y", "z"])
        drum.moveHeadUp("y")
        self.assertEqual(list(drum), ["x", "y", "z"])
        drum.moveHeadUp("z")
        self.assertEqual(list(drum), ["x", "z", "y"])
        drum.moveHeadUp("a")
        self.assertEqual(list(drum), ["x", "z", "y"])

    def testMoveDown(self):
        drum, first_, second_ = self.makeDrum()
        self.assertEqual(list(drum), ["x", "y", "z"])
        drum.moveHeadDown("x")
        self.assertEqual(list(drum), ["x", "y", "z"])
        drum.moveHeadDown("z")
        self.assertEqual(list(drum), ["x", "y", "z"])
        drum.moveHeadDown("y")
        self.assertEqual(list(drum), ["x", "z", "y"])
        drum.moveHeadDown("a")
        self.assertEqual(list(drum), ["x", "z", "y"])

    def testGetShortcuts(self):
        drum, first_, second_ = self.makeDrum()
        second_.shortcut = "a"
        shorts = drum.shortcutsAndNoteHeads()
        self.assertEqual(shorts, [("y", "x"), ("a", "y"), ("z", "z")])

    def testSetDefault(self):
        drum, first_, second_ = self.makeDrum()
        self.assertEqual(drum.head, "x")
        self.assertEqual(list(drum), ["x", "y", "z"])
        drum.setDefaultHead("y")
        self.assertEqual(drum.head, "y")
        self.assertEqual(list(drum), ["y", "x", "z"])
        drum.setDefaultHead("z")
        self.assertEqual(drum.head, "z")
        self.assertEqual(list(drum), ["z", "y", "x"])
        drum.setDefaultHead("z")
        self.assertEqual(drum.head, "z")
        self.assertEqual(list(drum), ["z", "y", "x"])
        drum.setDefaultHead("a")
        self.assertEqual(drum.head, "z")
        self.assertEqual(list(drum), ["z", "y", "x"])

    def testReadHead(self):
        dataString = "x 72,100,ghost,cross,1,choke,1,c"
        drum = Drum("test", "td", "x")
        drum.readHeadData(dataString)
        self.assertEqual(len(drum), 1)
        self.assertEqual(drum.head, "x")
        self.assertEqual(drum[0], "x")

    def testGuessHeadData_Unknown(self):
        drum = Drum("test", "td", "x")
        drum.guessHeadData()
        self.assertEqual(len(drum), 1)
        self.assertEqual(drum[0], "x")
        headData = drum.headData(None)
        self.assertEqual(headData.midiNote, DefaultKits.DEFAULT_NOTE)
        self.assertEqual(headData.midiVolume, DefaultKits.DEFAULT_VOLUME)
        self.assertEqual(headData.effect, "normal")
        self.assertEqual(headData.notationHead, "default")
        self.assertEqual(headData.notationLine, 0)
        self.assertEqual(headData.notationEffect, "none")
        self.assertEqual(headData.stemDirection, DefaultKits.STEM_UP)
        self.assertEqual(headData.shortcut, "x")

    def testGuessHeadData_Known(self):
        drum = Drum("HiTom", "HT", "o")
        drum.guessHeadData()
        self.assertEqual(list(drum), ["o", "O", "g", "f", "d"])
        headData = drum.headData(None)
        self.assertEqual(headData.midiNote, 50)

if __name__ == "__main__":
    unittest.main()
