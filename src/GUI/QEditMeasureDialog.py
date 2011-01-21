'''
Created on 20 Jan 2011

@author: Mike Thomas

'''

from ui_measurePropertiesDialog import Ui_measurePropertiesDialog
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature
from Data.TimeCounter import counterMaker
import DBUtility


class QEditMeasureDialog(QDialog, Ui_measurePropertiesDialog):
    '''
    classdocs
    '''


    def __init__(self, parent = None, numTicks = 16, beatCounter = None,
                 defaultBeats = 4, defaultBeatCounter = None):
        '''
        Constructor
        '''
        super(QEditMeasureDialog, self).__init__(parent = parent)
        self.setupUi(self)
        if beatCounter == None:
            beatCounter = counterMaker(1)
        DBUtility.populateCounterCombo(self.beatCountComboBox,
                                       beatCounter)
        self.beats = numTicks / beatCounter.beatLength
        self.beatsSpinBox.setValue(self.beats)
        self.beatCounter = beatCounter
        self.defaultBeats = defaultBeats
        self.defaultBeatCounter = defaultBeatCounter

    def getValues(self):
        cb = self.beatCountComboBox
        beatCount = cb.itemData(cb.currentIndex()).toInt()[0]
        return (self.beatsSpinBox.value(),
                beatCount)

    @pyqtSignature("")
    def on_restoreButton_clicked(self):
        self.beatsSpinBox.setValue(self.beats)
        DBUtility.populateCounterCombo(self.beatCountComboBox,
                                       self.beatCounter)

    @pyqtSignature("")
    def on_defaultButton_clicked(self):
        self.beatsSpinBox.setValue(self.defaultBeats)
        DBUtility.populateCounterCombo(self.beatCountComboBox,
                                       self.defaultBeatCounter)
