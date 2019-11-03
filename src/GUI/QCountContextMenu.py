# Copyright 2014 Michael Thomas
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
Created on May 11, 2014

@author: Mike Thomas
'''
# import copy

from GUI.QMenuIgnoreCancelClick import QMenuIgnoreCancelClick
from GUI.DBCommands import (ChangeMeasureCountCommand,
                            ContractMeasureCountCommand,
                            ContractAllMeasureCountsCommand)
from Data.MeasureCount import makeSimpleCount
from GUI.DBFSMEvents import EditMeasureProperties


class QCountContextMenu(QMenuIgnoreCancelClick):
    def __init__(self, qScore, np, qmeasure):
        super(QCountContextMenu, self).__init__(qScore)
        self._np = np
        self._qmeasure = qmeasure
        self._measure = self._qScore.score.getMeasureByPosition(self._np)
        self._counter = self._measure.counter
        self._setup()

    def _setup(self):
        if not self._measure.simileDistance > 0:
            self.addAction("Edit Measure Count", self._editMeasureCount)
            measureMenu = self.addMenu("Measure Count")
            self._addCountActions(measureMenu, self._setMeasureCount)
            self.addSeparator()
            self.addSeparator()
            contractAction = self.addAction("Contract Count",
                                            self._contractCount)
            contractAction.setEnabled(
                self._measure.getSmallestSimpleCount() != None)
        self.addAction("Contract All Counts", self._contractAllCounts)

    def _addCountActions(self, menu, countFunction):
        for name, counter in self._qScore.displayProperties.counterRegistry:
            menu.addAction(name, lambda beat=counter: countFunction(beat))

    @QMenuIgnoreCancelClick.menuSelection
    def _setMeasureCount(self, newCounter):
        newMeasureCount = makeSimpleCount(newCounter,
                                          self._counter.numBeats())
        command = ChangeMeasureCountCommand(self._qScore, self._np,
                                            newMeasureCount)
        self._qScore.addCommand(command)

    @QMenuIgnoreCancelClick.menuSelection
    def _contractCount(self):
        command = ContractMeasureCountCommand(self._qScore, self._np)
        self._qScore.clearDragSelection()
        self._qScore.addCommand(command)

    @QMenuIgnoreCancelClick.menuSelection
    def _contractAllCounts(self):
        command = ContractAllMeasureCountsCommand(self._qScore, self._np)
        self._qScore.clearDragSelection()
        self._qScore.addCommand(command)

    def _editMeasureCount(self):
        fsmEvent = EditMeasureProperties(self._counter,
                                         self._props.counterRegistry,
                                         self._np)
        self._qScore.sendFsmEvent(fsmEvent)
