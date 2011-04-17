# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\alternateRepeats.ui'
#
# Created: Sun Apr 17 16:05:19 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AlternateDialog(object):
    def setupUi(self, AlternateDialog):
        AlternateDialog.setObjectName(_fromUtf8("AlternateDialog"))
        AlternateDialog.resize(244, 92)
        self.gridLayout = QtGui.QGridLayout(AlternateDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(AlternateDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.repeatText = QtGui.QLineEdit(AlternateDialog)
        self.repeatText.setObjectName(_fromUtf8("repeatText"))
        self.gridLayout.addWidget(self.repeatText, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(AlternateDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(AlternateDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AlternateDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AlternateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AlternateDialog)

    def retranslateUi(self, AlternateDialog):
        AlternateDialog.setWindowTitle(QtGui.QApplication.translate("AlternateDialog", "Alternate Repeats", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AlternateDialog", "Enter alternate repeat information:", None, QtGui.QApplication.UnicodeUTF8))

