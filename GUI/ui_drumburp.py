# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\drumburp.ui'
#
# Created: Sat Dec 11 19:14:41 2010
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DrumBurpWindow(object):
    def setupUi(self, DrumBurpWindow):
        DrumBurpWindow.setObjectName(_fromUtf8("DrumBurpWindow"))
        DrumBurpWindow.resize(800, 600)
        DrumBurpWindow.setAnimated(True)
        self.centralwidget = QtGui.QWidget(DrumBurpWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.optionsFrame = QtGui.QFrame(self.centralwidget)
        self.optionsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.optionsFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.optionsFrame.setObjectName(_fromUtf8("optionsFrame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.optionsFrame)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.noteHeadGroupBox = QtGui.QGroupBox(self.optionsFrame)
        self.noteHeadGroupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.noteHeadGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.noteHeadGroupBox.setObjectName(_fromUtf8("noteHeadGroupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.noteHeadGroupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.defaultNoteHeadButton = RadioButtonTeller(self.noteHeadGroupBox)
        self.defaultNoteHeadButton.setChecked(True)
        self.defaultNoteHeadButton.setObjectName(_fromUtf8("defaultNoteHeadButton"))
        self.verticalLayout.addWidget(self.defaultNoteHeadButton)
        self.xNoteHeadButton = RadioButtonTeller(self.noteHeadGroupBox)
        self.xNoteHeadButton.setObjectName(_fromUtf8("xNoteHeadButton"))
        self.verticalLayout.addWidget(self.xNoteHeadButton)
        self.bigXNoteHeadButton = RadioButtonTeller(self.noteHeadGroupBox)
        self.bigXNoteHeadButton.setObjectName(_fromUtf8("bigXNoteHeadButton"))
        self.verticalLayout.addWidget(self.bigXNoteHeadButton)
        self.oNoteHeadButton = RadioButtonTeller(self.noteHeadGroupBox)
        self.oNoteHeadButton.setObjectName(_fromUtf8("oNoteHeadButton"))
        self.verticalLayout.addWidget(self.oNoteHeadButton)
        self.bigONoteHeadButton = RadioButtonTeller(self.noteHeadGroupBox)
        self.bigONoteHeadButton.setObjectName(_fromUtf8("bigONoteHeadButton"))
        self.verticalLayout.addWidget(self.bigONoteHeadButton)
        self.plusNoteHeadButton = RadioButtonTeller(self.noteHeadGroupBox)
        self.plusNoteHeadButton.setObjectName(_fromUtf8("plusNoteHeadButton"))
        self.verticalLayout.addWidget(self.plusNoteHeadButton)
        self.gNoteHeadButton = RadioButtonTeller(self.noteHeadGroupBox)
        self.gNoteHeadButton.setObjectName(_fromUtf8("gNoteHeadButton"))
        self.verticalLayout.addWidget(self.gNoteHeadButton)
        self.verticalLayout_2.addWidget(self.noteHeadGroupBox)
        self.displayOptionsGroupBox = QtGui.QGroupBox(self.optionsFrame)
        self.displayOptionsGroupBox.setObjectName(_fromUtf8("displayOptionsGroupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.displayOptionsGroupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.spacingLabel = QtGui.QLabel(self.displayOptionsGroupBox)
        self.spacingLabel.setWordWrap(True)
        self.spacingLabel.setObjectName(_fromUtf8("spacingLabel"))
        self.verticalLayout_3.addWidget(self.spacingLabel)
        self.spaceSlider = QtGui.QSlider(self.displayOptionsGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spaceSlider.sizePolicy().hasHeightForWidth())
        self.spaceSlider.setSizePolicy(sizePolicy)
        self.spaceSlider.setMaximum(100)
        self.spaceSlider.setProperty(_fromUtf8("value"), 0)
        self.spaceSlider.setTracking(False)
        self.spaceSlider.setOrientation(QtCore.Qt.Horizontal)
        self.spaceSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.spaceSlider.setObjectName(_fromUtf8("spaceSlider"))
        self.verticalLayout_3.addWidget(self.spaceSlider)
        self.label = QtGui.QLabel(self.displayOptionsGroupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.verticalSlider = QtGui.QSlider(self.displayOptionsGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalSlider.sizePolicy().hasHeightForWidth())
        self.verticalSlider.setSizePolicy(sizePolicy)
        self.verticalSlider.setMaximum(100)
        self.verticalSlider.setTracking(False)
        self.verticalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.verticalSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.verticalSlider.setObjectName(_fromUtf8("verticalSlider"))
        self.verticalLayout_3.addWidget(self.verticalSlider)
        self.label_2 = QtGui.QLabel(self.displayOptionsGroupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_3.addWidget(self.label_2)
        self.lineSpaceSlider = QtGui.QSlider(self.displayOptionsGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineSpaceSlider.sizePolicy().hasHeightForWidth())
        self.lineSpaceSlider.setSizePolicy(sizePolicy)
        self.lineSpaceSlider.setMaximum(100)
        self.lineSpaceSlider.setTracking(False)
        self.lineSpaceSlider.setOrientation(QtCore.Qt.Horizontal)
        self.lineSpaceSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.lineSpaceSlider.setObjectName(_fromUtf8("lineSpaceSlider"))
        self.verticalLayout_3.addWidget(self.lineSpaceSlider)
        self.widthLabel = QtGui.QLabel(self.displayOptionsGroupBox)
        self.widthLabel.setObjectName(_fromUtf8("widthLabel"))
        self.verticalLayout_3.addWidget(self.widthLabel)
        self.widthGroupBox = QtGui.QFrame(self.displayOptionsGroupBox)
        self.widthGroupBox.setFrameShape(QtGui.QFrame.StyledPanel)
        self.widthGroupBox.setFrameShadow(QtGui.QFrame.Raised)
        self.widthGroupBox.setObjectName(_fromUtf8("widthGroupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widthGroupBox)
        self.horizontalLayout_2.setContentsMargins(-1, 0, 0, 0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.fixedWidthCheckBox = QtGui.QCheckBox(self.widthGroupBox)
        self.fixedWidthCheckBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.fixedWidthCheckBox.setChecked(True)
        self.fixedWidthCheckBox.setObjectName(_fromUtf8("fixedWidthCheckBox"))
        self.horizontalLayout_2.addWidget(self.fixedWidthCheckBox)
        self.widthSpinBox = QtGui.QSpinBox(self.widthGroupBox)
        self.widthSpinBox.setMinimum(10)
        self.widthSpinBox.setMaximum(1000)
        self.widthSpinBox.setProperty(_fromUtf8("value"), 80)
        self.widthSpinBox.setObjectName(_fromUtf8("widthSpinBox"))
        self.horizontalLayout_2.addWidget(self.widthSpinBox)
        self.verticalLayout_3.addWidget(self.widthGroupBox)
        self.fontComboBox = QtGui.QFontComboBox(self.displayOptionsGroupBox)
        self.fontComboBox.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fontComboBox.sizePolicy().hasHeightForWidth())
        self.fontComboBox.setSizePolicy(sizePolicy)
        self.fontComboBox.setEditable(False)
        self.fontComboBox.setMaxVisibleItems(20)
        self.fontComboBox.setFontFilters(QtGui.QFontComboBox.ScalableFonts)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("BatangChe"))
        font.setPointSize(10)
        self.fontComboBox.setCurrentFont(font)
        self.fontComboBox.setObjectName(_fromUtf8("fontComboBox"))
        self.verticalLayout_3.addWidget(self.fontComboBox)
        self.verticalLayout_2.addWidget(self.displayOptionsGroupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout_2.addWidget(self.optionsFrame, 0, 0, 2, 1)
        self.songPropertiesGroupBox = QtGui.QGroupBox(self.centralwidget)
        self.songPropertiesGroupBox.setObjectName(_fromUtf8("songPropertiesGroupBox"))
        self.gridLayout = QtGui.QGridLayout(self.songPropertiesGroupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.songNameLabel = QtGui.QLabel(self.songPropertiesGroupBox)
        self.songNameLabel.setObjectName(_fromUtf8("songNameLabel"))
        self.gridLayout.addWidget(self.songNameLabel, 0, 0, 1, 1)
        self.songNameEdit = QtGui.QLineEdit(self.songPropertiesGroupBox)
        self.songNameEdit.setObjectName(_fromUtf8("songNameEdit"))
        self.gridLayout.addWidget(self.songNameEdit, 0, 1, 1, 1)
        self.bpmLabel = QtGui.QLabel(self.songPropertiesGroupBox)
        self.bpmLabel.setObjectName(_fromUtf8("bpmLabel"))
        self.gridLayout.addWidget(self.bpmLabel, 0, 2, 1, 1)
        self.artistNameLabel = QtGui.QLabel(self.songPropertiesGroupBox)
        self.artistNameLabel.setObjectName(_fromUtf8("artistNameLabel"))
        self.gridLayout.addWidget(self.artistNameLabel, 1, 0, 1, 1)
        self.artistNameEdit = QtGui.QLineEdit(self.songPropertiesGroupBox)
        self.artistNameEdit.setObjectName(_fromUtf8("artistNameEdit"))
        self.gridLayout.addWidget(self.artistNameEdit, 1, 1, 1, 1)
        self.tabberLabel = QtGui.QLabel(self.songPropertiesGroupBox)
        self.tabberLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.tabberLabel.setObjectName(_fromUtf8("tabberLabel"))
        self.gridLayout.addWidget(self.tabberLabel, 1, 2, 1, 1)
        self.tabberEdit = QtGui.QLineEdit(self.songPropertiesGroupBox)
        self.tabberEdit.setObjectName(_fromUtf8("tabberEdit"))
        self.gridLayout.addWidget(self.tabberEdit, 1, 3, 1, 1)
        self.bpmFrame = QtGui.QFrame(self.songPropertiesGroupBox)
        self.bpmFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.bpmFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.bpmFrame.setObjectName(_fromUtf8("bpmFrame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.bpmFrame)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.bpmSpinBox = QtGui.QSpinBox(self.bpmFrame)
        self.bpmSpinBox.setMaximum(300)
        self.bpmSpinBox.setProperty(_fromUtf8("value"), 120)
        self.bpmSpinBox.setObjectName(_fromUtf8("bpmSpinBox"))
        self.horizontalLayout.addWidget(self.bpmSpinBox)
        spacerItem1 = QtGui.QSpacerItem(154, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addWidget(self.bpmFrame, 0, 3, 1, 1)
        self.gridLayout_2.addWidget(self.songPropertiesGroupBox, 0, 1, 1, 1)
        self.scoreView = ScoreView(self.centralwidget)
        self.scoreView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.scoreView.setAcceptDrops(False)
        self.scoreView.setLineWidth(1)
        self.scoreView.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scoreView.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.scoreView.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)
        self.scoreView.setObjectName(_fromUtf8("scoreView"))
        self.gridLayout_2.addWidget(self.scoreView, 1, 1, 1, 1)
        DrumBurpWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(DrumBurpWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        DrumBurpWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(DrumBurpWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        DrumBurpWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(DrumBurpWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        DrumBurpWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionQuit = QtGui.QAction(DrumBurpWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionNew = QtGui.QAction(DrumBurpWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionLoad = QtGui.QAction(DrumBurpWindow)
        self.actionLoad.setObjectName(_fromUtf8("actionLoad"))
        self.actionSave = QtGui.QAction(DrumBurpWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_As = QtGui.QAction(DrumBurpWindow)
        self.actionSave_As.setObjectName(_fromUtf8("actionSave_As"))
        self.actionExport_ASCII = QtGui.QAction(DrumBurpWindow)
        self.actionExport_ASCII.setObjectName(_fromUtf8("actionExport_ASCII"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_ASCII)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionLoad)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSave_As)
        self.toolBar.addAction(self.actionExport_ASCII)
        self.spacingLabel.setBuddy(self.spaceSlider)
        self.songNameLabel.setBuddy(self.songNameEdit)
        self.bpmLabel.setBuddy(self.bpmSpinBox)
        self.artistNameLabel.setBuddy(self.artistNameEdit)
        self.tabberLabel.setBuddy(self.tabberEdit)

        self.retranslateUi(DrumBurpWindow)
        QtCore.QObject.connect(self.fixedWidthCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.widthSpinBox.setEnabled)
        QtCore.QObject.connect(self.defaultNoteHeadButton, QtCore.SIGNAL(_fromUtf8("emitValue(QString)")), self.scoreView.setNoteHead)
        QtCore.QObject.connect(self.xNoteHeadButton, QtCore.SIGNAL(_fromUtf8("emitValue(QString)")), self.scoreView.setNoteHead)
        QtCore.QObject.connect(self.bigXNoteHeadButton, QtCore.SIGNAL(_fromUtf8("emitValue(QString)")), self.scoreView.setNoteHead)
        QtCore.QObject.connect(self.oNoteHeadButton, QtCore.SIGNAL(_fromUtf8("emitValue(QString)")), self.scoreView.setNoteHead)
        QtCore.QObject.connect(self.bigONoteHeadButton, QtCore.SIGNAL(_fromUtf8("emitValue(QString)")), self.scoreView.setNoteHead)
        QtCore.QObject.connect(self.plusNoteHeadButton, QtCore.SIGNAL(_fromUtf8("emitValue(QString)")), self.scoreView.setNoteHead)
        QtCore.QObject.connect(self.gNoteHeadButton, QtCore.SIGNAL(_fromUtf8("emitValue(QString)")), self.scoreView.setNoteHead)
        QtCore.QObject.connect(self.spaceSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.scoreView.horizontalSpacingChanged)
        QtCore.QObject.connect(self.verticalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.scoreView.verticalSpacingChanged)
        QtCore.QObject.connect(self.lineSpaceSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.scoreView.systemSpacingChanged)
        QtCore.QObject.connect(self.fontComboBox, QtCore.SIGNAL(_fromUtf8("currentFontChanged(QFont)")), self.scoreView.setFont)
        QtCore.QMetaObject.connectSlotsByName(DrumBurpWindow)
        DrumBurpWindow.setTabOrder(self.defaultNoteHeadButton, self.xNoteHeadButton)
        DrumBurpWindow.setTabOrder(self.xNoteHeadButton, self.bigXNoteHeadButton)
        DrumBurpWindow.setTabOrder(self.bigXNoteHeadButton, self.oNoteHeadButton)
        DrumBurpWindow.setTabOrder(self.oNoteHeadButton, self.bigONoteHeadButton)
        DrumBurpWindow.setTabOrder(self.bigONoteHeadButton, self.plusNoteHeadButton)
        DrumBurpWindow.setTabOrder(self.plusNoteHeadButton, self.songNameEdit)
        DrumBurpWindow.setTabOrder(self.songNameEdit, self.artistNameEdit)
        DrumBurpWindow.setTabOrder(self.artistNameEdit, self.bpmSpinBox)
        DrumBurpWindow.setTabOrder(self.bpmSpinBox, self.tabberEdit)

    def retranslateUi(self, DrumBurpWindow):
        DrumBurpWindow.setWindowTitle(QtGui.QApplication.translate("DrumBurpWindow", "DrumBurp", None, QtGui.QApplication.UnicodeUTF8))
        self.noteHeadGroupBox.setTitle(QtGui.QApplication.translate("DrumBurpWindow", "Note Head", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultNoteHeadButton.setText(QtGui.QApplication.translate("DrumBurpWindow", "Default", None, QtGui.QApplication.UnicodeUTF8))
        self.xNoteHeadButton.setText(QtGui.QApplication.translate("DrumBurpWindow", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.xNoteHeadButton.setProperty(_fromUtf8("buttonValue"), QtGui.QApplication.translate("DrumBurpWindow", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.bigXNoteHeadButton.setText(QtGui.QApplication.translate("DrumBurpWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.bigXNoteHeadButton.setProperty(_fromUtf8("buttonValue"), QtGui.QApplication.translate("DrumBurpWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.oNoteHeadButton.setText(QtGui.QApplication.translate("DrumBurpWindow", "o", None, QtGui.QApplication.UnicodeUTF8))
        self.oNoteHeadButton.setProperty(_fromUtf8("buttonValue"), QtGui.QApplication.translate("DrumBurpWindow", "o", None, QtGui.QApplication.UnicodeUTF8))
        self.bigONoteHeadButton.setText(QtGui.QApplication.translate("DrumBurpWindow", "O", None, QtGui.QApplication.UnicodeUTF8))
        self.bigONoteHeadButton.setProperty(_fromUtf8("buttonValue"), QtGui.QApplication.translate("DrumBurpWindow", "O", None, QtGui.QApplication.UnicodeUTF8))
        self.plusNoteHeadButton.setText(QtGui.QApplication.translate("DrumBurpWindow", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.plusNoteHeadButton.setProperty(_fromUtf8("buttonValue"), QtGui.QApplication.translate("DrumBurpWindow", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.gNoteHeadButton.setText(QtGui.QApplication.translate("DrumBurpWindow", "g", None, QtGui.QApplication.UnicodeUTF8))
        self.gNoteHeadButton.setProperty(_fromUtf8("buttonValue"), QtGui.QApplication.translate("DrumBurpWindow", "g", None, QtGui.QApplication.UnicodeUTF8))
        self.displayOptionsGroupBox.setTitle(QtGui.QApplication.translate("DrumBurpWindow", "Display Options", None, QtGui.QApplication.UnicodeUTF8))
        self.spacingLabel.setText(QtGui.QApplication.translate("DrumBurpWindow", "Horizontal Spacing", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DrumBurpWindow", "Vertical Spacing", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DrumBurpWindow", "System Spacing", None, QtGui.QApplication.UnicodeUTF8))
        self.widthLabel.setText(QtGui.QApplication.translate("DrumBurpWindow", "Width", None, QtGui.QApplication.UnicodeUTF8))
        self.fixedWidthCheckBox.setText(QtGui.QApplication.translate("DrumBurpWindow", "Fixed", None, QtGui.QApplication.UnicodeUTF8))
        self.songPropertiesGroupBox.setTitle(QtGui.QApplication.translate("DrumBurpWindow", "Song Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.songNameLabel.setText(QtGui.QApplication.translate("DrumBurpWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.bpmLabel.setText(QtGui.QApplication.translate("DrumBurpWindow", "&BPM", None, QtGui.QApplication.UnicodeUTF8))
        self.artistNameLabel.setText(QtGui.QApplication.translate("DrumBurpWindow", "&Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.tabberLabel.setText(QtGui.QApplication.translate("DrumBurpWindow", "&Tabbed by", None, QtGui.QApplication.UnicodeUTF8))
        self.bpmSpinBox.setSuffix(QtGui.QApplication.translate("DrumBurpWindow", " bpm", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("DrumBurpWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("DrumBurpWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("DrumBurpWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setToolTip(QtGui.QApplication.translate("DrumBurpWindow", "Quit DrumBurp", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("DrumBurpWindow", "&New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setShortcut(QtGui.QApplication.translate("DrumBurpWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setText(QtGui.QApplication.translate("DrumBurpWindow", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setShortcut(QtGui.QApplication.translate("DrumBurpWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("DrumBurpWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("DrumBurpWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_As.setText(QtGui.QApplication.translate("DrumBurpWindow", "Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_ASCII.setText(QtGui.QApplication.translate("DrumBurpWindow", "&Export ASCII", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_ASCII.setShortcut(QtGui.QApplication.translate("DrumBurpWindow", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))

from Widgets.ScoreView_plugin import ScoreView
from Widgets.RadioButtonTeller_plugin import RadioButtonTeller