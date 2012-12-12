'''
Created on 12 Dec 2012

@author: Mike Thomas
'''
import unittest
from cStringIO import StringIO
from Data import Counter
from Data import fileUtils
# pylint: disable-msg=R0904

class TestCounter(unittest.TestCase):
    counter = Counter.Counter("^bcd", "^fgh", "^jkl")
    def testLength(self):
        self.assertEqual(len(self.counter), 4)

    def testIter(self):
        self.assertEqual(list(self.counter), ["^", "b", "c", "d"])

    def testStr(self):
        self.assertEqual(str(self.counter), "^bcd")

    def testBadCounter(self):
        self.assertRaises(ValueError, Counter.Counter, "abcd")
        self.assertRaises(ValueError, Counter.Counter, "^bcd", "defg")
        self.assertRaises(ValueError, Counter.Counter, "^bcd", "^de")

    def testWrite(self):
        indenter = fileUtils.Indenter()
        handle = StringIO()
        self.counter.write(handle, indenter)
        self.assertEqual(handle.getvalue(), "COUNT |^bcd|\n")

    def testMatchExact(self):
        self.assert_(self.counter.matchesExact("^bcd"))
        self.assertFalse(self.counter.matchesExact("^fgh"))
        self.assertFalse(self.counter.matchesExact("^xyz"))

    def testMatchAlternative(self):
        self.assertFalse(self.counter.matchesAlternative("^bcd"))
        self.assert_(self.counter.matchesAlternative("^fgh"))
        self.assert_(self.counter.matchesAlternative("^jkl"))
        self.assertFalse(self.counter.matchesAlternative("^xyz"))

class TestCounterRegistryInit(unittest.TestCase):
    def testRegisterIterAndClear(self):
        reg = Counter.CounterRegistry(False)
        tc1 = Counter.Counter("^bcd")
        tc2 = Counter.Counter("^vw", "^yz")
        tc3 = Counter.Counter("^fgh")
        reg.register("four", tc1)
        reg.register("three", tc2)
        self.assertRaises(KeyError, reg.register, "four", tc3)
        self.assertRaises(ValueError, reg.register, "test", tc1)
        counts = list(reg)
        self.assertEqual(counts, [("four", tc1),
                                  ("three", tc2)])
        reg.clear()
        counts = list(reg)
        self.assertEqual(counts, [])

class TestCounterRegistryLookups(unittest.TestCase):
    def setUp(self):
        self.reg = Counter.CounterRegistry(False)
        self.counter1 = Counter.Counter("^bcd")
        self.counter2 = Counter.Counter("^vw", "^yz")
        self.counter3 = Counter.Counter("^fgh")
        self.reg.register("four", self.counter1)
        self.reg.register("three", self.counter2)
        self.reg.register("four2", self.counter3)

    def testGetItem(self):
        self.assertEqual(self.reg[1], self.counter2)
        self.assertRaises(IndexError, self.reg.__getitem__, 4)

    def testGetCounterByIndex(self):
        self.assertEqual(self.reg.getCounterByIndex(1), self.counter2)
        self.assertRaises(IndexError, self.reg.getCounterByIndex, 4)

    def testGetCounterByName(self):
        self.assertEqual(self.reg.getCounterByName("three"), self.counter2)
        self.assertRaises(KeyError, self.reg.getCounterByName, "bad name")

    def testCountsByTicks(self):
        twos = list(self.reg.countsByTicks(2))
        threes = list(self.reg.countsByTicks(3))
        fours = list(self.reg.countsByTicks(4))
        self.assertEqual(twos, [])
        self.assertEqual(threes, [("three", self.counter2)])
        self.assertEqual(fours, [("four", self.counter1),
                                 ("four2", self.counter3)])

    def testlookupIndex(self):
        self.assertEqual(self.reg.lookupIndex("^bcd"), 0)
        self.assertEqual(self.reg.lookupIndex("^vw"), 1)
        self.assertEqual(self.reg.lookupIndex("^yz"), 1)
        self.assertEqual(self.reg.lookupIndex("^fgh"), 2)
        self.assertEqual(self.reg.lookupIndex("^jkl"), -1)

    def testFindMaster(self):
        self.assertEqual(self.reg.findMaster("^bcd"), self.counter1)
        self.assertEqual(self.reg.findMaster("^vw"), self.counter2)
        self.assertEqual(self.reg.findMaster("^yz"), self.counter2)
        self.assertEqual(self.reg.findMaster("^fgh"), self.counter3)
        self.assertRaises(KeyError, self.reg.findMaster, "^jkl")

class TestDefaultRegistry(unittest.TestCase):
    reg = Counter.CounterRegistry()

    def testIter(self):
        self.assertEqual(len(list(self.reg)), 11)

    def testQuarters(self):
        names = [name for name, unusedCount in self.reg.countsByTicks(1)]
        self.assertEqual(names, ["Quarter Notes"])

    def testEighths(self):
        names = [name for name, unusedCount in self.reg.countsByTicks(2)]
        self.assertEqual(names, ["8ths"])

    def testSixteenths(self):
        names = [name for name, unusedCount in self.reg.countsByTicks(4)]
        self.assertEqual(names, ["16ths", "Sparse 16ths"])

    def testThirtySeconds(self):
        names = [name for name, unusedCount in self.reg.countsByTicks(8)]
        self.assertEqual(names, ["32nds", "Sparse 32nds"])

    def testTriplets(self):
        names = [name for name, unusedCount in self.reg.countsByTicks(3)]
        self.assertEqual(names, ["Triplets"])

    def testSixteenthTriplets(self):
        names = [name for name, unusedCount in self.reg.countsByTicks(6)]
        self.assertEqual(names, ["16th Triplets", "Sparse 16th Triplets"])

    def testThirtySecondTriplets(self):
        names = [name for name, unusedCount in self.reg.countsByTicks(12)]
        self.assertEqual(names, ["32nd Triplets", "Sparse 32nd Triplets"])

if __name__ == "__main__":
    unittest.main()
