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
Created on 26 Jan 2011

@author: Mike Thomas

'''
from PyQt4.QtGui import (QDialog, QRadioButton, QFileDialog, QDesktopServices,
                         QMessageBox, QInputDialog, QColor, QDialogButtonBox)
from ui_editKit import Ui_editKitDialog
from PyQt4.QtCore import QVariant
from Data import DrumKit
from Data.Drum import Drum
from Data.DefaultKits import GHOST_VOLUME, ACCENT_VOLUME
from Data import fileUtils
from QDefaultKitManager import QDefaultKitManager
import copy
import os
import string #IGNORE:W0402
import DBMidi
from QNotationScene import QNotationScene

_KIT_FILE_EXT = ".dbk"
_KIT_FILTER = "DrumBurp kits (*%s)" % _KIT_FILE_EXT

_BAD_ABBR_COLOR = QColor("red")
_GOOD_ABBR_COLOR = QColor("black")

class QEditKitDialog(QDialog, Ui_editKitDialog):
    '''
    classdocs
    '''

    def __init__(self, kit, emptyDrums = None, parent = None, directory = None):
        '''
        Constructor
        '''
        super(QEditKitDialog, self).__init__(parent)
        self.setupUi(self)
        self.muteButton.setChecked(DBMidi.isMuted())
        if emptyDrums is None:
            emptyDrums = []
            self.deleteEmptyButton.setEnabled(False)
        self._scoreDirectory = directory
        self._emptyDrums = emptyDrums
        self._currentKit = []
        self._oldLines = {}
        self._initialKit = kit
        self._initialize()
        self.kitTable.currentRowChanged.connect(self._drumChanged)
        self.upButton.clicked.connect(self._moveDrumUp)
        self.downButton.clicked.connect(self._moveDrumDown)
        self.addButton.clicked.connect(self._addDrum)
        self.deleteButton.clicked.connect(self._removeDrum)
        self.deleteEmptyButton.clicked.connect(self._deleteEmpty)
        self.clearButton.clicked.connect(self._clearKit)
        self.resetButton.clicked.connect(self._resetKit)
        self.defaultKitButton.clicked.connect(self._manageDefaultKits)
        self.loadButton.clicked.connect(self._loadKit)
        self.saveButton.clicked.connect(self._saveKit)
        self.drumName.textEdited.connect(self._drumNameEdited)
        self.drumAbbr.editingFinished.connect(self._drumAbbrEdited)
        self.oldDrum.currentIndexChanged.connect(self._oldDrumChanged)
        self.currentNoteHead.currentIndexChanged.connect(self._headEdited)
        self.noteHeadTable.currentRowChanged.connect(self._noteHeadChanged)
        self.addHeadButton.clicked.connect(self._addNoteHead)
        self.headUpButton.clicked.connect(self._moveNoteHeadUp)
        self.setDefaultHeadButton.clicked.connect(self._setDefaultHead)
        self.headDownButton.clicked.connect(self._moveNoteHeadDown)
        self.deleteHeadButton.clicked.connect(self._removeNoteHead)
        self.noteHeadBox.currentIndexChanged.connect(self._notationHeadChanged)
        self.effectBox.currentIndexChanged.connect(self._notationEffectChanged)
        self.stemUpDownBox.stateChanged.connect(self._stemDirectionChanged)
        self.noteUpButton.clicked.connect(self._moveNotationUp)
        self.noteDownButton.clicked.connect(self._moveNotationDown)
        self.shortcutCombo.currentIndexChanged.connect(self._shortcutEdited)
        self._populateMidiCombo()
        self.midiNoteCombo.currentIndexChanged.connect(self._midiNoteChanged)
        self.volumeSlider.valueChanged.connect(self._midiVolumeChanged)
        for effect in self.effectsGroup.children():
            if isinstance(effect, QRadioButton):
                effect.toggled.connect(self._effectChanged)
        self.lockedCheckBox.stateChanged.connect(self._lockChanged)
        self._notationScene = QNotationScene(self)
        self.noteView.setScene(self._notationScene)
        self.noteView.centerOn(*self._notationScene.getCenter())
        self._populate()


    def _initialize(self):
        self.oldDrum.addItem("None", userData = QVariant(-1))
        for drumIndex, drum in enumerate(reversed(self._initialKit)):
            drum = copy.deepcopy(drum)
            self._currentKit.append(drum)
            self.oldDrum.addItem(drum.name, userData = QVariant(drumIndex))
            self._oldLines[drum] = drumIndex

    def _populate(self):
        self.kitTable.blockSignals(True)
        self.kitTable.clear()
        for drum in self._currentKit:
            self.kitTable.addItem(drum.name)
        self.kitTable.blockSignals(False)
        self.kitTable.setCurrentRow(0)
        self._checkAbbrs()

    @property
    def _currentDrumIndex(self):
        return self.kitTable.currentRow()

    @property
    def _currentDrum(self):
        drumIndex = self._currentDrumIndex
        return self._currentKit[drumIndex]

    def _checkDrumButtons(self):
        self.deleteButton.setEnabled(len(self._currentKit) > 1)
        index = self._currentDrumIndex
        self.upButton.setEnabled(index > 0)
        self.downButton.setEnabled(index < len(self._currentKit) - 1)

    def _drumChanged(self):
        drum = self._currentDrum
        self.drumName.setText(drum.name)
        self.drumAbbr.setText(drum.abbr)
        self.oldDrum.setCurrentIndex(self._oldLines[drum] + 1)
        self.lockedCheckBox.setChecked(drum.locked)
        self._populateHeadTable()
        self._checkDrumButtons()


    def _addDrum(self):
        drum = Drum("New drum", "XX", "o")
        drum.guessHeadData()
        drum.checkShortcuts()
        self._currentKit.append(drum)
        self._oldLines[drum] = -1
        self.kitTable.addItem(drum.name)
        self.kitTable.setCurrentRow(len(self._currentKit) - 1)
        self._checkDrumButtons()
        self._checkAbbrs()
        self.drumName.setFocus()
        self.drumName.selectAll()

    def _removeDrum(self):
        index = self._currentDrumIndex
        drum = self._currentDrum
        self._currentKit = (self._currentKit[:index]
                            + self._currentKit[index + 1:])
        self._oldLines.pop(drum)
        if index < len(self._currentKit) - 1:
            self._drumChanged()
        else:
            self.kitTable.setCurrentRow(index - 1)
        self.kitTable.takeItem(index)
        self._checkDrumButtons()
        self._checkAbbrs()

    def _moveDrumUp(self):
        idx = self._currentDrumIndex
        druma, drumb = self._currentKit[idx - 1], self._currentKit[idx]
        self._currentKit[idx - 1], self._currentKit[idx] = drumb, druma
        self.kitTable.item(idx).setText(self._currentKit[idx].name)
        self.kitTable.item(idx - 1).setText(self._currentKit[idx - 1].name)
        self.kitTable.setCurrentRow(idx - 1)

    def _moveDrumDown(self):
        idx = self._currentDrumIndex
        druma, drumb = self._currentKit[idx], self._currentKit[idx + 1]
        self._currentKit[idx], self._currentKit[idx + 1] = drumb, druma
        self.kitTable.item(idx).setText(self._currentKit[idx].name)
        self.kitTable.item(idx + 1).setText(self._currentKit[idx + 1].name)
        self.kitTable.setCurrentRow(idx + 1)

    def _clearKit(self):
        self._currentKit = []
        self._oldLines.clear()
        self.kitTable.blockSignals(True)
        self.kitTable.clear()
        self.kitTable.blockSignals(False)
        self._addDrum()

    def _deleteEmpty(self):
        newKit = []
        toDelete = []
        for drum in self._currentKit:
            oldIndex = self._oldLines[drum]
            if oldIndex == -1:
                newKit.append(drum)
                continue
            oldDrum = self._initialKit[len(self._initialKit)
                                       - 1 - self._oldLines[drum]]
            if oldDrum in self._emptyDrums:
                toDelete.append(drum)
            else:
                newKit.append(drum)
        for drum in toDelete:
            self._oldLines.pop(drum)
        self._currentKit = newKit
        self._populate()

    def _resetKit(self):
        self._currentKit = []
        self._oldLines = {}
        for drumIndex, drum in enumerate(reversed(self._initialKit)):
            drum = copy.deepcopy(drum)
            self._currentKit.append(drum)
            self._oldLines[drum] = drumIndex
        self._populate()

    def _loadKit(self):
        directory = self._scoreDirectory
        if directory is None:
            home = QDesktopServices.HomeLocation
            directory = unicode(QDesktopServices.storageLocation(home))
        fname = QFileDialog.getOpenFileName(parent = self,
                                            caption = "Load DrumBurp kit",
                                            directory = directory,
                                            filter = _KIT_FILTER)
        if len(fname) == 0:
            return
        with open(fname, 'rU') as handle:
            fileIterator = fileUtils.dbFileIterator(handle)
            newKit = DrumKit.DrumKit()
            newKit.read(fileIterator)
        self._currentKit = list(reversed(newKit))
        self._oldLines.clear()
        for drum in self._currentKit:
            self._oldLines[drum] = -1
        self._populate()

    def _manageDefaultKits(self):
        currentKit, unused_ = self.getNewKit()
        dialog = QDefaultKitManager(currentKit, self)
        if dialog.exec_():
            newKit = dialog.getKit()
            self._currentKit = list(reversed(newKit))
            self._oldLines.clear()
            for drum in self._currentKit:
                self._oldLines[drum] = -1
            self._populate()

    def _saveKit(self):
        directory = self._scoreDirectory
        if directory is None:
            home = QDesktopServices.HomeLocation
            directory = unicode(QDesktopServices.storageLocation(home))
        fname = QFileDialog.getSaveFileName(parent = self,
                                            caption = "Save DrumBurp kit",
                                            directory = directory,
                                            filter = _KIT_FILTER)
        if len(fname) == 0:
            return
        fname = unicode(fname)
        indenter = fileUtils.Indenter()
        newKit, unused = self.getNewKit()
        with open(fname, 'w') as handle:
            newKit.write(handle, indenter)
        QMessageBox.information(self, "Kit saved", "Successfully saved drumkit")


    def _drumNameEdited(self):
        self._currentDrum.name = unicode(self.drumName.text())
        drumIndex = self._currentDrumIndex
        self.kitTable.item(drumIndex).setText(self._currentDrum.name)

    def _drumAbbrEdited(self):
        self._currentDrum.abbr = unicode(self.drumAbbr.text())
        self._checkAbbrs()

    def _checkAbbrs(self):
        # Check that there is not more than one drum with the same
        # abbreviation. If there is, highlight them and disable the OK button 
        # and accept action.
        drumIndicesByAbbr = {}
        for index, drum in enumerate(self._currentKit):
            if drum.abbr not in drumIndicesByAbbr:
                drumIndicesByAbbr[drum.abbr] = []
            drumIndicesByAbbr[drum.abbr].append(index)
        ok = True
        for indices in drumIndicesByAbbr.itervalues():
            if len(indices) > 1:
                ok = False
                for index in indices:
                    self.kitTable.item(index).setTextColor(_BAD_ABBR_COLOR)
            else:
                for index in indices:
                    self.kitTable.item(index).setTextColor(_GOOD_ABBR_COLOR)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(ok)
        self.saveButton.setEnabled(ok)
        return ok


    def _oldDrumChanged(self):
        drum = self._currentDrum
        newOldDrumIndex = self.oldDrum.currentIndex()
        newOldDrumIndex = self.oldDrum.itemData(newOldDrumIndex).toInt()[0]
        self._oldLines[drum] = newOldDrumIndex

    def _populateHeadTable(self):
        self.noteHeadTable.blockSignals(True)
        drum = self._currentDrum
        self.noteHeadTable.clear()
        for head in drum:
            headString = head
            if head == drum.head:
                headString += " (Default)"
            self.noteHeadTable.addItem(headString)
        self.noteHeadTable.setCurrentRow(-1)
        self.noteHeadTable.blockSignals(False)
        self.noteHeadTable.setCurrentRow(0)


    @property
    def _currentHead(self):
        drum = self._currentDrum
        row = self.noteHeadTable.currentRow()
        head = drum[row]
        return head

    @property
    def _currentHeadData(self):
        drum = self._currentDrum
        row = self.noteHeadTable.currentRow()
        head = drum[row]
        return drum.headData(head)

    def _headEdited(self):
        noteHead = str(self.currentNoteHead.currentText())
        row = self.noteHeadTable.currentRow()
        drum = self._currentDrum
        oldHead = drum[row]
        drum.renameHead(oldHead, noteHead)
        headString = noteHead
        if noteHead == drum.head:
            headString += " (Default)"
        self.noteHeadTable.item(row).setText(headString)
        self._populateCurrentNoteHead()

    def _noteHeadChanged(self):
        self._populateCurrentNoteHead()
        headData = self._currentHeadData
        self.volumeSlider.setValue(headData.midiVolume)
        midiIndex = self.midiNoteCombo.findData(QVariant(headData.midiNote))
        self.midiNoteCombo.setCurrentIndex(midiIndex)
        self._setEffect(headData.effect)
        if not self.muteButton.isChecked():
            DBMidi.playHeadData(self._currentHeadData)
        self._checkHeadButtons()
        self._setNotation()

    def _shortcutEdited(self):
        shortcut = str(self.shortcutCombo.currentText())
        self._currentHeadData.shortcut = shortcut

    def _populateCurrentNoteHead(self):
        self.currentNoteHead.blockSignals(True)
        self.shortcutCombo.blockSignals(True)
        try:
            self.currentNoteHead.clear()
            badNotes = set(self._currentDrum)
            badNotes.remove(self._currentHead)
            badNotes.update(["-", "|"])
            for head in string.printable:
                head = head.strip()
                if not head or head in badNotes:
                    continue
                self.currentNoteHead.addItem(head)
            headIndex = self.currentNoteHead.findText(self._currentHead)
            self.currentNoteHead.setCurrentIndex(headIndex)
            self.shortcutCombo.clear()
            availableShortcuts = set('abcdefghijklmnopqrstuvwxyz')
            for head in self._currentDrum:
                if head != self._currentHead:
                    shortcut = self._currentDrum.headData(head).shortcut
                    availableShortcuts.remove(shortcut)
            for okShortcut in sorted(list(availableShortcuts)):
                self.shortcutCombo.addItem(okShortcut)
            shortcut = self._currentHeadData.shortcut
            shortIndex = self.shortcutCombo.findText(shortcut)
            self.shortcutCombo.setCurrentIndex(shortIndex)
        finally:
            self.shortcutCombo.blockSignals(False)
            self.currentNoteHead.blockSignals(False)

    def _addNoteHead(self):
        badNotes = set(self._currentDrum)
        badNotes.update(["-", "|"])
        head = "?"
        if head in badNotes:
            candidates = string.printable
            for head in candidates:
                if head not in badNotes:
                    break
        self._currentDrum.addNoteHead(head)
        self._populateHeadTable()
        self.noteHeadTable.setCurrentRow(len(self._currentDrum) - 1)
        self._checkHeadButtons()
        self.currentNoteHead.setFocus()

    def _removeNoteHead(self):
        row = self.noteHeadTable.currentRow()
        head = self._currentHead
        self._currentDrum.removeNoteHead(head)
        self._populateHeadTable()
        if row >= len(self._currentDrum):
            self.noteHeadTable.setCurrentRow(row - 1)
        else:
            self.noteHeadTable.setCurrentRow(row)
        self._checkHeadButtons()

    def _checkHeadButtons(self):
        isDefault = (self._currentHead == self._currentDrum.head)
        self.deleteHeadButton.setEnabled(not isDefault)
        if isDefault:
            self.headUpButton.setEnabled(False)
            self.headDownButton.setEnabled(False)
        else:
            index = self.noteHeadTable.currentRow()
            self.headUpButton.setEnabled(index > 1)
            self.headDownButton.setEnabled(index <
                                           len(self._currentDrum) - 1)

    def _moveNoteHeadUp(self):
        index = self.noteHeadTable.currentRow()
        self._currentDrum.moveHeadUp(self._currentHead)
        self._populateHeadTable()
        self.noteHeadTable.setCurrentRow(index - 1)

    def _moveNoteHeadDown(self):
        index = self.noteHeadTable.currentRow()
        self._currentDrum.moveHeadDown(self._currentHead)
        self._populateHeadTable()
        self.noteHeadTable.setCurrentRow(index + 1)

    def _setDefaultHead(self):
        self.noteHeadTable.blockSignals(True)
        self._currentDrum.setDefaultHead(self._currentHead)
        self._populateHeadTable()
        self.noteHeadTable.blockSignals(False)
        self.noteHeadTable.setCurrentRow(0)


    def _midiNoteChanged(self):
        midiNote = self.midiNoteCombo.currentIndex()
        midiNote = self.midiNoteCombo.itemData(midiNote).toInt()[0]
        self._currentHeadData.midiNote = midiNote
        if not self.muteButton.isChecked():
            DBMidi.playHeadData(self._currentHeadData)

    def _midiVolumeChanged(self):
        self._currentHeadData.midiVolume = self.volumeSlider.value()

    def _setEffect(self, effect):
        effectMap = {"normal":self.normalEffect,
                     "accent":self.accentEffect,
                     "ghost":self.ghostEffect,
                     "flam":self.flamEffect,
                     "choke":self.chokeEffect,
                     "drag":self.dragEffect}
        effect = effectMap[effect]
        effect.setChecked(True)

    def _effectChanged(self):
        for effect in self.effectsGroup.children():
            if not isinstance(effect, QRadioButton):
                continue
            if effect.isChecked():
                self._currentHeadData.effect = str(effect.text()).lower()
                if not self.muteButton.isChecked():
                    DBMidi.playHeadData(self._currentHeadData)
                break

    def _lockChanged(self):
        self._currentDrum.locked = self.lockedCheckBox.isChecked()

    def _populateMidiCombo(self):
        for midiNote, midiName in _MIDIDATA:
            self.midiNoteCombo.addItem(midiName, userData = QVariant(midiNote))

    def _checkNotationButtons(self):
        headData = self._currentHeadData
        line = headData.notationLine
        self.noteUpButton.setDisabled(line >= 9)
        self.noteDownButton.setDisabled(line <= -7)


    def _setNotation(self):
        headData = self._currentHeadData
        self.stemUpDownBox.setChecked(headData.stemDirection
                                      == DrumKit.STEM_UP)
        effectIndex = self.effectBox.findText(headData.notationEffect)
        self.effectBox.setCurrentIndex(effectIndex)
        headIndex = self.noteHeadBox.findText(headData.notationHead)
        self.noteHeadBox.setCurrentIndex(headIndex)
        self._notationScene.setHeadData(headData)
        self._checkNotationButtons()

    def _notationEffectChanged(self):
        self._currentHeadData.notationEffect = str(self.effectBox.currentText())
        self._notationScene.setHeadData(self._currentHeadData)

    def _notationHeadChanged(self):
        self._currentHeadData.notationHead = str(self.noteHeadBox.currentText())
        self._notationScene.setHeadData(self._currentHeadData)

    def _stemDirectionChanged(self):
        if self.stemUpDownBox.isChecked():
            self._currentHeadData.stemDirection = DrumKit.STEM_UP
        else:
            self._currentHeadData.stemDirection = DrumKit.STEM_DOWN
        self._notationScene.setHeadData(self._currentHeadData)

    def _moveNotationUp(self):
        self._currentHeadData.notationLine += 1
        self._notationScene.setHeadData(self._currentHeadData)
        self._checkNotationButtons()

    def _moveNotationDown(self):
        self._currentHeadData.notationLine -= 1
        self._notationScene.setHeadData(self._currentHeadData)
        self._checkNotationButtons()

    def accept(self):
        if all(old == -1 for old in self._oldLines.itervalues()):
            if QMessageBox.question(self.parent(),
                                    "Discard all existing notes?",
                                    "Warning! You have changed the kit, but none of the old drums are being converted to new drums. This will discard all notes currently in the score. Are you sure you want to proceed?",
                                    buttons = QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
                return
        super(QEditKitDialog, self).accept()

    def getNewKit(self):
        newKit = DrumKit.DrumKit()
        oldLines = []
        for drum in reversed(self._currentKit):
            newKit.addDrum(drum)
            if self._oldLines[drum] == -1:
                oldLines.append(-1)
            else:
                oldLines.append(len(self._initialKit)
                                - self._oldLines[drum] - 1)
        return newKit, oldLines

_MIDIDATA = [(35, "Acoustic Bass Drum"),
             (36, "Bass Drum 1"),
             (37, "Side Stick"),
             (38, "Acoustic Snare"),
             (39, "Hand Clap"),
             (40, "Electric Snare"),
             (41, "Low Floor Tom"),
             (42, "Closed Hi Hat"),
             (43, "High Floor Tom"),
             (44, "Pedal Hi Hat"),
             (45, "Low Tom"),
             (46, "Open Hi Hat"),
             (47, "Low-Mid Tom"),
             (48, "Hi-Mid Tom"),
             (49, "Crash Cymbal 1"),
             (50, "High Tom"),
             (51, "Ride Cymbal 1"),
             (52, "Chinese Cymbal"),
             (53, "Ride Bell"),
             (54, "Tambourine"),
             (55, "Splash Cymbal"),
             (56, "Cowbell"),
             (57, "Crash Cymbal 2"),
             (58, "Vibraslap"),
             (59, "Ride Cymbal 2"),
             (60, "Hi Bongo"),
             (61, "Low Bongo"),
             (62, "Mute Hi Conga"),
             (63, "Open Hi Conga"),
             (64, "Low Conga"),
             (65, "High Timbale"),
             (66, "Low Timbale"),
             (67, "High Agogo"),
             (68, "Low Agogo"),
             (69, "Cabasa"),
             (70, "Maracas"),
             (71, "Short Whistle"),
             (72, "Long Whistle"),
             (73, "Short Guiro"),
             (74, "Long Guiro"),
             (75, "Claves"),
             (76, "Hi Wood Block"),
             (77, "Low Wood Block"),
             (78, "Mute Cuica"),
             (79, "Open Cuica"),
             (80, "Mute Triangle"),
             (81, "Open Triangle")]



def main():
    from PyQt4.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    kit = DrumKit.getNamedDefaultKit()
    dialog = QEditKitDialog(kit, [kit[0]])
    dialog.show()
    app.exec_()
    if dialog.result():
        kitname, ok = QInputDialog.getText(None, "Enter new kit name",
                                           "Kit name")
        if not ok:
            return
        kitname = unicode(kitname)
        kitvar = kitname.upper()
        kitvar = "".join([ch if ch.isalnum() else "_" for ch in kitvar])
        kitvar = "_" + kitvar
        newKit, changes_ = dialog.getNewKit()
        lines = []
        indent = '%s_DRUMS = [' % kitvar
        for drum in newKit:
            line = indent
            headData = drum.headData(drum.head)
            values = (drum.name, drum.abbr, drum.head, str(drum.locked),
                      headData.midiNote, headData.effect, headData.notationLine,
                      "UP" if headData.stemDirection == DrumKit.STEM_UP
                      else "DOWN")
            line += '(("%s", "%s", "%s", %s), %d, "%s", %d, STEM_%s)' % values
            lines.append(line)
            indent = " " * len(indent)
        lines = ("," + os.linesep).join(lines) + "]"
        print lines
        indent = '%s_HEADS = {' % kitvar
        lines = []
        volumeSymbols = {GHOST_VOLUME: "GHOST_VOLUME",
                         ACCENT_VOLUME:"ACCENT_VOLUME"}
        for drum in newKit:
            headLines = []
            headIndent = indent + '"%s" : [' % drum.abbr
            defaultData = drum.headData(drum.head)
            for head in drum:
                if head == drum.head:
                    continue
                data = drum.headData(head)
                line = headIndent
                values = (head,
                          "None" if data.midiNote == defaultData.midiNote
                          else str(data.midiNote),
                          "None" if data.midiVolume == defaultData.midiVolume
                          else volumeSymbols.get(data.midiVolume,
                                                str(data.midiVolume)),
                          data.effect, data.notationHead,
                          data.notationEffect, data.shortcut)
                line += '("%s", %s, %s, "%s", "%s", "%s", "%s")' % values
                headLines.append(line)
                headIndent = ' ' * len(headIndent)
            if headLines:
                headLines = ("," + os.linesep).join(headLines) + "]"
                lines.append(headLines)
                indent = ' ' * len(indent)
        if lines:
            lines = ("," + os.linesep).join(lines) + "}"
        else:
            lines = '%s_HEADS = {}' % kitvar
        print lines
        print ('%s_KIT = {"drums":%s_DRUMS, "heads":%s_HEADS}'
               % (kitvar, kitvar, kitvar))
        print 'NAMED_DEFAULTS["%s"] = %s_KIT' % (kitname, kitvar)
        print 'DEFAULT_KIT_NAMES.append("%s")' % kitname


if __name__ == "__main__":
    main()
