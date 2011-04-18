'''
Created on 16 Apr 2011

@author: Mike Thomas

'''
import copy
from PyQt4 import QtGui

from QMenuIgnoreCancelClick import QMenuIgnoreCancelClick
import DBIcons
from Data import DBConstants
from DBCommands import (RepeatNoteCommand, InsertMeasuresCommand,
                        InsertSectionCommand, DeleteMeasureCommand,
                        SetAlternateCommand)
from QRepeatDialog import QRepeatDialog
from QInsertMeasuresDialog import QInsertMeasuresDialog

class QMeasureContextMenu(QMenuIgnoreCancelClick):
    '''
    classdocs
    '''


    def __init__(self, qScore, qmeasure, notePosition, noteText, alternateText):
        '''
        Constructor
        '''
        super(QMeasureContextMenu, self).__init__(qScore)
        self._qmeasure = qmeasure
        self._np = notePosition
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
                           self._qmeasure.setAlternate)

    def _setupEditSection(self):
        actionText = "Repeat note"
        repeatNoteAction = self.addAction(DBIcons.getIcon("repeat"),
                                          actionText, self._repeatNote)
        if (self._noteText ==
            DBConstants.EMPTY_NOTE):
            repeatNoteAction.setEnabled(False)
        self.addSeparator()
        self.addAction(DBIcons.getIcon("copy"), "Copy Measure",
                       lambda:self._qScore.copyMeasure(self._np))
        pasteAction = self.addAction(DBIcons.getIcon("paste"),
            "Paste Measure",
            lambda:self._qScore.pasteMeasure(self._np))
        if self._qScore.measureClipboard is None:
            pasteAction.setEnabled(False)
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
        deleteAction = self.addAction(DBIcons.getIcon("delete"),
                                      "Delete Measure", self._deleteMeasure)
        deleteAction.setEnabled(score.numMeasures() > 1)
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
        repeatDialog = QRepeatDialog(self._qScore.parent())
        if repeatDialog.exec_():
            nRepeats, repInterval = repeatDialog.getValues()
            command = RepeatNoteCommand(self._qScore, self._np,
                                        nRepeats,
                                        repInterval, self._noteText)
            self._qScore.addCommand(command)

    def _insertDefaultMeasure(self, np):
        mc = self._props.defaultCounter
        command = InsertMeasuresCommand(self._qScore, np, 1,
                                        mc)
        self._qScore.addCommand(command)

    def _insertMeasureBefore(self):
        self._insertDefaultMeasure(self._np)

    def _insertMeasureAfter(self):
        np = copy.copy(self._np)
        np.measureIndex += 1
        self._insertDefaultMeasure(np)

    def _insertOtherMeasures(self):
        np = copy.copy(self._np)
        counter = self._props.defaultCounter
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

    def _deleteMeasure(self):
        yesNo = QtGui.QMessageBox.question(self._qScore.parent(),
                                           "Delete Measure",
                                           "Really delete this measure?",
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Cancel)
        if yesNo == QtGui.QMessageBox.Ok:
            command = DeleteMeasureCommand(self._qScore,
                                           self._np)
            self._qScore.addCommand(command)

    def _deleteStaff(self):
        score = self._qScore.score
        msg = "Really delete this staff?"
        yesNo = QtGui.QMessageBox.question(self._qScore.parent(),
                                           "Delete Staff?",
                                           msg,
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Cancel)
        if yesNo == QtGui.QMessageBox.Ok:
            np = copy.copy(self._np)
            np.measureIndex = None
            staff = score.getItemAtPosition(np)
            arguments = []
            np.measureIndex = staff.numMeasures() - 1
            while np.measureIndex >= 0:
                arguments.append((copy.copy(np),))
                np.measureIndex -= 1
            self._qScore.addRepeatedCommand("Delete Staff",
                                            DeleteMeasureCommand, arguments)

    def _deleteSection(self):
        score = self._qScore.score
        msg = "Really delete this section?"
        yesNo = QtGui.QMessageBox.question(self._qScore.parent(),
                                           "Delete Staff?",
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
            self._qScore.addRepeatedCommand("Delete Section: " + sectionName,
                                            DeleteMeasureCommand, arguments)

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
            self._qScore.addRepeatedCommand("Delete Empty Measures",
                                            DeleteMeasureCommand, arguments)

    def _deleteAlternate(self):
        command = SetAlternateCommand(self._qScore, self._np,
                                      None)
        self._qScore.addCommand(command)
