# Copyright 2012 Michael Thomas
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
Created on 13 Oct 2012

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore
from cStringIO import StringIO
from GUI.ui_defaultKitManager import Ui_DefaulKitManager
from Data import DefaultKits, DrumKitFactory, DrumKitSerializer

_IS_USER_KIT = QtCore.Qt.UserRole

class QDefaultKitManager(Ui_DefaulKitManager, QtGui.QDialog):
    def __init__(self, currentKit, parent = None):
        super(QDefaultKitManager, self).__init__(parent)
        self.setupUi(self)
        self._currentKit = currentKit
        self._settings = QtCore.QSettings()
        self._settings.beginGroup("UserDefaultKits")
        self._populate()
        self.defaultKitList.currentItemChanged.connect(self._checkButtons)
        self.defaultKitList.setCurrentRow(0)
        self.openButton.setFocus()

    def _populate(self):
        self.defaultKitList.blockSignals(True)
        self.defaultKitList.clear()
        for kitName in DefaultKits.DEFAULT_KIT_NAMES:
            item = QtGui.QListWidgetItem(kitName, self.defaultKitList)
            font = item.font()
            font.setItalic(True)
            item.setFont(font)
            item.setData(_IS_USER_KIT, QtCore.QVariant(False))
        for kitName in self._settings.allKeys():
            item = QtGui.QListWidgetItem(kitName, self.defaultKitList)
            item.setData(_IS_USER_KIT, QtCore.QVariant(True))
        self.defaultKitList.blockSignals(False)

    def _checkButtons(self):
        item = self.defaultKitList.currentItem()
        if item:
            isUser = item.data(_IS_USER_KIT).toBool()
            self.openButton.setEnabled(True)
            self.overwriteButton.setEnabled(isUser)
            self.deleteButton.setEnabled(isUser)
        else:
            self.openButton.setEnabled(False)
            self.overwriteButton.setEnabled(False)
            self.deleteButton.setEnabled(False)


    @QtCore.pyqtSignature("")
    def on_deleteButton_clicked(self):
        item = self.defaultKitList.currentItem()
        if item:
            isUser = item.data(_IS_USER_KIT).toBool()
            if isUser:
                kitName = item.text()
                self._settings.remove(kitName)
                index = self.defaultKitList.currentRow()
                self._populate()
                if index >= self.defaultKitList.count():
                    index -= 1
                self.defaultKitList.setCurrentRow(index)

    def _writeKit(self, name):
        handle = StringIO()
        DrumKitSerializer.DrumKitSerializer.write(self._currentKit, handle)
        self._settings.setValue(name, handle.getvalue())
        self._populate()

    @QtCore.pyqtSignature("")
    def on_saveButton_clicked(self):
        name, ok = QtGui.QInputDialog.getText(self, "Kit name",
                                              "Enter a name for the "
                                              "new default kit",
                                              text = "New kit")
        if not ok:
            return
        if self._settings.contains(name):
            QtGui.QMessageBox.information(self,
                                          "Duplicate kit name!",
                                          "That kit name already exists.")
            return
        index = self.defaultKitList.currentRow()
        self._writeKit(name)
        self.defaultKitList.setCurrentRow(index)

    @QtCore.pyqtSignature("")
    def on_overwriteButton_clicked(self):
        item = self.defaultKitList.currentItem()
        if item:
            index = self.defaultKitList.currentRow()
            isUser = item.data(_IS_USER_KIT).toBool()
            if isUser:
                kitName = unicode(item.text())
                self._writeKit(kitName)
                self.defaultKitList.setCurrentRow(index)
            else:
                QtGui.QMessageBox.information(self,
                                              "Default kit",
                                              "Cannot overwrite default kits!")

    def getKit(self):
        item = self.defaultKitList.currentItem()
        isUser = item.data(_IS_USER_KIT).toBool()
        kitName = unicode(item.text())
        if isUser:
            kitString = unicode(self._settings.value(kitName).toString())
            handle = StringIO(kitString)
            return DrumKitSerializer.DrumKitSerializer.read(handle)
        else:
            return DrumKitFactory.DrumKitFactory.getNamedDefaultKit(kitName)


def main():
    from PyQt4.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    app.setOrganizationName("Whatang Software")
    app.setOrganizationDomain("whatang.org")
    app.setApplicationName("DefaultKitManagerTest")
    oldkit = DrumKitFactory.DrumKitFactory.getNamedDefaultKit()
    dialog = QDefaultKitManager(oldkit)
    dialog.show()
    app.exec_()
    if dialog.result():
        print dialog.getKit()

if __name__ == "__main__":
    main()
