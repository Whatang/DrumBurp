# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike\workspace\DrumBurp\src\GUI\DBComplextCountDialog.ui'
#
# Created: Sat Mar 03 22:59:53 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_complexCountDialog(object):
    def setupUi(self, complexCountDialog):
        complexCountDialog.setObjectName(_fromUtf8("complexCountDialog"))
        complexCountDialog.resize(322, 251)
        complexCountDialog.setWindowTitle(QtGui.QApplication.translate("complexCountDialog", "Edit Complex Measure Count", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout_2 = QtGui.QVBoxLayout(complexCountDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.beatList = QtGui.QListWidget(complexCountDialog)
        self.beatList.setToolTip(QtGui.QApplication.translate("complexCountDialog", "List of beats in the measure count", None, QtGui.QApplication.UnicodeUTF8))
        self.beatList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.beatList.setProperty("showDropIndicator", False)
        self.beatList.setObjectName(_fromUtf8("beatList"))
        self.horizontalLayout_2.addWidget(self.beatList)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.addButton = QtGui.QPushButton(complexCountDialog)
        self.addButton.setToolTip(QtGui.QApplication.translate("complexCountDialog", "Add a new beat at the end of this count", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("complexCountDialog", "Add Beat", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout.addWidget(self.addButton)
        self.deleteButton = QtGui.QPushButton(complexCountDialog)
        self.deleteButton.setToolTip(QtGui.QApplication.translate("complexCountDialog", "Delete the currently selected count", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("complexCountDialog", "Delete Beat", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.verticalLayout.addWidget(self.deleteButton)
        self.label_2 = QtGui.QLabel(complexCountDialog)
        self.label_2.setText(QtGui.QApplication.translate("complexCountDialog", "Count", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.countBox = QtGui.QComboBox(complexCountDialog)
        self.countBox.setToolTip(QtGui.QApplication.translate("complexCountDialog", "Count to use for the current beat", None, QtGui.QApplication.UnicodeUTF8))
        self.countBox.setObjectName(_fromUtf8("countBox"))
        self.verticalLayout.addWidget(self.countBox)
        self.label_3 = QtGui.QLabel(complexCountDialog)
        self.label_3.setText(QtGui.QApplication.translate("complexCountDialog", "Ticks", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.numTicksSpinBox = QtGui.QSpinBox(complexCountDialog)
        self.numTicksSpinBox.setToolTip(QtGui.QApplication.translate("complexCountDialog", "How many ticks of the count should the current beat use?", None, QtGui.QApplication.UnicodeUTF8))
        self.numTicksSpinBox.setObjectName(_fromUtf8("numTicksSpinBox"))
        self.verticalLayout.addWidget(self.numTicksSpinBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.groupBox = QtGui.QGroupBox(complexCountDialog)
        self.groupBox.setToolTip(QtGui.QApplication.translate("complexCountDialog", "Preview of the measure count according to the current settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("complexCountDialog", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.previewText = QtGui.QLabel(self.groupBox)
        self.previewText.setAutoFillBackground(False)
        self.previewText.setFrameShape(QtGui.QFrame.NoFrame)
        self.previewText.setFrameShadow(QtGui.QFrame.Sunken)
        self.previewText.setText(QtGui.QApplication.translate("complexCountDialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.previewText.setAlignment(QtCore.Qt.AlignCenter)
        self.previewText.setWordWrap(True)
        self.previewText.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.previewText.setObjectName(_fromUtf8("previewText"))
        self.horizontalLayout.addWidget(self.previewText)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(complexCountDialog)
        self.buttonBox.setToolTip(QtGui.QApplication.translate("complexCountDialog", "Reset the count to the original settings", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(complexCountDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), complexCountDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), complexCountDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(complexCountDialog)

    def retranslateUi(self, complexCountDialog):
        pass

