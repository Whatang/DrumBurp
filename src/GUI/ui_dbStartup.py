# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\dbStartup.ui'
#
# Created: Sat Feb 18 12:40:46 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dbStartup(object):
    def setupUi(self, dbStartup):
        dbStartup.setObjectName(_fromUtf8("dbStartup"))
        dbStartup.resize(411, 172)
        self.verticalLayout = QtGui.QVBoxLayout(dbStartup)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textBrowser = QtGui.QTextBrowser(dbStartup)
        self.textBrowser.setAutoFillBackground(True)
        self.textBrowser.setFrameShape(QtGui.QFrame.NoFrame)
        self.textBrowser.setFrameShadow(QtGui.QFrame.Plain)
        self.textBrowser.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout.addWidget(self.textBrowser)
        self.buttonBox = QtGui.QDialogButtonBox(dbStartup)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(dbStartup)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), dbStartup.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), dbStartup.reject)
        QtCore.QMetaObject.connectSlotsByName(dbStartup)
        dbStartup.setTabOrder(self.buttonBox, self.textBrowser)

    def retranslateUi(self, dbStartup):
        dbStartup.setWindowTitle(QtGui.QApplication.translate("dbStartup", "Welcome to DrumBurp", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("dbStartup", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600; font-style:italic;\">DrumBurp Copyright (C) 2011-12 Michael Thomas</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">This program comes with ABSOLUTELY NO WARRANTY; for details see the </span><span style=\" font-size:8pt; font-weight:600;\">Help&gt;About DrumBurp</span><span style=\" font-size:8pt;\"> menu item. This is free software, and you are welcome to redistribute it under certain conditions; see the licensing information in </span><span style=\" font-size:8pt; font-weight:600;\">Help&gt;About DrumBurp</span><span style=\" font-size:8pt;\"> for details.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Support and further licensing information is available at </span><a href=\"http://www.whatang.org\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">www.whatang.org</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

