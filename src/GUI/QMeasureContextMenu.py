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
Created on 16 Apr 2011

@author: Mike Thomas

'''
from PyQt4 import QtGui

from GUI.QMenuIgnoreCancelClick import QMenuIgnoreCancelClick
import GUI.DBIcons as DBIcons
from GUI.DBCommands import (InsertMeasuresCommand,
                            InsertSectionCommand, DeleteMeasureCommand,
                            SetAlternateCommand, ToggleSimileCommand,
                            SetStickingVisibility, SetNewBpmCommand)
from GUI.QInsertMeasuresDialog import QInsertMeasuresDialog
from GUI.DBFSMEvents import RepeatNotes
from Data import DBConstants


class QMeasureContextMenu(QMenuIgnoreCancelClick):
    def __init__(self, qScore, qmeasure, firstNote, alternateText):
        super(QMeasureContextMenu, self).__init__(qScore)
        self._qmeasure = qmeasure
        self._np = firstNote
        self._score = self._qScore.score
        self._measure = self._score.getMeasureByPosition(self._np)
        self._noteText = qmeasure.noteAt(firstNote)
        self._draggedMeasures = None
        if self._qScore.hasDragSelection():
            self._draggedMeasures = list(self._qScore.iterDragSelection())
            if len(self._draggedMeasures) <= 1:
                self._draggedMeasures = None
        if self._draggedMeasures is not None:
            self._hasSimile = any(measure.simileDistance > 0
                                  for measure, unusedIndex, unusedPos
                                  in self._draggedMeasures)
        else:
            self._hasSimile = self._measure.simileDistance > 0
        self._alternate = alternateText
        self._setup()

    def _setup(self):
        self._setupEditSection()
        self._setupInsertSection()
        self._setupDeleteSection()
        if self._alternate is not None:
            self.addAction("Delete Alternate Ending",
                           self._deleteAlternate)
        else:
            self.addAction("Add Alternate Ending",
                           self._qmeasure.setAlternate)
        if self._draggedMeasures is None:
            if self._measure.simileDistance > 0:
                self.addAction("Remove simile mark",
                               self._toggleSimile)
            else:
                self.addAction("Add simile mark",
                               self._toggleSimile)
        else:
            if self._hasSimile:
                self.addAction("Remove simile marks",
                               self._toggleSimile)
            elif (not any(measure.isSectionEnd() or measure.isRepeatEnd()
                          or measure.isLineBreak()
                          for measure, unusedIndex, unusedPos
                          in self._draggedMeasures[:-1])
                  and
                  not any(measure.isRepeatStart()
                          for measure, unusedIndex, unusedPos
                          in self._draggedMeasures[1:])):
                self.addAction("Add %d bar simile mark"
                               % len(self._draggedMeasures),
                               self._toggleSimile)
        if not self._hasSimile:
            self._setupStickingSection()
            self._setupBpmSection()

    def _setupEditSection(self):
        if self._measure.simileDistance > 0:
            return
        if self._noteText != DBConstants.EMPTY_NOTE:
            actionText = "Repeat note"
            self.addAction(DBIcons.getIcon("repeat"),
                           actionText, self._repeatNote)
        self.addSeparator()
        if self._qScore.hasDragSelection():
            self.addAction(DBIcons.getIcon("copy"),
                           "Copy Selected Measures",
                           self._copyMeasures)
            pasteAction = self.addAction(DBIcons.getIcon("paste"),
                                         "Paste Over Selected Measures",
                                         self._pasteMeasuresOver)
            fillAction = self.addAction(DBIcons.getIcon("paste"),
                                        "Fill Paste Selected Measures",
                                        self._fillPaste)
            fillAction.setEnabled(len(self._qScore.measureClipboard) > 0)
        else:
            self.addAction(DBIcons.getIcon("copy"), "Copy Measure",
                           self._copyOneMeasure)
            pasteAction = self.addAction(DBIcons.getIcon("paste"),
                                         "Insert Measures From Clipboard",
                                         self._insertOneMeasure)
        pasteAction.setEnabled(len(self._qScore.measureClipboard) > 0)
        self.addSeparator()

    def _setupInsertSection(self):
        if self._hasSimile:
            return
        actionText = "Insert Default Measure"
        self.addAction(actionText, self._insertMeasureBefore)
        insertMenu = self.addMenu("Insert...")
        insertMenu.addAction("Default Measure After", self._insertMeasureAfter)
        insertMenu.addAction("Other Measures...", self._insertOtherMeasures)
        sectionCopyMenu = insertMenu.addMenu("Section Copy")
        sectionCopyMenu.setEnabled(self._score.numSections() > 0)
        for si, sectionTitle in enumerate(self._score.iterSections()):
            copyIt = lambda i = si: self._copySection(i)
            sectionCopyMenu.addAction(sectionTitle, copyIt)
        self.addSeparator()

    def _setupDeleteSection(self):
        if not self._hasSimile:
            if self._qScore.hasDragSelection():
                deleteAction = self.addAction(DBIcons.getIcon("delete"),
                                              "Delete Selected Measures",
                                              self._deleteMeasures)
                deleteAction.setEnabled(self._score.numMeasures() >
                                        len(list(self._qScore.iterDragSelection())))
                self.addAction("Clear Selected Measures",
                               self._clearMeasures)
            else:
                deleteAction = self.addAction(DBIcons.getIcon("delete"),
                                              "Delete Measure",
                                              self._deleteOneMeasure)
                deleteAction.setEnabled(self._score.numMeasures() > 1)
                self.addAction("Clear Measure",
                               self._clearOneMeasure)
        deleteMenu = self.addMenu("Delete...")
        deleteSectionAction = deleteMenu.addAction("Section",
                                                   self._deleteSection)
        deleteSectionAction.setEnabled(self._score.numSections() > 1)
        deleteEmptyAction = deleteMenu.addAction("Empty Trailing Measures",
                                                 self._deleteEmptyMeasures)
        emptyPositions = self._score.trailingEmptyMeasures()
        deleteEmptyAction.setEnabled(self._score.numMeasures() > 1
                                     and len(emptyPositions) > 0)
        self.addSeparator()

    def _setupStickingSection(self):
        self.addSeparator()
        action = QtGui.QAction("Show Sticking Above", self,
                               checkable=True)
        action.setChecked(self._measure.showAbove)
        action.triggered.connect(lambda: self._showSticking(
            True, not self._measure.showAbove))
        self.addAction(action)
        action = QtGui.QAction("Show Sticking Below", self,
                               checkable=True)
        action.setChecked(self._measure.showBelow)
        action.triggered.connect(lambda: self._showSticking(
            False, not self._measure.showBelow))
        self.addAction(action)

    def _setupBpmSection(self):
        self.addSeparator()
        self.addAction("Set new BPM",
                       self._qmeasure.setNewBpm)
        if self._measure.newBpm != 0:
            self.addAction("Delete BPM change", self._removeBpmChange)

    def _repeatNote(self):
        self._qScore.sendFsmEvent(RepeatNotes(self._np))

    @QMenuIgnoreCancelClick.menuSelection
    def _insertDefaultMeasure(self, np, preserveSectionEnd=False):
        mc = self._qScore.defaultCount
        command = InsertMeasuresCommand(self._qScore, np, 1,
                                        mc, preserveSectionEnd)
        self._qScore.clearDragSelection()
        self._qScore.addCommand(command)

    @QMenuIgnoreCancelClick.menuSelection
    def _insertMeasureBefore(self):
        self._insertDefaultMeasure(self._np)

    @QMenuIgnoreCancelClick.menuSelection
    def _insertMeasureAfter(self):
        np = self._np.makeMeasurePosition()
        np.measureIndex += 1
        self._insertDefaultMeasure(np, True)

    @QMenuIgnoreCancelClick.menuSelection
    def _insertOtherMeasures(self):
        np = self._np.makeMeasurePosition()
        counter = self._qScore.defaultCount
        insertDialog = QInsertMeasuresDialog(self._qScore.parent(),
                                             counter,
                                             self._props.counterRegistry)
        if insertDialog.exec_():
            nMeasures, counter, insertBefore = insertDialog.getValues()
            preserve = False
            if not insertBefore:
                np.measureIndex += 1
                preserve = True
            command = InsertMeasuresCommand(self._qScore, np, nMeasures,
                                            counter, preserve)
            self._qScore.clearDragSelection()
            self._qScore.addCommand(command)

    @QMenuIgnoreCancelClick.menuSelection
    def _copySection(self, sectionIndex):
        command = InsertSectionCommand(self._qScore, self._np, sectionIndex)
        self._qScore.clearDragSelection()
        self._qScore.addCommand(command)

    @QMenuIgnoreCancelClick.menuSelection
    def _deleteStaff(self):
        msg = "Really delete this staff?"
        yesNo = QtGui.QMessageBox.question(self._qScore.parent(),
                                           "Delete Staff?",
                                           msg,
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Cancel)
        if yesNo == QtGui.QMessageBox.Ok:
            np = self._np.makeCopy()
            staff = self._score.getStaffByIndex(np.staffIndex)
            arguments = []
            np.measureIndex = staff.numMeasures() - 1
            while np.measureIndex >= 0:
                arguments.append((np.makeCopy(),))
                np.measureIndex -= 1
            self._qScore.clearDragSelection()
            self._qScore.addRepeatedCommand("delete staff",
                                            DeleteMeasureCommand, arguments)

    @QMenuIgnoreCancelClick.menuSelection
    def _deleteSection(self):
        msg = "Really delete this section?"
        yesNo = QtGui.QMessageBox.question(self._qScore.parent(),
                                           "Delete Section?",
                                           msg,
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Cancel)
        if yesNo == QtGui.QMessageBox.Ok:
            np = self._np.makeMeasurePosition()
            startIndex = self._score.getSectionStartStaffIndex(np)
            sectionIndex = self._score.positionToSectionIndex(np)
            sectionName = self._score.getSectionTitle(sectionIndex)
            np.staffIndex = startIndex
            while (np.staffIndex < self._score.numStaffs()
                   and not self._score.getStaffByIndex(np.staffIndex).isSectionEnd()):
                np.staffIndex += 1
            arguments = []
            for np.staffIndex in xrange(np.staffIndex, startIndex - 1, -1):
                staff = self._score.getStaffByIndex(np.staffIndex)
                for np.measureIndex in xrange(staff.numMeasures() - 1, -1, -1):
                    arguments.append((np.makeCopy(),))
            self._qScore.clearDragSelection()
            self._qScore.addRepeatedCommand("delete section: " + sectionName,
                                            DeleteMeasureCommand, arguments)

    @QMenuIgnoreCancelClick.menuSelection
    def _deleteEmptyMeasures(self):
        msg = "This will delete all empty trailing measures.\nContinue?"
        yesNo = QtGui.QMessageBox.question(self._qScore.parent(),
                                           "Delete Empty Measures",
                                           msg,
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Cancel)
        if yesNo == QtGui.QMessageBox.Ok:
            positions = self._score.trailingEmptyMeasures()
            arguments = [(np,) for np in positions]
            self._qScore.clearDragSelection()
            self._qScore.addRepeatedCommand("delete empty measures",
                                            DeleteMeasureCommand, arguments)

    @QMenuIgnoreCancelClick.menuSelection
    def _deleteAlternate(self):
        command = SetAlternateCommand(self._qScore, self._np,
                                      None)
        self._qScore.addCommand(command)

    @QMenuIgnoreCancelClick.menuSelection
    def _copyOneMeasure(self):
        self._qScore.copyMeasures(self._np)

    @QMenuIgnoreCancelClick.menuSelection
    def _copyMeasures(self):
        self._qScore.copyMeasures()

    @QMenuIgnoreCancelClick.menuSelection
    def _pasteMeasuresOver(self):
        self._qScore.pasteMeasuresOver()

    @QMenuIgnoreCancelClick.menuSelection
    def _fillPaste(self):
        self._qScore.pasteMeasuresOver(True)

    @QMenuIgnoreCancelClick.menuSelection
    def _insertOneMeasure(self):
        self._qScore.insertMeasures(self._np)

    @QMenuIgnoreCancelClick.menuSelection
    def _deleteMeasures(self):
        self._qScore.deleteMeasures()

    @QMenuIgnoreCancelClick.menuSelection
    def _deleteOneMeasure(self):
        self._qScore.deleteMeasures(self._np)

    @QMenuIgnoreCancelClick.menuSelection
    def _clearMeasures(self):
        self._qScore.clearMeasures()

    @QMenuIgnoreCancelClick.menuSelection
    def _clearOneMeasure(self):
        self._qScore.clearMeasures(self._np)

    @QMenuIgnoreCancelClick.menuSelection
    def _toggleSimile(self):
        self._qScore.clearDragSelection()
        if self._draggedMeasures is None:
            startIndex = self._score.measurePositionToIndex(self._np)
            endIndex = startIndex
        else:
            startIndex = self._draggedMeasures[0][1]
            endIndex = self._draggedMeasures[-1][1]
        if self._hasSimile:
            startMeasure = self._score.getMeasureByIndex(startIndex)
            while startIndex > 0 and startMeasure.simileIndex > 0:
                startIndex -= 1
                startMeasure = self._score.getMeasureByIndex(startIndex)
            endMeasure = self._score.getMeasureByIndex(endIndex)
            while (endIndex < self._score.numMeasures() - 1 and
                   endMeasure.simileIndex < endMeasure.simileDistance - 1):
                endIndex += 1
                endMeasure = self._score.getMeasureByIndex(endIndex)
            simileDistance = 0
            macroName = "Remove simile mark"
        else:
            if self._draggedMeasures is None:
                simileDistance = 1
            else:
                simileDistance = len(self._draggedMeasures)
            macroName = "Add simile mark"
        if endIndex - startIndex > 0:
            macroName += "s"
        self._qScore.beginMacro(macroName)
        for simileIndex, measureIndex in enumerate(xrange(startIndex,
                                                          endIndex + 1)):
            np = self._score.measureIndexToPosition(measureIndex)
            command = ToggleSimileCommand(self._qScore, np,
                                          simileIndex, simileDistance)
            self._qScore.addCommand(command)
        self._qScore.endMacro()

    @QMenuIgnoreCancelClick.menuSelection
    def _showSticking(self, above, onOff):
        command = SetStickingVisibility(self._qScore,
                                        self._np,
                                        above, onOff)
        self._qScore.addCommand(command)

    @QMenuIgnoreCancelClick.menuSelection
    def _removeBpmChange(self):
        if self._measure.newBpm == 0:
            return
        command = SetNewBpmCommand(self._qScore, self._np, 0)
        self._qScore.addCommand(command)
