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
import copy
from PyQt4 import QtGui

from QMenuIgnoreCancelClick import QMenuIgnoreCancelClick
import DBIcons
from Data import DBConstants
from DBCommands import (InsertMeasuresCommand,
                        InsertSectionCommand, DeleteMeasureCommand,
                        SetAlternateCommand)
from QInsertMeasuresDialog import QInsertMeasuresDialog
from DBFSMEvents import MenuSelect, RepeatNotes

class QMeasureContextMenu(QMenuIgnoreCancelClick):
    def __init__(self, qScore, qmeasure, firstNote, noteText, alternateText):
        '''
        Constructor
        '''
        super(QMeasureContextMenu, self).__init__(qScore)
        self._qmeasure = qmeasure
        self._np = firstNote
        self._noteText = noteText
        self._alternate = alternateText
        self._props = self._qScore.displayProperties
        self._setup()

    def _setup(self):
        score = self._qScore.score
        self._setupEditSection()
        self._setupInsertSection(score)
        self._setupDeleteSection(score)
        if self._alternate is not None:
            self.addAction("Delete Alternate Ending",
                           self._deleteAlternate)
        else:
            self.addAction("Add Alternate Ending",
                           self._setAlternate)

    def _setupEditSection(self):
        if (self._noteText !=
            DBConstants.EMPTY_NOTE):
            actionText = "Repeat note"
            self.addAction(DBIcons.getIcon("repeat"),
                           actionText, self._repeatNote)
        self.addSeparator()
        if self._qScore.hasDragSelection():
            self.addAction(DBIcons.getIcon("copy"), "Copy Selected Measures",
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

    def _setupInsertSection(self, score):
        actionText = "Insert Default Measure"
        self.addAction(actionText, self._insertMeasureBefore)
        insertMenu = self.addMenu("Insert...")
        insertMenu.addAction("Default Measure After", self._insertMeasureAfter)
        insertMenu.addAction("Other Measures", self._insertOtherMeasures)
        sectionCopyMenu = insertMenu.addMenu("Section Copy")
        sectionCopyMenu.setEnabled(score.numSections() > 0)
        for si, sectionTitle in enumerate(score.iterSections()):
            copyIt = lambda i = si:self._copySection(i)
            sectionCopyMenu.addAction(sectionTitle, copyIt)
        self.addSeparator()

    def _setupDeleteSection(self, score):
        if self._qScore.hasDragSelection():
            deleteAction = self.addAction(DBIcons.getIcon("delete"),
                                          "Delete Selected Measures",
                                          self._deleteMeasures)
            deleteAction.setEnabled(score.numMeasures() >
                                    len(list(self._qScore.iterDragSelection())))
            self.addAction("Clear Selected Measures",
                           self._clearMeasures)
        else:
            deleteAction = self.addAction(DBIcons.getIcon("delete"),
                                          "Delete Measure",
                                          self._deleteOneMeasure)
            deleteAction.setEnabled(score.numMeasures() > 1)
            self.addAction("Clear Measure",
                           self._clearOneMeasure)
        deleteMenu = self.addMenu("Delete...")
        deleteStaffAction = deleteMenu.addAction("Staff", self._deleteStaff)
        deleteStaffAction.setEnabled(score.numStaffs() > 1)
        deleteSectionAction = deleteMenu.addAction("Section",
                                                   self._deleteSection)
        deleteSectionAction.setEnabled(score.numSections() > 1)
        deleteEmptyAction = deleteMenu.addAction("Empty Trailing Measures",
                                                 self._deleteEmptyMeasures)
        emptyPositions = score.trailingEmptyMeasures()
        deleteEmptyAction.setEnabled(score.numMeasures() > 1
                                     and len(emptyPositions) > 0)
        self.addSeparator()

    def _repeatNote(self):
        self._qScore.sendFsmEvent(RepeatNotes())

    def _insertDefaultMeasure(self, np):
        mc = self._qScore.defaultCount
        command = InsertMeasuresCommand(self._qScore, np, 1,
                                        mc)
        self._qScore.addCommand(command)

    def _insertMeasureBefore(self):
        self._insertDefaultMeasure(self._np)
        self._qScore.sendFsmEvent(MenuSelect())

    def _insertMeasureAfter(self):
        np = copy.copy(self._np)
        np.measureIndex += 1
        self._insertDefaultMeasure(np)
        self._qScore.sendFsmEvent(MenuSelect())

    def _insertOtherMeasures(self):
        np = copy.copy(self._np)
        counter = self._qScore.defaultCount
        insertDialog = QInsertMeasuresDialog(self._qScore.parent(),
                                             counter,
                                             self._props.counterRegistry)
        if insertDialog.exec_():
            nMeasures, counter, insertBefore = insertDialog.getValues()
            if not insertBefore:
                np.measureIndex += 1
            command = InsertMeasuresCommand(self._qScore, np, nMeasures,
                                            counter)
            self._qScore.addCommand(command)

    def _copySection(self, sectionIndex):
        command = InsertSectionCommand(self._qScore, self._np, sectionIndex)
        self._qScore.addCommand(command)
        self._qScore.sendFsmEvent(MenuSelect())

    def _deleteStaff(self):
        score = self._qScore.score
        msg = "Really delete this staff?"
        yesNo = QtGui.QMessageBox.question(self._qScore.parent(),
                                           "Delete Staff?",
                                           msg,
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Cancel)
        if yesNo == QtGui.QMessageBox.Ok:
            np = self._np.makeStaffPosition()
            staff = score.getItemAtPosition(np)
            arguments = []
            np.measureIndex = staff.numMeasures() - 1
            while np.measureIndex >= 0:
                arguments.append((copy.copy(np),))
                np.measureIndex -= 1
            self._qScore.addRepeatedCommand("delete staff",
                                            DeleteMeasureCommand, arguments)
        self._qScore.sendFsmEvent(MenuSelect())

    def _deleteSection(self):
        score = self._qScore.score
        msg = "Really delete this section?"
        yesNo = QtGui.QMessageBox.question(self._qScore.parent(),
                                           "Delete Section?",
                                           msg,
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Cancel)
        if yesNo == QtGui.QMessageBox.Ok:
            np = copy.copy(self._np)
            startIndex = score.getSectionStartStaffIndex(np)
            sectionIndex = score.getSectionIndex(np)
            sectionName = score.getSectionTitle(sectionIndex)
            np.staffIndex = startIndex
            while (np.staffIndex < score.numStaffs()
                   and not score.getStaff(np.staffIndex).isSectionEnd()):
                np.staffIndex += 1
            arguments = []
            for np.staffIndex in range(np.staffIndex, startIndex - 1, -1):
                staff = score.getStaff(np.staffIndex)
                for np.measureIndex in range(staff.numMeasures() - 1, -1, -1):
                    arguments.append((copy.copy(np),))
                np.staffIndex -= 1
            self._qScore.addRepeatedCommand("delete section: " + sectionName,
                                            DeleteMeasureCommand, arguments)
        self._qScore.sendFsmEvent(MenuSelect())

    def _deleteEmptyMeasures(self):
        score = self._qScore.score
        msg = "This will delete all empty trailing measures.\nContinue?"
        yesNo = QtGui.QMessageBox.question(self._qScore.parent(),
                                           "Delete Empty Measures",
                                           msg,
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Cancel)
        if yesNo == QtGui.QMessageBox.Ok:
            positions = score.trailingEmptyMeasures()
            arguments = [(np,) for np in positions]
            self._qScore.addRepeatedCommand("delete empty measures",
                                            DeleteMeasureCommand, arguments)
        self._qScore.sendFsmEvent(MenuSelect())

    def _deleteAlternate(self):
        np = self._np.makeMeasurePosition()
        command = SetAlternateCommand(self._qScore, np,
                                      None)
        self._qScore.addCommand(command)
        self._qScore.sendFsmEvent(MenuSelect())

    def _setAlternate(self):
        self._qmeasure.setAlternate()
        self._qScore.sendFsmEvent(MenuSelect())

    def _copyOneMeasure(self):
        self._qScore.copyMeasures(self._np)

    def _copyMeasures(self):
        self._qScore.copyMeasures()
        self._qScore.sendFsmEvent(MenuSelect())

    def _pasteMeasuresOver(self):
        self._qScore.pasteMeasuresOver()
        self._qScore.sendFsmEvent(MenuSelect())

    def _fillPaste(self):
        self._qScore.pasteMeasuresOver(True)
        self._qScore.sendFsmEvent(MenuSelect())

    def _insertOneMeasure(self):
        self._qScore.insertMeasures(self._np)
        self._qScore.sendFsmEvent(MenuSelect())

    def _deleteMeasures(self):
        self._qScore.deleteMeasures()
        self._qScore.sendFsmEvent(MenuSelect())

    def _deleteOneMeasure(self):
        self._qScore.deleteMeasures(self._np)
        self._qScore.sendFsmEvent(MenuSelect())

    def _clearMeasures(self):
        self._qScore.clearMeasures()
        self._qScore.sendFsmEvent(MenuSelect())

    def _clearOneMeasure(self):
        self._qScore.clearMeasures(self._np)
        self._qScore.sendFsmEvent(MenuSelect())
