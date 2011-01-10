# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\newScoreDialog.ui'
#
# Created: Sun Jan 09 23:39:51 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_newScoreDialog(object):
    def setupUi(self, newScoreDialog):
        newScoreDialog.setObjectName(_fromUtf8("newScoreDialog"))
        newScoreDialog.resize(243, 109)
        newScoreDialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.verticalLayout = QtGui.QVBoxLayout(newScoreDialog)
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setMargin(9)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.label = QtGui.QLabel(newScoreDialog)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.numMeasuresSpinBox = QtGui.QSpinBox(newScoreDialog)
        self.numMeasuresSpinBox.setMinimum(1)
        self.numMeasuresSpinBox.setMaximum(100000)
        self.numMeasuresSpinBox.setProperty(_fromUtf8("value"), 32)
        self.numMeasuresSpinBox.setObjectName(_fromUtf8("numMeasuresSpinBox"))
        self.gridLayout.addWidget(self.numMeasuresSpinBox, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(newScoreDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.measureSizeSpinBox = QtGui.QSpinBox(newScoreDialog)
        self.measureSizeSpinBox.setMinimum(1)
        self.measureSizeSpinBox.setMaximum(256)
        self.measureSizeSpinBox.setProperty(_fromUtf8("value"), 16)
        self.measureSizeSpinBox.setObjectName(_fromUtf8("measureSizeSpinBox"))
        self.gridLayout.addWidget(self.measureSizeSpinBox, 1, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem4 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.buttonBox = QtGui.QDialogButtonBox(newScoreDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label.setBuddy(self.numMeasuresSpinBox)
        self.label_2.setBuddy(self.measureSizeSpinBox)

        self.retranslateUi(newScoreDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), newScoreDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), newScoreDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(newScoreDialog)

    def retranslateUi(self, newScoreDialog):
        newScoreDialog.setWindowTitle(QtGui.QApplication.translate("newScoreDialog", "New Score", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("newScoreDialog", "Number of measures", None, QtGui.QApplication.UnicodeUTF8))
        self.numMeasuresSpinBox.setToolTip(QtGui.QApplication.translate("newScoreDialog", "The number of measures in the new score", None, QtGui.QApplication.UnicodeUTF8))
        self.numMeasuresSpinBox.setStatusTip(QtGui.QApplication.translate("newScoreDialog", "The number of measures in the new score", None, QtGui.QApplication.UnicodeUTF8))
        self.numMeasuresSpinBox.setSuffix(QtGui.QApplication.translate("newScoreDialog", " measures", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("newScoreDialog", "Measure size", None, QtGui.QApplication.UnicodeUTF8))
        self.measureSizeSpinBox.setToolTip(QtGui.QApplication.translate("newScoreDialog", "The size of each measure in the new score in ticks", None, QtGui.QApplication.UnicodeUTF8))
        self.measureSizeSpinBox.setStatusTip(QtGui.QApplication.translate("newScoreDialog", "The size of each measure in the new score in ticks", None, QtGui.QApplication.UnicodeUTF8))
        self.measureSizeSpinBox.setSuffix(QtGui.QApplication.translate("newScoreDialog", " ticks", None, QtGui.QApplication.UnicodeUTF8))

