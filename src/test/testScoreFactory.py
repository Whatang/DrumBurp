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
import glob
import os
from cStringIO import StringIO
from Data.ScoreFactory import ScoreFactory, DataReader, DataWriter, DBFF_0
from Data import DBErrors

class Test(unittest.TestCase):
    def testMakeEmptyDefault(self):
        score = ScoreFactory.makeEmptyScore(16, None, None)
        self.assertEqual(score.numMeasures(), 16)

    def testFactory(self):
        factory = ScoreFactory()
        score = factory()
        self.assertEqual(score.numMeasures(), 32)

    def testReadTooHighVersionNumber(self):
        data = """DB_FILE_FORMAT 10000
        """
        handle = StringIO(data)
        self.assertRaises(DBErrors.DBVersionError, ScoreFactory.read, handle)

    ff_zero_data = """
    SCORE_METADATA
      TITLE Sample
    END_SCORE_METADATA
    KIT_START
      DRUM Foot pedal,Hf,x,False
        NOTEHEAD x 44,96,normal,cross,-5,none,1,x
      DRUM Kick,Bd,o,True
        NOTEHEAD o 36,96,normal,default,-3,none,1,a
        NOTEHEAD O 36,127,accent,default,-3,accent,1,o
        NOTEHEAD g 36,50,ghost,default,-3,ghost,1,g
        NOTEHEAD d 36,96,drag,default,-3,drag,1,d
      DRUM Floor Tom,FT,o,False
        NOTEHEAD o 43,96,normal,default,-1,none,1,a
        NOTEHEAD O 43,127,accent,default,-1,accent,1,o
        NOTEHEAD g 43,50,ghost,default,-1,ghost,1,g
        NOTEHEAD f 43,96,flam,default,-1,flam,1,f
        NOTEHEAD d 43,96,drag,default,-1,drag,1,d
      DRUM Snare,Sn,o,True
        NOTEHEAD o 38,96,normal,default,1,none,1,a
        NOTEHEAD O 38,127,accent,default,1,accent,1,o
        NOTEHEAD g 38,50,ghost,default,1,ghost,1,g
        NOTEHEAD x 37,96,normal,cross,1,none,1,x
        NOTEHEAD f 38,96,flam,default,1,flam,1,f
        NOTEHEAD d 38,96,drag,default,1,drag,1,d
      DRUM Mid Tom,MT,o,False
        NOTEHEAD o 47,96,normal,default,2,none,1,a
        NOTEHEAD O 47,127,accent,default,2,accent,1,o
        NOTEHEAD g 47,50,ghost,default,2,ghost,1,g
        NOTEHEAD f 47,96,flam,default,2,flam,1,f
        NOTEHEAD d 47,96,drag,default,2,drag,1,d
      DRUM High Tom,HT,o,False
        NOTEHEAD o 50,96,normal,default,3,none,1,a
        NOTEHEAD O 50,127,accent,default,3,accent,1,o
        NOTEHEAD g 50,50,ghost,default,3,ghost,1,g
        NOTEHEAD f 50,96,flam,default,3,flam,1,f
        NOTEHEAD d 50,96,drag,default,3,drag,1,d
      DRUM Ride,Ri,x,False
        NOTEHEAD x 51,96,normal,cross,4,none,0,a
        NOTEHEAD X 51,127,accent,cross,4,accent,0,x
        NOTEHEAD b 53,96,normal,triangle,4,none,0,b
        NOTEHEAD d 51,96,drag,cross,4,drag,0,d
      DRUM HiHat,Hh,x,False
        NOTEHEAD x 42,96,normal,cross,5,none,0,b
        NOTEHEAD X 42,127,accent,cross,5,accent,0,x
        NOTEHEAD o 46,96,normal,cross,5,open,0,o
        NOTEHEAD O 46,127,accent,cross,5,accent,0,a
        NOTEHEAD d 42,96,drag,cross,5,drag,0,d
        NOTEHEAD + 42,96,choke,cross,5,stopped,0,s
        NOTEHEAD # 42,96,choke,cross,5,choke,0,c
      DRUM Crash,Cr,x,False
        NOTEHEAD x 49,96,normal,cross,6,none,0,a
        NOTEHEAD X 49,127,accent,cross,6,accent,0,x
        NOTEHEAD # 49,96,choke,cross,6,stopped,0,c
    KIT_END
    START_BAR 8
      COUNT_INFO_START
        REPEAT_BEATS 4
        BEAT_START
          COUNT |^+|
        BEAT_END
      COUNT_INFO_END
      BARLINE NORMAL_BAR,REPEAT_START,NO_BAR
      BARLINE NORMAL_BAR,NO_BAR,REPEAT_END
      REPEAT_COUNT 3
    END_BAR
    START_BAR 8
      COUNT_INFO_START
        REPEAT_BEATS 4
        BEAT_START
          COUNT |^+|
        BEAT_END
      COUNT_INFO_END
      BARLINE NORMAL_BAR,NO_BAR
      NOTE 5,3,o
      NOTE 6,3,o
      BARLINE NORMAL_BAR,NO_BAR
    END_BAR
    START_BAR 8
      COUNT_INFO_START
        REPEAT_BEATS 4
        BEAT_START
          COUNT |^+|
        BEAT_END
      COUNT_INFO_END
      BARLINE NORMAL_BAR,REPEAT_START,NO_BAR
      NOTE 0,1,q
      NOTE 0,7,x
      NOTE 2,3,o
      NOTE 2,7,x
      NOTE 4,1,o
      NOTE 4,7,x
      NOTE 6,3,o
      NOTE 6,7,x
      BARLINE NORMAL_BAR,NO_BAR
    END_BAR
    START_BAR 8
      COUNT_INFO_START
        REPEAT_BEATS 4
        BEAT_START
          COUNT |^+|
        BEAT_END
      COUNT_INFO_END
      BARLINE NORMAL_BAR,NO_BAR
      NOTE 0,1,o
      NOTE 0,7,x
      NOTE 2,3,o
      NOTE 2,7,x
      NOTE 3,1,o
      NOTE 4,7,x
      NOTE 5,1,o
      NOTE 6,3,o
      NOTE 6,7,x
      BARLINE NORMAL_BAR,NO_BAR,REPEAT_END
      REPEAT_COUNT 10
    END_BAR
    START_BAR 8
      COUNT_INFO_START
        REPEAT_BEATS 4
        BEAT_START
          COUNT |^+|
        BEAT_END
      COUNT_INFO_END
      BARLINE NORMAL_BAR,REPEAT_START,NO_BAR
      NOTE 0,1,o
      NOTE 0,6,x
      NOTE 2,3,o
      NOTE 2,6,x
      NOTE 4,1,o
      NOTE 4,6,x
      NOTE 6,3,o
      NOTE 6,6,x
      NOTE 7,1,o
      BARLINE NORMAL_BAR,NO_BAR
    END_BAR
    START_BAR 8
      COUNT_INFO_START
        REPEAT_BEATS 4
        BEAT_START
          COUNT |^+|
        BEAT_END
      COUNT_INFO_END
      BARLINE NORMAL_BAR,NO_BAR
      NOTE 0,6,x
      NOTE 1,1,o
      NOTE 2,3,o
      NOTE 2,6,x
      NOTE 4,1,o
      NOTE 4,6,x
      NOTE 6,3,o
      NOTE 6,6,x
      BARLINE NORMAL_BAR,NO_BAR,REPEAT_END
      REPEAT_COUNT 2
      ALTERNATE 1-14.
    END_BAR
    START_BAR 8
      COUNT_INFO_START
        REPEAT_BEATS 4
        BEAT_START
          COUNT |^+|
        BEAT_END
      COUNT_INFO_END
      BARLINE NORMAL_BAR,NO_BAR
      NOTE 0,6,x
      NOTE 1,1,o
      NOTE 2,3,o
      NOTE 2,6,x
      NOTE 4,6,x
      NOTE 5,1,o
      NOTE 6,3,f
      BARLINE NORMAL_BAR,NO_BAR,SECTION_END
      ALTERNATE 15.
    END_BAR
    SECTION_TITLE A title
    PAPER_SIZE Letter
    LILYSIZE 18
    LILYPAGES 2
    LILYFILL YES
    DEFAULT_COUNT_INFO_START
      REPEAT_BEATS 4
      BEAT_START
        COUNT |^+|
      BEAT_END
    COUNT_INFO_END
    SYSTEM_SPACE 25
    FONT_OPTIONS_START
      NOTEFONT MS Shell Dlg 2
      NOTEFONTSIZE 10
      SECTIONFONT MS Shell Dlg 2
      SECTIONFONTSIZE 14
      METADATAFONT MS Shell Dlg 2
      METADATAFONTSIZE 16
    FONT_OPTIONS_END
    """

    def testReadNoFileFormatNumber(self):
        handle = StringIO(self.ff_zero_data)
        score = ScoreFactory.read(handle)
        self.assert_(score.lilyFill)
        self.assertEqual(score.lilypages, 2)
        self.assertEqual(score.lilysize, 18)
        self.assertEqual(score.scoreData.title, "Sample")
        self.assertEqual(score.numSections(), 1)
        self.assertEqual(score.getSectionTitle(0), "A title")
        self.assertEqual(score.numMeasures(), 7)
        self.assert_(score.drumKit[1].isAllowedHead('q'))

    def testReadVersion0(self):
        handle = StringIO("""DB_FILE_FORMAT 0
        """ + self.ff_zero_data)
        score = ScoreFactory.read(handle)
        self.assert_(score.lilyFill)
        self.assertEqual(score.lilypages, 2)
        self.assertEqual(score.lilysize, 18)
        self.assertEqual(score.scoreData.title, "Sample")
        self.assertEqual(score.numSections(), 1)
        self.assertEqual(score.getSectionTitle(0), "A title")
        self.assertEqual(score.numMeasures(), 7)
        self.assert_(score.drumKit[1].isAllowedHead('q'))

    def testVersion0Files(self):
        fileglob = os.path.join("testdata", "v0", "*.brp")
        for testfile in glob.glob(fileglob):
            print testfile
            score = ScoreFactory.loadScore(testfile)
            written = StringIO()
            ScoreFactory.write(score, written, DBFF_0)
            with DataReader(testfile) as reader:
                data = reader.read().splitlines()
            written = written.getvalue().splitlines()
            class NoFF(RuntimeError):
                pass
            class MCounts(RuntimeError):
                pass
            class Barline(RuntimeError):
                pass
            class NoLilyFormat(RuntimeError):
                pass
            class NoLilySize(RuntimeError):
                pass
            class NoLilyPages(RuntimeError):
                pass
            class ShortNoteHeads(RuntimeError):
                pass
            class OldTriplets(RuntimeError):
                pass
            class NoNoteheads(RuntimeError):
                pass
            while True:
                try:
                    for line1, line2 in zip(data, written):
                        try:
                            self.assertEqual(line1, line2)
                        except AssertionError:
                            if line2.startswith('DB_FILE_FORMAT'):
                                raise NoFF()
                            elif line2.lstrip().startswith('LILYFORMAT'):
                                raise NoLilyFormat()
                            elif line2.lstrip().startswith('LILYSIZE'):
                                raise NoLilySize()
                            elif line2.lstrip().startswith('LILYPAGES'):
                                raise NoLilyPages()
                            elif line2.startswith("  MEASURECOUNTSVISIBLE"):
                                raise MCounts()
                            elif "NORMAL_BAR," in line1:
                                raise Barline()
                            elif line1.lstrip().startswith("NOTEHEAD"):
                                raise ShortNoteHeads()
                            elif "|^ea|" in line1:
                                raise OldTriplets()
                            elif line1.lstrip().startswith("DRUM") and "NOTEHEAD" in line2:
                                raise NoNoteheads()
                            else:
                                raise
                    break
                except NoFF:
                     written = written[1:]
                except MCounts:
                    written = [x for x in written
                               if not x.startswith("  MEASURECOUNTSVISIBLE")]
                except Barline:
                    data = [x.replace('NORMAL_BAR,','') for x in data]
                except NoLilyFormat:
                    written = [x for x in written
                               if not x.lstrip().startswith("LILYFORMAT")]
                except NoLilySize:
                    written = [x for x in written
                               if not x.lstrip().startswith("LILYSIZE")]
                except NoLilyPages:
                    written = [x for x in written
                               if not x.lstrip().startswith("LILYPAGES")]
                except ShortNoteHeads:
                    for line1 in data:
                        numCommas = 0
                        if "NOTEHEAD" in line1:
                            numCommas = len([ch for ch in line1 if ch == ","])
                            break
                    written = [",".join(x.split(",", numCommas + 1)[:numCommas + 1])
                               if "NOTEHEAD" in x else x
                               for x in written]
                    data = [x.rstrip(",") for x in data]
                except OldTriplets:
                    data = [x.replace("|^ea|", "|^+a|") for x in data]
                except NoNoteheads:
                    written = [x for x in written
                             if "NOTEHEAD" not in x]
                    data = [x for x in data
                             if "NOTEHEAD" not in x]


if __name__ == "__main__":
    unittest.main()
