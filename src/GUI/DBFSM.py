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
'''Created on Feb 26, 2012

@author: Mike
'''
import copy

from DBCommands import (ToggleNote, RepeatNoteCommand,
                        EditMeasurePropertiesCommand, SetRepeatCountCommand,
                        SetAlternateCommand)
from QMenuIgnoreCancelClick import QMenuIgnoreCancelClick
from QMeasureContextMenu import QMeasureContextMenu
from QMeasureLineContextMenu import QMeasureLineContextMenu
from QEditMeasureDialog import QEditMeasureDialog
from QRepeatCountDialog import QRepeatCountDialog
from QAlternateDialog import QAlternateDialog
import DBFSMEvents as Event
from PyQt4 import QtCore

class FsmState(object):
    def __init__(self, qscore):
        self.qscore = qscore

    def send(self, event_):
        # Ignore this event
        return self

class Waiting(FsmState):
    def send(self, event):
        msgType = type(event)
        newState = self
        if msgType == Event.Escape:
            self.qscore.clearDragSelection()
        elif msgType == Event.LeftPress:
            self.qscore.clearDragSelection()
            if event.note is not None:
                newState = ButtonDown(self.qscore, event.measure, event.note)
        elif msgType == Event.MidPress:
            newState = NotesMenu(self.qscore, event.note, event.screenPos)
        elif msgType == Event.RightPress:
            newState = ContextMenu(self.qscore, event.measure,
                                   event.note, event.screenPos)
        elif msgType == Event.MeasureLineContext:
            newState = MeasureLineContextMenuState(self.qscore,
                                                   event.prevMeasure,
                                                   event.nextMeasure,
                                                   event.endNote,
                                                   event.startNote,
                                                   event.screenPos)
        elif msgType == Event.StartPlaying:
            newState = Playing(self.qscore)
        elif msgType == Event.EditMeasureProperties:
            newState = EditMeasurePropertiesState(self.qscore,
                                              event.counter,
                                              event.counterRegistry,
                                              event.measurePosition)
        elif msgType == Event.ChangeRepeatCount:
            newState = RepeatCountState(self.qscore, event.repeatCount,
                                        event.measurePosition)
        elif msgType == Event.SetAlternateEvent:
            newState = SetAlternateState(self.qscore, event.alternateText,
                                         event.measurePosition)
        return newState

class ButtonDown(FsmState):
    def __init__(self, qscore, measure, note):
        super(ButtonDown, self).__init__(qscore)
        qscore.clearDragSelection()
        self.measure = measure
        self.note = note

    def send(self, event):
        msgType = type(event)
        if msgType == Event.MouseMove:
            if event.note != self.note:
                return Dragging(self.qscore, event.measure)
            else:
                return self
        elif msgType == Event.MouseRelease:
            command = ToggleNote(self.qscore, self.note)
            self.qscore.addCommand(command)
            return Waiting(self.qscore)
        elif msgType == Event.StartPlaying:
            return Playing(self.qscore)
        else:
            return self

class Dragging(FsmState):
    def __init__(self, qscore, measure):
        super(Dragging, self).__init__(qscore)
        self.qscore.dragging(measure)

    def send(self, event):
        msgType = type(event)
        if msgType == Event.MouseMove:
            self.qscore.dragging(event.measure)
            return self
        elif msgType == Event.MouseRelease:
            self.qscore.endDragging()
            return Waiting(self.qscore)
        elif msgType == Event.StartPlaying:
            return Playing(self.qscore)
        else:
            return self


class NotesMenu(FsmState):
    def __init__(self, qscore, note, screenPos):
        super(NotesMenu, self).__init__(qscore)
        self.note = note
        qscore.clearDragSelection()
        self.menu = QMenuIgnoreCancelClick(qscore)
        kit = qscore.score.drumKit
        for noteHead in kit.allowedNoteHeads(note.drumIndex):
            def noteAction(nh = noteHead):
                qscore.sendFsmEvent(Event.MenuSelect(nh))
            self.menu.addAction(noteHead, noteAction)
        QtCore.QTimer.singleShot(0, lambda: self.menu.exec_(screenPos))

    def send(self, event):
        msgType = type(event)
        if msgType == Event.MenuSelect:
            command = ToggleNote(self.qscore, self.note, event.data)
            self.qscore.addCommand(command)
            return Waiting(self.qscore)
        elif msgType == Event.MenuCancel:
            return Waiting(self.qscore)
        elif msgType == Event.Escape:
            self.menu.close()
            return Waiting(self.qscore)
        elif msgType == Event.StartPlaying:
            self.menu.close()
            return Playing(self.qscore)
        else:
            return self


class ContextMenu(FsmState):
    def __init__(self, qscore, measure, note, screenPos):
        super(ContextMenu, self).__init__(qscore)
        if qscore.hasDragSelection():
            if not qscore.inDragSelection(note):
                qscore.clearDragSelection()
        self.menu = QMeasureContextMenu(qscore, measure, note,
                                        measure.noteAt(note),
                                        measure.alternateText())
        self.measure = measure
        self.note = note
        QtCore.QTimer.singleShot(0, lambda: self.menu.exec_(screenPos))


    def send(self, event):
        msgType = type(event)
        newState = self
        if msgType == Event.MenuSelect:
            newState = Waiting(self.qscore)
        elif msgType == Event.MenuCancel:
            newState = Waiting(self.qscore)
        elif msgType == Event.Escape:
            self.menu.close()
            newState = Waiting(self.qscore)
        elif msgType == Event.RepeatNotes:
            newState = Repeating(self.qscore, self.note)
        elif msgType == Event.StartPlaying:
            self.menu.close()
            newState = Playing(self.qscore)
        elif msgType == Event.SetAlternateEvent:
            newState = SetAlternateState(self.qscore, event.alternateText,
                                     event.measurePosition)
        return newState

class Repeating(FsmState):
    def __init__(self, qscore, note):
        super(Repeating, self).__init__(qscore)
        self.qscore.clearDragSelection()
        self.statusBar = qscore.parent().statusBar()
        self.statusBar.showMessage("Drag from the first repeat "
                                   "of this note to the last "
                                   "(or press ESCAPE to cancel)", 0)
        self.note = note

    def send(self, event):
        msgType = type(event)
        if msgType == Event.LeftPress:
            if event.note is None:
                return self
            interval = self.qscore.score.tickDifference(event.note, self.note)
            if interval <= 0:
                self.statusBar.showMessage("Cannot repeat notes backwards!",
                                           5000)
                return Waiting(self.qscore)
            head = self.qscore.score.getNote(self.note)
            return RepeatingDragging(self.qscore, self.note,
                                     event.note, interval, head)
        elif msgType == Event.Escape:
            self.statusBar.clearMessage()
            return Waiting(self.qscore)
        elif msgType == Event.StartPlaying:
            self.statusBar.clearMessage()
            return Playing(self.qscore)
        else:
            return self

class RepeatingDragging(FsmState):
    def __init__(self, qscore, firstNote, secondNote, interval, head):
        super(RepeatingDragging, self).__init__(qscore)
        self.statusBar = qscore.parent().statusBar()
        self.statusBar.showMessage("Drag to the last repeat of this note "
                                   "(or press ESCAPE to cancel)", 0)
        self.firstNote = firstNote
        self.secondNote = secondNote
        self._lastNote = secondNote
        self.interval = interval
        self._notes = []
        self.score = self.qscore.score
        self._head = head
        self._makeNotePositions()

    def send(self, event):
        msgType = type(event)
        if msgType == Event.MouseRelease:
            self.qscore.setPotentialRepeatNotes([], None)
            if self._lastNote is not None:
                totalTicks = self.qscore.score.tickDifference(self._lastNote,
                                                              self.firstNote)
                numRepeats = totalTicks / self.interval
                if numRepeats <= 0:
                    self.statusBar.showMessage("Must repeat note "
                                               "at least once!",
                                               5000)
                    return Waiting(self.qscore)
                command = RepeatNoteCommand(self.qscore, self.firstNote,
                                            numRepeats, self.interval)
                self.qscore.addCommand(command)
            self.statusBar.clearMessage()
            return Waiting(self.qscore)
        elif msgType == Event.MouseMove:
            if event.note is not None and event.note != self._lastNote:
                self._lastNote = event.note
                self._makeNotePositions()
            return self
        elif msgType == Event.Escape:
            self.statusBar.clearMessage()
            self.qscore.setPotentialRepeatNotes([], None)
            return Waiting(self.qscore)
        elif msgType == Event.StartPlaying:
            self.statusBar.clearMessage()
            self.qscore.setPotentialRepeatNotes([], None)
            return Playing(self.qscore)
        else:
            return self

    def _makeNotePositions(self):
        note = copy.copy(self.secondNote)
        notes = [note]
        more = True
        while more:
            note = copy.copy(note)
            note = self.score.notePlus(note, self.interval)
            more = ((note.staffIndex < self._lastNote.staffIndex) or
                    (note.staffIndex == self._lastNote.staffIndex
                     and note.measureIndex < self._lastNote.measureIndex) or
                    ((note.staffIndex == self._lastNote.staffIndex
                      and note.measureIndex == self._lastNote.measureIndex
                      and note.noteTime <= self._lastNote.noteTime)))
            if more:
                notes.append(note)


        if len(notes) != len(self._notes):
            self.qscore.setPotentialRepeatNotes(notes, self._head)
            self._notes = notes

class MeasureLineContextMenuState(FsmState):
    def __init__(self, qscore, prevMeasure, nextMeasure,
                 endNote, startNote, screenPos):
        super(MeasureLineContextMenuState, self).__init__(qscore)
        self.menu = QMeasureLineContextMenu(qscore, prevMeasure, nextMeasure,
                                            endNote, startNote)
        QtCore.QTimer.singleShot(0, lambda: self.menu.exec_(screenPos))

    def send(self, event):
        msgType = type(event)
        if msgType == Event.MenuSelect:
            return Waiting(self.qscore)
        elif msgType == Event.MenuCancel:
            return Waiting(self.qscore)
        elif msgType == Event.Escape:
            self.menu.close()
            return Waiting(self.qscore)
        elif msgType == Event.StartPlaying:
            self.menu.close()
            return Playing(self.qscore)
        elif msgType == Event.ChangeRepeatCount:
            return RepeatCountState(self.qscore, event.repeatCount,
                                    event.measurePosition)
        else:
            return self

class Playing(FsmState):
    def __init__(self, qscore):
        super(Playing, self).__init__(qscore)
        self.qscore.playing.emit(True)
    def send(self, event):
        msgType = type(event)
        if msgType == Event.StopPlaying:
            self.qscore.playing.emit(False)
            return Waiting(self.qscore)
        else:
            return self

class DialogState(FsmState):
    def __init__(self, qscore, measurePosition):
        super(DialogState, self).__init__(qscore)
        self.measurePosition = measurePosition
        self.dialog = None

    def setupDialog(self, dialog):
        self.dialog = dialog
        self.dialog.accepted.connect(self._accepted)
        self.dialog.rejected.connect(self._rejected)
        QtCore.QTimer.singleShot(0, self.dialog.exec_)

    def _accepted(self):
        self.qscore.sendFsmEvent(Event.MenuSelect())

    def _rejected(self):
        self.qscore.sendFsmEvent(Event.MenuCancel())

    def send(self, event):
        msgType = type(event)
        if msgType == Event.StartPlaying:
            self.dialog.reject()
            return Playing(self.qscore)
        elif msgType == Event.MenuSelect:
            return Waiting(self.qscore)
        elif msgType == Event.MenuCancel:
            return Waiting(self.qscore)
        else:
            return self

class EditMeasurePropertiesState(DialogState):
    def __init__(self, qscore, counter, counterRegistry, measurePosition):
        super(EditMeasurePropertiesState, self).__init__(qscore,
                                                         measurePosition)
        self.counter = counter
        defCounter = qscore.defaultCount
        dialog = QEditMeasureDialog(counter, defCounter,
                                    counterRegistry, qscore.parent())
        self.setupDialog(dialog)

    def _accepted(self):
        newCounter = self.dialog.getValues()
        if (newCounter.countString() != self.counter.countString()):
            command = EditMeasurePropertiesCommand(self.qscore,
                                                   self.measurePosition,
                                                   newCounter)
            self.qscore.addCommand(command)
        super(EditMeasurePropertiesState, self)._accepted() #IGNORE:W0212

class RepeatCountState(DialogState):
    def __init__(self, qscore, repeatCount, position):
        super(RepeatCountState, self).__init__(qscore, position)
        self.oldCount = repeatCount
        dialog = QRepeatCountDialog(self.oldCount, qscore.parent())
        self.setupDialog(dialog)

    def _accepted(self):
        newCount = self.dialog.getValue()
        if self.oldCount != newCount:
            command = SetRepeatCountCommand(self.qscore,
                                            self.measurePosition,
                                            self.oldCount,
                                            newCount)
            self.qscore.addCommand(command)
        super(RepeatCountState, self)._accepted() #IGNORE:W0212

class SetAlternateState(DialogState):
    def __init__(self, qscore, alternateText, position):
        super(SetAlternateState, self).__init__(qscore, position)
        self.oldText = alternateText
        altDialog = QAlternateDialog(alternateText, qscore.parent())
        self.setupDialog(altDialog)

    def _accepted(self):
        newText = self.dialog.getValue()
        if self.oldText != newText:
            command = SetAlternateCommand(self.qscore, self.measurePosition,
                                          newText)
            self.qscore.addCommand(command)
        super(SetAlternateState, self)._accepted() #IGNORE:W0212
