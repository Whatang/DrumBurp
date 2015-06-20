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

class DataReader(object):
    def __init__(self, filename):
        self.filename = filename
        self._reader = None
        self._gzHandle = None

    def __enter__(self):
        try:
            with gzip.open(self.filename, 'rb') as handle:
                with codecs.getreader('utf-8')(handle) as reader:
                    reader.read(50)
            self._gzHandle = gzip.open(self.filename, 'rb')
            self._reader = codecs.getreader('utf-8')(self._gzHandle)
        except IOError:
            self._gzHandle = None
            self._reader = codecs.getreader('utf-8')(open(self.filename))
        return self._reader

    def __exit__(self, exc_type, exc_value, traceback):
        self._reader.close()
        if self._gzHandle is not None:
            self._gzHandle.close()

class DataWriter(object):
    def __init__(self, filename, compressed):
        self.filename = filename
        self.compressed = compressed
        self._writer = None
        self._gzHandle = None

    def __enter__(self):
        if self.compressed:
            self._gzHandle = gzip.open(self.filename, 'wb')
            self._writer = codecs.getwriter('utf-8')(self._gzHandle)
        else:
            self._gzHandle = None
            self._writer = codecs.getwriter('utf-8')(open(self.filename, 'w'))
        return self._writer

    def __exit__(self, exc_type, exc_value, traceback):
        self._writer.close()
        if self._gzHandle is not None:
            self._gzHandle.close()


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
        with DataReader(filename) as reader:
            score = cls.read(reader)
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
        fileStructure = FS_MAPS[CURRENT_FILE_FORMAT]()
        return fileStructure.read(scoreIterator)
    
    @staticmethod
    def write(score, handle, version = CURRENT_FILE_FORMAT):
        scoreBuffer = StringIO()
        indenter = fileUtils.Indenter(scoreBuffer)
        indenter("DB_FILE_FORMAT", version)
#         fileStructure = FS_MAPS.get(version, CURRENT_FILE_FORMAT)()
#         fileStructure.write(score, indenter)
        score.write(scoreBuffer)
        handle.write(scoreBuffer.getvalue())
        
    @classmethod
    def saveScore(cls, score, filename, version = CURRENT_FILE_FORMAT, compressed = True):
        with DataWriter(filename, compressed) as writer:
            cls.write(score, writer, version)
