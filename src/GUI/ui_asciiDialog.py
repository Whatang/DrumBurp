# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\asciiDialog.ui'
#
# Created: Sat Mar 31 13:52:19 2012
#      by: PyQt4 UI code generator 4.9.1
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
        asciiDialog.resize(487, 169)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(asciiDialog.sizePolicy().hasHeightForWidth())
        asciiDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(asciiDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
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
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.metadataCheck = QtGui.QCheckBox(asciiDialog)
        self.metadataCheck.setChecked(True)
        self.metadataCheck.setObjectName(_fromUtf8("metadataCheck"))
        self.gridLayout.addWidget(self.metadataCheck, 0, 0, 1, 1)
        self.underlineCheck = QtGui.QCheckBox(asciiDialog)
        self.underlineCheck.setChecked(True)
        self.underlineCheck.setObjectName(_fromUtf8("underlineCheck"))
        self.gridLayout.addWidget(self.underlineCheck, 0, 1, 1, 1)
        self.kitKeyCheck = QtGui.QCheckBox(asciiDialog)
        self.kitKeyCheck.setChecked(True)
        self.kitKeyCheck.setObjectName(_fromUtf8("kitKeyCheck"))
        self.gridLayout.addWidget(self.kitKeyCheck, 2, 0, 1, 1)
        self.omitEmptyCheck = QtGui.QCheckBox(asciiDialog)
        self.omitEmptyCheck.setChecked(True)
        self.omitEmptyCheck.setObjectName(_fromUtf8("omitEmptyCheck"))
        self.gridLayout.addWidget(self.omitEmptyCheck, 3, 0, 1, 1)
        self.printCountsCheck = QtGui.QCheckBox(asciiDialog)
        self.printCountsCheck.setChecked(True)
        self.printCountsCheck.setObjectName(_fromUtf8("printCountsCheck"))
        self.gridLayout.addWidget(self.printCountsCheck, 4, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        self.emptyLineAfterSectionCheck = QtGui.QCheckBox(asciiDialog)
        self.emptyLineAfterSectionCheck.setChecked(True)
        self.emptyLineAfterSectionCheck.setObjectName(_fromUtf8("emptyLineAfterSectionCheck"))
        self.gridLayout.addWidget(self.emptyLineAfterSectionCheck, 3, 1, 1, 1)
        self.emptyLineBeforeSectionCheck = QtGui.QCheckBox(asciiDialog)
        self.emptyLineBeforeSectionCheck.setChecked(True)
        self.emptyLineBeforeSectionCheck.setObjectName(_fromUtf8("emptyLineBeforeSectionCheck"))
        self.gridLayout.addWidget(self.emptyLineBeforeSectionCheck, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtGui.QDialogButtonBox(asciiDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(asciiDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), asciiDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), asciiDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(asciiDialog)

    def retranslateUi(self, asciiDialog):
        asciiDialog.setWindowTitle(QtGui.QApplication.translate("asciiDialog", "Export ASCII file", None, QtGui.QApplication.UnicodeUTF8))
        self.filenameButton.setToolTip(QtGui.QApplication.translate("asciiDialog", "Click to select a new filename", None, QtGui.QApplication.UnicodeUTF8))
        self.filenameButton.setText(QtGui.QApplication.translate("asciiDialog", "Filename:", None, QtGui.QApplication.UnicodeUTF8))
        self.filenameLabel.setToolTip(QtGui.QApplication.translate("asciiDialog", "The filename to export this score to", None, QtGui.QApplication.UnicodeUTF8))
        self.filenameLabel.setText(QtGui.QApplication.translate("asciiDialog", "Filename", None, QtGui.QApplication.UnicodeUTF8))
        self.metadataCheck.setToolTip(QtGui.QApplication.translate("asciiDialog", "Export the song information", None, QtGui.QApplication.UnicodeUTF8))
        self.metadataCheck.setText(QtGui.QApplication.translate("asciiDialog", "Song info (Title, artist, etc.)", None, QtGui.QApplication.UnicodeUTF8))
        self.underlineCheck.setToolTip(QtGui.QApplication.translate("asciiDialog", "Underline each section title", None, QtGui.QApplication.UnicodeUTF8))
        self.underlineCheck.setText(QtGui.QApplication.translate("asciiDialog", "Underline section titles with ~ characters", None, QtGui.QApplication.UnicodeUTF8))
        self.kitKeyCheck.setToolTip(QtGui.QApplication.translate("asciiDialog", "Export the drum kit key", None, QtGui.QApplication.UnicodeUTF8))
        self.kitKeyCheck.setText(QtGui.QApplication.translate("asciiDialog", "Drum kit key", None, QtGui.QApplication.UnicodeUTF8))
        self.omitEmptyCheck.setToolTip(QtGui.QApplication.translate("asciiDialog", "Empty lines for unlocked drums are not written to the ASCII tab", None, QtGui.QApplication.UnicodeUTF8))
        self.omitEmptyCheck.setText(QtGui.QApplication.translate("asciiDialog", "Omit empty lines for unlocked drums", None, QtGui.QApplication.UnicodeUTF8))
        self.printCountsCheck.setToolTip(QtGui.QApplication.translate("asciiDialog", "Export the beat count underneath each measure", None, QtGui.QApplication.UnicodeUTF8))
        self.printCountsCheck.setText(QtGui.QApplication.translate("asciiDialog", "Beat count", None, QtGui.QApplication.UnicodeUTF8))
        self.emptyLineAfterSectionCheck.setToolTip(QtGui.QApplication.translate("asciiDialog", "Include a blank line after each section title", None, QtGui.QApplication.UnicodeUTF8))
        self.emptyLineAfterSectionCheck.setText(QtGui.QApplication.translate("asciiDialog", "Empty line after section title", None, QtGui.QApplication.UnicodeUTF8))
        self.emptyLineBeforeSectionCheck.setToolTip(QtGui.QApplication.translate("asciiDialog", "Include a blank line before each section title", None, QtGui.QApplication.UnicodeUTF8))
        self.emptyLineBeforeSectionCheck.setText(QtGui.QApplication.translate("asciiDialog", "Empty line before section title", None, QtGui.QApplication.UnicodeUTF8))

