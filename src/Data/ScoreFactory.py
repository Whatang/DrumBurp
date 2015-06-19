import gzip
import codecs
import itertools
from cStringIO import StringIO
from Data.fileStructures import dbfsv0
from Data.Score import Score
from Data import DrumKit
from Data.Counter import CounterRegistry
from Data.MeasureCount import makeSimpleCount
from Data.DBErrors import DBVersionError
import Data.fileUtils as fileUtils

DBFF_0 = 0
CURRENT_FILE_FORMAT = DBFF_0

FS_MAPS = {DBFF_0: dbfsv0.ScoreStructureV0}

class ScoreFactory(object):
    def __call__(self, filename = None,
                 numMeasures = 32,
                 counter = None,
                 kit = None):
        if filename is not None:
            score = self.loadScore(filename)
        else:
            score = self.makeEmptyScore(numMeasures, counter, kit)
        return score

    @staticmethod
    def makeEmptyScore(numMeasures, counter, kit):
        score = Score()
        if kit is None:
            kit = DrumKit.getNamedDefaultKit()
        score.drumKit = kit
        if counter is None:
            registry = CounterRegistry()
            counter = list(registry.countsByTicks(2))
            counter = counter[0][1]
            counter = makeSimpleCount(counter, 4)
        for dummy in xrange(numMeasures):
            score.insertMeasureByIndex(len(counter), counter = counter)
        score.scoreData.makeEmpty()
        return score

    @classmethod
    def loadScore(cls, filename):
        try:
            with gzip.open(filename, 'rb') as handle:
                with codecs.getreader('utf-8')(handle) as reader:
                    score = cls.read(reader)
        except IOError:
            with open(filename, 'rU') as handle:
                score = cls.read(handle)
        return score
    
    @staticmethod
    def read(handle):
        # Check the file format version
        handle, handleCopy = itertools.tee(handle)
        firstline = handleCopy.next()
        del handleCopy
        scoreIterator = fileUtils.dbFileIterator(handle)
        if firstline.startswith("DB_FILE_FORMAT"):
            versionDict = {}
            with scoreIterator.section(None, None, readLines = 1) as section:
                section.readNonNegativeInteger("DB_FILE_FORMAT", versionDict,
                                               "fileVersion")
            fileVersion = versionDict.get("fileVersion", DBFF_0)
        else:
            fileVersion = DBFF_0
        if fileVersion > CURRENT_FILE_FORMAT:
            raise DBVersionError(scoreIterator)
        # TODO
        fileStructure = FS_MAPS[CURRENT_FILE_FORMAT]()
        return fileStructure.read(scoreIterator)

    @staticmethod
    def saveScore(score, filename):
        scoreBuffer = StringIO()
        indenter = fileUtils.Indenter(scoreBuffer)
        indenter("DB_FILE_FORMAT", CURRENT_FILE_FORMAT)
        fileStructure = FS_MAPS[CURRENT_FILE_FORMAT]()
        fileStructure.write(score, indenter)
        with gzip.open(filename, 'wb') as handle:
            with codecs.getwriter('utf-8')(handle) as writer:
                writer.write(scoreBuffer.getvalue())
