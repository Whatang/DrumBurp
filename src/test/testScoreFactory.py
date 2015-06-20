# Copyright 2015 Michael Thomas
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

import unittest
from Data.ScoreFactory import ScoreFactory

class TestScoreFactory(unittest.TestCase):
    def testMakeEmptyDefault(self):
        score = ScoreFactory.makeEmptyScore(16, None, None)
        self.assertEqual(score.numMeasures(), 16)

if __name__ == "__main__":
    unittest.main()
