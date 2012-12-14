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

class _Target(object):
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

    def testSectionWithObject(self):
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
        mockfile = StringIO(mockfile)
        iterator = fileUtils.dbFileIterator(mockfile)
        with iterator.section("START", "END", "empty") as section:
            section.readString("STRING1", _Target, "s1")
            section.readString("STRING2", _Target, "s2")
            section.readString("EMPTY", _Target, "e")
            section.readInteger("INT1", _Target, "i1")
            section.readInteger("INT2", _Target, "i2")
            section.readBoolean("BOOL1", _Target, "b1")
            section.readBoolean("BOOL2", _Target, "b2")
            section.readPositiveInteger("POSINT", _Target, "pi")
            section.readNonNegativeInteger("NNINT", _Target, "nni")
            def reader(subiterator):
                _Target.sub_read = subiterator
            section.readSubsection("SUBSECTION", reader)
            def getlength(data):
                _Target.cb = len(data)
            section.readCallback("CALLBACK", getlength)
        self.assertEqual(_Target.s1, "string1")
        self.assertEqual(_Target.s2, "string2")
        self.assertEqual(_Target.e, "empty")
        self.assertEqual(_Target.i1, 1)
        self.assertEqual(_Target.i2, 2)
        self.assertEqual(_Target.pi, 100)
        self.assertEqual(_Target.nni, 0)
        self.assertEqual(_Target.b1, True)
        self.assertEqual(_Target.b2, False)
        self.assertEqual(_Target.sub_read, iterator)
        self.assertEqual(_Target.cb, 18)

    def testSectionWithDictionary(self):
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
        target = {}
        mockfile = StringIO(mockfile)
        iterator = fileUtils.dbFileIterator(mockfile)
        with iterator.section("START", "END", "empty") as section:
            section.readString("STRING1", target, "s1")
            section.readString("STRING2", target, "s2")
            section.readString("EMPTY", target, "e")
            section.readInteger("INT1", target, "i1")
            section.readInteger("INT2", target, "i2")
            section.readBoolean("BOOL1", target, "b1")
            section.readBoolean("BOOL2", target, "b2")
            section.readPositiveInteger("POSINT", target, "pi")
            section.readNonNegativeInteger("NNINT", target, "nni")
            def reader(subiterator):
                target["sub_read"] = subiterator
            section.readSubsection("SUBSECTION", reader)
            def getlength(data):
                target["cb"] = len(data)
            section.readCallback("CALLBACK", getlength)
        self.assertEqual(target["s1"], "string1")
        self.assertEqual(target["s2"], "string2")
        self.assertEqual(target["e"], "empty")
        self.assertEqual(target["i1"], 1)
        self.assertEqual(target["i2"], 2)
        self.assertEqual(target["pi"], 100)
        self.assertEqual(target["nni"], 0)
        self.assertEqual(target["b1"], True)
        self.assertEqual(target["b2"], False)
        self.assertEqual(target["sub_read"], iterator)
        self.assertEqual(target["cb"], 18)


    def testUnrecognisedLine(self):
        mockfile = """START
        STRING1 string1
        BAD LINE
        INT1 1
        END
        """
        mockfile = StringIO(mockfile)
        iterator = fileUtils.dbFileIterator(mockfile)
        errorRaised = False
        try:
            with iterator.section("START", "END", "empty") as section:
                section.readString("STRING1", _Target, "s1")
                section.readInteger("INT1", _Target, "i1")
        except IOError:
            errorRaised = True
        self.assert_(errorRaised)

    def testBadInteger(self):
        mockfile = """START
        STRING1 string1
        INT1 xxx
        END
        """
        mockfile = StringIO(mockfile)
        iterator = fileUtils.dbFileIterator(mockfile)
        errorRaised = False
        try:
            with iterator.section("START", "END", "empty") as section:
                section.readString("STRING1", _Target, "s1")
                section.readInteger("INT1", _Target, "i1")
        except IOError:
            errorRaised = True
        self.assert_(errorRaised)

    def testBadPositiveInteger(self):
        mockfile = """START
        STRING1 string1
        INT1 0
        END
        """
        mockfile = StringIO(mockfile)
        iterator = fileUtils.dbFileIterator(mockfile)
        errorRaised = False
        try:
            with iterator.section("START", "END", "empty") as section:
                section.readString("STRING1", _Target, "s1")
                section.readPositiveInteger("INT1", _Target, "i1")
        except IOError:
            errorRaised = True
        self.assert_(errorRaised)

    def testBadPositiveInteger2(self):
        mockfile = """START
        STRING1 string1
        INT1 -100
        END
        """
        mockfile = StringIO(mockfile)
        iterator = fileUtils.dbFileIterator(mockfile)
        errorRaised = False
        try:
            with iterator.section("START", "END", "empty") as section:
                section.readString("STRING1", _Target, "s1")
                section.readPositiveInteger("INT1", _Target, "i1")
        except IOError:
            errorRaised = True
        self.assert_(errorRaised)

    def testBadNonNegativeInteger(self):
        mockfile = """START
        STRING1 string1
        INT1 -1
        END
        """
        mockfile = StringIO(mockfile)
        iterator = fileUtils.dbFileIterator(mockfile)
        errorRaised = False
        try:
            with iterator.section("START", "END", "empty") as section:
                section.readString("STRING1", _Target, "s1")
                section.readNonNegativeInteger("INT1", _Target, "i1")
        except IOError:
            errorRaised = True
        self.assert_(errorRaised)

    def testBadNonNegativeInteger2(self):
        mockfile = """START
        STRING1 string1
        INT1 -100
        END
        """
        mockfile = StringIO(mockfile)
        iterator = fileUtils.dbFileIterator(mockfile)
        errorRaised = False
        try:
            with iterator.section("START", "END", "empty") as section:
                section.readString("STRING1", _Target, "s1")
                section.readNonNegativeInteger("INT1", _Target, "i1")
        except IOError:
            errorRaised = True
        self.assert_(errorRaised)

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
