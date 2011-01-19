'''
Created on 9 Jan 2011

@author: Mike Thomas
'''
from ui_insertMeasuresDialog import Ui_InsertMeasuresDialog
from PyQt4.QtGui import QDialog
import DBUtility

class QInsertMeasuresDialog(QDialog, Ui_InsertMeasuresDialog):
    '''
    classdocs
    '''
    def __init__(self, parent = None, measureBeats = 4, beatCounter = None):
        '''
        Constructor
        '''
        super(QInsertMeasuresDialog, self).__init__(parent)
        self.setupUi(self)
        self.beatsSpinBox.setValue(measureBeats)
        DBUtility.populateCounterCombo(self.countComboBox, beatCounter)

    def getValues(self):
        cb = self.countComboBox
        beatCount = cb.itemData(cb.currentIndex()).toInt()[0]
        return (self.numMeasuresSpinBox.value(),
                self.beatsSpinBox.value(),
                beatCount,
                self.beforeButton.isChecked())
