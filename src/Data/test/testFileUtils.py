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

    def testSections(self):
        handle = StringIO()
        with self.indenter.section(handle, "START1", "END1"):
            print >> handle, self.indenter("data1")
            with self.indenter.section(handle, "START2", "END2"):
                print >> handle, self.indenter("data2")
            with self.indenter.section(handle, "START3", "END3"):
                print >> handle, self.indenter("data3")
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["START1",
                          "  data1",
                          "  START2",
                          "    data2",
                          "  END2",
                          "  START3",
                          "    data3",
                          "  END3",
                          "END1"])


if __name__ == "__main__":
    unittest.main()
