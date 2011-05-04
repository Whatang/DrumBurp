# -*- coding: utf-8 -*-

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

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\newScoreDialog.ui'
#
# Created: Sun Apr 17 18:21:30 2011
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
        newScoreDialog.resize(288, 281)
        newScoreDialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.verticalLayout = QtGui.QVBoxLayout(newScoreDialog)
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setMargin(9)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(newScoreDialog)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.numMeasuresSpinBox = QtGui.QSpinBox(newScoreDialog)
        self.numMeasuresSpinBox.setMinimum(1)
        self.numMeasuresSpinBox.setMaximum(100000)
        self.numMeasuresSpinBox.setProperty(_fromUtf8("value"), 32)
        self.numMeasuresSpinBox.setObjectName(_fromUtf8("numMeasuresSpinBox"))
        self.gridLayout.addWidget(self.numMeasuresSpinBox, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.measureTabs = measureTabs(newScoreDialog)
        self.measureTabs.setObjectName(_fromUtf8("measureTabs"))
        self.verticalLayout.addWidget(self.measureTabs)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.buttonBox = QtGui.QDialogButtonBox(newScoreDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label.setBuddy(self.numMeasuresSpinBox)

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

from Widgets.measureTabs_plugin import measureTabs
