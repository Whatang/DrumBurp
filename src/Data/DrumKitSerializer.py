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
from cStringIO import StringIO
import itertools
from Data import fileUtils
from Data import DBConstants
from Data import DBErrors
from Data.fileStructures import dbfsv0, dbfsv1

class DrumKitSerializer(object):
    _KIT_FF_MAP = {DBConstants.KIT_FF_0:dbfsv0.DrumKitStructureV0,
                   DBConstants.KIT_FF_1:dbfsv1.DrumKitStructureV1}

    @classmethod
    def read(cls, handle):
        # Check the file format version
        handle, handleCopy = itertools.tee(handle)
        firstline = handleCopy.next()
        del handleCopy
        kitIterator = fileUtils.dbFileIterator(handle)
        if firstline.startswith(DBConstants.DB_KIT_FILE_FORMAT_STR):
            fileVersion = firstline.split()
            try:
                if len(fileVersion) >= 2:
                    fileVersion = int(fileVersion[1])
            except (TypeError, ValueError):
                fileVersion = DBConstants.KIT_FF_0
            kitIterator.next()
        else:
            fileVersion = DBConstants.KIT_FF_0
        if fileVersion > DBConstants.CURRENT_KIT_FORMAT:
            raise DBErrors.DBVersionError(kitIterator)
        fileStructure = cls._KIT_FF_MAP[fileVersion]()
        return fileStructure.read(kitIterator)

    @classmethod
    def loadKit(cls, filename):
        with fileUtils.DataReader(filename) as reader:
            score = cls.read(reader)
        return score

    @classmethod
    def write(cls, kit, handle, version = DBConstants.CURRENT_KIT_FORMAT):
        kitBuffer = StringIO()
        indenter = fileUtils.Indenter(kitBuffer)
        indenter(DBConstants.DB_KIT_FILE_FORMAT_STR, version)
        fileStructure = cls._KIT_FF_MAP.get(version,
                                            cls._KIT_FF_MAP[DBConstants.CURRENT_KIT_FORMAT])()
        fileStructure.write(kit, indenter)
        handle.write(kitBuffer.getvalue())

    @classmethod
    def saveKit(cls, kit, filename, version = DBConstants.CURRENT_KIT_FORMAT,
                compressed = True):
        with fileUtils.DataWriter(filename, compressed) as writer:
            cls.write(kit, writer, version)
