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

from DBCommands import (ToggleNote, RepeatNoteCommand,
                        EditMeasurePropertiesCommand, SetRepeatCountCommand,
                        SetAlternateCommand)
from QMenuIgnoreCancelClick import QMenuIgnoreCancelClick
from QMeasureContextMenu import QMeasureContextMenu
from QMeasureLineContextMenu import QMeasureLineContextMenu
from QEditMeasureDialog import QEditMeasureDialog
from QRepeatCountDialog import QRepeatCountDialog
from QAlternateDialog import QAlternateDialog
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
        elif msgType == ChangeRepeatCount:
            return RepeatCountState(self.qscore, event.repeatCount,
                                    event.measurePosition)
        elif msgType == SetAlternateEvent:
            return SetAlternateState(self.qscore, event.alternateText,
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
        elif msgType == SetAlternateEvent:
            return SetAlternateState(self.qscore, event.alternateText,
                                     event.measurePosition)
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
        elif msgType == ChangeRepeatCount:
            return RepeatCountState(self.qscore, event.repeatCount,
                                    event.measurePosition)
        else:
            return self

class Playing(FsmState):
    def send(self, event):
        msgType = type(event)
        if msgType == StopPlaying:
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
        self.qscore.sendFsmEvent(MenuSelect())

    def _rejected(self):
        self.qscore.sendFsmEvent(MenuCancel())

    def send(self, event):
        msgType = type(event)
        if msgType == StartPlaying:
            self.dialog.reject()
            return Playing(self.qscore)
        elif msgType == MenuSelect:
            return Waiting(self.qscore)
        elif msgType == MenuCancel:
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
        super(EditMeasurePropertiesState, self)._accepted()

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
        super(RepeatCountState, self)._accepted()

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
        super(SetAlternateState, self)._accepted()
