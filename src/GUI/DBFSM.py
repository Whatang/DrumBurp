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
from PyQt4 import QtCore

from DBCommands import ToggleNote, RepeatNoteCommand, EditMeasurePropertiesCommand
from QMenuIgnoreCancelClick import QMenuIgnoreCancelClick
from QMeasureContextMenu import QMeasureContextMenu
from QMeasureLineContextMenu import QMeasureLineContextMenu
from QEditMeasureDialog import QEditMeasureDialog
from DBFSMEvents import *

class FsmState(object):
    def __init__(self, qscore):
        self.qscore = qscore

    def send(self, event_):
        # Ignore this event
        return self

class Waiting(FsmState):
    def send(self, event):
        msgType = type(event)
        if msgType == Escape:
            self.qscore.clearDragSelection()
            return self
        elif msgType == LeftPress:
            self.qscore.clearDragSelection()
            if event.note is not None:
                return ButtonDown(self.qscore, event.measure, event.note)
            else:
                return self
        elif msgType == MidPress:
            return NotesMenu(self.qscore, event.note, event.screenPos)
        elif msgType == RightPress:
            return ContextMenu(self.qscore, event.measure, event.note, event.screenPos)
        elif msgType == MeasureLineContext:
            return MeasureLineContextMenuState(self.qscore,
                                               event.prevMeasure, event.nextMeasure,
                                               event.endNote, event.startNote,
                                               event.screenPos)
        elif msgType == StartPlaying:
            return Playing(self.qscore)
        elif msgType == EditMeasureProperties:
            return EditMeasurePropertiesState(self.qscore,
                                              event.counter, event.counterRegistry,
                                              event.measurePosition)
        else:
            return self

class ButtonDown(FsmState):
    def __init__(self, qscore, measure, note):
        super(ButtonDown, self).__init__(qscore)
        qscore.clearDragSelection()
        self.measure = measure
        self.note = note

    def send(self, event):
        msgType = type(event)
        if msgType == MouseMove:
            if event.note != self.note:
                return Dragging(self.qscore, event.measure)
            else:
                return self
        elif msgType == MouseRelease:
            command = ToggleNote(self.qscore, self.note)
            self.qscore.addCommand(command)
            return Waiting(self.qscore)
        elif msgType == StartPlaying:
            return Playing(self.qscore)
        else:
            return self

class Dragging(FsmState):
    def __init__(self, qscore, measure):
        super(Dragging, self).__init__(qscore)
        self.qscore.dragging(measure)

    def send(self, event):
        msgType = type(event)
        if msgType == MouseMove:
            self.qscore.dragging(event.measure)
            return self
        elif msgType == MouseRelease:
            self.qscore.endDragging()
            return Waiting(self.qscore)
        elif msgType == StartPlaying:
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
                qscore.sendFsmEvent(MenuSelect(nh))
            self.menu.addAction(noteHead, noteAction)
        QtCore.QTimer.singleShot(0, lambda: self.menu.exec_(screenPos))

    def send(self, event):
        msgType = type(event)
        if msgType == MenuSelect:
            command = ToggleNote(self.qscore, self.note, event.data)
            self.qscore.addCommand(command)
            return Waiting(self.qscore)
        elif msgType == MenuCancel:
            return Waiting(self.qscore)
        elif msgType == Escape:
            self.menu.close()
            return Waiting(self.qscore)
        elif msgType == StartPlaying:
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
        if msgType == MenuSelect:
            return Waiting(self.qscore)
        elif msgType == MenuCancel:
            return Waiting(self.qscore)
        elif msgType == Escape:
            self.menu.close()
            return Waiting(self.qscore)
        elif msgType == RepeatNotes:
            return Repeating(self.qscore, self.note)
        elif msgType == StartPlaying:
            self.menu.close()
            return Playing(self.qscore)
        else:
            return self

class Repeating(FsmState):
    def __init__(self, qscore, note):
        super(Repeating, self).__init__(qscore)
        self.statusBar = qscore.parent().statusBar()
        self.statusBar.showMessage("Place the first repeat of this note "
                                   "(or press ESCAPE to cancel)", 0)
        self.note = note

    def send(self, event):
        msgType = type(event)
        if msgType == MouseRelease:
            if event.note is None:
                return self
            interval = self.qscore.score.tickDifference(event.note, self.note)
            if interval <= 0:
                self.statusBar.showMessage("Cannot repeat notes backwards!",
                                           5000)
                return Waiting(self.qscore)
            return RepeatingSecond(self.qscore, self.note, interval)
        elif msgType == Escape:
            self.statusBar.clearMessage()
            return Waiting(self.qscore)
        elif msgType == StartPlaying:
            self.statusBar.clearMessage()
            return Playing(self.qscore)
        else:
            return self

class RepeatingSecond(FsmState):
    def __init__(self, qscore, firstNote, interval):
        super(RepeatingSecond, self).__init__(qscore)
        self.statusBar = qscore.parent().statusBar()
        self.statusBar.showMessage("Place the last repeat of this note "
                                   "(or press ESCAPE to cancel)", 0)
        self.firstNote = firstNote
        self.interval = interval

    def send(self, event):
        msgType = type(event)
        if msgType == MouseRelease:
            if event.note is None:
                return self
            totalTicks = self.qscore.score.tickDifference(event.note, self.firstNote)
            numRepeats = totalTicks / self.interval
            if numRepeats <= 0:
                self.statusBar.showMessage("Must repeat note at least once!",
                                           5000)
                return Waiting(self.qscore)
            command = RepeatNoteCommand(self.qscore, self.firstNote,
                                        numRepeats, self.interval)
            self.qscore.addCommand(command)
            self.statusBar.clearMessage()
            return Waiting(self.qscore)
        elif msgType == Escape:
            self.statusBar.clearMessage()
            return Waiting(self.qscore)
        elif msgType == StartPlaying:
            self.statusBar.clearMessage()
            return Playing(self.qscore)
        else:
            return self

class MeasureLineContextMenuState(FsmState):
    def __init__(self, qscore, prevMeasure, nextMeasure,
                 endNote, startNote, screenPos):
        super(MeasureLineContextMenuState, self).__init__(qscore)
        self.menu = QMeasureLineContextMenu(qscore, prevMeasure, nextMeasure,
                                            endNote, startNote)
        QtCore.QTimer.singleShot(0, lambda: self.menu.exec_(screenPos))

    def send(self, event):
        msgType = type(event)
        if msgType == MenuSelect:
            return Waiting(self.qscore)
        elif msgType == MenuCancel:
            return Waiting(self.qscore)
        elif msgType == Escape:
            self.menu.close()
            return Waiting(self.qscore)
        elif msgType == StartPlaying:
            self.menu.close()
            return Playing(self.qscore)
        else:
            return self

class Playing(FsmState):
    def send(self, event):
        msgType = type(event)
        if msgType == StopPlaying:
            return Waiting(self.qscore)
        else:
            return self

class EditMeasurePropertiesState(FsmState):
    def __init__(self, qscore, counter, counterRegistry, measurePosition):
        super(EditMeasurePropertiesState, self).__init__(qscore)
        self.counter = counter
        self.measurePosition = measurePosition
        defCounter = qscore.defaultCount
        self.editDialog = QEditMeasureDialog(counter,
                                             defCounter,
                                             counterRegistry,
                                             qscore.parent())
        self.editDialog.accepted.connect(self._accepted)
        self.editDialog.rejected.connect(self._rejected)
        QtCore.QTimer.singleShot(0, self.editDialog.exec_)

    def _accepted(self):
        newCounter = self.editDialog.getValues()
        if (newCounter.countString() != self.counter.countString()):
            command = EditMeasurePropertiesCommand(self.qscore,
                                                   self.measurePosition,
                                                   newCounter)
            self.qscore.addCommand(command)
        self.qscore.sendFsmEvent(MenuSelect())

    def _rejected(self):
        self.qscore.sendFsmEvent(MenuSelect())

    def send(self, event):
        msgType = type(event)
        if msgType == StartPlaying:
            self.editDialog.reject()
            return Playing(self.qscore)
        elif msgType == MenuSelect:
            return Waiting(self.qscore)
        else:
            return self


