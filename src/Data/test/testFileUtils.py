'''
Created on 12 Dec 2012

@author: Mike Thomas
'''
import unittest
from cStringIO import StringIO
from Data import fileUtils

# pylint: disable-msg=R0904

class TestDbFileIterator(unittest.TestCase):
    def testIterate(self):
        mockfile = """firstline
        secondline hasdata
        
        thirdline comes after a blank
        """
        mockfile = StringIO(mockfile)
        iterator = fileUtils.dbFileIterator(mockfile)
        lines = list(iterator)
        self.assertEqual(lines,
                         [("FIRSTLINE", None),
                          ("SECONDLINE", "hasdata"),
                          ("THIRDLINE", "comes after a blank")])

class TestIndenter(unittest.TestCase):

    def setUp(self):
        self.indenter = fileUtils.Indenter()

    def testNoIndent(self):
        self.assert_(self.indenter("a", "b", "c"), "a b c")

    def testIndent(self):
        self.indenter.increase()
        self.assert_(self.indenter("a", "b", "c"), "  a b c")
        self.indenter.increase()
        self.assert_(self.indenter("a", "b", "c"), "    a b c")
        self.indenter.decrease()
        self.assert_(self.indenter("a", "b", "c"), "  a b c")
        self.indenter.decrease()
        self.assert_(self.indenter("a", "b", "c"), "a b c")

    def testContext(self):
        self.assert_(self.indenter("a", "b", "c"), "a b c")
        with self.indenter:
            self.assert_(self.indenter("a", "b", "c"), "  a b c")
            with self.indenter:
                self.assert_(self.indenter("a", "b", "c"), "    a b c")
        self.assert_(self.indenter("a", "b", "c"), "a b c")

if __name__ == "__main__":
    unittest.main()
