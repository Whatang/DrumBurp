# Copyright 2011 Michael Thomas
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
from PyQt4.QtCore import pyqtSignature, Qt, QVariant
from Data.DrumKit import DrumKit
from Data.Drum import Drum
import copy
import string

class QEditKitDialog(QDialog, Ui_editKitDialog):
    '''
    classdocs
    '''

    def __init__(self, kit, parent = None):
        '''
        Constructor
        '''
        super(QEditKitDialog, self).__init__(parent)
        self.setupUi(self)
        self._currentKit = []
        self._oldLines = []
        self._initialKit = kit
        self._populate()
        self.kitTable.currentRowChanged.connect(self._drumChanged)
        self.upButton.clicked.connect(self._moveDrumUp)
        self.downButton.clicked.connect(self._moveDrumDown)
        self.addButton.clicked.connect(self._addDrum)
        self.deleteButton.clicked.connect(self._removeDrum)
        self.clearButton.clicked.connect(self._clearKit)
        self.clearButton.setDisabled(True)
        self.resetButton.clicked.connect(self._resetKit)
        self.resetButton.setDisabled(True)
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
        self._populateMidiCombo()
        self.midiNoteCombo.currentIndexChanged.connect(self._midiNoteChanged)
        self.volumeSlider.valueChanged.connect(self._midiVolumeChanged)
        for effect in self.effectsGroup.children():
            if isinstance(effect, QRadioButton):
                effect.toggled.connect(self._effectChanged)
        self.lockedCheckBox.stateChanged.connect(self._lockChanged)
        self.kitTable.setCurrentRow(0)


    def _populate(self):
        self.oldDrum.addItem("None", userData = QVariant(-1))
        for drumIndex, drum in enumerate(reversed(self._initialKit)):
            self.kitTable.insertItem(drumIndex, drum.name)
            self._currentKit.append(copy.deepcopy(drum))
            self.oldDrum.addItem(drum.name, userData = QVariant(drumIndex))
            self._oldLines.append(drumIndex)
        self._checkEnoughDrums()

    @property
    def _currentDrumIndex(self):
        return self.kitTable.currentRow()

    @property
    def _currentDrum(self):
        drumIndex = self._currentDrumIndex
        return self._currentKit[drumIndex]

    def _checkEnoughDrums(self):
        self.deleteButton.setEnabled(len(self._currentKit) > 1)

    def _drumChanged(self):
        self._checkDrumMoveButtons()
        drumIndex = self._currentDrumIndex
        drum = self._currentDrum
        self.drumName.setText(drum.name)
        self.drumAbbr.setText(drum.abbr)
        self.oldDrum.setCurrentIndex(self._oldLines[drumIndex] + 1)
        self.lockedCheckBox.setChecked(drum.locked)
        self._populateHeadTable()
        self.noteHeadTable.blockSignals(False)

    def _addDrum(self):
        drum = Drum("New drum", "XX", "x")
        self._currentKit.append(drum)
        self._oldLines.append(-1)
        self.kitTable.addItem(drum.name)
        self.kitTable.setCurrentRow(len(self._currentKit) - 1)
        self._checkEnoughDrums()

    def _removeDrum(self):
        index = self._currentDrumIndex
        self._currentKit = self._currentKit[:index] + self._currentKit[index + 1:]
        self._oldLines = self._oldLines[:index] + self._oldLines[index + 1:]
        if index < len(self._currentKit) - 1 :
            self._drumChanged()
        else:
            self.kitTable.setCurrentRow(index - 1)
        self.kitTable.takeItem(index)
        self._checkEnoughDrums()

    def _checkDrumMoveButtons(self):
        index = self._currentDrumIndex
        self.upButton.setEnabled(index > 0)
        self.downButton.setEnabled(index < len(self._currentKit) - 1)

    def _moveDrumUp(self):
        index = self._currentDrumIndex
        self._currentKit[index - 1:index + 1] = reversed(self._currentKit[index - 1:index + 1])
        self._oldLines[index - 1:index + 1] = reversed(self._oldLines[index - 1:index + 1])
        self.kitTable.item(index).setText(self._currentKit[index].name)
        self.kitTable.item(index - 1).setText(self._currentKit[index - 1].name)
        self.kitTable.setCurrentRow(index - 1)

    def _moveDrumDown(self):
        index = self._currentDrumIndex
        self._currentKit[index:index + 2] = reversed(self._currentKit[index:index + 2])
        self._oldLines[index:index + 2] = reversed(self._oldLines[index:index + 2])
        self.kitTable.item(index).setText(self._currentKit[index].name)
        self.kitTable.item(index + 1).setText(self._currentKit[index + 1].name)
        self.kitTable.setCurrentRow(index + 1)

    def _clearKit(self):
        pass

    def _resetKit(self):
        pass

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
        drumIndex = self._currentDrumIndex
        newOldDrumIndex = self.oldDrum.currentIndex()
        newOldDrumIndex = self.oldDrum.itemData(newOldDrumIndex).toInt()[0]
        self._oldLines[drumIndex] = newOldDrumIndex

    def _populateHeadTable(self):
        self.noteHeadTable.blockSignals(True)
        drum = self._currentDrum
        self.noteHeadTable.clear()
        for head in drum.noteHeads:
            headString = head
            if head == drum.head:
                headString += " (Default)"
            self.noteHeadTable.addItem(headString)
        self.noteHeadTable.blockSignals(False)
        self.noteHeadTable.setCurrentRow(0)

    @property
    def _currentHead(self):
        drum = self._currentDrum
        row = self.noteHeadTable.currentRow()
        head = drum.noteHeads[row]
        return head

    @property
    def _currentHeadData(self):
        drum = self._currentDrum
        row = self.noteHeadTable.currentRow()
        head = drum.noteHeads[row]
        return drum.headData[head]

    def _checkHeadDelete(self):
        self.deleteHeadButton.setEnabled(self._currentHead != self._currentDrum.head)

    def _headEdited(self):
        noteHead = str(self.currentNoteHead.currentText())
        row = self.noteHeadTable.currentRow()
        drum = self._currentDrum
        oldHead = drum.noteHeads[row]
        drum.renameHead(oldHead, noteHead)
        headString = noteHead
        if noteHead == drum.head:
            headString += " (Default)"
        self.noteHeadTable.item(row).setText(headString)
        self._populateCurrentNoteHead()

    def _noteHeadChanged(self):
        self._populateCurrentNoteHead()
        headIndex = self.currentNoteHead.findText(self._currentHead)
        self.currentNoteHead.setCurrentIndex(headIndex)
        headData = self._currentHeadData
        self.volumeSlider.setValue(headData.midiVolume)
        midiIndex = self.midiNoteCombo.findData(QVariant(headData.midiNote))
        self.midiNoteCombo.setCurrentIndex(midiIndex)
        self._setEffect(headData.effect)
        self._checkHeadDelete()
        self._checkHeadMoveButtons()

    def _populateCurrentNoteHead(self):
        self.currentNoteHead.blockSignals(True)
        try:
            badNotes = set(self._currentDrum.noteHeads)
            badNotes.remove(self._currentHead)
            badNotes.update(["-", "|"])
            for head in string.printable:
                if head in badNotes:
                    continue
                self.currentNoteHead.addItem(head)
        finally:
            self.currentNoteHead.blockSignals(False)

    def _addNoteHead(self):
        pass

    def _removeNoteHead(self):
        pass

    def _checkHeadMoveButtons(self):
        index = self.noteHeadTable.currentRow()
        self.headUpButton.setEnabled(index > 0)
        self.headDownButton.setEnabled(index < len(self._currentDrum.noteHeads) - 1)

    def _moveNoteHeadUp(self):
        pass

    def _moveNoteHeadDown(self):
        pass

    def _setDefaultHead(self):
        self.noteHeadTable.blockSignals(True)
        index = self.noteHeadTable.currentIndex()
        self._currentDrum.head = self._currentHead
        self._populateHeadTable()
        self.noteHeadTable.blockSignals(False)
        self.noteHeadTable.setCurrentIndex(index)


    def _midiNoteChanged(self):
        midiNote = self.midiNoteCombo.currentIndex()
        midiNote = self.midiNoteCombo.itemData(midiNote).toInt()[0]
        self._currentHeadData.midiNote = midiNote

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

    def _lockChanged(self):
        pass

    def _populateMidiCombo(self):
        for midiNote, midiName in _MIDIDATA:
            self.midiNoteCombo.addItem(midiName, userData = QVariant(midiNote))

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

#class Bob(object):
#
##        header.setResizeMode(3, QHeaderView.ResizeToContents)
##        header.setResizeMode(4, QHeaderView.ResizeToContents)
##        self._populate()
##        self.kitTable.selectRow(0)
##        self.kitTable.itemChanged.connect(self._checkItem)
#
#    def _populate(self):
#        self.kitTable.setRowCount(len(self._kit))
#        drums = list(self._kit)
#        drums.reverse()
#        for row, drum in enumerate(drums):
#            self._setDrum(drum, row, len(self._kit) - row - 1)
#
#    def _setDrum(self, drum, row, previous):
#        name = QTableWidgetItem(drum.name)
#        self.kitTable.setItem(row, 0, name)
#        abbr = QTableWidgetItem(drum.abbr)
#        abbr.setTextAlignment(Qt.AlignCenter)
#        self.kitTable.setItem(row, 1, abbr)
#        head = QTableWidgetItem(drum.head)
#        head.setTextAlignment(Qt.AlignCenter)
#        self.kitTable.setItem(row, 2, head)
#        layout = QHBoxLayout()
#        check = QCheckBox(self)
#        check.setChecked(drum.locked)
#        layout.addWidget(check, alignment = Qt.AlignCenter)
#        layout.setContentsMargins(0, 0, 0, 0)
#        frame = QFrame()
#        frame.setLayout(layout)
#        self.kitTable.setCellWidget(row, 3, frame)
#        combo = self._createCombo(previous)
#        def focusOnRow(dummy = None):
#            self.kitTable.selectRow(self.kitTable.currentRow())
#            self.kitTable.setFocus()
#        check.clicked.connect(focusOnRow)
#        combo.activated.connect(focusOnRow)
#        def callExclusive(newValue):
#            qv = combo.itemData(newValue)
#            newValue = qv.toInt()[0]
#            self._exclusiveCombos(self.kitTable.currentRow(), newValue)
#        combo.currentIndexChanged.connect(callExclusive)
#        self.kitTable.setCellWidget(row, 4, combo)
#        return name
#
#    def _exclusiveCombos(self, row, newValue):
#        if newValue == -1:
#            return
#        for otherRow in range(self.kitTable.rowCount()):
#            if otherRow == row:
#                continue
#            combo = self.kitTable.cellWidget(otherRow, 4)
#            currentValue = combo.itemData(combo.currentIndex())
#            currentValue = currentValue.toInt()[0]
#            if currentValue == newValue:
#                combo.setCurrentIndex(0)
#
#    def _getData(self, row):
#        name = unicode(self.kitTable.item(row, 0).text())
#        abbr = unicode(self.kitTable.item(row, 1).text())
#        head = unicode(self.kitTable.item(row, 2).text())
#        frame = self.kitTable.cellWidget(row, 3)
#        check = None
#        for child in frame.children():
#            if isinstance(child, QCheckBox):
#                check = child
#                break
#        locked = check.isChecked()
#        drum = Drum(name, abbr, head, locked)
#        combo = self.kitTable.cellWidget(row, 4)
#        previous = combo.itemData(combo.currentIndex()).toInt()[0]
#        return drum, previous
#
#    def _switchRows(self, row1, row2):
#        drum1, previous1 = self._getData(row1)
#        drum2, previous2 = self._getData(row2)
#        self._setDrum(drum1, row2, previous1)
#        self._setDrum(drum2, row1, previous2)
#
#    def _createCombo(self, index):
#        combo = QComboBox(self.kitTable)
#        combo.addItem("None", userData = QVariant(-1))
#        if index == -1:
#            combo.setCurrentIndex(0)
#        for drumIndex, drum in enumerate(self._kit):
#            combo.addItem(drum.name, userData = QVariant(drumIndex))
#            if drumIndex == index:
#                combo.setCurrentIndex(index + 1)
#        combo.setEditable(False)
#        return combo
#
#    @pyqtSignature("")
#    def on_resetButton_clicked(self):
#        self._populate()
#        self.kitTable.scrollToTop()
#        self.kitTable.selectRow(0)
#        self.kitTable.setFocus()
#
#    @pyqtSignature("")
#    def on_clearButton_clicked(self):
#        self.kitTable.setRowCount(0)
#        self.kitTable.scrollToTop()
#
#    @pyqtSignature("")
#    def on_deleteButton_clicked(self):
#        row = self.kitTable.currentRow()
#        self.kitTable.removeRow(row)
#        self.kitTable.selectRow(max(0, row - 1))
#        self.kitTable.setFocus()
#
#    @pyqtSignature("")
#    def on_addButton_clicked(self):
#        row = self.kitTable.rowCount()
#        self.kitTable.setRowCount(row + 1)
#        drum = Drum("New Drum", "??", "x")
#        name = self._setDrum(drum, row, -1)
#        self.kitTable.scrollToItem(name)
#        self.kitTable.selectRow(row)
#        self.kitTable.setFocus()
#
#    @pyqtSignature("int, int, int, int")
#    def on_kitTable_currentCellChanged(self, currentRow, *dummyArgs):
#        self.downButton.setEnabled(currentRow != -1
#                                   and (currentRow !=
#                                        self.kitTable.rowCount() - 1))
#        self.upButton.setEnabled(currentRow != -1
#                                 and currentRow != 0)
#
#    @pyqtSignature("")
#    def on_downButton_clicked(self):
#        row = self.kitTable.currentRow()
#        self._switchRows(row, row + 1)
#        self.kitTable.selectRow(row + 1)
#        self.kitTable.setFocus()
#
#    @pyqtSignature("")
#    def on_upButton_clicked(self):
#        row = self.kitTable.currentRow()
#        self._switchRows(row, row - 1)
#        self.kitTable.selectRow(row - 1)
#        self.kitTable.setFocus()
#
#    @pyqtSignature("QTableWidgetItem *")
#    def _checkItem(self, item):
#        if item.column() not in (1, 2):
#            return
#        elif item.column() == 1:
#            text = unicode(item.text())
#            if not 1 <= len(text) <= 2:
#                msg = "Abbreviations must be 1 or 2 characters long"
#                QMessageBox.warning(self,
#                                    "Bad abbreviation",
#                                    msg)
#                item.setText("??")
#                self.kitTable.selectItem(item)
#                self.kitTable.setFocus()
#        elif item.column() == 2:
#            text = unicode(item.text())
#            if len(text) != 1:
#                msg = "Default note heads must be a single character"
#                QMessageBox.warning(self,
#                                    "Bad note head",
#                                    msg)
#                item.setText("?")
#                self.kitTable.selectItem(item)
#                self.kitTable.setFocus()
#
#
#    def _validate(self):
#        badRow = -1
#        msg = ""
#        drumNames = set()
#        drumAbs = set()
#        for row in range(self.kitTable.rowCount()):
#            drum, dummyPrevious = self._getData(row)
#            if len(drum.name) == 0:
#                badRow = row
#                msg = "Drum %d has no name" % drum.name
#                break
#            elif drum.name in drumNames:
#                badRow = row
#                msg = "%s is a duplicated name" % drum.name
#                break
#            drumNames.add(drum.name)
#            if len(drum.abbr) == 0:
#                badRow = row
#                msg = "Drum %d has no abbreviation" % drum.abbr
#                break
#            elif drum.abbr in drumAbs:
#                badRow = row
#                msg = ("For %s, %s is a duplicated drum abbreviation"
#                       % (drum.name, drum.abbr))
#                break
#            drumAbs.add(drum.abbr)
#        return badRow == -1, badRow, msg
#
#    def _badKit(self, row, msg):
#        QMessageBox.warning(self,
#                            "Drum kit error",
#                            "There is a problem with the drum kit.\n\n" +
#                            msg)
#        self.kitTable.selectRow(row)
#        self.kitTable.setFocus()
#
#    def accept(self):
#        ok, badRow, msg = self._validate()
#        if ok:
#            super(QEditKitDialog, self).accept()
#        else:
#            self._badKit(badRow, msg)
#
#    def getNewKit(self):
#        numDrums = self.kitTable.rowCount()
#        indexes = range(numDrums)
#        indexes.reverse()
#        newKit = DrumKit()
#        changes = [-1] * len(self._kit)
#        for row in indexes:
#            drum, previous = self._getData(row)
#            newKit.addDrum(drum)
#            if previous != -1:
#                changes[previous] = numDrums - row - 1
#        return newKit, changes


def main():
    from PyQt4.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    kit = DrumKit()
    kit.loadDefaultKit()
    dialog = QEditKitDialog(kit)
    dialog.show()
    print kit
    app.exec_()
    if dialog.result():
        newKit, changes = dialog.getNewKit()
        print changes
        for drum in newKit:
            print drum.name
        for drum, change in zip(kit, changes):
            print drum.name, newKit[change].name if change != -1 else None

if __name__ == "__main__":
    main()
