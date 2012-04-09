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
from PyQt4.QtGui import QDialog, QRadioButton
from ui_editKit import Ui_editKitDialog
from PyQt4.QtCore import QVariant
from Data.DrumKit import DrumKit
from Data.Drum import Drum
import copy
import string #IGNORE:W0402
import DBMidi
from QNotationScene import QNotationScene

class QEditKitDialog(QDialog, Ui_editKitDialog):
    '''
    classdocs
    '''

    def __init__(self, kit, emptyDrums = None, parent = None):
        '''
        Constructor
        '''
        super(QEditKitDialog, self).__init__(parent)
        self.setupUi(self)
        if emptyDrums is None:
            emptyDrums = []
            self.deleteEmptyButton.setEnabled(False)
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
        self.effectBox.currentIndexChanged.connect(self._effectChanged)
        self.stemUpDownBox.stateChanged.connect(self._stemDirectionChanged)
        self.noteUpButton.clicked.connect(self._moveNotationUp)
        self.noteDownButton.clicked.connect(self._moveNotationDown)
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
        drum = Drum("New drum", "XX", "x")
        drum.guessHeadData()
        self._currentKit.append(drum)
        self._oldLines[drum] = -1
        self.kitTable.addItem(drum.name)
        self.kitTable.setCurrentRow(len(self._currentKit) - 1)
        self._checkDrumButtons()

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

    def _moveDrumUp(self):
        index = self._currentDrumIndex
        self._currentKit[index - 1:index + 1] = reversed(self._currentKit[index - 1:index + 1])
        self.kitTable.item(index).setText(self._currentKit[index].name)
        self.kitTable.item(index - 1).setText(self._currentKit[index - 1].name)
        self.kitTable.setCurrentRow(index - 1)

    def _moveDrumDown(self):
        index = self._currentDrumIndex
        self._currentKit[index:index + 2] = reversed(self._currentKit[index:index + 2])
        self.kitTable.item(index).setText(self._currentKit[index].name)
        self.kitTable.item(index + 1).setText(self._currentKit[index + 1].name)
        self.kitTable.setCurrentRow(index + 1)

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
        pass

    def _saveKit(self):
        pass

    def _drumNameEdited(self):
        self._currentDrum.name = unicode(self.drumName.text())
        drumIndex = self._currentDrumIndex
        self.kitTable.item(drumIndex).setText(self._currentDrum.name)

    def _drumAbbrEdited(self):
        self._currentDrum.abbr = unicode(self.drumAbbr.text())

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

    def _populateCurrentNoteHead(self):
        self.currentNoteHead.blockSignals(True)
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
        finally:
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

    def _setNotation(self):
        headData = self._currentHeadData
        self.stemUpDownBox.setChecked(headData.stemDirection == DrumKit.UP)
        effectIndex = self.effectBox.findText(headData.notationEffect)
        self.effectBox.setCurrentIndex(effectIndex)
        headIndex = self.noteHeadBox.findText(headData.notationHead)
        self.noteHeadBox.setCurrentIndex(headIndex)
        self._notationScene.setHeadData(headData)

    def _notationEffectChanged(self):
        self._currentHeadData.notationEffect = str(self.effectBox.currentText())
        self._notationScene.setHeadData(self._currentHeadData)

    def _notationHeadChanged(self):
        self._currentHeadData.notationHead = str(self.noteHeadBox.currentText())
        self._notationScene.setHeadData(self._currentHeadData)

    def _stemDirectionChanged(self):
        if self.stemUpDownBox.isChecked():
            self._currentHeadData.stemDirection = DrumKit.UP
        else:
            self._currentHeadData.stemDirection = DrumKit.DOWN
        self._notationScene.setHeadData(self._currentHeadData)

    def _moveNotationUp(self):
        self._currentHeadData.notationLine += 1
        self._notationScene.setHeadData(self._currentHeadData)

    def _moveNotationDown(self):
        self._currentHeadData.notationLine -= 1
        self._notationScene.setHeadData(self._currentHeadData)

    def getNewKit(self):
        newKit = DrumKit()
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
    kit = DrumKit()
    kit.loadDefaultKit()
    dialog = QEditKitDialog(kit, [kit[0]])
    dialog.show()
    print kit
    app.exec_()
    if dialog.result():
        newKit, changes = dialog.getNewKit()
        print changes
        for drum, oldDrumIndex in zip(newKit, changes):
            print (drum.name, kit[oldDrumIndex].name
                   if oldDrumIndex != -1
                   else None, drum.head)


if __name__ == "__main__":
    main()
