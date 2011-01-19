# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\measurePropertiesDialog.ui'
#
# Created: Wed Jan 19 01:06:14 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_measurePropertiesDialog(object):
    def setupUi(self, measurePropertiesDialog):
        measurePropertiesDialog.setObjectName(_fromUtf8("measurePropertiesDialog"))
        measurePropertiesDialog.resize(226, 109)
        measurePropertiesDialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.verticalLayout = QtGui.QVBoxLayout(measurePropertiesDialog)
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setMargin(9)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(measurePropertiesDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.beatsSpinBox = QtGui.QSpinBox(measurePropertiesDialog)
        self.beatsSpinBox.setMinimum(1)
        self.beatsSpinBox.setMaximum(256)
        self.beatsSpinBox.setProperty(_fromUtf8("value"), 4)
        self.beatsSpinBox.setObjectName(_fromUtf8("beatsSpinBox"))
        self.gridLayout.addWidget(self.beatsSpinBox, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.label_3 = QtGui.QLabel(measurePropertiesDialog)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        self.beatCountComboBox = QtGui.QComboBox(measurePropertiesDialog)
        self.beatCountComboBox.setObjectName(_fromUtf8("beatCountComboBox"))
        self.gridLayout.addWidget(self.beatCountComboBox, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.buttonBox = QtGui.QDialogButtonBox(measurePropertiesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_2.setBuddy(self.beatsSpinBox)

        self.retranslateUi(measurePropertiesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), measurePropertiesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), measurePropertiesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(measurePropertiesDialog)

    def retranslateUi(self, measurePropertiesDialog):
        measurePropertiesDialog.setWindowTitle(QtGui.QApplication.translate("measurePropertiesDialog", "Measure Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("measurePropertiesDialog", "Beats", None, QtGui.QApplication.UnicodeUTF8))
        self.beatsSpinBox.setToolTip(QtGui.QApplication.translate("measurePropertiesDialog", "The size of each measure in the new score in ticks", None, QtGui.QApplication.UnicodeUTF8))
        self.beatsSpinBox.setStatusTip(QtGui.QApplication.translate("measurePropertiesDialog", "The size of each measure in the new score in ticks", None, QtGui.QApplication.UnicodeUTF8))
        self.beatsSpinBox.setSuffix(QtGui.QApplication.translate("measurePropertiesDialog", " beats", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("measurePropertiesDialog", "Beat count", None, QtGui.QApplication.UnicodeUTF8))

