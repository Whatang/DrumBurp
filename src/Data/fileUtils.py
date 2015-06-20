# Copyright 2012 Michael Thomas
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
Created on 7 Oct 2012

@author: Mike Thomas
'''
import itertools
import weakref
import Data.DBErrors as DBErrors

class dbFileIterator(object):
    class _Section(object):
        def __init__(self, iterator, startLine, endLine, convertNone = None, readLines = None):
            self._iterator = iterator
            self._startLine = startLine
            self._endLine = endLine
            self._convertNone = convertNone
            self._lines = {}
            self._readLines = readLines

        def __enter__(self):
            return self

        def _process(self):
            linesRead = 0
            for lineType, lineData in self._iterator:
                if lineData == None:
                    lineData = self._convertNone
                if lineType == self._startLine:
                    pass
                elif lineType == self._endLine:
                    break
                elif lineType in self._lines:
                    self._lines[lineType](lineData)
                else:
                    raise DBErrors.UnrecognisedLine(self._iterator)
                if self._readLines is not None:
                    linesRead += 1
                    if linesRead == self._readLines:
                        break


        def _parseInteger(self, data, lineName_):
            try:
                data = int(data)
            except (TypeError, ValueError):
                raise DBErrors.InvalidInteger(self._iterator)
            return data

        def _parsePositiveInteger(self, data, lineName):
            data = self._parseInteger(data, lineName)
            if data <= 0:
                raise DBErrors.InvalidPositiveInteger(self._iterator)
            return data

        def _parseNonNegativeInteger(self, data, lineName):
            data = self._parseInteger(data, lineName)
            if data < 0:
                raise DBErrors.InvalidNonNegativeInteger(self._iterator)
            return data

        @staticmethod
        def _parseBoolean(data, unusedLineName):
            return (data == "True" or data.upper() == "YES")


        @staticmethod
        def _parseString(data, unusedLineName):
            return data if data is not None else ""

        @staticmethod
        def _updateDict(target, key, value):
            target[key] = value

        def _storeReader(self, lineType, target, attrName, parser):
            if isinstance(target, dict):
                setter = self._updateDict
            else:
                setter = setattr
            self._lines[lineType] = lambda data: setter(target, attrName,
                                                        parser(data, lineType))

        def readInteger(self, lineType, target, attrName):
            self._storeReader(lineType, target, attrName, self._parseInteger)

        def readPositiveInteger(self, lineType, target, attrName):
            self._storeReader(lineType, target, attrName,
                              self._parsePositiveInteger)

        def readNonNegativeInteger(self, lineType, target, attrName):
            self._storeReader(lineType, target, attrName,
                              self._parseNonNegativeInteger)

        def readBoolean(self, lineType, target, attrName):
            self._storeReader(lineType, target, attrName,
                              self._parseBoolean)

        def readString(self, lineType, target, attrName):
            self._storeReader(lineType, target, attrName,
                              self._parseString)

        def readSubsection(self, lineType, callback):
            self._lines[lineType] = lambda unused: callback(self._iterator)

        def readCallback(self, lineType, callback):
            self._lines[lineType] = callback

        def __exit__(self, excType, excValue, excTraceback):
            if excType is None:
                self._process()
            return False

    def __init__(self, handle):
        self._handle = handle
        self.lineNumber = 0
        self.currentLine = ""

    def __iter__(self):
        for lineNumber, line in enumerate(self._handle):
            self.lineNumber = lineNumber
            line = line.strip()
            self.currentLine = line
            fields = line.split(None, 1)
            if len(fields) == 1:
                fields.append(None)
            elif len(fields) == 0:
                # Blank line
                continue
            lineType, lineData = fields
            lineType = lineType.upper()
            yield lineType, lineData

    def section(self, startLine, endLine, convertNone = None, readLines = None):
        return self._Section(self, startLine, endLine, convertNone, readLines)


class Indenter(object):
    class Section(object):
        def __init__(self, indenter, sectionStart, sectionEnd):
            self.indenter = indenter
            self.start = sectionStart
            self.end = sectionEnd

        def __enter__(self):
            self.indenter(self.start)
            self.indenter.increase()
            return self

        def __exit__(self, excType, excValue, excTraceback):
            self.indenter.decrease()
            self.indenter(self.end)
            return False

    def __init__(self, handle, indent = "  "):
        self._indent = indent
        self._handle = handle
        self._level = 0

    def increase(self):
        self._level += 1

    def decrease(self):
        self._level -= 1
        self._level = max(0, self._level)

    def __call__(self, *args):
        argString = " ".join(unicode(ar) for ar in args)
        if self._level != 0:
            argString = (self._indent * self._level) + argString
        print >> self._handle, argString

    def __enter__(self):
        self.increase()
        return self

    def __exit__(self, excType, excValue, excTraceback):
        self.decrease()
        return False

    def section(self, sectionStart, sectionEnd):
        return self.Section(self, sectionStart, sectionEnd)

class _IDMaker(object):
    _next_id = 0

    @classmethod
    def get(cls):
        next_id = cls._next_id
        cls._next_id += 1
        return cls._next_id

class ObjectsOrderedByID(object):
    def __init__(self):
        self.ordered_id = _IDMaker.get()

class Field(ObjectsOrderedByID):
    def __init__(self, title, attributeName = None, singleton = True):
        super(Field, self).__init__()
        self.title = title.upper()
        self.attributeName = attributeName
        self.singleton = singleton
        

    def read(self, target, data):
        raise NotImplementedError()
    
    def write(self, source):
        raise NotImplementedError()

class SimpleValueField(Field):
    def read(self, target, data):
        data = self._processData(data)
        if self.singleton:
            if isinstance(target, dict):
                target[self.attributeName] = data
            else:
                setattr(target, self.attributeName, data)
        else:
            if isinstance(target, dict):
                if self.attributeName not in target:
                    target[self.attributeName] = []
                target[self.attributeName].append(data)
            else:
                if not hasattr(target, self.attributeName):
                    setattr(target, self.attributeName, [])
                getattr(target, self.attributeName).append(data)
        
    def _processData(self, data):
        raise NotImplementedError()
    
    def write(self, source):
        if self.singleton:
            values = [getattr(source, self.attributeName)]
        else:
            values = getattr(source, self.attributeName)
        for value in values:
            value = self._toString(value)
            if value:
                yield "%s %s" % (self.title, value)
    
    def _toString(self, value):
        raise NotImplementedError()

class StringField(SimpleValueField):
    def _processData(self, data):
        return data
    
    def _toString(self, value):
        return unicode(value)

class IntegerField(SimpleValueField):
    def _processData(self, data):
        try:
            data = int(data)
        except (TypeError, ValueError):
            raise DBErrors.InvalidInteger()
        return data

    def _toString(self, value):
        return "%d" % value

class NonNegativeIntegerField(IntegerField):
    def _processData(self, data):
        data = IntegerField._processData(self, data)
        if data < 0:
            raise DBErrors.InvalidNonNegativeInteger()
        return data
        
class PositiveIntegerField(IntegerField):
    def _processData(self, data):
        data = IntegerField._processData(self, data)
        if data <= 0:
            raise DBErrors.InvalidPositiveInteger()
        return data

class BooleanField(SimpleValueField):
    def _processData(self, data):
        data = data.upper()
        return data in ("TRUE", "YES")

    def _toString(self, value):
        if value:
            return "True"
        else:
            return "False"

class CallbackField(Field):
    def __init__(self, title, readCallback, writeCallback, attributeName = None,
                 singleton = None):
        super(CallbackField, self).__init__(title,
                                            attributeName = attributeName,
                                            singleton = singleton)
        self.readCallback = readCallback
        self.writeCallback = writeCallback

class FileStructureMetaClass(type):
    def __init__(cls, name, bases, dct):
        super(FileStructureMetaClass, cls).__init__(name, bases, dct)
        cls._fields = []
        cls._structures = []
        cls._ordered_data = []
        for attr, value in dct.iteritems():
            if isinstance(value, Field):
                cls._fields.append(value)
                cls._ordered_data.append((value.ordered_id, attr, value))
                if value.attributeName is None:
                    value.attributeName = attr
            elif name != 'FileStructure' and isinstance(value, FileStructure):
                if value.attributeName is None:
                    value.attributeName = attr
                cls._structures.append(value)
                cls._ordered_data.append((value.ordered_id, attr, value))
        cls._ordered_data.sort()
        for _, attr, value in cls._ordered_data:
            print name, attr
        if cls.tag is not None:
            if cls.startTag is None:
                cls.startTag = "START_" + cls.tag
            if cls.endTag is None:
                cls.endTag = "END_" + cls.tag


class FileStructure(ObjectsOrderedByID):
    __metaclass__ = FileStructureMetaClass
    targetClass = dict
    tag = None
    startTag = None
    endTag = None
    autoMake = False
    _fields = []
    _structures = []

    def __init__(self, attributeName = None, singleton = True,
                 startTag = None, endTag = None):
        super(FileStructure, self).__init__()
        self.attributeName = attributeName
        self.singleton = singleton
        if startTag is not None:
            self.startTag = startTag
        if endTag is not None:
            self.endTag = endTag

    def read(self, fileIterator, startData = None):
        instance = None
        if self.autoMake:
            instance = self.makeObject(None)
        fieldDict = dict((field.title, field) for field in self._fields)
        structDict = dict((structure.startTag, structure)
                          for structure in self._structures)
        if startData is not None:
            iterator = itertools.chain([startData], fileIterator)
        else:
            iterator = fileIterator
        try:
            for lineType, lineData in iterator:
#                 print lineType, lineData
                if lineType in fieldDict:
                    field = fieldDict[lineType]
                    field.read(instance, lineData)
                elif lineType in structDict:
                    structure = structDict[lineType]
                    subInstance = structure.read(fileIterator,
                                                 (lineType, lineData))
                    if structure.singleton:
                        if isinstance(instance, dict):
                            instance[structure.attributeName] = subInstance
                        else:
                            setattr(instance, structure.attributeName, subInstance)
                    else:
                        if isinstance(instance, dict):
                            if structure.attributeName not in instance:
                                instance[structure.attributeName] = []
                            instance[structure.attributeName].append(subInstance)
                        else:
                            if not hasattr(instance, structure.attributeName):
                                setattr(instance, structure.attributeName, [])
                            getattr(instance, structure.attributeName).append(subInstance)
                elif lineType == self.startTag:
                    instance = self.makeObject(lineData)
                elif lineType == self.endTag:
                    break
                else:
                    raise DBErrors.UnrecognisedLine()
            return self.postProcessObject(instance)
        except DBErrors.DbReadError, exc:
            exc.setIterator(fileIterator)
            raise
    
    def makeObject(self, objectData):
        return self.targetClass()

    def postProcessObject(self, instance):
        return instance

    def write(self, src, indenter):
        # TODO:
        raise RuntimeError("Not implemented")
