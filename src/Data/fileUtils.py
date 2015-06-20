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

    def next(self):
        return self._handle.next()

    def section(self, startLine, endLine, convertNone = None, readLines = None):
        return self._Section(self, startLine, endLine, convertNone, readLines)


class Indenter(object):
    class Section(object):
        def __init__(self, indenter, sectionStart, sectionEnd):
            self.indenter = indenter
            self._doIndent = sectionStart is not None and sectionEnd is not None
            self.start = sectionStart
            self.end = sectionEnd

        def __enter__(self):
            if self._doIndent:
                self.indenter(self.start)
                self.indenter.increase()
            return self

        def __exit__(self, excType, excValue, excTraceback):
            if self._doIndent:
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
        nextId = cls._next_id
        cls._next_id += 1
        return nextId

class ObjectsOrderedByID(object):
    def __init__(self):
        self.ordered_id = _IDMaker.get()

class WriteAllInterface(object):
    def write_all(self, src, indenter):
        raise NotImplementedError()

class Field(ObjectsOrderedByID, WriteAllInterface):
    def __init__(self, title, attributeName = None, singleton = True,
                 getter = None):
        super(Field, self).__init__()
        self.title = title.upper()
        self.attributeName = attributeName
        self.singleton = singleton
        self.getter = getter

    def getValue(self, src):
        if self.getter is None:
            return getattr(src, self.attributeName)
        else:
            return self.getter(src)

    def read(self, target, data):
        raise NotImplementedError()

    def write(self, source):
        raise NotImplementedError()

    def write_all(self, src, indenter):
        valueList = self.getValue(src)
        if self.singleton and valueList is not None:
            valueList = [valueList]
        elif valueList is None:
            valueList = []
        for value in valueList:
            for subValue in self.write(value):
                indenter(subValue)

    def format(self, outdata):
        return "%s %s" % (self.title, outdata)

def conditionalWriteField(field, predicate):
    getter = field.getValue
    def getterWrapper(source):
        if predicate(source):
            return getter(source)
    field.getValue = getterWrapper
    return field

class SimpleReadField(Field):
    def __init__(self, title, attributeName = None, singleton = True,
                 getter = None):
        super(SimpleReadField, self).__init__(title, attributeName, singleton,
                                               getter)

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

class SimpleWriteField(Field):
    def __init__(self, title, attributeName = None, singleton = True,
                 getter = None):
        super(SimpleWriteField, self).__init__(title, attributeName, singleton,
                                               getter)

    def write(self, source):
        value = self._toString(source)
        if value:
            yield self.format(value)

    def _toString(self, value):
        raise NotImplementedError()

class SimpleValueField(SimpleReadField, SimpleWriteField):
    pass

class NoReadField(Field):
    def __init__(self, title, attributeName = None, singleton = True,
                 getter = None):
        super(NoReadField, self).__init__(title, attributeName, singleton,
                                          getter)

    def read(self, target, data):
        pass

class NoWriteField(Field):
    def __init__(self, title, attributeName = None, singleton = True):
        super(NoWriteField, self).__init__(title, attributeName, singleton,
                                           getter = lambda _:None)

    def write(self, src):
        pass

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

class YesNoField(BooleanField):
    def _toString(self, value):
        if value:
            return "YES"
        else:
            return "NO"

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
        if cls.tag is not None:
            if cls.startTag is None:
                cls.startTag = "START_" + cls.tag
            if cls.endTag is None:
                cls.endTag = "END_" + cls.tag


class FileStructure(ObjectsOrderedByID, WriteAllInterface):
    __metaclass__ = FileStructureMetaClass
    targetClass = dict
    tag = None
    startTag = None
    endTag = None
    autoMake = False
    _fields = []
    _structures = []
    _ordered_data = []

    def __init__(self, attributeName = None, singleton = True,
                 startTag = None, endTag = None, getter = None):
        super(FileStructure, self).__init__()
        self.attributeName = attributeName
        self.singleton = singleton
        self.getter = getter
        if startTag is not None:
            self.startTag = startTag
        if endTag is not None:
            self.endTag = endTag

    def getValue(self, src):
        if self.getter is None:
            return getattr(src, self.attributeName)
        else:
            return self.getter(src)

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

    def startTagData(self, source):
        return None

    def postProcessObject(self, instance):
        return instance

    def write(self, src, indenter):
        startTag = self.startTag
        if startTag is not None:
            extra = self.startTagData(src)
            if extra is not None:
                startTag += " " + extra
        with indenter.section(startTag, self.endTag):
            for _, attr, structure in self._ordered_data:
                structure.write_all(src, indenter)

    def write_all(self, src, indenter):
        valueList = self.getValue(src)
        if self.singleton:
            valueList = [valueList]
        for subValue in valueList:
            self.write(subValue, indenter)
