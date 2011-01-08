'''
Created on 31 Jul 2010

@author: Mike Thomas

'''

from GUI.ui_drumburp import Ui_DrumBurpWindow
from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import QTimer
from GUI.QScore import QScore, QSongProperties

APPNAME = "DrumBurp"

class DrumBurp(QMainWindow, Ui_DrumBurpWindow):
    '''
    classdocs
    '''


    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(DrumBurp, self).__init__(parent)
        self.setupUi(self)
        self.filename = None
        self.songProperties = QSongProperties()
        self.scoreScene = QScore(self)
        self.scoreView.setScene(self.scoreScene)

        self.fontComboBox.setWritingSystem(1)
#        QTimer.singleShot(0, lambda: self.widthSpinBox.setValue(80))
        xValue, yValue, lValue = self.songProperties.proportionalSpacing()
        QTimer.singleShot(0, lambda: self.spaceSlider.setValue(xValue))
        QTimer.singleShot(0, lambda: self.verticalSlider.setValue(yValue))
        QTimer.singleShot(0, lambda: self.lineSpaceSlider.setValue(lValue))
        font = self.scoreScene.font()
        self.fontComboBox.setCurrentFont(font)
        self.actionDisplayOptionsIsVisible.setChecked(True)
        self.actionNoteHeadSelectorIsVisble.setChecked(True)
        self.actionSongPropertiesIsVisible.setChecked(True)
        statusBar = self.statusBar()
        statusBar.showMessage("Welcome to %s" % APPNAME, 5000)
