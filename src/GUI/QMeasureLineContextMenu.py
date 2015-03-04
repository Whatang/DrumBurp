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
'''
Created on Feb 26, 2012

@author: Mike
'''

from GUI.QMenuIgnoreCancelClick import QMenuIgnoreCancelClick
from GUI.DBCommands import (SetSectionEndCommand, SetLineBreakCommand,
                            SetRepeatEndCommand, SetRepeatStartCommand)
from GUI.DBFSMEvents import MenuSelect, ChangeRepeatCount

class QMeasureLineContextMenu(QMenuIgnoreCancelClick):
    def __init__(self, qScore, lastMeasure, nextMeasure,
                 endNotePosition, startNotePosition):
        super(QMeasureLineContextMenu, self).__init__(qScore)
        self._endNotePosition = endNotePosition
        self._startNotePosition = startNotePosition
        self._lastMeasure = lastMeasure
        # Repeat Start
        if nextMeasure is not None:
            onOff = nextMeasure.isRepeatStart()
            setIt = lambda v = onOff : self._setRepeatStart(not v)
            repeatStartAction = self.addAction("Repeat Start",
                                               setIt)
            repeatStartAction.setCheckable(True)
            repeatStartAction.setChecked(onOff)
        if lastMeasure is not None:
            # Repeat End
            onOff = lastMeasure.isRepeatEnd()
            setIt = lambda v = onOff:self._setRepeatEnd(not v)
            repeatEndAction = self.addAction("Repeat End",
                                             setIt)
            repeatEndAction.setCheckable(True)
            repeatEndAction.setChecked(onOff)
            # Section Ending
            onOff = lastMeasure.isSectionEnd()
            setIt = lambda v = onOff:self._setSectionEnd(not v)
            sectionEndAction = self.addAction("Section End",
                                              setIt)
            sectionEndAction.setCheckable(True)
            sectionEndAction.setChecked(onOff)
            # Line break
            onOff = lastMeasure.isLineBreak()
            setIt = lambda v = onOff:self._setLineBreak(not v)
            lineBreakAction = self.addAction("Line Break",
                                             setIt)
            lineBreakAction.setCheckable(True)
            lineBreakAction.setChecked(onOff)
            self.addSeparator()
            # Repeat count
            repeatCountAction = self.addAction("Set repeat count",
                                               self._setRepeatCount)
            repeatCountAction.setEnabled(lastMeasure.isRepeatEnd())

    def _setSectionEnd(self, onOff):
        command = SetSectionEndCommand(self._qScore,
                                       self._endNotePosition,
                                       onOff)
        self._qScore.clearDragSelection()
        self._qScore.addCommand(command)
        self._qScore.sendFsmEvent(MenuSelect())

    def _setLineBreak(self, onOff):
        command = SetLineBreakCommand(self._qScore,
                                      self._endNotePosition,
                                      onOff)
        self._qScore.clearDragSelection()
        self._qScore.addCommand(command)
        self._qScore.sendFsmEvent(MenuSelect())

    def _setRepeatEnd(self, onOff):
        command = SetRepeatEndCommand(self._qScore,
                                      self._endNotePosition,
                                      onOff)
        self._qScore.clearDragSelection()
        self._qScore.addCommand(command)
        self._qScore.sendFsmEvent(MenuSelect())


    def _setRepeatStart(self, onOff):
        command = SetRepeatStartCommand(self._qScore,
                                        self._startNotePosition,
                                        onOff)
        self._qScore.clearDragSelection()
        self._qScore.addCommand(command)
        self._qScore.sendFsmEvent(MenuSelect())

    def _setRepeatCount(self):
        fsmEvent = ChangeRepeatCount(self._lastMeasure.repeatCount,
                                     self._endNotePosition)
        self._qScore.sendFsmEvent(fsmEvent)
