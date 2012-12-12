'''
Created on 12 Dec 2012

@author: Mike Thomas
'''
import unittest
import time
from cStringIO import StringIO

# pylint: disable-msg=R0904

from Data import ScoreMetaData, fileUtils

class Test(unittest.TestCase):
    def testWrite(self):
        meta = ScoreMetaData.ScoreMetaData()
        meta.makeEmpty()
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        meta.save(indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["SCORE_METADATA",
                          "  TITLE Untitled",
                          "  ARTIST Unknown",
                          "  ARTISTVISIBLE True",
                          "  CREATOR Nobody",
                          "  CREATORVISIBLE True",
                          "  BPM 120",
                          "  BPMVISIBLE True",
                          "  WIDTH 80",
                          "  KITDATAVISIBLE True",
                          "  METADATAVISIBLE True",
                          "  BEATCOUNTVISIBLE True",
                          "  EMPTYLINESVISIBLE True",
                          "END_SCORE_METADATA"])

    def testExport(self):
        meta = ScoreMetaData.ScoreMetaData()
        meta.makeEmpty()
        ascii = meta.exportASCII()
        self.assertEqual(ascii,
                         ["Title     : Untitled",
                          "Artist    : Unknown",
                          "BPM       : 120",
                          "Tabbed by : Nobody",
                          "Date      : " + time.strftime("%d %B %Y"),
                          ""])

    def testRead(self):
        data = """SCORE_METADATA
                    TITLE Song
                    ARTIST xxx
                    ARTISTVISIBLE False
                    CREATOR zzz
                    CREATORVISIBLE False
                    BPM 200
                    BPMVISIBLE False
                    WIDTH 100
                    KITDATAVISIBLE False
                    METADATAVISIBLE False
                    BEATCOUNTVISIBLE False
                    EMPTYLINESVISIBLE False
                  END_SCORE_METADATA"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        meta = ScoreMetaData.ScoreMetaData()
        meta.load(iterator)
        self.assertEqual(meta.title, "Song")
        self.assertEqual(meta.artist, "xxx")
        self.assertEqual(meta.artistVisible, False)
        self.assertEqual(meta.creator, "zzz")
        self.assertEqual(meta.creatorVisible, False)
        self.assertEqual(meta.bpm, 200)
        self.assertEqual(meta.bpmVisible, False)
        self.assertEqual(meta.width, 100)
        self.assertEqual(meta.kitDataVisible, False)
        self.assertEqual(meta.metadataVisible, False)
        self.assertEqual(meta.beatCountVisible, False)
        self.assertEqual(meta.emptyLinesVisible, False)

    def testBadRead(self):
        data = """SCORE_METADATA
                    TITLE Song
                    ARTIST xxx
                    ARTISTVISIBLE False
                    BAD LINE
                    CREATOR zzz
                    CREATORVISIBLE False
                    BPM 200
                    BPMVISIBLE False
                    WIDTH 100
                    KITDATAVISIBLE False
                    METADATAVISIBLE False
                    BEATCOUNTVISIBLE False
                    EMPTYLINESVISIBLE False
                  END_SCORE_METADATA"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        meta = ScoreMetaData.ScoreMetaData()
        self.assertRaises(IOError, meta.load, iterator)

    def testBadBpm(self):
        data = """SCORE_METADATA
                    TITLE Song
                    ARTIST xxx
                    ARTISTVISIBLE False
                    CREATOR zzz
                    CREATORVISIBLE False
                    BPM qqq
                    BPMVISIBLE False
                    WIDTH 100
                    KITDATAVISIBLE False
                    METADATAVISIBLE False
                    BEATCOUNTVISIBLE False
                    EMPTYLINESVISIBLE False
                  END_SCORE_METADATA"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        meta = ScoreMetaData.ScoreMetaData()
        self.assertRaises(IOError, meta.load, iterator)

    def testNegativeBpm(self):
        data = """SCORE_METADATA
                    TITLE Song
                    ARTIST xxx
                    ARTISTVISIBLE False
                    CREATOR zzz
                    CREATORVISIBLE False
                    BPM -1
                    BPMVISIBLE False
                    WIDTH 100
                    KITDATAVISIBLE False
                    METADATAVISIBLE False
                    BEATCOUNTVISIBLE False
                    EMPTYLINESVISIBLE False
                  END_SCORE_METADATA"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        meta = ScoreMetaData.ScoreMetaData()
        self.assertRaises(IOError, meta.load, iterator)

    def testBadWidth(self):
        data = """SCORE_METADATA
                    TITLE Song
                    ARTIST xxx
                    ARTISTVISIBLE False
                    CREATOR zzz
                    CREATORVISIBLE False
                    BPM 200
                    BPMVISIBLE False
                    WIDTH zzz
                    KITDATAVISIBLE False
                    METADATAVISIBLE False
                    BEATCOUNTVISIBLE False
                    EMPTYLINESVISIBLE False
                  END_SCORE_METADATA"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        meta = ScoreMetaData.ScoreMetaData()
        self.assertRaises(IOError, meta.load, iterator)

    def testNegativeWidth(self):
        data = """SCORE_METADATA
                    TITLE Song
                    ARTIST xxx
                    ARTISTVISIBLE False
                    CREATOR zzz
                    CREATORVISIBLE False
                    BPM 200
                    BPMVISIBLE False
                    WIDTH -1
                    KITDATAVISIBLE False
                    METADATAVISIBLE False
                    BEATCOUNTVISIBLE False
                    EMPTYLINESVISIBLE False
                  END_SCORE_METADATA"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        meta = ScoreMetaData.ScoreMetaData()
        self.assertRaises(IOError, meta.load, iterator)

if __name__ == "__main__":
    unittest.main()
