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
