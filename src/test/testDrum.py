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
        self.assertRaises(KeyError, drum.headData, None)

    @staticmethod
    def makeDrum():
        drum = Drum("test", "td", "x")
        defaultHead = HeadData(shortcut="y")
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


if __name__ == "__main__":
    unittest.main()
