'''
Created on 20 Jan 2011

@author: Mike Thomas

'''

from ui_measurePropertiesDialog import Ui_measurePropertiesDialog
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature
import DBUtility
from Data.MeasureCount import makeSimpleCount

class QEditMeasureDialog(QDialog, Ui_measurePropertiesDialog):
    '''
    classdocs
    '''


    def __init__(self, parent = None, beats = 4, beatCounter = None,
                 defaultBeats = 4, defaultBeatCounter = None, counterRegistry = None):
        '''
        Constructor
        '''
        super(QEditMeasureDialog, self).__init__(parent = parent)
        self.setupUi(self)
        if beatCounter == None:
            beatCounter = defaultBeatCounter
        DBUtility.populateCounterCombo(self.beatCountComboBox,
                                       beatCounter, counterRegistry)
        self.beats = beats
        self.beatsSpinBox.setValue(self.beats)
        self.beatCounter = beatCounter
        self.defaultBeats = defaultBeats
        self.defaultBeatCounter = defaultBeatCounter
        self.registry = counterRegistry

    def getValues(self):
        cb = self.beatCountComboBox
        beatCount = self.registry[cb.currentIndex()]
        mc = makeSimpleCount(beatCount, self.beatsSpinBox.value())
        return mc

    @pyqtSignature("")
    def on_restoreButton_clicked(self):
        self.beatsSpinBox.setValue(self.beats)
        DBUtility.populateCounterCombo(self.beatCountComboBox,
                                       self.beatCounter,
                                       self.registry)

    @pyqtSignature("")
    def on_defaultButton_clicked(self):
        self.beatsSpinBox.setValue(self.defaultBeats)
        DBUtility.populateCounterCombo(self.beatCountComboBox,
                                       self.defaultBeatCounter,
                                       self.registry)
