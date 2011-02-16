'''
Created on 13 Feb 2011

@author: Mike Thomas
'''
from PyQt4.QtGui import QUndoCommand
from Data import DBConstants
from Data.Score import Score
import copy

class ScoreCommand(QUndoCommand):
    def __init__(self, qScore, description):
        super(ScoreCommand, self).__init__(description)
        self._qScore = qScore
        self._score = self._qScore.score

class NoteCommand(ScoreCommand):
    def __init__(self, qScore, notePosition, head):
        super(NoteCommand, self).__init__(qScore, "Set note")
        self._oldHead = self._score.getNote(notePosition)
        self._np = notePosition
        self._head = head

    def undo(self):
        if self._oldHead == DBConstants.EMPTY_NOTE:
            self._score.deleteNote(self._np)
        else:
            self._score.addNote(self._np, self._oldHead)
        super(NoteCommand, self).undo()

class SetNote(NoteCommand):
    def redo(self):
        self._score.addNote(self._np, self._head)
        super(SetNote, self).redo()

class ToggleNote(NoteCommand):
    def redo(self):
        self._score.toggleNote(self._np, self._head)
        super(ToggleNote, self).redo()

class MetaDataCommand(ScoreCommand):
    def __init__(self, qScore, varName, setName, value):
        super(MetaDataCommand, self).__init__(qScore, "Edit metadata")
        self._oldValue = getattr(self._score.scoreData, varName)
        self._varname = varName
        self._setName = setName
        self._value = value

    def redo(self):
        setattr(self._score.scoreData, self._varname, self._value)
        for view in self._qScore.views():
            getattr(view, self._setName)(self._value)
        super(MetaDataCommand, self).redo()

    def undo(self):
        setattr(self._score.scoreData, self._varname, self._oldValue)
        for view in self._qScore.views():
            getattr(view, self._setName)(self._oldValue)
        super(MetaDataCommand, self).undo()

class ScoreWidthCommand(ScoreCommand):
    def __init__(self, qScore, value):
        super(ScoreWidthCommand, self).__init__(qScore, "Set Width")
        self._oldValue = self._score.scoreData.width
        self._value = value

    def redo(self):
        self._score.scoreData.width = self._value
        for view in self._qScore.views():
            view.setWidth(self._value)
        if self._score is not None:
            self._qScore.checkFormatting()

    def undo(self):
        self._score.scoreData.width = self._oldValue
        for view in self._qScore.views():
            view.setWidth(self._oldValue)
        if self._score is not None:
            self._qScore.checkFormatting()
        super(ScoreWidthCommand, self).undo()

class PasteMeasure(ScoreCommand):
    def __init__(self, qScore, notePosition, clipboard):
        super(PasteMeasure, self).__init__(qScore, "Paste Measure")
        self._np = notePosition
        self._measure = clipboard
        self._oldMeasure = None

    def redo(self):
        self._oldMeasure = self._score.pasteMeasure(self._np, self._measure)
        self._qScore.checkFormatting()

    def undo(self):
        self._score.pasteMeasure(self._np, self._oldMeasure)
        self._qScore.checkFormatting()

class RepeatNoteCommand(ScoreCommand):
    def __init__(self, qScore, notePosition, nRepeats, repInterval, head):
        super(RepeatNoteCommand, self).__init__(qScore, "Repeat Note")
        self._head = head
        np = copy.copy(notePosition)
        self._oldNotes = [(np, self._score.getNote(np))]
        for dummyIndex in range(nRepeats):
            np = copy.copy(np)
            np = self._score.notePlus(np, repInterval)
            self._oldNotes.append((np, self._score.getNote(np)))

    def redo(self):
        for np, dummyHead in self._oldNotes:
            self._score.addNote(np, self._head)

    def undo(self):
        for np, head in self._oldNotes:
            if head == DBConstants.EMPTY_NOTE:
                self._score.deleteNote(np)
            else:
                self._score.addNote(np, head)

class InsertMeasuresCommand(ScoreCommand):
    def __init__(self, qScore, notePosition, numMeasures, width, counter):
        super(InsertMeasuresCommand, self).__init__(qScore,
                                                    "Insert Measures")
        self._np = notePosition
        self._numMeasures = numMeasures
        self._width = width
        self._counter = counter

    def redo(self):
        for dummyMeasureIndex in range(self._numMeasures):
            self._score.insertMeasureByPosition(self._width, self._np,
                                                counter = self._counter)
        self._qScore.reBuild()

    def undo(self):
        for dummyMeasureIndex in range(self._numMeasures):
            self._score.deleteMeasureByPosition(self._np)
        self._qScore.reBuild()

class SetRepeatCountCommand(ScoreCommand):
    def __init__(self, qScore, notePosition, oldCount, newCount):
        super(SetRepeatCountCommand, self).__init__(qScore, "Set Repeat Count")
        self._oldCount = oldCount
        self._newCount = newCount
        self._np = notePosition

    def redo(self):
        measure = self._score.getItemAtPosition(self._np)
        measure.repeatCount = self._newCount

    def undo(self):
        measure = self._score.getItemAtPosition(self._np)
        measure.repeatCount = self._oldCount

class EditMeasurePropertiesCommand(ScoreCommand):
    def __init__(self, qScore, np, beats, newCounter):
        name = "Edit Measure Properties"
        super(EditMeasurePropertiesCommand, self).__init__(qScore,
                                                           name)
        self._np = np
        self._beats = beats
        self._newCounter = newCounter
        self._oldMeasure = self._score.copyMeasure(np)

    def redo(self):
        self._score.setMeasureBeatCount(self._np,
                                        self._beats, self._newCounter)
        self._qScore.reBuild()

    def undo(self):
        self._score.pasteMeasure(self._np, self._oldMeasure, True)
        self._qScore.reBuild()

class SetMeasureLineCommand(ScoreCommand):
    def __init__(self, qScore, descr, np, onOff, method):
        super(SetMeasureLineCommand, self).__init__(qScore, descr)
        self._np = np
        self._onOff = onOff
        self._method = method

    def redo(self):
        self._method(self._score, self._np, self._onOff)
        self._qScore.reBuild()

    def undo(self):
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

    def undo(self):
        super(SetSectionEndCommand, self).undo()
        if not self._onOff:
            self._score.setSectionTitle(self._index, self._title)

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

class DeleteMeasureCommand(ScoreCommand):
    def __init__(self, qScore, np):
        super(DeleteMeasureCommand, self).__init__(qScore, "Delete Measure")
        self._np = np
        self._oldMeasure = self._score.copyMeasure(np)
        self._sectionIndex = None
        self._sectionTitle = None
        if self._oldMeasure.isSectionEnd():
            self._sectionIndex = self._score.getSectionIndex(np)
            self._sectionTitle = self._score.getSectionTitle(self._sectionIndex)

    def redo(self):
        self._score.deleteMeasureByPosition(self._np)
        self._score.gridFormatScore(None)
        self._qScore.reBuild()

    def undo(self):
        self._score.insertMeasureByPosition(1, self._np)
        if self._sectionIndex is not None:
            self._score.setSectionEnd(self._np, True)
            self._score.setSectionTitle(self._sectionIndex,
                                        self._sectionTitle)
        self._score.pasteMeasure(self._np, self._oldMeasure, True)
        self._score.gridFormatScore(None)
        self._qScore.reBuild()
