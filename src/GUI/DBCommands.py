'''
Created on 13 Feb 2011

@author: Mike Thomas
'''
from PyQt4.QtGui import QUndoCommand
from Data import DBConstants

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
