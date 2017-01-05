# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\mike_000\workspace\DrumBurp\src\GUI\scorePropertiesDialog.ui'
#
# Created: Thu Jan 05 13:27:53 2017
#      by: PyQt4 UI code generator 4.11
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ScoreDialog(object):
    def setupUi(self, ScoreDialog):
        ScoreDialog.setObjectName(_fromUtf8("ScoreDialog"))
        ScoreDialog.resize(482, 173)
        self.gridLayout = QtGui.QGridLayout(ScoreDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.titleEdit = QtGui.QLineEdit(ScoreDialog)
        self.titleEdit.setObjectName(_fromUtf8("titleEdit"))
        self.gridLayout.addWidget(self.titleEdit, 0, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ScoreDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 4)
        self.label = QtGui.QLabel(ScoreDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(ScoreDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(ScoreDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.artistVisible = QtGui.QCheckBox(ScoreDialog)
        self.artistVisible.setText(_fromUtf8(""))
        self.artistVisible.setChecked(True)
        self.artistVisible.setObjectName(_fromUtf8("artistVisible"))
        self.gridLayout.addWidget(self.artistVisible, 1, 1, 1, 1)
        self.artistEdit = QtGui.QLineEdit(ScoreDialog)
        self.artistEdit.setObjectName(_fromUtf8("artistEdit"))
        self.gridLayout.addWidget(self.artistEdit, 1, 2, 1, 1)
        self.creatorEdit = QtGui.QLineEdit(ScoreDialog)
        self.creatorEdit.setObjectName(_fromUtf8("creatorEdit"))
        self.gridLayout.addWidget(self.creatorEdit, 2, 2, 1, 1)
        self.creatorVisible = QtGui.QCheckBox(ScoreDialog)
        self.creatorVisible.setText(_fromUtf8(""))
        self.creatorVisible.setChecked(True)
        self.creatorVisible.setObjectName(_fromUtf8("creatorVisible"))
        self.gridLayout.addWidget(self.creatorVisible, 2, 1, 1, 1)
        self.label_5 = QtGui.QLabel(ScoreDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.swingComboBox = QtGui.QComboBox(ScoreDialog)
        self.swingComboBox.setObjectName(_fromUtf8("swingComboBox"))
        self.swingComboBox.addItem(_fromUtf8(""))
        self.swingComboBox.addItem(_fromUtf8(""))
        self.swingComboBox.addItem(_fromUtf8(""))
        self.swingComboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.swingComboBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 2, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.bpmSpinBox = QtGui.QSpinBox(ScoreDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bpmSpinBox.sizePolicy().hasHeightForWidth())
        self.bpmSpinBox.setSizePolicy(sizePolicy)
        self.bpmSpinBox.setFrame(True)
        self.bpmSpinBox.setMaximum(300)
        self.bpmSpinBox.setProperty("value", 120)
        self.bpmSpinBox.setObjectName(_fromUtf8("bpmSpinBox"))
        self.horizontalLayout_2.addWidget(self.bpmSpinBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 2, 1, 1)
        self.label_4 = QtGui.QLabel(ScoreDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.bpmVisible = QtGui.QCheckBox(ScoreDialog)
        self.bpmVisible.setText(_fromUtf8(""))
        self.bpmVisible.setChecked(True)
        self.bpmVisible.setObjectName(_fromUtf8("bpmVisible"))
        self.gridLayout.addWidget(self.bpmVisible, 3, 1, 1, 1)

        self.retranslateUi(ScoreDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ScoreDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ScoreDialog.reject)
        QtCore.QObject.connect(self.artistVisible, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.artistEdit.setEnabled)
        QtCore.QObject.connect(self.creatorVisible, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.creatorEdit.setEnabled)
        QtCore.QObject.connect(self.bpmVisible, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.bpmSpinBox.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ScoreDialog)
        ScoreDialog.setTabOrder(self.titleEdit, self.artistVisible)
        ScoreDialog.setTabOrder(self.artistVisible, self.artistEdit)
        ScoreDialog.setTabOrder(self.artistEdit, self.creatorVisible)
        ScoreDialog.setTabOrder(self.creatorVisible, self.creatorEdit)
        ScoreDialog.setTabOrder(self.creatorEdit, self.bpmVisible)
        ScoreDialog.setTabOrder(self.bpmVisible, self.bpmSpinBox)
        ScoreDialog.setTabOrder(self.bpmSpinBox, self.swingComboBox)
        ScoreDialog.setTabOrder(self.swingComboBox, self.buttonBox)

    def retranslateUi(self, ScoreDialog):
        ScoreDialog.setWindowTitle(_translate("ScoreDialog", "Edit Score Properties", None))
        self.titleEdit.setToolTip(_translate("ScoreDialog", "The title of the score", None))
        self.label.setToolTip(_translate("ScoreDialog", "The title of the score", None))
        self.label.setText(_translate("ScoreDialog", "Title", None))
        self.label_2.setToolTip(_translate("ScoreDialog", "The score\'s artist", None))
        self.label_2.setText(_translate("ScoreDialog", "Artist", None))
        self.label_3.setToolTip(_translate("ScoreDialog", "The name of the person who wrote this score", None))
        self.label_3.setText(_translate("ScoreDialog", "Tabbed by", None))
        self.artistVisible.setToolTip(_translate("ScoreDialog", "Show/hide artist name", None))
        self.artistEdit.setToolTip(_translate("ScoreDialog", "The score\'s artist", None))
        self.creatorEdit.setToolTip(_translate("ScoreDialog", "The name of the person who wrote this score", None))
        self.creatorVisible.setToolTip(_translate("ScoreDialog", "Show.hide tabber name", None))
        self.label_5.setText(_translate("ScoreDialog", "Swing?", None))
        self.swingComboBox.setItemText(0, _translate("ScoreDialog", "No", None))
        self.swingComboBox.setItemText(1, _translate("ScoreDialog", "8ths", None))
        self.swingComboBox.setItemText(2, _translate("ScoreDialog", "16ths", None))
        self.swingComboBox.setItemText(3, _translate("ScoreDialog", "32nds", None))
        self.bpmSpinBox.setToolTip(_translate("ScoreDialog", "Beats per minute of this score", None))
        self.bpmSpinBox.setStatusTip(_translate("ScoreDialog", "Beats per minute", None))
        self.bpmSpinBox.setSuffix(_translate("ScoreDialog", " bpm", None))
        self.label_4.setToolTip(_translate("ScoreDialog", "Beats per minute of this score", None))
        self.label_4.setText(_translate("ScoreDialog", "BPM", None))
        self.bpmVisible.setToolTip(_translate("ScoreDialog", "Show/hide BPM", None))

