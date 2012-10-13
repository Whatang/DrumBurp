# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\defaultKitManager.ui'
#
# Created: Sat Oct 13 16:38:05 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DefaulKitManager(object):
    def setupUi(self, DefaulKitManager):
        DefaulKitManager.setObjectName(_fromUtf8("DefaulKitManager"))
        DefaulKitManager.resize(353, 311)
        self.horizontalLayout = QtGui.QHBoxLayout(DefaulKitManager)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.defaultKitList = QtGui.QListWidget(DefaulKitManager)
        self.defaultKitList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.defaultKitList.setProperty("showDropIndicator", False)
        self.defaultKitList.setObjectName(_fromUtf8("defaultKitList"))
        self.horizontalLayout.addWidget(self.defaultKitList)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.saveButton = QtGui.QPushButton(DefaulKitManager)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.verticalLayout.addWidget(self.saveButton)
        self.overwriteButton = QtGui.QPushButton(DefaulKitManager)
        self.overwriteButton.setObjectName(_fromUtf8("overwriteButton"))
        self.verticalLayout.addWidget(self.overwriteButton)
        self.deleteButton = QtGui.QPushButton(DefaulKitManager)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.verticalLayout.addWidget(self.deleteButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.openButton = QtGui.QPushButton(DefaulKitManager)
        self.openButton.setObjectName(_fromUtf8("openButton"))
        self.verticalLayout.addWidget(self.openButton)
        self.cancelButton = QtGui.QPushButton(DefaulKitManager)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.verticalLayout.addWidget(self.cancelButton)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(DefaulKitManager)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), DefaulKitManager.reject)
        QtCore.QObject.connect(self.openButton, QtCore.SIGNAL(_fromUtf8("clicked()")), DefaulKitManager.accept)
        QtCore.QObject.connect(self.defaultKitList, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), DefaulKitManager.accept)
        QtCore.QMetaObject.connectSlotsByName(DefaulKitManager)
        DefaulKitManager.setTabOrder(self.defaultKitList, self.saveButton)
        DefaulKitManager.setTabOrder(self.saveButton, self.overwriteButton)
        DefaulKitManager.setTabOrder(self.overwriteButton, self.deleteButton)
        DefaulKitManager.setTabOrder(self.deleteButton, self.openButton)
        DefaulKitManager.setTabOrder(self.openButton, self.cancelButton)

    def retranslateUi(self, DefaulKitManager):
        DefaulKitManager.setWindowTitle(QtGui.QApplication.translate("DefaulKitManager", "Default Kit Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultKitList.setToolTip(QtGui.QApplication.translate("DefaulKitManager", "Available default kits", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultKitList.setWhatsThis(QtGui.QApplication.translate("DefaulKitManager", "<html><head/><body><p><span style=\" font-weight:600;\">Default kit list</span></p><p><br/></p><p>Kits listed here can be loaded into the kit editor by double-clicking, or selecting them and clicking the <span style=\" font-style:italic;\">Open</span> button.</p><p><br/></p><p>Kits listed in <span style=\" font-style:italic;\">italics</span> are built into DrumBurp and cannot be overwritten, deleted or renamed.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setToolTip(QtGui.QApplication.translate("DefaulKitManager", "Save the current kit as a new default", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setWhatsThis(QtGui.QApplication.translate("DefaulKitManager", "<html><head/><body><p><span style=\" font-weight:600;\">Save a new default kit</span></p><p><br/></p><p>Save the kit currently loaded in the kit editor as a new default. You will be asked a name to save it under, then it will appear in this dialog whenever you run DrumBurp in the future.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("DefaulKitManager", "Save New", None, QtGui.QApplication.UnicodeUTF8))
        self.overwriteButton.setToolTip(QtGui.QApplication.translate("DefaulKitManager", "Overwrite this default kit", None, QtGui.QApplication.UnicodeUTF8))
        self.overwriteButton.setWhatsThis(QtGui.QApplication.translate("DefaulKitManager", "<html><head/><body><p><span style=\" font-weight:600;\">Overwrite this default kit</span></p><p><br/></p><p>The currently selected default kit will be overwritten with the kit currently loaded into the kit editor.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.overwriteButton.setText(QtGui.QApplication.translate("DefaulKitManager", "Overwrite", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setToolTip(QtGui.QApplication.translate("DefaulKitManager", "Delete this default kit", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setWhatsThis(QtGui.QApplication.translate("DefaulKitManager", "<html><head/><body><p><span style=\" font-weight:600;\">Delete this default kit</span></p><p><br/></p><p>Delete this default kit from the default kit list. DrumBurp builtin default kits cannot be deleted.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("DefaulKitManager", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.openButton.setToolTip(QtGui.QApplication.translate("DefaulKitManager", "Load this default kit", None, QtGui.QApplication.UnicodeUTF8))
        self.openButton.setWhatsThis(QtGui.QApplication.translate("DefaulKitManager", "<html><head/><body><p><span style=\" font-weight:600;\">Load default kit</span></p><p><br/></p><p>Load the currently selected default kit into the kit editor.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.openButton.setText(QtGui.QApplication.translate("DefaulKitManager", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setToolTip(QtGui.QApplication.translate("DefaulKitManager", "Cancel this dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("DefaulKitManager", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

