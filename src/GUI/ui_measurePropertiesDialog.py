# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\measurePropertiesDialog.ui'
#
# Created: Sun Apr 17 17:50:28 2011
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
        measurePropertiesDialog.resize(352, 223)
        measurePropertiesDialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.verticalLayout = QtGui.QVBoxLayout(measurePropertiesDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.measureTabs = measureTabs(measurePropertiesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.measureTabs.sizePolicy().hasHeightForWidth())
        self.measureTabs.setSizePolicy(sizePolicy)
        self.measureTabs.setObjectName(_fromUtf8("measureTabs"))
        self.horizontalLayout_2.addWidget(self.measureTabs)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(measurePropertiesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset|QtGui.QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(measurePropertiesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), measurePropertiesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), measurePropertiesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(measurePropertiesDialog)

    def retranslateUi(self, measurePropertiesDialog):
        measurePropertiesDialog.setWindowTitle(QtGui.QApplication.translate("measurePropertiesDialog", "Measure Properties", None, QtGui.QApplication.UnicodeUTF8))

from Widgets.measureTabs_plugin import measureTabs
