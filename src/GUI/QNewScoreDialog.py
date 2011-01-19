'''
Created on 9 Jan 2011

@author: Mike Thomas

'''

from ui_newScoreDialog import Ui_newScoreDialog
from PyQt4.QtGui import QDialog
from DBUtility import populateCounterCombo

class QNewScoreDialog(QDialog, Ui_newScoreDialog):
    '''
    classdocs
    '''
    def __init__(self, parent = None, beats = 4, counter = None):
        '''
        Constructor
        '''
        super(QNewScoreDialog, self).__init__(parent)
        self.setupUi(self)
        self.beatsSpinBox.setValue(beats)
        populateCounterCombo(self.beatCountComboBox, counter)

    def getValues(self):
        bc = self.beatCountComboBox
        beatCount = bc.itemData(bc.currentIndex()).toInt()[0]
        return (self.numMeasuresSpinBox.value(),
                self.beatsSpinBox.value(),
                beatCount)
