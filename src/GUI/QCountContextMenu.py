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
from GUI.DBCommands import ChangeMeasureCountCommand
from Data.MeasureCount import makeSimpleCount
# from Data.Beat import Beat

class QCountContextMenu(QMenuIgnoreCancelClick):
    def __init__(self, qScore, np, qmeasure):
        '''
        Constructor
        '''
        super(QCountContextMenu, self).__init__(qScore)
        self._np = np
        self._qmeasure = qmeasure
        self._measurePos = self._qmeasure.measurePosition()
        self._measure = self._qScore.score.getItemAtPosition(self._measurePos)
        self._counter = self._measure.counter
        self._setup()

    def _setup(self):
        # beatMenu = self.addMenu("Beat Count")
        measureMenu = self.addMenu("Measure Count")
        # self._addCountActions(beatMenu, self._setBeatCount)
        self._addCountActions(measureMenu, self._setMeasureCount)
        self.addSeparator()
        # self.addAction("Insert Before", self._insertBeatBefore)
        # after = self.addAction("Insert After", self._insertBeatAfter)
        # if self._counter.endsWithPartialBeat():
        #    after.setDisabled(True)
        self.addSeparator()
        # self.addAction("Delete", self._deleteBeat)

    def _addCountActions(self, menu, countFunction):
        for name, counter in self._qScore.displayProperties.counterRegistry:
            menu.addAction(name, lambda beat = counter: countFunction(beat))

#     @QMenuIgnoreCancelClick.menuSelection
#     def _setBeatCount(self, newCount):
#         print "Beat", repr(newCount)

    @QMenuIgnoreCancelClick.menuSelection
    def _setMeasureCount(self, newCounter):
        newMeasureCount = makeSimpleCount(newCounter,
                                          self._counter.numBeats())
        command = ChangeMeasureCountCommand(self._qScore, self._measurePos,
                                            newMeasureCount)
        self._qScore.addCommand(command)
        

#     @QMenuIgnoreCancelClick.menuSelection
#     def _insertBeatBefore(self):
#         tickIndex = self._np.noteTime
#         beatIndex = self._counter.beatIndexContainingTickIndex(tickIndex)
#         newMeasureCount = copy.copy(self._counter)
#         newMeasureCount.insertBeat(Beat(self._counter[beatIndex].counter),
#                                    beatIndex)
#         command = ChangeMeasureCountCommand(self._qScore, self._measurePos,
#                                             newMeasureCount)
#         self._qScore.addCommand(command)

#     @QMenuIgnoreCancelClick.menuSelection
#     def _insertBeatAfter(self):
#         tickIndex = self._np.noteTime
#         beatIndex = self._counter.beatIndexContainingTickIndex(tickIndex)
#         newMeasureCount = copy.copy(self._counter)
#         newMeasureCount.insertBeat(Beat(self._counter[beatIndex].counter),
#                                    beatIndex + 1)
#         command = ChangeMeasureCountCommand(self._qScore, self._measurePos,
#                                             newMeasureCount)
#         self._qScore.addCommand(command)


#     @QMenuIgnoreCancelClick.menuSelection
#     def _deleteBeat(self):
#         pass
