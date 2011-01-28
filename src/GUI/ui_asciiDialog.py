# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike\workspace\DrumBurp\src\GUI\asciiDialog.ui'
#
# Created: Thu Jan 27 22:27:19 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_asciiDialog(object):
    def setupUi(self, asciiDialog):
        asciiDialog.setObjectName(_fromUtf8("asciiDialog"))
        asciiDialog.resize(359, 220)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(asciiDialog.sizePolicy().hasHeightForWidth())
        asciiDialog.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtGui.QVBoxLayout(asciiDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.filenameButton = QtGui.QPushButton(asciiDialog)
        self.filenameButton.setObjectName(_fromUtf8("filenameButton"))
        self.horizontalLayout.addWidget(self.filenameButton)
        self.filenameLabel = QtGui.QLabel(asciiDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filenameLabel.sizePolicy().hasHeightForWidth())
        self.filenameLabel.setSizePolicy(sizePolicy)
        self.filenameLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.filenameLabel.setObjectName(_fromUtf8("filenameLabel"))
        self.horizontalLayout.addWidget(self.filenameLabel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.metadataCheck = QtGui.QCheckBox(asciiDialog)
        self.metadataCheck.setChecked(True)
        self.metadataCheck.setObjectName(_fromUtf8("metadataCheck"))
        self.verticalLayout.addWidget(self.metadataCheck)
        self.kitKeyCheck = QtGui.QCheckBox(asciiDialog)
        self.kitKeyCheck.setChecked(True)
        self.kitKeyCheck.setObjectName(_fromUtf8("kitKeyCheck"))
        self.verticalLayout.addWidget(self.kitKeyCheck)
        self.omitEmptyCheck = QtGui.QCheckBox(asciiDialog)
        self.omitEmptyCheck.setChecked(True)
        self.omitEmptyCheck.setObjectName(_fromUtf8("omitEmptyCheck"))
        self.verticalLayout.addWidget(self.omitEmptyCheck)
        self.underlineCheck = QtGui.QCheckBox(asciiDialog)
        self.underlineCheck.setChecked(True)
        self.underlineCheck.setObjectName(_fromUtf8("underlineCheck"))
        self.verticalLayout.addWidget(self.underlineCheck)
        self.countCheck = QtGui.QCheckBox(asciiDialog)
        self.countCheck.setChecked(True)
        self.countCheck.setObjectName(_fromUtf8("countCheck"))
        self.verticalLayout.addWidget(self.countCheck)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(asciiDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(asciiDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), asciiDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), asciiDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(asciiDialog)

    def retranslateUi(self, asciiDialog):
        asciiDialog.setWindowTitle(QtGui.QApplication.translate("asciiDialog", "Export ASCII file", None, QtGui.QApplication.UnicodeUTF8))
        self.filenameButton.setText(QtGui.QApplication.translate("asciiDialog", "Filename:", None, QtGui.QApplication.UnicodeUTF8))
        self.filenameLabel.setText(QtGui.QApplication.translate("asciiDialog", "Filename", None, QtGui.QApplication.UnicodeUTF8))
        self.metadataCheck.setText(QtGui.QApplication.translate("asciiDialog", "Song metadata (Title, artist, etc.)", None, QtGui.QApplication.UnicodeUTF8))
        self.kitKeyCheck.setText(QtGui.QApplication.translate("asciiDialog", "Drum kit key", None, QtGui.QApplication.UnicodeUTF8))
        self.omitEmptyCheck.setText(QtGui.QApplication.translate("asciiDialog", "Omit empty lines for unlocked drums", None, QtGui.QApplication.UnicodeUTF8))
        self.underlineCheck.setText(QtGui.QApplication.translate("asciiDialog", "Underline section titles with ~ characters", None, QtGui.QApplication.UnicodeUTF8))
        self.countCheck.setText(QtGui.QApplication.translate("asciiDialog", "Beat count", None, QtGui.QApplication.UnicodeUTF8))

