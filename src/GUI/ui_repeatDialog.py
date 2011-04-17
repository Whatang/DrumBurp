# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\repeatDialog.ui'
#
# Created: Sun Apr 17 16:05:25 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RepeatDialog(object):
    def setupUi(self, RepeatDialog):
        RepeatDialog.setObjectName(_fromUtf8("RepeatDialog"))
        RepeatDialog.resize(215, 97)
        self.verticalLayout = QtGui.QVBoxLayout(RepeatDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(RepeatDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.numRepeatsSpinBox = QtGui.QSpinBox(RepeatDialog)
        self.numRepeatsSpinBox.setMinimum(1)
        self.numRepeatsSpinBox.setMaximum(1024)
        self.numRepeatsSpinBox.setObjectName(_fromUtf8("numRepeatsSpinBox"))
        self.gridLayout.addWidget(self.numRepeatsSpinBox, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(RepeatDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.repeatIntervalSpinBox = QtGui.QSpinBox(RepeatDialog)
        self.repeatIntervalSpinBox.setMinimum(1)
        self.repeatIntervalSpinBox.setMaximum(128)
        self.repeatIntervalSpinBox.setProperty(_fromUtf8("value"), 1)
        self.repeatIntervalSpinBox.setObjectName(_fromUtf8("repeatIntervalSpinBox"))
        self.gridLayout.addWidget(self.repeatIntervalSpinBox, 1, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(RepeatDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.numRepeatsSpinBox)
        self.label_2.setBuddy(self.repeatIntervalSpinBox)

        self.retranslateUi(RepeatDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RepeatDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RepeatDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RepeatDialog)

    def retranslateUi(self, RepeatDialog):
        RepeatDialog.setWindowTitle(QtGui.QApplication.translate("RepeatDialog", "Choose number of repeats", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setToolTip(QtGui.QApplication.translate("RepeatDialog", "Number of times to repeat this note", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RepeatDialog", "Number of repeats", None, QtGui.QApplication.UnicodeUTF8))
        self.numRepeatsSpinBox.setToolTip(QtGui.QApplication.translate("RepeatDialog", "Number of times to repeat this note", None, QtGui.QApplication.UnicodeUTF8))
        self.numRepeatsSpinBox.setSuffix(QtGui.QApplication.translate("RepeatDialog", " repeats", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setToolTip(QtGui.QApplication.translate("RepeatDialog", "Interval at which to repeat this note, in ticks", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("RepeatDialog", "Repeat interval", None, QtGui.QApplication.UnicodeUTF8))
        self.repeatIntervalSpinBox.setToolTip(QtGui.QApplication.translate("RepeatDialog", "Interval at which to repeat this note, in ticks", None, QtGui.QApplication.UnicodeUTF8))
        self.repeatIntervalSpinBox.setSuffix(QtGui.QApplication.translate("RepeatDialog", " ticks", None, QtGui.QApplication.UnicodeUTF8))

