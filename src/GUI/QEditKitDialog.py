'''
Created on 26 Jan 2011

@author: Mike Thomas

'''
from PyQt4.QtGui import QDialog, QTableWidgetItem, QCheckBox, QHBoxLayout, QFrame, QHeaderView, QComboBox
from ui_editKit import Ui_editKitDialog
from PyQt4.QtCore import pyqtSignature, Qt, QVariant, SIGNAL
from Data.DrumKit import DrumKit
from Data.Drum import Drum
import copy

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
        self._kit = kit
        header = self.kitTable.horizontalHeader()
        header.setResizeMode(0, QHeaderView.Stretch)
        header.setResizeMode(1, QHeaderView.ResizeToContents)
        header.setResizeMode(2, QHeaderView.ResizeToContents)
        header.setResizeMode(3, QHeaderView.ResizeToContents)
        header.setResizeMode(4, QHeaderView.ResizeToContents)
        self._populate()
        self.kitTable.selectRow(0)

    def _populate(self):
        self.kitTable.setRowCount(len(self._kit))
        drums = list(self._kit)
        drums.reverse()
        for row, drum in enumerate(drums):
            self._setDrum(drum, row, len(self._kit) - row - 1)

    def _setDrum(self, drum, row, previous):
        name = QTableWidgetItem(drum.name)
        self.kitTable.setItem(row, 0, name)
        abbr = QTableWidgetItem(drum.abbr)
        abbr.setTextAlignment(Qt.AlignCenter)
        self.kitTable.setItem(row, 1, abbr)
        head = QTableWidgetItem(drum.head)
        head.setTextAlignment(Qt.AlignCenter)
        self.kitTable.setItem(row, 2, head)
        layout = QHBoxLayout()
        check = QCheckBox(self)
        check.setChecked(drum.locked)
        layout.addWidget(check, alignment = Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        frame = QFrame()
        frame.setLayout(layout)
        self.kitTable.setCellWidget(row, 3, frame)
        combo = self._createCombo(previous)
        def focusOnRow(dummy = None):
            self.kitTable.selectRow(row)
            self.kitTable.setFocus()
        self.connect(check, SIGNAL("clicked()"),
                     focusOnRow)
        self.connect(combo, SIGNAL("activated(int)"),
                     focusOnRow)
        self.kitTable.setCellWidget(row, 4, combo)
        return name

    def _getData(self, row):
        name = unicode(self.kitTable.item(row, 0).text())
        abbr = unicode(self.kitTable.item(row, 1).text())
        head = unicode(self.kitTable.item(row, 2).text())
        frame = self.kitTable.cellWidget(row, 3)
        check = None
        for child in frame.children():
            if isinstance(child, QCheckBox):
                check = child
                break
        locked = check.isChecked()
        drum = Drum(name, abbr, head, locked)
        combo = self.kitTable.cellWidget(row, 4)
        previous = combo.itemData(combo.currentIndex()).toInt()[0]
        return drum, previous

    def _switchRows(self, row1, row2):
        drum1, previous1 = self._getData(row1)
        drum2, previous2 = self._getData(row2)
        self._setDrum(drum1, row2, previous1)
        self._setDrum(drum2, row1, previous2)

    def _createCombo(self, index):
        combo = QComboBox(self.kitTable)
        combo.addItem("None", userData = QVariant(-1))
        if index == -1:
            combo.setCurrentIndex(0)
        for drumIndex, drum in enumerate(self._kit):
            combo.addItem(drum.name, userData = QVariant(drumIndex))
            if drumIndex == index:
                combo.setCurrentIndex(index + 1)
        combo.setEditable(False)
        return combo

    @pyqtSignature("")
    def on_resetButton_clicked(self):
        self._populate()
        self.kitTable.scrollToTop()
        self.kitTable.selectRow(0)
        self.kitTable.setFocus()

    @pyqtSignature("")
    def on_clearButton_clicked(self):
        self.kitTable.setRowCount(0)
        self.kitTable.scrollToTop()

    @pyqtSignature("")
    def on_deleteButton_clicked(self):
        row = self.kitTable.currentRow()
        self.kitTable.removeRow(row)
        self.kitTable.selectRow(max(0, row - 1))
        self.kitTable.setFocus()

    @pyqtSignature("")
    def on_addButton_clicked(self):
        row = self.kitTable.rowCount()
        self.kitTable.setRowCount(row + 1)
        drum = Drum("New Drum", "??", "x")
        name = self._setDrum(drum, row, -1)
        self.kitTable.scrollToItem(name)
        self.kitTable.selectRow(row)
        self.kitTable.setFocus()

    @pyqtSignature("int, int, int, int")
    def on_kitTable_currentCellChanged(self, currentRow, *dummyArgs):
        self.downButton.setEnabled(currentRow != -1
                                   and currentRow != self.kitTable.rowCount() - 1)
        self.upButton.setEnabled(currentRow != -1
                                 and currentRow != 0)

    @pyqtSignature("")
    def on_downButton_clicked(self):
        row = self.kitTable.currentRow()
        self._switchRows(row, row + 1)
        self.kitTable.selectRow(row + 1)
        self.kitTable.setFocus()

    @pyqtSignature("")
    def on_upButton_clicked(self):
        row = self.kitTable.currentRow()
        self._switchRows(row, row - 1)
        self.kitTable.selectRow(row - 1)
        self.kitTable.setFocus()


def main():
    from PyQt4.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    kit = DrumKit()
    kit.loadDefaultKit()
    dialog = QEditKitDialog(kit)
    dialog.show()
    app.exec_()

if __name__ == "__main__":
    main()
