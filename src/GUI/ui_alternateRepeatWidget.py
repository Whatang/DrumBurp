# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike\workspace\DrumBurp\src\GUI\alternateRepeatWidget.ui'
#
# Created: Sat Feb 25 16:10:40 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AlternateWidget(QtGui.QWidget):
    def setupUi(self, AlternateWidget):
        AlternateWidget.setObjectName(_fromUtf8("AlternateWidget"))
        AlternateWidget.resize(273, 24)
        AlternateWidget.setWindowTitle(QtGui.QApplication.translate("AlternateWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(AlternateWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.startBox = QtGui.QSpinBox(AlternateWidget)
        self.startBox.setToolTip(QtGui.QApplication.translate("AlternateWidget", "Repeat number", None, QtGui.QApplication.UnicodeUTF8))
        self.startBox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.startBox.setMinimum(1)
        self.startBox.setMaximum(100000000)
        self.startBox.setObjectName(_fromUtf8("startBox"))
        self.horizontalLayout.addWidget(self.startBox)
        self.endBox = QtGui.QSpinBox(AlternateWidget)
        self.endBox.setEnabled(True)
        self.endBox.setToolTip(QtGui.QApplication.translate("AlternateWidget", "Repeat number range end", None, QtGui.QApplication.UnicodeUTF8))
        self.endBox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.endBox.setReadOnly(False)
        self.endBox.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.endBox.setMinimum(1)
        self.endBox.setMaximum(10000000)
        self.endBox.setObjectName(_fromUtf8("endBox"))
        self.horizontalLayout.addWidget(self.endBox)
        self.rangeCheck = QtGui.QCheckBox(AlternateWidget)
        self.rangeCheck.setToolTip(QtGui.QApplication.translate("AlternateWidget", "Range of repeat numbers?", None, QtGui.QApplication.UnicodeUTF8))
        self.rangeCheck.setText(QtGui.QApplication.translate("AlternateWidget", "Range?", None, QtGui.QApplication.UnicodeUTF8))
        self.rangeCheck.setChecked(True)
        self.rangeCheck.setObjectName(_fromUtf8("rangeCheck"))
        self.horizontalLayout.addWidget(self.rangeCheck)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.deleteButton = QtGui.QPushButton(AlternateWidget)
        self.deleteButton.setToolTip(QtGui.QApplication.translate("AlternateWidget", "Delete this repeat", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Icons/Icons/process-stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon)
        self.deleteButton.setFlat(True)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.horizontalLayout.addWidget(self.deleteButton)

        self.retranslateUi(AlternateWidget)
        QtCore.QObject.connect(self.rangeCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.endBox.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(AlternateWidget)

    def retranslateUi(self, AlternateWidget):
        pass

import DrumBurp_rc
