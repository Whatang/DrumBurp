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
