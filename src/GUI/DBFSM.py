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
from GUI.StateMachine import stateMachineClass, State
from GUI.DBCommands import (ToggleNote, RepeatNoteCommand,
                            ChangeMeasureCountCommand, SetRepeatCountCommand,
                            SetAlternateCommand)
from GUI.QMenuIgnoreCancelClick import QMenuIgnoreCancelClick
from GUI.QMeasureContextMenu import QMeasureContextMenu
from GUI.QMeasureLineContextMenu import QMeasureLineContextMenu
from GUI.QCountContextMenu import QCountContextMenu
from GUI.QEditMeasureDialog import QEditMeasureDialog
from GUI.QRepeatCountDialog import QRepeatCountDialog
from GUI.QAlternateDialog import QAlternateDialog
import GUI.DBFSMEvents as Event
from PyQt4 import QtCore

class DbState(State):
    @property
    def qscore(self):
        return self.machine.qscore

class DBStateMachine(stateMachineClass()):
    def __init__(self, initial_state, qscore):
        super(DBStateMachine, self).__init__(initial_state)
        self.qscore = qscore

    def setQscore(self, qscore):
        self.qscore = qscore

@DBStateMachine.add_state
class Waiting(DbState):
    def clearDrag(self, event_):
        self.qscore.clearDragSelection()

@DBStateMachine.add_state
class ButtonDown(DbState):
    def isSameNote(self, event):
        return event.note != self.event.note

    def release(self, event_):
        head = self.qscore.getCurrentHead()
        command = ToggleNote(self.qscore, self.event.note, head)
        self.qscore.addCommand(command)


@DBStateMachine.add_state
class Dragging(DbState):
    def initialize(self):
        self.dragging(self.event)

    def dragging(self, event):
        self.qscore.dragging(event.measure)

    def release(self, event_):
        self.qscore.endDragging()

    def cancel(self, event):
        self.release(event)
        self.qscore.clearDragSelection()

@DBStateMachine.add_state
class NotesMenu(DbState):
    def initialize(self):
        self.qscore.clearDragSelection()
        self.menu = QMenuIgnoreCancelClick(self.qscore)
        kit = self.qscore.score.drumKit
        for noteHead in kit.allowedNoteHeads(self.event.note.drumIndex):
            def noteAction(nh = noteHead):
                self.qscore.sendFsmEvent(Event.MenuSelect(nh))
            self.menu.addAction(noteHead, noteAction)
        QtCore.QTimer.singleShot(0,
                                 lambda: self.menu.exec_(self.event.screenPos))

    def select(self, event):
        command = ToggleNote(self.qscore, self.event.note, event.data)
        self.qscore.addCommand(command)

    def close(self, event_):
        self.menu.close()

@DBStateMachine.add_state
class ContextMenu(DbState):
    def initialize(self):
        if self.qscore.hasDragSelection():
            if not self.qscore.inDragSelection(self.event.note):
                self.qscore.clearDragSelection()
        self.menu = QMeasureContextMenu(self.qscore, self.event.measure,
                                        self.event.note,
                                        self.event.measure.alternateText())
        QtCore.QTimer.singleShot(0,
                                 lambda: self.menu.exec_(self.event.screenPos))

    def close(self, event_):
        self.menu.close()

@DBStateMachine.add_state
class Repeating(DbState):
    def initialize(self):
        self.qscore.clearDragSelection()
        self.statusBar = self.qscore.parent().statusBar()
        self.statusBar.showMessage("Drag from the first repeat "
                                   "of this note to the last "
                                   "(or press ESCAPE to cancel)", 0)

    def clear(self, event_):
        self.statusBar.clearMessage()

    def startRepeatDrag(self, event):
        if event.note is None:
            return self
        interval = self.qscore.score.tickDifference(event.note, self.event.note)
        if interval <= 0:
            self.statusBar.showMessage("Cannot repeat notes backwards!",
                                       5000)
            return Waiting(self.machine, None)
        head = self.qscore.score.getItemAtPosition(self.event.note)
        return RepeatingDragging(self.machine, event, self.event.note,
                                  interval, head)

@DBStateMachine.add_state
class RepeatingDragging(DbState):
    def __init__(self, machine, event, firstNote, interval, head):
        super(RepeatingDragging, self).__init__(machine, event)
        self.statusBar = self.qscore.parent().statusBar()
        self.statusBar.showMessage("Drag to the last repeat of this note "
                                   "(or press ESCAPE to cancel)", 0)
        self.firstNote = firstNote
        self.secondNote = event.note
        self._lastNote = event.note
        self.interval = interval
        self._notes = []
        self.score = self.qscore.score
        self._head = head
        self._makeNotePositions()

    def _makeNotePositions(self):
        note = self.secondNote.makeCopy()
        notes = [note]
        more = True
        while more:
            note = note.makeCopy()
            note = self.score.notePlus(note, self.interval)
            more = (note is not None and
                    ((note.staffIndex < self._lastNote.staffIndex) or
                    (note.staffIndex == self._lastNote.staffIndex
                     and note.measureIndex < self._lastNote.measureIndex) or
                    ((note.staffIndex == self._lastNote.staffIndex
                      and note.measureIndex == self._lastNote.measureIndex
                      and note.noteTime <= self._lastNote.noteTime))))
            if more:
                notes.append(note)
        if len(notes) != len(self._notes):
            self.qscore.setPotentialRepeatNotes(notes, self._head)
            self._notes = notes

    def move(self, event):
        if event.note is not None and event.note != self._lastNote:
            self._lastNote = event.note
            self._makeNotePositions()

    def cancel(self, event_):
        self.statusBar.clearMessage()
        self.qscore.setPotentialRepeatNotes([], None)

    def release(self, event_):
        self.qscore.setPotentialRepeatNotes([], None)
        if self._lastNote is not None:
            totalTicks = self.qscore.score.tickDifference(self._lastNote,
                                                          self.firstNote)
            numRepeats = totalTicks / self.interval
            if numRepeats <= 0:
                self.statusBar.showMessage("Must repeat note "
                                           "at least once!",
                                           5000)
            else:
                command = RepeatNoteCommand(self.qscore, self.firstNote,
                                            numRepeats, self.interval)
                self.qscore.addCommand(command)
        self.statusBar.clearMessage()


@DBStateMachine.add_state
class MeasureLineContextMenuState(DbState):
    def initialize(self):
        self.menu = QMeasureLineContextMenu(self.qscore,
                                            self.event.prevMeasure,
                                            self.event.nextMeasure,
                                            self.event.endNote,
                                            self.event.startNote)
        self.qscore.clearDragSelection()
        QtCore.QTimer.singleShot(0,
                                 lambda: self.menu.exec_(self.event.screenPos))

    def close(self, event_):
        self.menu.close()

@DBStateMachine.add_state
class MeasureCountContextMenuState(DbState):
    def initialize(self):
        self.menu = QCountContextMenu(self.qscore, self.event.note,
                                      self.event.measure)
        self.qscore.clearDragSelection()
        QtCore.QTimer.singleShot(0,
                                 lambda: self.menu.exec_(self.event.screenPos))

    def close(self, event_):
        self.menu.close()

@DBStateMachine.add_state
class Playing(DbState):
    def initialize(self):
        self.qscore.playing.emit(True)

    def stop(self, event_):
        self.qscore.playing.emit(False)

class DialogState_(DbState):
    def __init__(self, machine, event):
        super(DialogState_, self).__init__(machine, event)
        self.dialog = self.makeDialog()
        self.dialog.accepted.connect(self._accepted)
        self.dialog.rejected.connect(self._rejected)
        QtCore.QTimer.singleShot(0, self.dialog.exec_)

    def makeDialog(self):
        raise NotImplementedError()

    def _accepted(self):
        self.qscore.sendFsmEvent(Event.MenuSelect())

    def _rejected(self):
        self.qscore.sendFsmEvent(Event.MenuCancel())

    def reject(self, event_):
        self.dialog.reject()

@DBStateMachine.add_state
class EditMeasurePropertiesState(DialogState_):
    def makeDialog(self):
        return QEditMeasureDialog(self.event.counter,
                                  self.qscore.defaultCount,
                                  self.event.counterRegistry,
                                  self.qscore.parent())


    def _accepted(self):
        newCounter = self.dialog.getValues()
        if newCounter.countString() != self.event.counter.countString():
            command = ChangeMeasureCountCommand(self.qscore,
                                                self.event.measurePosition,
                                                newCounter)
            self.qscore.clearDragSelection()
            self.qscore.addCommand(command)
        super(EditMeasurePropertiesState, self)._accepted()  # IGNORE:W0212

@DBStateMachine.add_state
class RepeatCountState(DialogState_):
    def makeDialog(self):
        return QRepeatCountDialog(self.event.repeatCount,
                                  self.qscore.parent())

    def _accepted(self):
        newCount = self.dialog.getValue()
        if self.event.repeatCount != newCount:
            command = SetRepeatCountCommand(self.qscore,
                                            self.event.measurePosition,
                                            self.event.repeatCount,
                                            newCount)
            self.qscore.addCommand(command)
        super(RepeatCountState, self)._accepted()  # IGNORE:W0212

@DBStateMachine.add_state
class SetAlternateState(DialogState_):
    def makeDialog(self):
        return QAlternateDialog(self.event.alternateText, self.qscore.parent())

    def _accepted(self):
        newText = self.dialog.getValue()
        if self.event.alternateText != newText:
            command = SetAlternateCommand(self.qscore,
                                          self.event.measurePosition,
                                          newText)
            self.qscore.addCommand(command)
        super(SetAlternateState, self)._accepted()  # IGNORE:W0212

DBStateMachine.add_transition(Waiting, Event.Escape, Waiting,
                              Waiting.clearDrag)
DBStateMachine.add_transition(Waiting, Event.LeftPress, ButtonDown,
                              Waiting.clearDrag,
                              lambda state_, event: event.note is not None)
DBStateMachine.add_transition(Waiting, Event.MidPress, NotesMenu)
DBStateMachine.add_transition(Waiting, Event.RightPress, ContextMenu)
DBStateMachine.add_transition(Waiting, Event.MeasureLineContext,
                              MeasureLineContextMenuState)
DBStateMachine.add_transition(Waiting, Event.MeasureCountContext,
                              MeasureCountContextMenuState)
DBStateMachine.add_transition(Waiting, Event.StartPlaying, Playing)
DBStateMachine.add_transition(Waiting, Event.EditMeasureProperties,
                              EditMeasurePropertiesState)
DBStateMachine.add_transition(Waiting, Event.ChangeRepeatCount,
                              RepeatCountState)
DBStateMachine.add_transition(Waiting, Event.SetAlternateEvent,
                              SetAlternateState)

DBStateMachine.add_transition(ButtonDown, Event.MouseMove, Dragging,
                              guard = ButtonDown.isSameNote)
DBStateMachine.add_transition(ButtonDown, Event.MouseRelease, Waiting,
                              ButtonDown.release)
DBStateMachine.add_transition(ButtonDown, Event.StartPlaying, Playing)
DBStateMachine.add_transition(ButtonDown, Event.Escape, Waiting)


DBStateMachine.add_transition(Dragging, Event.MouseMove, Dragging,
                              Dragging.dragging)
DBStateMachine.add_transition(Dragging, Event.MouseRelease, Waiting,
                              Dragging.release)
DBStateMachine.add_transition(Dragging, Event.StartPlaying, Playing)
DBStateMachine.add_transition(Dragging, Event.Escape, Waiting,
                              Dragging.cancel)


DBStateMachine.add_transition(NotesMenu, Event.MenuSelect, Waiting,
                              NotesMenu.select)
DBStateMachine.add_transition(NotesMenu, Event.MenuCancel, Waiting)
DBStateMachine.add_transition(NotesMenu, Event.Escape, Waiting,
                              NotesMenu.close)
DBStateMachine.add_transition(NotesMenu, Event.StartPlaying, Playing,
                              NotesMenu.close)


DBStateMachine.add_transition(ContextMenu, Event.MenuSelect, Waiting)
DBStateMachine.add_transition(ContextMenu, Event.MenuCancel, Waiting)
DBStateMachine.add_transition(ContextMenu, Event.Escape, Waiting,
                              ContextMenu.close)
DBStateMachine.add_transition(ContextMenu, Event.RepeatNotes, Repeating)
DBStateMachine.add_transition(ContextMenu, Event.StartPlaying, Playing,
                              ContextMenu.close)
DBStateMachine.add_transition(ContextMenu, Event.SetAlternateEvent,
                              SetAlternateState)

DBStateMachine.add_factory_transition(Repeating, Event.LeftPress,
                                      Repeating.startRepeatDrag)
DBStateMachine.add_transition(Repeating, Event.Escape, Waiting,
                              Repeating.clear)
DBStateMachine.add_transition(Repeating, Event.StartPlaying, Playing,
                              Repeating.clear)

DBStateMachine.add_transition(RepeatingDragging, Event.MouseRelease, Waiting,
                                  RepeatingDragging.release)
DBStateMachine.add_transition(RepeatingDragging, Event.MouseMove, Waiting,
                              RepeatingDragging.move,
                              lambda state, event: False)
DBStateMachine.add_transition(RepeatingDragging, Event.Escape, Waiting,
                              RepeatingDragging.cancel)
DBStateMachine.add_transition(RepeatingDragging, Event.StartPlaying, Playing,
                              RepeatingDragging.cancel)


DBStateMachine.add_transition(MeasureLineContextMenuState, Event.MenuSelect,
                              Waiting)
DBStateMachine.add_transition(MeasureLineContextMenuState, Event.MenuCancel,
                              Waiting, MeasureLineContextMenuState.close)
DBStateMachine.add_transition(MeasureLineContextMenuState, Event.Escape,
                              Waiting, MeasureLineContextMenuState.close)
DBStateMachine.add_transition(MeasureLineContextMenuState, Event.StartPlaying,
                              Playing, MeasureLineContextMenuState.close)
DBStateMachine.add_transition(MeasureLineContextMenuState,
                              Event.ChangeRepeatCount, RepeatCountState)

DBStateMachine.add_transition(MeasureCountContextMenuState, Event.Escape,
                              Waiting, MeasureCountContextMenuState.close)
DBStateMachine.add_transition(MeasureCountContextMenuState, Event.MenuSelect,
                              Waiting)
DBStateMachine.add_transition(MeasureCountContextMenuState, Event.MenuCancel,
                              Waiting, MeasureCountContextMenuState.close)
DBStateMachine.add_transition(MeasureCountContextMenuState,
                              Event.EditMeasureProperties,
                              EditMeasurePropertiesState)


DBStateMachine.add_transition(Playing, Event.StopPlaying, Waiting, Playing.stop)

DBStateMachine.add_transition(EditMeasurePropertiesState, Event.StartPlaying,
                              Playing, DialogState_.reject)
DBStateMachine.add_transition(EditMeasurePropertiesState, Event.MenuSelect,
                              Waiting)
DBStateMachine.add_transition(EditMeasurePropertiesState, Event.MenuCancel,
                              Waiting)

DBStateMachine.add_transition(RepeatCountState, Event.StartPlaying, Playing,
                              DialogState_.reject)
DBStateMachine.add_transition(RepeatCountState, Event.MenuSelect, Waiting)
DBStateMachine.add_transition(RepeatCountState, Event.MenuCancel, Waiting)

DBStateMachine.add_transition(SetAlternateState, Event.StartPlaying, Playing,
                              DialogState_.reject)
DBStateMachine.add_transition(SetAlternateState, Event.MenuSelect, Waiting)
DBStateMachine.add_transition(SetAlternateState, Event.MenuCancel, Waiting)

