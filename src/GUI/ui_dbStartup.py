# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\mike_000\workspace\DrumBurp\src\GUI\dbStartup.ui'
#
# Created: Sun Feb 22 11:31:19 2015
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_dbStartup(object):
    def setupUi(self, dbStartup):
        dbStartup.setObjectName(_fromUtf8("dbStartup"))
        dbStartup.resize(771, 335)
        self.verticalLayout = QtGui.QVBoxLayout(dbStartup)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(dbStartup)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtGui.QDialogButtonBox(dbStartup)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(dbStartup)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), dbStartup.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), dbStartup.reject)
        QtCore.QMetaObject.connectSlotsByName(dbStartup)

    def retranslateUi(self, dbStartup):
        dbStartup.setWindowTitle(_translate("dbStartup", "Welcome to DrumBurp", None))
        self.label.setText(_translate("dbStartup", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; font-style:italic;\">DrumBurp Copyright (C) 2011-15 Michael Thomas</span></p><p><br/></p><p>This program comes with ABSOLUTELY NO WARRANTY; for details see the <span style=\" font-weight:600;\">Help&gt;About DrumBurp</span> menu item. This is free software, and you are welcome to redistribute it under certain conditions; see the licensing information in <span style=\" font-weight:600;\">Help&gt;About DrumBurp</span> for details.</p><p><br/></p><p>Support and further licensing information is available at <a href=\"http://www.whatang.org\"><span style=\" text-decoration: underline; color:#0000ff;\">www.whatang.org</span></a></p></body></html>", None))

