'''
Created on 12 Dec 2010

@author: Mike Thomas
'''
import unittest
from Data.FormattedScore import FormattedScore
from Data.Score import makeEmptyScore

#pylint: disable-msg=R0904

class Test(unittest.TestCase):
    def testMakeEmptyFormattedScore(self):
        score = makeEmptyScore(8, 16, FormattedScore)


if __name__ == "__main__":
    unittest.main()
