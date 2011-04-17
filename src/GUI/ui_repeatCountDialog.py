# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\repeatCountDialog.ui'
#
# Created: Sun Apr 17 16:05:24 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_repeatCountDialog(object):
    def setupUi(self, repeatCountDialog):
        repeatCountDialog.setObjectName(_fromUtf8("repeatCountDialog"))
        repeatCountDialog.resize(174, 81)
        self.verticalLayout = QtGui.QVBoxLayout(repeatCountDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label = QtGui.QLabel(repeatCountDialog)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.countBox = QtGui.QSpinBox(repeatCountDialog)
        self.countBox.setMinimum(2)
        self.countBox.setMaximum(128)
        self.countBox.setObjectName(_fromUtf8("countBox"))
        self.horizontalLayout.addWidget(self.countBox)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem3 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.buttonBox = QtGui.QDialogButtonBox(repeatCountDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(repeatCountDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), repeatCountDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), repeatCountDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(repeatCountDialog)

    def retranslateUi(self, repeatCountDialog):
        repeatCountDialog.setWindowTitle(QtGui.QApplication.translate("repeatCountDialog", "Set repeat count", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("repeatCountDialog", "Repeat count", None, QtGui.QApplication.UnicodeUTF8))

