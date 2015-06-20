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
import itertools
from cStringIO import StringIO
from Data.fileStructures import dbfsv0
from Data.Score import Score
from Data import DrumKitFactory
from Data.Counter import CounterRegistry
from Data.MeasureCount import makeSimpleCount
from Data.DBErrors import DBVersionError
from Data import DBConstants
import Data.fileUtils as fileUtils

_FS_MAP = {DBConstants.DBFF_0: dbfsv0.ScoreStructureV0}

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
            kit = DrumKitFactory.DrumKitFactory.getNamedDefaultKit()
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
        with fileUtils.DataReader(filename) as reader:
            score = cls.read(reader)
        return score

    @staticmethod
    def read(handle):
        # Check the file format version
        handle, handleCopy = itertools.tee(handle)
        firstline = handleCopy.next()
        del handleCopy
        scoreIterator = fileUtils.dbFileIterator(handle)
        if firstline.startswith(DBConstants.DB_FILE_FORMAT_STR):
            fileVersion = firstline.split()
            try:
                if len(fileVersion) >= 2:
                    fileVersion = int(fileVersion[1])
            except (TypeError, ValueError):
                fileVersion = DBConstants.DBFF_0
            scoreIterator.next()
        else:
            fileVersion = DBConstants.DBFF_0
        if fileVersion > DBConstants.CURRENT_FILE_FORMAT:
            raise DBVersionError(scoreIterator)
        fileStructure = _FS_MAP[fileVersion]()
        return fileStructure.read(scoreIterator)

    @staticmethod
    def write(score, handle, version = DBConstants.CURRENT_FILE_FORMAT):
        scoreBuffer = StringIO()
        indenter = fileUtils.Indenter(scoreBuffer)
        indenter(DBConstants.DB_FILE_FORMAT_STR, version)
        fileStructure = _FS_MAP.get(version,
                                    _FS_MAP[DBConstants.CURRENT_FILE_FORMAT])()
        fileStructure.write(score, indenter)
        handle.write(scoreBuffer.getvalue())

    @classmethod
    def saveScore(cls, score, filename,
                  version = DBConstants.CURRENT_FILE_FORMAT,
                  compressed = True):
        with fileUtils.DataWriter(filename, compressed) as writer:
            cls.write(score, writer, version)
