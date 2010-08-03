'''
Created on 31 Jul 2010

@author: Mike Thomas

'''

from GUI.ui_drumburp import Ui_DrumBurpWindow
from Model.SongModel import SongModel
from PyQt4.QtCore import pyqtSignature, Qt, SIGNAL, QTimer
from PyQt4.QtGui import QMainWindow, QFontMetrics

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
        self.oldRowCount = 0
        self.model = SongModel()
        self.scoreView.setModel(self.model)
        self.connect(self.model, SIGNAL("modelReset()"),
                     self.scoreView.resizeTable)
        QTimer.singleShot(0, self.scoreView.resizeTable)
        statusBar = self.statusBar()
        statusBar.showMessage("Welcome to %s" % APPNAME, 5000)
