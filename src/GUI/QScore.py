# Copyright 2011-12 Michael Thomas
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
from PyQt4.QtGui import QGraphicsItem
'''
Created on 4 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore
import itertools
import functools
from GUI.QStaff import QStaff
from GUI.QSection import QSection
from GUI.QMeasure import QMeasure
from GUI.QMetaData import QMetaData
from GUI.QKitData import QKitData
from GUI.QEditKitDialog import QEditKitDialog
from GUI.DBCommands import (MetaDataCommand, ScoreWidthCommand,
                            DeleteMeasureCommand, InsertAndPasteMeasures,
                            ClearMeasureCommand, PasteMeasuresCommand,
                            SetPaperSizeCommand, SetDefaultCountCommand,
                            SetSystemSpacingCommand, InsertMeasuresCommand,
                            SetFontCommand, SetFontSizeCommand,
                            SetVisibilityCommand, SetLilypondSizeCommand,
                            SetLilypondPagesCommand, SetLilypondFillCommand,
                            SaveFormatStateCommand, CheckFormatStateCommand,
                            CheckUndo, SetLilypondFormatCommand)
import GUI.DBMidi as DBMidi
from GUI.DBFSM import Waiting
from GUI.DBFSMEvents import Escape
from Data import DBErrors
from Data.Score import ScoreFactory
from Data.NotePosition import NotePosition
_SCORE_FACTORY = ScoreFactory()

class DragSelection(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

class _HeadShortcut(object):
    def __init__(self, currentHeads):
        self._headDict = dict((unicode(x), y) for (x, y) in currentHeads)
        self._headOrder = [unicode(x) for (x, y_) in currentHeads]
        self._textMemo = {}

    def text(self, currentKey):
        if currentKey not in self._headDict:
            currentKey = None
        if currentKey not in self._textMemo:
            self._textMemo[currentKey] = self._shortcutString(currentKey)
        return self._textMemo[currentKey]

    def getCurrentHead(self, currentKey):
        return self._headDict.get(currentKey, None)

    def _keyString(self, head):
        if head == unicode(self._headDict[head]):
            return head
        else:
            return u"%s(%s)" % (self._headDict[head], head)

    def _shortcutString(self, currentKey):
        if len(self._headOrder) > 1:
            headText = []
            for head in self._headOrder[1:]:  # Do not display default
                if head == currentKey:
                    headText.append(u'<span style="background-color:#55aaff;">'
                                    + self._keyString(head) + u"</span>")
                else:
                    headText.append(self._keyString(head))
            headText = "Head (Shortcut): " + u" ".join(headText)
        else:
            headText = ""
        return headText

class _HeadShortcutsMap(object):
    def __init__(self, drumkit):
        self.drumkit = drumkit
        self._shortcuts = {}
        self._current = None

    def setDrumKit(self, drumkit):
        self.drumkit = drumkit
        self._shortcuts = {}

    def setDrumIndex(self, index):
        if index is None:
            self._current = None
            return
        if index not in self._shortcuts:
            currentHeads = self.drumkit.shortcutsAndNoteHeads(index)
            self._shortcuts[index] = _HeadShortcut(currentHeads)
        self._current = self._shortcuts[index]

    def getShortcutText(self, currentKey):
        if self._current is None:
            return ""
        return self._current.text(currentKey)

    def getCurrentHead(self, currentKey):
        if self._current is None:
            return None
        return self._current.getCurrentHead(currentKey)

def delayCall(method):
    @functools.wraps(method)
    def delayer(*args, **kwargs):
        QtCore.QTimer.singleShot(0, lambda: method(*args, **kwargs))
    return delayer

def _metaDataProperty(varname):
    def _getData(self):
        return getattr(self.score.scoreData, varname)
    def _setData(self, value):
        if getattr(self, varname) != value:
            command = MetaDataCommand(self, varname,
                                      self.metadataChanged, value)
            self.addCommand(command)
    return property(fget = _getData, fset = _setData)

class QScore(QtGui.QGraphicsScene):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        super(QScore, self).__init__(parent)
        self._scale = 1
        self._qStaffs = []
        self._qSections = []
        self._properties = parent.songProperties
        self._score = None
        self._dirty = None
        self._currentKey = None
        self._ignoreNext = False
        self.measureClipboard = []
        self._playingMeasure = None
        self._nextMeasure = None
        self._dragStart = None
        self._lastDrag = None
        self._dragSelection = DragSelection(None, None)
        self._dragged = []
        self._saved = False
        self._undoStack = QtGui.QUndoStack(self)
        self._inMacro = False
        self._macroCanReformat = False
        self._undoStack.canUndoChanged.connect(self.canUndoChanged)
        self._undoStack.undoTextChanged.connect(self.undoTextChanged)
        self._undoStack.canRedoChanged.connect(self.canRedoChanged)
        self._undoStack.redoTextChanged.connect(self.redoTextChanged)
        self._metaData = QMetaData(self)
        self._metaData.setPos(self.xMargins,
                              self.yMargins)
        self._metaData.setVisible(self._properties.metadataVisible)
        self.metadataChanged.connect(lambda n_, v_: self.reBuild())
        self.paperSizeChanged.connect(parent.setPaperSize)
        self._kitData = QKitData(self)
        self._kitData.setPos(self.xMargins, 0)
        self._kitData.setVisible(self._properties.kitDataVisible)
        if parent.filename is not None:
            if not self.loadScore(parent.filename, quiet = False):
                parent.filename = None
                self.newScore(None)
        else:
            self.newScore(None)
        self.defaultCountChanged.connect(parent.setDefaultCount)
        self.spacingChanged.connect(parent.setSystemSpacing)
        self.sectionsChanged.connect(parent.setSections)
        self._properties.connectScore(self)
        self._potentials = []
        self._shortcutMemo = _HeadShortcutsMap(self._score.drumKit)
        self._state = Waiting(self)

    canUndoChanged = QtCore.pyqtSignal(bool)
    canRedoChanged = QtCore.pyqtSignal(bool)
    undoTextChanged = QtCore.pyqtSignal(str)
    redoTextChanged = QtCore.pyqtSignal(str)
    metadataChanged = QtCore.pyqtSignal(str, object)
    paperSizeChanged = QtCore.pyqtSignal(str)
    defaultCountChanged = QtCore.pyqtSignal(object)
    spacingChanged = QtCore.pyqtSignal(int)
    sectionsChanged = QtCore.pyqtSignal()
    showItem = QtCore.pyqtSignal(QGraphicsItem)
    dragHighlight = QtCore.pyqtSignal(bool)
    sceneFormatted = QtCore.pyqtSignal()
    playing = QtCore.pyqtSignal(bool)
    currentHeadsChanged = QtCore.pyqtSignal(QtCore.QString)
    statusMessageSet = QtCore.pyqtSignal(QtCore.QString)
    lilysizeChanged = QtCore.pyqtSignal(int)
    lilypagesChanged = QtCore.pyqtSignal(int)
    lilyFillChanged = QtCore.pyqtSignal(bool)
    lilyFormatChanged = QtCore.pyqtSignal(int)

    def addCommand(self, command):
        if not self._inMacro:
            self._undoStack.beginMacro(command.description)
            self._undoStack.push(CheckUndo(self))
            if command.canReformat:
                self._addSaveStateCommand()
        self._undoStack.push(command)
        if not self._inMacro:
            if command.canReformat:
                self._addCheckStateCommand()
            self._undoStack.endMacro()
        self.dirty = not (self._undoStack.isClean() and self._saved)

    def addRepeatedCommand(self, name, command, arguments):
        self.beginMacro(name, command.canReformat)
        for args in arguments:
            self.addCommand(command(self, *args))
        self.endMacro()

    def beginMacro(self, name, canReformat = True):
        self._undoStack.beginMacro(name)
        self._inMacro = True
        self._undoStack.push(CheckUndo(self))
        self._macroCanReformat = canReformat
        if canReformat:
            self._addSaveStateCommand()

    def endMacro(self):
        if self._macroCanReformat:
            self._addCheckStateCommand()
        self._undoStack.endMacro()
        self._inMacro = False

    def _addSaveStateCommand(self):
        command = SaveFormatStateCommand(self)
        self._undoStack.push(command)

    def _addCheckStateCommand(self):
        command = CheckFormatStateCommand(self)
        self._undoStack.push(command)

    def undo(self):
        self._undoStack.undo()
        self.dirty = not (self._undoStack.isClean() and self._saved)

    def redo(self):
        self._undoStack.redo()
        self.dirty = not (self._undoStack.isClean() and self._saved)

    def startUp(self):
        self.metadataChanged.emit("width", self.scoreWidth)
        self.setCurrentHeads(None)

    def _getscoreWidth(self):
        if self._score is not None:
            return self._score.scoreData.width
        else:
            return None
    def _setscoreWidth(self, value):
        if self._score is None:
            return
        if self.scoreWidth != value:
            command = ScoreWidthCommand(self, value)
            self.clearDragSelection()
            self.addCommand(command)
    scoreWidth = property(fget = _getscoreWidth,
                          fset = _setscoreWidth)

    artist = _metaDataProperty("artist")
    artistVisible = _metaDataProperty("artistVisible")
    creator = _metaDataProperty("creator")
    creatorVisible = _metaDataProperty("creatorVisible")
    title = _metaDataProperty("title")
    bpm = _metaDataProperty("bpm")
    bpmVisible = _metaDataProperty("bpmVisible")

    @property
    def displayProperties(self):
        return self._properties

    def _getdirty(self):
        return self._dirty
    def _setdirty(self, value):
        if self._dirty != value:
            self._dirty = value
            self.dirtySignal.emit(self._dirty)
    dirty = property(fget = _getdirty, fset = _setdirty)
    dirtySignal = QtCore.pyqtSignal(bool)

    @property
    def kitSize(self):
        return len(self._score.drumKit)

    @property
    def lineOffsets(self):
        yOffsets = [drumIndex * self.ySpacing
                    for drumIndex in range(0, self.kitSize)]
        yOffsets.reverse()
        return yOffsets

    def _setScore(self, score):
        if score != self._score:
            score.formatScore(None)
            self._score = score
            self._shortcutMemo = _HeadShortcutsMap(score.drumKit)
            if score is not None:
                self.startUp()
            self._score.setCallBack(self.dataChanged)
            self._build()
            self._properties.lineSpacing = self._score.systemSpacing - 101
            self.paperSizeChanged.emit(self._score.paperSize)
            self.defaultCountChanged.emit(self._score.defaultCount)
            self.spacingChanged.emit(self._score.systemSpacing)
            self.lilysizeChanged.emit(self._score.lilysize)
            self.lilypagesChanged.emit(self._score.lilypages)
            self.lilyFillChanged.emit(self._score.lilyFill)
            self.lilyFormatChanged.emit(self._score.lilyFormat)
            self.sectionsChanged.emit()
            self._properties.newScore(self)
            self._kitData.setVisible(self._properties.kitDataVisible)
            self._metaData.setVisible(self._properties.metadataVisible)
            DBMidi.setKit(score.drumKit)
            self._undoStack.clear()
            self._undoStack.setClean()
            self._inMacro = False
            for view in self.views():
                view.setWidth(self.scoreWidth)
            self.reBuild()
            self.dirty = False
            self._state = Waiting(self)
            self.scoreDisplayChanged.emit()

    @property
    def score(self):
        return self._score

    def _getscale(self):
        return self._scale
    def _setscale(self, value):
        if self._scale != value:
            self._scale = value
            yOffset = self.yMargins
            self._metaData.setPos(self.xMargins,
                                  yOffset)
            if self._properties.metadataVisible:
                yOffset += self._metaData.boundingRect().height()
            self._kitData.setPos(self.xMargins, yOffset)
            self._build()
            self.invalidate()
    scale = property(fget = _getscale, fset = _setscale)

    @property
    def xSpacing(self):
        return self._properties.xSpacing * self.scale

    @property
    def ySpacing(self):
        return self._properties.ySpacing * self.scale

    @property
    def lineSpacing(self):
        return self._properties.lineSpacing * self.scale

    @property
    def xMargins(self):
        return self._properties.xMargins * self.scale

    @property
    def yMargins(self):
        return self._properties.yMargins * self.scale

    def _build(self):
        self._clearStaffs()
        for staff in self._score.iterStaffs():
            self._addStaff(staff)
        for title in self._score.iterSections():
            self._addSection(title)
        self.placeStaffs()
        self.invalidate()

    scoreDisplayChanged = QtCore.pyqtSignal()

    @delayCall
    def reBuild(self):
        if self._score.formatScore(None):
            self.scoreDisplayChanged.emit()
        self._build()

    def checkFormatting(self):
        if self._score.formatScore(None):
            self.scoreDisplayChanged.emit()
            self.reBuild()

    def __iter__(self):
        return iter(self._qStaffs)

    def _clearStaffs(self):
        for qStaff in self._qStaffs:
            self.removeItem(qStaff)
        self._qStaffs = []
        for qSection in self._qSections:
            self.removeItem(qSection)
        self._qSections = []

    def _addStaff(self, staff):
        qStaff = QStaff(staff, len(self._qStaffs), self)
        self._qStaffs.append(qStaff)

    def _addSection(self, title):
        qSection = QSection(title, qScore = self)
        qSection.setIndex(len(self._qSections))
        self._qSections.append(qSection)

    def setSectionTitle(self, index, title):
        qSection = self._qSections[index]
        qSection.setTitle(title)

    def setPaperSize(self, newPaperSize):
        if newPaperSize != self._score.paperSize:
            command = SetPaperSizeCommand(self,
                                          newPaperSize)
            self.addCommand(command)

    def getQSection(self, sectionIndex):
        if 0 <= sectionIndex < len(self._qSections):
            return self._qSections[sectionIndex]

    def _getdefaultCount(self):
        return self._score.defaultCount
    def _setdefaultCount(self, newCount):
        if newCount != self._score.defaultCount:
            command = SetDefaultCountCommand(self, newCount)
            self.addCommand(command)
    defaultCount = property(_getdefaultCount,
                            _setdefaultCount)

    def _getsystemSpacing(self):
        return self._score.systemSpacing
    def _setsystemSpacing(self, value):
        if self._score.systemSpacing != value:
            command = SetSystemSpacingCommand(self, value)
            self.addCommand(command)
    systemSpacing = property(_getsystemSpacing, _setsystemSpacing)

    def placeStaffs(self, staffCall = QStaff.placeMeasures):
        xMargins = self.xMargins
        yMargins = self.yMargins
        lineSpacing = self.lineSpacing
        yOffset = self.yMargins
        if self._properties.metadataVisible:
            yOffset += self._metaData.boundingRect().height()
        if self._properties.kitDataVisible:
            self._kitData.setY(yOffset)
            yOffset += self._kitData.boundingRect().height()
        newSection = True
        sectionIndex = 0
        maxWidth = 0
        for qStaff in self:
            if newSection:
                newSection = False
                if sectionIndex < len(self._qSections):
                    qSection = self._qSections[sectionIndex]
                    sectionIndex += 1
                    qSection.setPos(xMargins, yOffset)
                    yOffset += qSection.boundingRect().height()
            newSection = qStaff.isSectionEnd()
            qStaff.setPos(xMargins, yOffset)
            if staffCall is not None:
                staffCall(qStaff)
            yOffset += qStaff.height() + lineSpacing
            maxWidth = max(maxWidth, qStaff.width())
            newSection = qStaff.isSectionEnd()
        self.setSceneRect(0, 0,
                          maxWidth + 2 * xMargins,
                          yOffset - lineSpacing + yMargins)
        self.sceneFormatted.emit()

    def xSpacingChanged(self):
        self.placeStaffs(QStaff.xSpacingChanged)

    def ySpacingChanged(self):
        self.placeStaffs(QStaff.ySpacingChanged)

    def lineSpacingChanged(self):
        self.placeStaffs(None)

    def sectionFontChanged(self):
        self._metaData.fontChanged()
        for qsection in self._qSections:
            qsection.setFont(self._properties.sectionFont)
        self.lineSpacingChanged()

    def metadataVisibilityChanged(self):
        self._metaData.setVisible(self._properties.metadataVisible)
        self.reBuild()

    def metadataFontChanged(self):
        with self.metaChange():
            self._metaData.fontChanged()

    def kitDataVisibleChanged(self):
        self._kitData.setVisible(self._properties.kitDataVisible)
        self.reBuild()

    def dataChanged(self, notePosition):
        staff = self._qStaffs[notePosition.staffIndex]
        staff.dataChanged(notePosition)
        self.scoreDisplayChanged.emit()

    def ignoreNextClick(self):
        self._ignoreNext = True

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos())
        if not isinstance(item, QMeasure):
            self.clearDragSelection()
        event.ignore()
        if self._ignoreNext:
            self._ignoreNext = False
        else:
            super(QScore, self).mousePressEvent(event)

    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            if event.key() == QtCore.Qt.Key_Escape:
                self.sendFsmEvent(Escape())
            else:
                if self._currentKey == None and event.text():
                    self._currentKey = unicode(event.text())
                    self._highlightCurrentKeyHead()
        return super(QScore, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            if event.key() != QtCore.Qt.Key_Escape:
                if unicode(event.text()) == self._currentKey:
                    self._currentKey = None
                    self._highlightCurrentKeyHead()
        return super(QScore, self).keyReleaseEvent(event)

    def getCurrentHead(self):
        return self._shortcutMemo.getCurrentHead(self._currentKey)

    def setCurrentHeads(self, drumIndex):
        self._shortcutMemo.setDrumIndex(drumIndex)
        self._highlightCurrentKeyHead()

    def _highlightCurrentKeyHead(self):
        headText = self._shortcutMemo.getShortcutText(self._currentKey)
        self.currentHeadsChanged.emit(QtCore.QString(headText))

    def copyMeasures(self, np = None):
        if np is not None:
            self.measureClipboard = [self._score.copyMeasure(np)]
        elif self.hasDragSelection():
            self.measureClipboard = [self._score.copyMeasure(dragNP)
                                     for (unusedMeasure, unusedIndex, dragNP)
                                     in self.iterDragSelection()]

    def clearMeasures(self, np = None):
        if np is not None:
            command = ClearMeasureCommand(self, [np])
        else:
            command = ClearMeasureCommand(self,
                                          [dragNP for (unusedMeasure,
                                                       unusedIndex,
                                                       dragNP)
                                           in self.iterDragSelection()])
        self.addCommand(command)

    def deleteMeasures(self, np = None):
        if np is not None:
            command = DeleteMeasureCommand(self, np)
            self.clearDragSelection()
            self.addCommand(command)
        else:
            if not self.hasDragSelection():
                return
            start = self._dragSelection.start
            measureIndex = self._score.getMeasureIndex(start)
            measures = list(self.iterDragSelection())
            self.clearDragSelection()
            self.beginMacro("delete measures")
            for unused in measures:
                command = DeleteMeasureCommand(self, start, measureIndex)
                self.addCommand(command)
            self.endMacro()

    @delayCall
    def insertMeasures(self, np):
        if len(self.measureClipboard) > 0:
            command = InsertAndPasteMeasures(self, np, self.measureClipboard)
            self.clearDragSelection()
            self.addCommand(command)

    @delayCall
    def pasteMeasuresOver(self, repeating = False):
        if len(self.measureClipboard) == 0 or not self.hasDragSelection():
            return
        start = self._dragSelection.start
        measureIndex = self._score.getMeasureIndex(start)
        sourceLength = len(self.measureClipboard)
        targetLength = len(list(self.iterDragSelection()))
        self.clearDragSelection()
        self.beginMacro("paste over measures")
        measureCount = 0
        clearPositions = []
        if repeating:
            resultLength = targetLength
            while measureCount < resultLength:
                position = self.score.getMeasurePosition(measureIndex
                                                         + measureCount)
                clearPositions.append(position)
                measureCount += 1
            command = ClearMeasureCommand(self, clearPositions)
            self.addCommand(command)
            measureData = []
            while len(measureData) < resultLength:
                measureData.extend(self.measureClipboard)
            measureData = measureData[:targetLength]
        else:
            resultLength = min([sourceLength, targetLength])
            while measureCount < resultLength:
                position = self.score.getMeasurePosition(measureIndex
                                                         + measureCount)
                clearPositions.append(position)
                measureCount += 1
            command = ClearMeasureCommand(self, clearPositions)
            self.addCommand(command)
            while measureCount < targetLength:
                deletePosition = self.score.getMeasurePosition(measureIndex
                                                               + sourceLength)
                command = DeleteMeasureCommand(self, deletePosition,
                                               measureIndex + sourceLength)
                self.addCommand(command)
                measureCount += 1
            if measureCount < sourceLength:
                position = self.score.getMeasurePosition(measureIndex
                                                         + measureCount)
                command = InsertMeasuresCommand(self,
                                                position,
                                                sourceLength - measureCount,
                                                self.defaultCount, True)
                self.addCommand(command)
            measureData = self.measureClipboard
            measureData = measureData[:sourceLength]
        command = PasteMeasuresCommand(self, start, measureData)
        self.addCommand(command)
        self.endMacro()

    def loadScore(self, filename, quiet = False):
        try:
            newScore = _SCORE_FACTORY(filename = filename)
        except DBErrors.DbReadError, exc:
            if not quiet:
                msg = "Error loading DrumBurp file %s" % filename
                QtGui.QMessageBox.warning(self.parent(),
                                          "Score load error",
                                          msg + "\n" + unicode(exc))
            return False
        except Exception, exc:
            raise
        self._setScore(newScore)
        self._saved = True
        return True

    def saveScore(self, filename):
        try:
            _SCORE_FACTORY.saveScore(self._score, filename)
        except StandardError, exc:
            msg = "Error saving DrumBurp file: %s" % unicode(exc)
            QtGui.QMessageBox.warning(self.parent(),
                                      "Score save error",
                                      msg)
            return False
        self._undoStack.setClean()
        self._saved = True
        self.dirty = False
        return True

    def newScore(self, kit, numMeasures = 16,
                 counter = None):
        if counter is None:
            if self._score is None:
                counter = None
            else:
                counter = self.defaultCount
        newScore = _SCORE_FACTORY(numMeasures = numMeasures,
                                  counter = counter,
                                  kit = kit)
        self._setScore(newScore)

    def numPages(self, pageHeight):
        topLeft = QtCore.QPointF(self.xMargins, self.yMargins)
        bottomRight = QtCore.QPointF(self.sceneRect().right() - self.xMargins,
                                     self.yMargins)
        numPages = 1
        for staff in self._qStaffs:
            newBottom = staff.y() + staff.height()
            if newBottom - topLeft.y() > pageHeight:
                numPages += 1
                topLeft.setY(bottomRight.y() + self.lineSpacing)
            bottomRight.setY(newBottom)
        return numPages

    def printScore(self, qprinter, scoreView):
        painter = QtGui.QPainter(qprinter)
        rect = qprinter.pageRect()
        printerDpi = float(qprinter.resolution())
        painter.save()
        painter.setFont(self._properties.metadataFont)
        fm = QtGui.QFontMetrics(painter.font())
        self._metaData.setRect(fm)
        painter.setFont(self._properties.noteFont)
        fm = QtGui.QFontMetrics(painter.font())
        self._kitData.setRect(fm)
        painter.restore()
        self.scale = printerDpi / scoreView.logicalDpiX()
        painter.save()
        painter.setFont(self._properties.sectionFont)
        for qSection in self._qSections:
            qSection.setFont(painter.font())
        painter.restore()
        self.placeStaffs()
        topLeft = QtCore.QPointF(self.xMargins, self.yMargins)
        bottomRight = QtCore.QPointF(self.sceneRect().right() - self.xMargins,
                                     self.yMargins)
        for staff in self._qStaffs:
            newBottom = staff.y() + staff.height()
            if newBottom - topLeft.y() > rect.height():
                sceneRect = QtCore.QRectF(topLeft, bottomRight)
                if sceneRect.width() > rect.width():
                    sceneRect.setWidth(rect.width())
                pageRect = QtCore.QRectF(0, 0,
                                         sceneRect.width(), sceneRect.height())
                self.render(painter, pageRect, sceneRect)
                qprinter.newPage()
                topLeft.setY(bottomRight.y() + self.lineSpacing)
            bottomRight.setY(newBottom)
        sceneRect = QtCore.QRectF(topLeft, bottomRight)
        if sceneRect.width() > rect.width():
            sceneRect.setWidth(rect.width())
        pageRect = QtCore.QRectF(0, 0, sceneRect.width(), sceneRect.height())
        self.render(painter, pageRect, sceneRect)
        painter.end()
        self._metaData.setRect()
        self._kitData.setRect()
        self.scale = 1

    def setLilypondSize(self, size):
        if size != self.score.lilysize:
            command = SetLilypondSizeCommand(self, size)
            self.addCommand(command)

    def setLilypondPages(self, numPages):
        if numPages != self.score.lilypages:
            command = SetLilypondPagesCommand(self, numPages)
            self.addCommand(command)

    def setLilyFill(self, lilyFill):
        if lilyFill != self.score.lilyFill:
            command = SetLilypondFillCommand(self, lilyFill)
            self.addCommand(command)

    def setLilyFormat(self, lilyFormat):
        if lilyFormat != self.score.lilyFormat:
            command = SetLilypondFormatCommand(self, lilyFormat)
            self.addCommand(command)

    def setScoreFontSize(self, size, fontType):
        fontName = fontType + "FontSize"
        if size == getattr(self._properties, fontName):
            return
        command = SetFontSizeCommand(self, size, fontType)
        self.addCommand(command)

    def setScoreFont(self, font, fontType):
        fontName = fontType + "Font"
        if self._properties is not None:
            fontFamily = getattr(self._properties, fontName)
            if fontFamily is None:
                setattr(self._properties, fontName, font)
                return
            elif font.family() == fontFamily.family():
                return
        command = SetFontCommand(self, font, fontType)
        self.addCommand(command)

    def setElementVisibility(self, onOff, elementName, text):
        element = elementName + "Visible"
        if getattr(self._properties, element) == onOff:
            return
        command = SetVisibilityCommand(self, onOff, elementName, text)
        self.addCommand(command)

    def getQMeasure(self, position):
        return self._qStaffs[position.staffIndex].getQMeasure(position)

    def getQStaff(self, possition):
        return self._qStaffs[possition.staffIndex]

    def highlightPlayingMeasure(self, position):
        if position == self._playingMeasure:
            return
        if self._playingMeasure != None:
            qMeasure = self.getQMeasure(self._playingMeasure)
            qMeasure.setPlaying(False)
        self._playingMeasure = position
        if self._playingMeasure == None:
            return
        qMeasure = self.getQMeasure(self._playingMeasure)
        qMeasure.setPlaying(True)

    def highlightNextMeasure(self, position):
        if position == self._nextMeasure:
            return
        if self._nextMeasure != None:
            qMeasure = self.getQMeasure(self._nextMeasure)
            qMeasure.setNextToPlay(False)
        self._nextMeasure = position
        if self._nextMeasure == None:
            return
        qMeasure = self.getQMeasure(self._nextMeasure)
        qMeasure.setNextToPlay(True)

    def editKit(self):
        emptyDrums = set(self.score.drumKit)
        for staffIndex in xrange(self.score.numStaffs()):
            lines = set(self.score.iterVisibleLines(staffIndex, True))
            emptyDrums.difference_update(lines)
            if not emptyDrums:
                break
        editDialog = QEditKitDialog(self.score.drumKit,
                                    emptyDrums,
                                    self.parent())
        if not editDialog.exec_():
            return
        kit, changes = editDialog.getNewKit()
        box = QtGui.QMessageBox.question(self.parent(),
                                         "Apply kit changes?",
                                         "Editing the kit cannot be undone. "
                                         "Proceed?",
                                         buttons = (QtGui.QMessageBox.Yes
                                                    | QtGui.QMessageBox.No))
        if box == QtGui.QMessageBox.Yes:
            self.score.changeKit(kit, changes)
            DBMidi.setKit(kit)
            self._shortcutMemo = _HeadShortcutsMap(kit)
            self._undoStack.clear()
            self._saved = False
            self.reBuild()
            self.dirty = True

    def _startDragging(self, qmeasure):
        self._dragStart = qmeasure
        self._lastDrag = qmeasure
        self._dragSelection.start = qmeasure.makeNotePosition(None, None)
        self._dragSelection.end = qmeasure.makeNotePosition(None, None)
        self._dragged = []
        self._updateDragged()
        self.dragHighlight.emit(True)

    def _updateDragged(self):
        if not self.hasDragSelection():
            for index, position in self._dragged:
                # Turn off
                self._setDragHighlight(position, False)
            self._dragged = []
            return
        newDragged = [(index, position) for (unused, index, position) in
                      self.score.iterMeasuresBetween(self._dragSelection.start,
                                                     self._dragSelection.end)]
        for index, position in newDragged:
            if all(x[0] != index for x in self._dragged):  # Turn on
                self._setDragHighlight(position, True)
        for index, position in self._dragged:
            if all(x[0] != index for x in newDragged):  # Turn off
                self._setDragHighlight(position, False)
        self._dragged = newDragged

    def dragging(self, qmeasure):
        if self._dragStart is None:
            self._startDragging(qmeasure)
        elif self._lastDrag != qmeasure:
            self._lastDrag = qmeasure
            self._dragSelection.end = self._lastDrag.makeNotePosition(None, None)
            self._updateDragged()

    def isDragging(self):
        return self._dragStart is not None

    def endDragging(self):
        self._dragStart = None
        self._lastDrag = None

    def hasDragSelection(self):
        return (self._dragSelection.start is not None and
                self._dragSelection.end is not None)

    def iterDragSelection(self):
        if self.hasDragSelection():
            return self.score.iterMeasuresBetween(self._dragSelection.start,
                                                  self._dragSelection.end)
        else:
            return iter([])

    def clearDragSelection(self):
        self._dragSelection.start = None
        self._dragSelection.end = None
        self._updateDragged()
        self.dragHighlight.emit(False)

    def _setDragHighlight(self, position, onOff):
        staff = self._qStaffs[position.staffIndex]
        qmeasure = staff.getQMeasure(position)
        qmeasure.setDragHighlight(onOff)

    def inDragSelection(self, np):
        if not self.hasDragSelection():
            return False
        start = self._dragSelection.start
        end = self._dragSelection.end
        return ((start.staffIndex == np.staffIndex
                 and start.measureIndex <= np.measureIndex
                 and (np.staffIndex < end.staffIndex or
                      np.measureIndex <= end.measureIndex))
                or (start.staffIndex < np.staffIndex < end.staffIndex)
                or (np.staffIndex == end.staffIndex
                    and np.measureIndex <= end.measureIndex))

    def metaChange(self):
        return _metaChangeContext(self, self._metaData)

    def sendFsmEvent(self, event):
#        print self._state, event
        try:
            self._state = self._state.send(event)
        except StandardError:
            self._state = Waiting(self)
            raise
#        print self._state

    def setStatusMessage(self, msg = None):
        if not msg:
            msg = ""
        self.statusMessageSet.emit(msg)

    def setPotentialRepeatNotes(self, notes, head):
        newMeasures = [(np.staffIndex, np.measureIndex) for np in notes]
        notesByMeasures = dict((x, list(y)) for x, y in
                               itertools.groupby(notes,
                                                 lambda np: (np.staffIndex,
                                                             np.measureIndex)))
        for measure in self._potentials:
            if measure not in notesByMeasures:
                qmeasure = self.getQMeasure(NotePosition(measure[0],
                                                         measure[1]))
                qmeasure.setPotentials()
        for measure in newMeasures:
            qmeasure = self.getQMeasure(NotePosition(measure[0], measure[1]))
            notes = notesByMeasures[measure]
            qmeasure.setPotentials(notes, head)
        self._potentials = newMeasures


class _metaChangeContext(object):
    def __init__(self, qScore, metaData):
        self._qScore = qScore
        self._metaData = metaData
        self._metaSize = metaData.boundingRect().height()
    def __enter__(self):
        return self
    def __exit__(self, excType, excValue, excTraceback):
        self._metaData.update()
        if self._metaData.boundingRect().height() != self._metaSize:
            self._qScore.placeStaffs()
        return False
