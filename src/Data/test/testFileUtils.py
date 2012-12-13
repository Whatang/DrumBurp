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

    def testSection(self):
        mockfile = """START
        STRING1 string1
        INT1 1
        STRING2 string2
        INT2 2
        POSINT 100
        NNINT 0
        BOOL1 True
        BOOL2 False
        CALLBACK some callback data
        SUBSECTION
        EMPTY 
        END
        """
        class Target(object):
            s1 = None
            s2 = None
            e = None
            i1 = None
            i2 = None
            pi = None
            nni = None
            b1 = None
            b2 = None
            cb = None
            sub_read = None
        mockfile = StringIO(mockfile)
        iterator = fileUtils.dbFileIterator(mockfile)
        with iterator.section("START", "END", "empty") as section:
            section.readString("STRING1", Target, "s1")
            section.readString("STRING2", Target, "s2")
            section.readString("EMPTY", Target, "e")
            section.readInteger("INT1", Target, "i1")
            section.readInteger("INT2", Target, "i2")
            section.readBoolean("BOOL1", Target, "b1")
            section.readBoolean("BOOL2", Target, "b2")
            section.readPositiveInteger("POSINT", Target, "pi")
            section.readNonNegativeInteger("NNINT", Target, "nni")
            def reader(sub_iterator):
                Target.sub_read = sub_iterator
            section.readSubsection("SUBSECTION", reader)
            def get_length(data):
                Target.cb = len(data)
            section.readCallback("CALLBACK", get_length)
        self.assertEqual(Target.s1, "string1")
        self.assertEqual(Target.s2, "string2")
        self.assertEqual(Target.e, "empty")
        self.assertEqual(Target.i1, 1)
        self.assertEqual(Target.i2, 2)
        self.assertEqual(Target.pi, 100)
        self.assertEqual(Target.nni, 0)
        self.assertEqual(Target.b1, True)
        self.assertEqual(Target.b2, False)
        self.assertEqual(Target.sub_read, iterator)
        self.assertEqual(Target.cb, 18)

class TestIndenter(unittest.TestCase):

    def setUp(self):
        self.handle = StringIO()
        self.indenter = fileUtils.Indenter(self.handle)

    def testNoIndent(self):
        self.indenter("a", "b", "c")
        self.assertEqual(self.handle.getvalue(), "a b c\n")

    def testIndent(self):
        self.indenter.increase()
        self.indenter("a", "b", "c")
        self.indenter.increase()
        self.indenter("a", "b", "c")
        self.indenter.decrease()
        self.indenter("a", "b", "c")
        self.indenter.decrease()
        self.indenter("a", "b", "c")
        output = self.handle.getvalue().splitlines()
        self.assert_(output,
                     ["  a b c",
                      "    a b c",
                      "  a b c",
                      "a b c"])

    def testContext(self):
        self.indenter("a", "b", "c")
        with self.indenter:
            self.indenter("a", "b", "c")
            with self.indenter:
                self.indenter("a", "b", "c")
        self.indenter("a", "b", "c")
        output = self.handle.getvalue().splitlines()
        self.assert_(output,
                     ["a b c",
                      "  a b c",
                      "    a b c",
                      "a b c"])

    def testSections(self):
        with self.indenter.section("START1", "END1"):
            self.indenter("data1")
            with self.indenter.section("START2", "END2"):
                self.indenter("data2")
            with self.indenter.section("START3", "END3"):
                self.indenter("data3")
        output = self.handle.getvalue().splitlines()
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
