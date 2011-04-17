'''
Created on 9 Jan 2011

@author: Mike Thomas

'''

from ui_newScoreDialog import Ui_newScoreDialog
from PyQt4.QtGui import QDialog
from DBUtility import populateCounterCombo
from Data.MeasureCount import makeSimpleCount

class QNewScoreDialog(QDialog, Ui_newScoreDialog):
    '''
    classdocs
    '''
    def __init__(self, parent = None, beats = 4,
                 counter = None, registry = None):
        '''
        Constructor
        '''
        super(QNewScoreDialog, self).__init__(parent)
        self.setupUi(self)
        self.beatsSpinBox.setValue(beats)
        populateCounterCombo(self.beatCountComboBox, counter, registry)
        self.registry = registry

    def getValues(self):
        bc = self.beatCountComboBox
        beatCount = self.registry[bc.currentIndex()]
        mc = makeSimpleCount(beatCount, self.beatsSpinBox.value())
        return (self.numMeasuresSpinBox.value(),
                mc)
