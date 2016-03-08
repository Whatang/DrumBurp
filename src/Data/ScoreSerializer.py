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

import itertools
from cStringIO import StringIO
import codecs
from Data.fileStructures import dbfsv0, dbfsv1
from Data.DBErrors import DBVersionError, NoContent
from Data import DBConstants
import Data.fileUtils as fileUtils

_FS_MAP = {DBConstants.DBFF_0: dbfsv0.ScoreStructureV0,
           DBConstants.DBFF_1: dbfsv1.ScoreStructureV1}

class ScoreSerializer(object):
    @classmethod
    def loadScore(cls, filename):
        with fileUtils.DataReader(filename) as reader:
            score = cls.read(reader)
        return score

    @staticmethod
    def read(handle):
        # Check the file format version
        handle, handleCopy = itertools.tee(handle)
        try:
            firstline = handleCopy.next()
        except StopIteration:
            raise NoContent()
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
        score = fileStructure.read(scoreIterator)
        score.fileFormat = fileVersion
        return score

    @staticmethod
    def write(score, handle, version = DBConstants.CURRENT_FILE_FORMAT):
        scoreBuffer = StringIO()
        scoreWriter = codecs.getwriter("utf-8")(scoreBuffer)
        indenter = fileUtils.Indenter(scoreWriter)
        indenter(DBConstants.DB_FILE_FORMAT_STR, version)
        fileStructure = _FS_MAP.get(version,
                                    _FS_MAP[DBConstants.CURRENT_FILE_FORMAT])()
        fileStructure.write(score, indenter)
        handle.write(scoreBuffer.getvalue().decode("utf-8"))

    @classmethod
    def saveScore(cls, score, filename,
                  version = DBConstants.CURRENT_FILE_FORMAT,
                  compressed = True):
        with fileUtils.DataWriter(filename, compressed) as writer:
            score.fileFormat = version
            cls.write(score, writer, version)
