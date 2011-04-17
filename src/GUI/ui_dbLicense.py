# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\dbLicense.ui'
#
# Created: Sun Apr 17 13:09:24 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dbLicense_dialog(object):
    def setupUi(self, dbLicense_dialog):
        dbLicense_dialog.setObjectName(_fromUtf8("dbLicense_dialog"))
        dbLicense_dialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(dbLicense_dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(dbLicense_dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.textBrowser = QtGui.QTextBrowser(dbLicense_dialog)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout.addWidget(self.textBrowser)
        self.buttonBox = QtGui.QDialogButtonBox(dbLicense_dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(dbLicense_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), dbLicense_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), dbLicense_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dbLicense_dialog)

    def retranslateUi(self, dbLicense_dialog):
        dbLicense_dialog.setWindowTitle(QtGui.QApplication.translate("dbLicense_dialog", "DrumBurp license", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dbLicense_dialog", "DrumBurp is issued under the GPLv3.", None, QtGui.QApplication.UnicodeUTF8))

