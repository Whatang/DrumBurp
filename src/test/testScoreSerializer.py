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
'''
Created on Jun 20, 2015

@author: Mike Thomas
'''

import unittest
import glob
import os
import tempfile
import codecs
import cStringIO
from Data.ScoreSerializer import ScoreSerializer
from Data.ScoreFactory import ScoreFactory
from Data import DBConstants
from Data import DBErrors
from Data import fileUtils


def StringIO(*args, **kwargs):  # IGNORE:invalid-name
    "Utility function to wrap StringIO with utf-8 reading/writing"
    handle = cStringIO.StringIO(*args, **kwargs)
    return codecs.StreamReaderWriter(handle,
                                     codecs.getreader('utf-8'),
                                     codecs.getwriter('utf-8'))


class TestScoreSerializerGeneral(unittest.TestCase):
    def testReadTooHighVersionNumber(self):
        data = """DB_FILE_FORMAT 10000
        """
        handle = StringIO(data)
        self.assertRaises(DBErrors.DBVersionError,
                          ScoreSerializer.read, handle)


class TestScoreSerializerV0(unittest.TestCase):

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
        score = ScoreSerializer.read(handle)
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
        score = ScoreSerializer.read(handle)
        self.assert_(score.lilyFill)
        self.assertEqual(score.lilypages, 2)
        self.assertEqual(score.lilysize, 18)
        self.assertEqual(score.scoreData.title, "Sample")
        self.assertEqual(score.numSections(), 1)
        self.assertEqual(score.getSectionTitle(0), "A title")
        self.assertEqual(score.numMeasures(), 7)
        self.assert_(score.drumKit[1].isAllowedHead('q'))

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

    class NoLilyFill(RuntimeError):
        pass

    class NoLilyPages(RuntimeError):
        pass

    class ShortNoteHeads(RuntimeError):
        pass

    class OldTriplets(RuntimeError):
        pass

    class NoNoteheads(RuntimeError):
        pass

    def _compareData(self, data, written):
        for line1, line2 in zip(data, written):
            try:
                self.assertEqual(line1, line2)
            except AssertionError:
                if line2.startswith('DB_FILE_FORMAT'):
                    raise self.NoFF()
                elif line2.lstrip().startswith('LILYFORMAT'):
                    raise self.NoLilyFormat()
                elif line2.lstrip().startswith('LILYSIZE'):
                    raise self.NoLilySize()
                elif line2.lstrip().startswith('LILYPAGES'):
                    raise self.NoLilyPages()
                elif line2.lstrip().startswith('LILYFILL'):
                    raise self.NoLilyFill()
                elif line2.startswith("  MEASURECOUNTSVISIBLE"):
                    raise self.MCounts()
                elif "NORMAL_BAR," in line1:
                    raise self.Barline()
                elif line1.lstrip().startswith("NOTEHEAD"):
                    raise self.ShortNoteHeads()
                elif "|^ea|" in line1:
                    raise self.OldTriplets()
                elif line1.lstrip().startswith("DRUM") and "NOTEHEAD" in line2:
                    raise self.NoNoteheads()
                else:
                    raise

    @staticmethod
    def _tidyShortNoteHeads(data, written):
        for line1 in data:
            numCommas = 0
            if "NOTEHEAD" in line1:
                numCommas = len([ch for ch in line1 if ch == ","])
                break
        written = [",".join(x.split(",", numCommas + 1)[:numCommas + 1])
                   if "NOTEHEAD" in x else x
                   for x in written]
        data = [x.rstrip(",") for x in data]
        return data, written

    def testVersion0Files(self):
        print "Version 0"
        fileglob = os.path.join("testdata", "v0", "*.brp")
        for testfile in glob.glob(fileglob):
            print testfile
            score = ScoreSerializer.loadScore(testfile)
            written = StringIO()
            ScoreSerializer.write(score, written, DBConstants.DBFF_0)
            with fileUtils.DataReader(testfile) as reader:
                data = reader.read().splitlines()
            written = written.getvalue().splitlines()
            while True:
                try:
                    self._compareData(data, written)
                    break
                except self.NoFF:
                    written = written[1:]
                except self.MCounts:
                    written = [x for x in written
                               if not x.lstrip().startswith("MEASURECOUNTSVISIBLE")]
                except self.Barline:
                    data = [x.replace('NORMAL_BAR,', '') for x in data]
                except self.NoLilyFormat:
                    written = [x for x in written
                               if not x.lstrip().startswith("LILYFORMAT")]
                except self.NoLilySize:
                    written = [x for x in written
                               if not x.lstrip().startswith("LILYSIZE")]
                except self.NoLilyPages:
                    written = [x for x in written
                               if not x.lstrip().startswith("LILYPAGES")]
                except self.NoLilyFill:
                    written = [x for x in written
                               if not x.lstrip().startswith("LILYFILL")]
                except self.ShortNoteHeads:
                    data, written = self._tidyShortNoteHeads(data, written)
                except self.OldTriplets:
                    data = [x.replace("|^ea|", "|^+a|") for x in data]
                except self.NoNoteheads:
                    written = [x for x in written if "NOTEHEAD" not in x]
                    data = [x for x in data if "NOTEHEAD" not in x]


class TestScoreSerializerV1(unittest.TestCase):
    def testReadV0WriteV1ReadV1(self):
        print "Read Version 0, Write Version 1"
        fileglob = os.path.join("testdata", "v0", "*.brp")
        for testfile in glob.glob(fileglob):
            print testfile
            score = ScoreSerializer.loadScore(testfile)
            written = StringIO()
            ScoreSerializer.write(score, written, DBConstants.DBFF_1)
            written.seek(0)
            score2 = ScoreSerializer.read(written)
            self.assertEqual(score.hashScore(), score2.hashScore())

    def testReadV1WriteV1(self):
        print "Read Version 1, Write Version 1"
        fileglob = os.path.join("testdata", "v1", "*.brp")
        for testfile in glob.glob(fileglob):
            print testfile
            score = ScoreSerializer.loadScore(testfile)
            written = StringIO()
            ScoreSerializer.write(score, written, DBConstants.DBFF_1)
            written.seek(0)
            score2 = ScoreSerializer.read(written)
            self.assertEqual(score.hashScore(), score2.hashScore())


class TestUnicode(unittest.TestCase):
    def testWriteUnicode(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".brp",
                                          prefix="unicode_test_v1",
                                          delete=False)
        try:
            tmp.close()
            score = ScoreFactory.makeEmptyScore(8)
            score.scoreData.title = u"\u20b9"
            ScoreSerializer.saveScore(score, tmp.name)
            score2 = ScoreSerializer.loadScore(tmp.name)
            self.assertEqual(score.hashScore(), score2.hashScore())
            self.assertEqual(score2.scoreData.title, u"\u20b9")
        finally:
            try:
                tmp.close()
            except RuntimeError:
                pass
            os.unlink(tmp.name)


if __name__ == "__main__":
    unittest.main()
