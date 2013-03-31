# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike\workspace\DrumBurp\src\GUI\versionDownloader.ui'
#
# Created: Sun Mar 31 17:03:40 2013
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_VersionDownloader(object):
    def setupUi(self, VersionDownloader):
        VersionDownloader.setObjectName(_fromUtf8("VersionDownloader"))
        VersionDownloader.setWindowModality(QtCore.Qt.ApplicationModal)
        VersionDownloader.resize(404, 151)
        VersionDownloader.setWindowTitle(QtGui.QApplication.translate("VersionDownloader", "Finding new version information", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(VersionDownloader)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.message = QtGui.QLabel(VersionDownloader)
        self.message.setText(QtGui.QApplication.translate("VersionDownloader", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Contacting </span><a href=\"htttp://www.whatang.org\"><span style=\" text-decoration: underline; color:#0000ff;\">www.whatang.org</span></a><span style=\" font-size:8pt;\"> to detect latest version. Please wait...</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.message.setObjectName(_fromUtf8("message"))
        self.verticalLayout.addWidget(self.message)
        self.resultBox = QtGui.QGroupBox(VersionDownloader)
        self.resultBox.setEnabled(False)
        self.resultBox.setTitle(QtGui.QApplication.translate("VersionDownloader", "Result", None, QtGui.QApplication.UnicodeUTF8))
        self.resultBox.setObjectName(_fromUtf8("resultBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.resultBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.resultLabel = QtGui.QLabel(self.resultBox)
        self.resultLabel.setText(_fromUtf8(""))
        self.resultLabel.setObjectName(_fromUtf8("resultLabel"))
        self.verticalLayout_2.addWidget(self.resultLabel)
        self.verticalLayout.addWidget(self.resultBox)
        self.buttonBox = QtGui.QDialogButtonBox(VersionDownloader)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(VersionDownloader)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), VersionDownloader.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), VersionDownloader.reject)
        QtCore.QMetaObject.connectSlotsByName(VersionDownloader)

    def retranslateUi(self, VersionDownloader):
        pass

