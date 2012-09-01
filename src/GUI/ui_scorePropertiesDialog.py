# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike\workspace\DrumBurp\src\GUI\scorePropertiesDialog.ui'
#
# Created: Sat Sep 01 17:27:14 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ScoreDialog(object):
    def setupUi(self, ScoreDialog):
        ScoreDialog.setObjectName(_fromUtf8("ScoreDialog"))
        ScoreDialog.resize(482, 145)
        ScoreDialog.setWindowTitle(QtGui.QApplication.translate("ScoreDialog", "Edit Score Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(ScoreDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(ScoreDialog)
        self.label.setToolTip(QtGui.QApplication.translate("ScoreDialog", "The title of the score", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ScoreDialog", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.titleEdit = QtGui.QLineEdit(ScoreDialog)
        self.titleEdit.setToolTip(QtGui.QApplication.translate("ScoreDialog", "The title of the score", None, QtGui.QApplication.UnicodeUTF8))
        self.titleEdit.setObjectName(_fromUtf8("titleEdit"))
        self.gridLayout.addWidget(self.titleEdit, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(ScoreDialog)
        self.label_2.setToolTip(QtGui.QApplication.translate("ScoreDialog", "The score\'s artist", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ScoreDialog", "Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.artistEdit = QtGui.QLineEdit(ScoreDialog)
        self.artistEdit.setToolTip(QtGui.QApplication.translate("ScoreDialog", "The score\'s artist", None, QtGui.QApplication.UnicodeUTF8))
        self.artistEdit.setObjectName(_fromUtf8("artistEdit"))
        self.gridLayout.addWidget(self.artistEdit, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(ScoreDialog)
        self.label_3.setToolTip(QtGui.QApplication.translate("ScoreDialog", "The name of the person who wrote this score", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ScoreDialog", "Tabbed by", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.creatorEdit = QtGui.QLineEdit(ScoreDialog)
        self.creatorEdit.setToolTip(QtGui.QApplication.translate("ScoreDialog", "The name of the person who wrote this score", None, QtGui.QApplication.UnicodeUTF8))
        self.creatorEdit.setObjectName(_fromUtf8("creatorEdit"))
        self.gridLayout.addWidget(self.creatorEdit, 2, 2, 1, 1)
        self.label_4 = QtGui.QLabel(ScoreDialog)
        self.label_4.setToolTip(QtGui.QApplication.translate("ScoreDialog", "Beats per minute of this score", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ScoreDialog", "BPM", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.bpmSpinBox = QtGui.QSpinBox(ScoreDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bpmSpinBox.sizePolicy().hasHeightForWidth())
        self.bpmSpinBox.setSizePolicy(sizePolicy)
        self.bpmSpinBox.setToolTip(QtGui.QApplication.translate("ScoreDialog", "Beats per minute of this score", None, QtGui.QApplication.UnicodeUTF8))
        self.bpmSpinBox.setStatusTip(QtGui.QApplication.translate("ScoreDialog", "Beats per minute", None, QtGui.QApplication.UnicodeUTF8))
        self.bpmSpinBox.setFrame(True)
        self.bpmSpinBox.setSuffix(QtGui.QApplication.translate("ScoreDialog", " bpm", None, QtGui.QApplication.UnicodeUTF8))
        self.bpmSpinBox.setMaximum(300)
        self.bpmSpinBox.setProperty("value", 120)
        self.bpmSpinBox.setObjectName(_fromUtf8("bpmSpinBox"))
        self.gridLayout.addWidget(self.bpmSpinBox, 3, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ScoreDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 4)
        self.artistVisible = QtGui.QCheckBox(ScoreDialog)
        self.artistVisible.setToolTip(QtGui.QApplication.translate("ScoreDialog", "Show/hide artist name", None, QtGui.QApplication.UnicodeUTF8))
        self.artistVisible.setText(_fromUtf8(""))
        self.artistVisible.setObjectName(_fromUtf8("artistVisible"))
        self.gridLayout.addWidget(self.artistVisible, 1, 1, 1, 1)
        self.creatorVisible = QtGui.QCheckBox(ScoreDialog)
        self.creatorVisible.setToolTip(QtGui.QApplication.translate("ScoreDialog", "Show.hide tabber name", None, QtGui.QApplication.UnicodeUTF8))
        self.creatorVisible.setText(_fromUtf8(""))
        self.creatorVisible.setObjectName(_fromUtf8("creatorVisible"))
        self.gridLayout.addWidget(self.creatorVisible, 2, 1, 1, 1)
        self.bpmVisible = QtGui.QCheckBox(ScoreDialog)
        self.bpmVisible.setToolTip(QtGui.QApplication.translate("ScoreDialog", "Show/hide BPM", None, QtGui.QApplication.UnicodeUTF8))
        self.bpmVisible.setText(_fromUtf8(""))
        self.bpmVisible.setObjectName(_fromUtf8("bpmVisible"))
        self.gridLayout.addWidget(self.bpmVisible, 3, 1, 1, 1)

        self.retranslateUi(ScoreDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ScoreDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ScoreDialog.reject)
        QtCore.QObject.connect(self.artistVisible, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.artistEdit.setEnabled)
        QtCore.QObject.connect(self.creatorVisible, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.creatorEdit.setEnabled)
        QtCore.QObject.connect(self.bpmVisible, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.bpmSpinBox.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ScoreDialog)

    def retranslateUi(self, ScoreDialog):
        pass

