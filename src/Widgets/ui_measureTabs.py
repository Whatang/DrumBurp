# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\mike_000\workspace\DrumBurp\src\Widgets\measureTabs.ui'
#
# Created: Sun Feb 22 11:49:19 2015
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


class Ui_measureTabs(object):
    def setupUi(self, measureTabs):
        measureTabs.setObjectName(_fromUtf8("measureTabs"))
        measureTabs.resize(441, 219)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            measureTabs.sizePolicy().hasHeightForWidth())
        measureTabs.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(measureTabs)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.counterTabs = QtGui.QTabWidget(measureTabs)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.counterTabs.sizePolicy().hasHeightForWidth())
        self.counterTabs.setSizePolicy(sizePolicy)
        self.counterTabs.setMinimumSize(QtCore.QSize(415, 111))
        self.counterTabs.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.counterTabs.setTabShape(QtGui.QTabWidget.Triangular)
        self.counterTabs.setObjectName(_fromUtf8("counterTabs"))
        self.simpleTab = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.simpleTab.sizePolicy().hasHeightForWidth())
        self.simpleTab.setSizePolicy(sizePolicy)
        self.simpleTab.setObjectName(_fromUtf8("simpleTab"))
        self.gridLayout = QtGui.QGridLayout(self.simpleTab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(
            0, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.beatCountComboBox = QtGui.QComboBox(self.simpleTab)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.beatCountComboBox.sizePolicy().hasHeightForWidth())
        self.beatCountComboBox.setSizePolicy(sizePolicy)
        self.beatCountComboBox.setMinimumSize(QtCore.QSize(0, 0))
        self.beatCountComboBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.beatCountComboBox.setBaseSize(QtCore.QSize(200, 0))
        self.beatCountComboBox.setObjectName(_fromUtf8("beatCountComboBox"))
        self.gridLayout.addWidget(self.beatCountComboBox, 1, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.simpleTab)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.beatsSpinBox = QtGui.QSpinBox(self.simpleTab)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.beatsSpinBox.sizePolicy().hasHeightForWidth())
        self.beatsSpinBox.setSizePolicy(sizePolicy)
        self.beatsSpinBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.beatsSpinBox.setBaseSize(QtCore.QSize(100, 0))
        self.beatsSpinBox.setMinimum(1)
        self.beatsSpinBox.setMaximum(256)
        self.beatsSpinBox.setProperty("value", 4)
        self.beatsSpinBox.setObjectName(_fromUtf8("beatsSpinBox"))
        self.gridLayout.addWidget(self.beatsSpinBox, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.simpleTab)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(
            0, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.counterTabs.addTab(self.simpleTab, _fromUtf8(""))
        self.complexTab = QtGui.QWidget()
        self.complexTab.setObjectName(_fromUtf8("complexTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.complexTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.complexEditButton = QtGui.QPushButton(self.complexTab)
        self.complexEditButton.setObjectName(_fromUtf8("complexEditButton"))
        self.gridLayout_3.addWidget(self.complexEditButton, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 0, 2, 1, 1)
        self.counterTabs.addTab(self.complexTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.counterTabs)
        self.groupBox = QtGui.QGroupBox(measureTabs)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(415, 66))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setBaseSize(QtCore.QSize(200, 0))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.previewText = QtGui.QLabel(self.groupBox)
        self.previewText.setAlignment(QtCore.Qt.AlignCenter)
        self.previewText.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.previewText.setObjectName(_fromUtf8("previewText"))
        self.verticalLayout_2.addWidget(self.previewText)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem4 = QtGui.QSpacerItem(
            20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem4)
        self.label_2.setBuddy(self.beatsSpinBox)

        self.retranslateUi(measureTabs)
        self.counterTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(measureTabs)

    def retranslateUi(self, measureTabs):
        measureTabs.setWindowTitle(_translate("measureTabs", "Form", None))
        self.simpleTab.setToolTip(_translate(
            "measureTabs", "Edit a simple measure count", None))
        self.beatCountComboBox.setToolTip(_translate(
            "measureTabs", "The number of beats in this measure", None))
        self.label_2.setToolTip(_translate(
            "measureTabs", "The size of each measure in the new score in beats", None))
        self.label_2.setText(_translate("measureTabs", "Beats", None))
        self.beatsSpinBox.setToolTip(_translate(
            "measureTabs", "The size of each measure in the new score in beats", None))
        self.beatsSpinBox.setStatusTip(_translate(
            "measureTabs", "The size of each measure in the new score in beats", None))
        self.beatsSpinBox.setSuffix(_translate("measureTabs", " beats", None))
        self.label_3.setToolTip(_translate(
            "measureTabs", "The number of beats in this measure", None))
        self.label_3.setText(_translate("measureTabs", "Beat count", None))
        self.counterTabs.setTabText(self.counterTabs.indexOf(
            self.simpleTab), _translate("measureTabs", "Simple Count", None))
        self.complexTab.setToolTip(_translate(
            "measureTabs", "Edit a complex measure count", None))
        self.complexEditButton.setToolTip(_translate(
            "measureTabs", "Edit a complex count", None))
        self.complexEditButton.setText(
            _translate("measureTabs", "Edit Count", None))
        self.counterTabs.setTabText(self.counterTabs.indexOf(
            self.complexTab), _translate("measureTabs", "Complex Count", None))
        self.groupBox.setToolTip(_translate(
            "measureTabs", "A preview of the measure count currently selected", None))
        self.groupBox.setTitle(_translate("measureTabs", "Preview", None))
        self.previewText.setText(_translate("measureTabs", "TextLabel", None))
