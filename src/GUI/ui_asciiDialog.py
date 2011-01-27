# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike\workspace\DrumBurp\src\GUI\asciiDialog.ui'
#
# Created: Thu Jan 27 18:13:58 2011
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
        asciiDialog.resize(284, 168)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(asciiDialog.sizePolicy().hasHeightForWidth())
        asciiDialog.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtGui.QVBoxLayout(asciiDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(asciiDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.filenameLabel = QtGui.QLabel(asciiDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filenameLabel.sizePolicy().hasHeightForWidth())
        self.filenameLabel.setSizePolicy(sizePolicy)
        self.filenameLabel.setFrameShape(QtGui.QFrame.Panel)
        self.filenameLabel.setObjectName(_fromUtf8("filenameLabel"))
        self.horizontalLayout.addWidget(self.filenameLabel)
        self.filenameButton = QtGui.QPushButton(asciiDialog)
        self.filenameButton.setObjectName(_fromUtf8("filenameButton"))
        self.horizontalLayout.addWidget(self.filenameButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.metadataCheck = QtGui.QCheckBox(asciiDialog)
        self.metadataCheck.setObjectName(_fromUtf8("metadataCheck"))
        self.verticalLayout.addWidget(self.metadataCheck)
        self.kitKeyCheck = QtGui.QCheckBox(asciiDialog)
        self.kitKeyCheck.setObjectName(_fromUtf8("kitKeyCheck"))
        self.verticalLayout.addWidget(self.kitKeyCheck)
        self.omitEmptyCheck = QtGui.QCheckBox(asciiDialog)
        self.omitEmptyCheck.setObjectName(_fromUtf8("omitEmptyCheck"))
        self.verticalLayout.addWidget(self.omitEmptyCheck)
        self.underlineCheck = QtGui.QCheckBox(asciiDialog)
        self.underlineCheck.setObjectName(_fromUtf8("underlineCheck"))
        self.verticalLayout.addWidget(self.underlineCheck)
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
        self.label.setText(QtGui.QApplication.translate("asciiDialog", "ASCII Filename:", None, QtGui.QApplication.UnicodeUTF8))
        self.filenameLabel.setText(QtGui.QApplication.translate("asciiDialog", "Filename", None, QtGui.QApplication.UnicodeUTF8))
        self.filenameButton.setText(QtGui.QApplication.translate("asciiDialog", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.metadataCheck.setText(QtGui.QApplication.translate("asciiDialog", "Song metadata (Title, artist, etc.)", None, QtGui.QApplication.UnicodeUTF8))
        self.kitKeyCheck.setText(QtGui.QApplication.translate("asciiDialog", "Drum kit key", None, QtGui.QApplication.UnicodeUTF8))
        self.omitEmptyCheck.setText(QtGui.QApplication.translate("asciiDialog", "Omit empty lines for unlocked drums", None, QtGui.QApplication.UnicodeUTF8))
        self.underlineCheck.setText(QtGui.QApplication.translate("asciiDialog", "Underline section titles with ~ characters", None, QtGui.QApplication.UnicodeUTF8))

