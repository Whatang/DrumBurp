'''
Created on 31 Jul 2010

@author: Mike Thomas

'''

from GUI.ui_drumburp import Ui_DrumBurpWindow
from PyQt4.QtGui import QMainWindow, QFontDatabase
from PyQt4.QtCore import QTimer
from QScore import QScore
from QSongProperties import QSongProperties

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
        self.fontComboBox.setWritingSystem(QFontDatabase.Latin)
#        QTimer.singleShot(0, lambda: self.widthSpinBox.setValue(80))
        xValue, yValue, lValue = self.songProperties.proportionalSpacing()
        QTimer.singleShot(0, lambda: self.spaceSlider.setValue(xValue))
        QTimer.singleShot(0, lambda: self.verticalSlider.setValue(yValue))
        QTimer.singleShot(0, lambda: self.lineSpaceSlider.setValue(lValue))
        font = self.scoreScene.font()
        self.fontComboBox.setCurrentFont(font)
        statusBar = self.statusBar()
        statusBar.showMessage("Welcome to %s" % APPNAME, 5000)

    def on_actionFitInWindow_triggered(self):
        widthInPixels = self.scoreView.width()
        maxColumns = self.songProperties.maxColumns(widthInPixels)
        self.widthSpinBox.setValue(maxColumns)
