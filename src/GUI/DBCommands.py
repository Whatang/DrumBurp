# Copyright 2011 Michael Thomas
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
Created on 13 Feb 2011

@author: Mike Thomas
'''
from PyQt4.QtGui import QUndoCommand
from Data import DBConstants
from Data.Score import Score
from Data.NotePosition import NotePosition
import copy

class ScoreCommand(QUndoCommand):
    def __init__(self, qScore, np, description):
        super(ScoreCommand, self).__init__(description)
        self._qScore = qScore
        self._np = copy.copy(np)
        self._score = self._qScore.score

    def undo(self):
        self._score.saveFormatState()
        self._undo()
        self._qScore.checkFormatting()

    def _undo(self):
        raise NotImplementedError()

    def redo(self):
        self._score.saveFormatState()
        self._redo()
        self._qScore.checkFormatting()

    def _redo(self):
        raise NotImplementedError()

class DebugScoreCommand(ScoreCommand): #pylint:disable-msg=W0223
    def __init__(self, qScore, np, description):
        super(DebugScoreCommand, self).__init__(qScore, np, description)
        self._hash = self._score.hashScore()

    def undo(self):
        super(DebugScoreCommand, self).undo()
        newHash = self._score.hashScore()
        print newHash.encode('hex'), self._hash.encode('hex')
        assert(newHash == self._hash)

_COMMAND_CLASS = DebugScoreCommand

class NoteCommand(_COMMAND_CLASS): #pylint:disable-msg=W0223
    def __init__(self, qScore, notePosition, head):
        super(NoteCommand, self).__init__(qScore, notePosition,
                                          "Set note")
        self._oldHead = self._score.getNote(notePosition)
        self._head = head

    def _undo(self):
        if self._oldHead == DBConstants.EMPTY_NOTE:
            self._score.deleteNote(self._np)
        else:
            self._score.addNote(self._np, self._oldHead)

class SetNote(NoteCommand):
    def _redo(self):
        self._score.addNote(self._np, self._head)

class ToggleNote(NoteCommand):
    def _redo(self):
        self._score.toggleNote(self._np, self._head)

class MetaDataCommand(_COMMAND_CLASS):
    def __init__(self, qScore, varName, signal, value):
        super(MetaDataCommand, self).__init__(qScore, None,
                                              "Edit metadata")
        self._oldValue = getattr(self._score.scoreData, varName)
        self._varname = varName
        self._signal = signal
        self._value = value

    def _redo(self):
        setattr(self._score.scoreData, self._varname, self._value)
        self._signal.emit(self._varname, self._value)

    def _undo(self):
        setattr(self._score.scoreData, self._varname, self._oldValue)
        self._signal.emit(self._varname, self._oldValue)

class ScoreWidthCommand(_COMMAND_CLASS):
    def __init__(self, qScore, value):
        super(ScoreWidthCommand, self).__init__(qScore, None,
                                                "Set Width")
        self._oldValue = self._score.scoreData.width
        self._value = value

    def _redo(self):
        self._score.scoreData.width = self._value
        for view in self._qScore.views():
            view.setWidth(self._value)

    def _undo(self):
        self._score.scoreData.width = self._oldValue
        for view in self._qScore.views():
            view.setWidth(self._oldValue)

class PasteMeasure(_COMMAND_CLASS):
    def __init__(self, qScore, notePosition, clipboard):
        super(PasteMeasure, self).__init__(qScore, notePosition,
                                           "Paste Measure")
        self._measure = clipboard
        self._oldMeasure = None

    def _redo(self):
        self._oldMeasure = self._score.pasteMeasure(self._np, self._measure)

    def _undo(self):
        self._score.pasteMeasure(self._np, self._oldMeasure)

class RepeatNoteCommand(_COMMAND_CLASS):
    def __init__(self, qScore, notePosition, nRepeats, repInterval, head):
        super(RepeatNoteCommand, self).__init__(qScore, notePosition,
                                                "Repeat Note")
        self._head = head
        np = copy.copy(notePosition)
        self._oldNotes = [(np, self._score.getNote(np))]
        for dummyIndex in range(nRepeats):
            np = copy.copy(np)
            np = self._score.notePlus(np, repInterval)
            self._oldNotes.append((np, self._score.getNote(np)))

    def _redo(self):
        for np, dummyHead in self._oldNotes:
            self._score.addNote(np, self._head)

    def _undo(self):
        for np, head in self._oldNotes:
            if head == DBConstants.EMPTY_NOTE:
                self._score.deleteNote(np)
            else:
                self._score.addNote(np, head)

class InsertMeasuresCommand(_COMMAND_CLASS):
    def __init__(self, qScore, notePosition, numMeasures, counter):
        super(InsertMeasuresCommand, self).__init__(qScore, notePosition,
                                                    "Insert Measures")
        self._index = self._score.getMeasureIndex(self._np)
        self._numMeasures = numMeasures
        self._width = len(counter)
        self._counter = counter

    def _redo(self):
        for dummyMeasureIndex in range(self._numMeasures):
            self._score.insertMeasureByIndex(self._width, self._index,
                                             counter = self._counter)

    def _undo(self):
        for dummyMeasureIndex in range(self._numMeasures):
            self._score.deleteMeasureByIndex(self._index)

class InsertSectionCommand(_COMMAND_CLASS):
    def __init__(self, qScore, np, sectionIndex):
        super(InsertSectionCommand, self).__init__(qScore, np,
                                                   "Insert Section Copy")
        self._np.measureIndex = 0
        self._np = self._np.makeMeasurePosition()
        self._np.staffIndex = self._score.getSectionStartStaffIndex(np)
        self._index = sectionIndex

    def _redo(self):
        self._score.insertSectionCopy(self._np,
                                      self._index)
        self._qScore.sectionsChanged.emit()

    def _undo(self):
        self._score.deleteSection(self._np)
        self._qScore.sectionsChanged.emit()

class SetRepeatCountCommand(_COMMAND_CLASS):
    def __init__(self, qScore, notePosition, oldCount, newCount):
        super(SetRepeatCountCommand, self).__init__(qScore, notePosition,
                                                    "Set Repeat Count")
        self._oldCount = oldCount
        self._newCount = newCount

    def _redo(self):
        measure = self._score.getItemAtPosition(self._np)
        measure.repeatCount = self._newCount

    def _undo(self):
        measure = self._score.getItemAtPosition(self._np)
        measure.repeatCount = self._oldCount

class EditMeasurePropertiesCommand(_COMMAND_CLASS):
    def __init__(self, qScore, np, newCounter):
        name = "Edit Measure Properties"
        super(EditMeasurePropertiesCommand, self).__init__(qScore,
                                                           np,
                                                           name)
        self._newCounter = newCounter
        self._oldMeasure = self._score.copyMeasure(np)

    def _redo(self):
        measure = self._score.getItemAtPosition(self._np)
        measure.setBeatCount(self._newCounter)

    def _undo(self):
        self._score.pasteMeasure(self._np, self._oldMeasure, True)

class SetMeasureLineCommand(_COMMAND_CLASS):
    def __init__(self, qScore, descr, np, onOff, method):
        super(SetMeasureLineCommand, self).__init__(qScore, np,
                                                    descr)
        self._onOff = onOff
        self._method = method

    def _redo(self):
        self._method(self._score, self._np, self._onOff)
        self._qScore.reBuild()

    def _undo(self):
        self._method(self._score, self._np, not self._onOff)
        self._qScore.reBuild()

class SetSectionEndCommand(SetMeasureLineCommand):
    def __init__(self, qScore, np, onOff):
        super(SetSectionEndCommand, self).__init__(qScore,
                                                   "Set Section End",
                                                   np, onOff,
                                                   Score.setSectionEnd)
        if not onOff:
            self._index = self._score.getSectionIndex(np)
            self._title = self._score.getSectionTitle(self._index)

    def _undo(self):
        super(SetSectionEndCommand, self)._undo()
        if not self._onOff:
            self._score.setSectionTitle(self._index, self._title)
        self._qScore.sectionsChanged.emit()

    def _redo(self):
        super(SetSectionEndCommand, self)._redo()
        self._qScore.sectionsChanged.emit()



class SetLineBreakCommand(SetMeasureLineCommand):
    def __init__(self, qScore, np, onOff):
        super(SetLineBreakCommand, self).__init__(qScore,
                                                  "Set Line Break",
                                                  np, onOff,
                                                  Score.setLineBreak)

class SetRepeatStartCommand(SetMeasureLineCommand):
    def __init__(self, qScore, np, onOff):
        super(SetRepeatStartCommand, self).__init__(qScore,
                                                    "Set Repeat Start",
                                                    np, onOff,
                                                    Score.setRepeatStart)

class SetRepeatEndCommand(SetMeasureLineCommand):
    def __init__(self, qScore, np, onOff):
        super(SetRepeatEndCommand, self).__init__(qScore,
                                                  "Set Repeat End",
                                                  np, onOff,
                                                  Score.setRepeatEnd)

class DeleteMeasureCommand(_COMMAND_CLASS):
    def __init__(self, qScore, np):
        super(DeleteMeasureCommand, self).__init__(qScore, np,
                                                   "Delete Measure")
        self._index = self._score.getMeasureIndex(np)
        self._oldMeasure = self._score.copyMeasure(np)
        self._sectionIndex = None
        self._sectionTitle = None
        if self._oldMeasure.isSectionEnd():
            self._sectionIndex = self._score.getSectionIndex(np)
            self._sectionTitle = self._score.getSectionTitle(self._sectionIndex)

    def _redo(self):
        self._score.deleteMeasureByIndex(self._index)
        if self._sectionIndex:
            self._qScore.sectionsChanged.emit()

    def _undo(self):
        self._score.turnOffCallBacks()
        self._score.insertMeasureByIndex(len(self._oldMeasure), self._index)
        self._score.gridFormatScore()
        if self._sectionIndex is not None:
            self._score.setSectionEnd(self._np, True)
            self._score.setSectionTitle(self._sectionIndex,
                                        self._sectionTitle)
            self._score.gridFormatScore()
            self._qScore.sectionsChanged.emit()
        self._score.pasteMeasureByIndex(self._index, self._oldMeasure, True)
        self._score.turnOnCallBacks()

class SetSectionTitleCommand(_COMMAND_CLASS):
    def __init__(self, qScore, sectionIndex, title):
        super(SetSectionTitleCommand, self).__init__(qScore,
                                                     None,
                                                     "Set Section Title")
        self._index = sectionIndex
        self._oldTitle = self._score.getSectionTitle(sectionIndex)
        self._title = title

    def _redo(self):
        self._score.setSectionTitle(self._index,
                                    self._title)
        self._qScore.setSectionTitle(self._index,
                                     self._title)
        self._qScore.sectionsChanged.emit()

    def _undo(self):
        self._score.setSectionTitle(self._index,
                                    self._oldTitle)
        self._qScore.setSectionTitle(self._index,
                                     self._oldTitle)
        self._qScore.sectionsChanged.emit()

class SetAlternateCommand(_COMMAND_CLASS):
    def __init__(self, qScore, np, alternate):
        super(SetAlternateCommand, self).__init__(qScore,
                                                  np,
                                                  "Set Alternate Text")
        self._alternate = alternate
        self._np.noteTime = None
        self._np.drumIndex = None
        measure = self._score.getItemAtPosition(self._np)
        self._oldAlternate = measure.alternateText

    def _redo(self):
        measure = self._score.getItemAtPosition(self._np)
        measure.alternateText = self._alternate
        self._qScore.dataChanged(self._np)

    def _undo(self):
        measure = self._score.getItemAtPosition(self._np)
        measure.alternateText = self._oldAlternate
        self._qScore.dataChanged(self._np)

class SetPaperSizeCommand(_COMMAND_CLASS):
    def __init__(self, qScore, newPaperSize):
        super(SetPaperSizeCommand, self).__init__(qScore,
                                                  NotePosition(),
                                                  "Set Page Size")
        self._new = newPaperSize
        self._old = self._score.paperSize

    def _redo(self):
        self._score.paperSize = self._new
        self._qScore.paperSizeChanged.emit(self._new)

    def _undo(self):
        self._score.paperSize = self._old
        self._qScore.paperSizeChanged.emit(self._old)

class SetDefaultCountCommand(_COMMAND_CLASS):
    def __init__(self, qScore, newCount):
        super(SetDefaultCountCommand, self).__init__(qScore,
                                                     NotePosition(),
                                                     "Set Default Count")
        self._new = newCount
        self._old = self._score.defaultCount

    def _redo(self):
        self._score.defaultCount = self._new
        self._qScore.defaultCountChanged.emit(self._new)

    def _undo(self):
        self._score.defaultCount = self._old
        self._qScore.defaultCountChanged.emit(self._old)

class SetSystemSpacingCommand(_COMMAND_CLASS):
    def __init__(self, qScore, newSpacing):
        super(SetSystemSpacingCommand, self).__init__(qScore,
                                                      NotePosition(),
                                                      "Set System Spacing")
        self._new = newSpacing
        self._old = self._score.systemSpacing

    def _redo(self):
        self._score.systemSpacing = self._new
        self._qScore.displayProperties.lineSpacing = self._new - 101
        self._qScore.spacingChanged.emit(self._new)

    def _undo(self):
        self._score.systemSpacing = self._old
        self._qScore.displayProperties.lineSpacing = self._old - 101
        self._qScore.spacingChanged.emit(self._old)

class SetNoteFontSizeCommand(_COMMAND_CLASS):
    def __init__(self, qScore, newSize):
        super(SetNoteFontSizeCommand, self).__init__(qScore,
                                              NotePosition(),
                                              "Set note font size")
        self._newSize = newSize
        self._oldSize = self._qScore.displayProperties.noteFontSize

    def _redo(self):
        self._qScore.displayProperties.setNoteFontSize(self._newSize)

    def _undo(self):
        self._qScore.displayProperties.setNoteFontSize(self._oldSize)

class SetSectionFontSizeCommand(_COMMAND_CLASS):
    def __init__(self, qScore, newSize):
        super(SetSectionFontSizeCommand, self).__init__(qScore,
                                                        NotePosition(),
                                                        "Set section font size")
        self._newSize = newSize
        self._oldSize = self._qScore.displayProperties.sectionFontSize

    def _redo(self):
        self._qScore.displayProperties.sectionFontSize = self._newSize

    def _undo(self):
        self._qScore.displayProperties.sectionFontSize = self._oldSize

class SetMetadataFontSizeCommand(_COMMAND_CLASS):
    def __init__(self, qScore, newSize):
        super(SetMetadataFontSizeCommand, self).__init__(qScore,
                                                        NotePosition(),
                                                        "Set metadata font size")
        self._newSize = newSize
        self._oldSize = self._qScore.displayProperties.metadataFontSize

    def _redo(self):
        self._qScore.displayProperties.metadataFontSize = self._newSize

    def _undo(self):
        self._qScore.displayProperties.metadataFontSize = self._oldSize
