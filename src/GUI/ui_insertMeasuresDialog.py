# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\insertMeasuresDialog.ui'
#
# Created: Sun Jan 09 23:39:50 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_InsertMeasuresDialog(object):
    def setupUi(self, InsertMeasuresDialog):
        InsertMeasuresDialog.setObjectName(_fromUtf8("InsertMeasuresDialog"))
        InsertMeasuresDialog.resize(231, 129)
        self.verticalLayout = QtGui.QVBoxLayout(InsertMeasuresDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(InsertMeasuresDialog)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.numMeasuresSpinBox = QtGui.QSpinBox(InsertMeasuresDialog)
        self.numMeasuresSpinBox.setSuffix(_fromUtf8(""))
        self.numMeasuresSpinBox.setMinimum(1)
        self.numMeasuresSpinBox.setMaximum(1000)
        self.numMeasuresSpinBox.setProperty(_fromUtf8("value"), 1)
        self.numMeasuresSpinBox.setObjectName(_fromUtf8("numMeasuresSpinBox"))
        self.gridLayout.addWidget(self.numMeasuresSpinBox, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(InsertMeasuresDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.measureSizeSpinBox = QtGui.QSpinBox(InsertMeasuresDialog)
        self.measureSizeSpinBox.setMinimum(1)
        self.measureSizeSpinBox.setMaximum(256)
        self.measureSizeSpinBox.setObjectName(_fromUtf8("measureSizeSpinBox"))
        self.gridLayout.addWidget(self.measureSizeSpinBox, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(InsertMeasuresDialog)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.beforeButton = QtGui.QRadioButton(InsertMeasuresDialog)
        self.beforeButton.setChecked(True)
        self.beforeButton.setObjectName(_fromUtf8("beforeButton"))
        self.horizontalLayout.addWidget(self.beforeButton)
        self.afterButton = QtGui.QRadioButton(InsertMeasuresDialog)
        self.afterButton.setObjectName(_fromUtf8("afterButton"))
        self.horizontalLayout.addWidget(self.afterButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.buttonBox = QtGui.QDialogButtonBox(InsertMeasuresDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.numMeasuresSpinBox)
        self.label_2.setBuddy(self.measureSizeSpinBox)
        self.label_3.setBuddy(self.beforeButton)

        self.retranslateUi(InsertMeasuresDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), InsertMeasuresDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), InsertMeasuresDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InsertMeasuresDialog)

    def retranslateUi(self, InsertMeasuresDialog):
        InsertMeasuresDialog.setWindowTitle(QtGui.QApplication.translate("InsertMeasuresDialog", "Insert Measures", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("InsertMeasuresDialog", "Number of measures", None, QtGui.QApplication.UnicodeUTF8))
        self.numMeasuresSpinBox.setToolTip(QtGui.QApplication.translate("InsertMeasuresDialog", "Number of measures to insert", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("InsertMeasuresDialog", "Measure size", None, QtGui.QApplication.UnicodeUTF8))
        self.measureSizeSpinBox.setToolTip(QtGui.QApplication.translate("InsertMeasuresDialog", "Size of each measure in ticks", None, QtGui.QApplication.UnicodeUTF8))
        self.measureSizeSpinBox.setSuffix(QtGui.QApplication.translate("InsertMeasuresDialog", " ticks", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("InsertMeasuresDialog", "Insert Measures...", None, QtGui.QApplication.UnicodeUTF8))
        self.beforeButton.setToolTip(QtGui.QApplication.translate("InsertMeasuresDialog", "Insert new measures before the current measure", None, QtGui.QApplication.UnicodeUTF8))
        self.beforeButton.setText(QtGui.QApplication.translate("InsertMeasuresDialog", "Before", None, QtGui.QApplication.UnicodeUTF8))
        self.afterButton.setToolTip(QtGui.QApplication.translate("InsertMeasuresDialog", "Insert new measures after the current measure", None, QtGui.QApplication.UnicodeUTF8))
        self.afterButton.setText(QtGui.QApplication.translate("InsertMeasuresDialog", "After", None, QtGui.QApplication.UnicodeUTF8))

