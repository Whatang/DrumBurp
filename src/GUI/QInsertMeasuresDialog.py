'''
Created on 9 Jan 2011

@author: Mike Thomas
'''
from ui_insertMeasuresDialog import Ui_InsertMeasuresDialog
from PyQt4.QtGui import QDialog
import DBUtility
from Data.MeasureCount import makeSimpleCount

class QInsertMeasuresDialog(QDialog, Ui_InsertMeasuresDialog):
    '''
    classdocs
    '''
    def __init__(self, parent, measureBeats, beatCounter, counterRegistry):
        '''
        Constructor
        '''
        super(QInsertMeasuresDialog, self).__init__(parent)
        self.setupUi(self)
        self.beatsSpinBox.setValue(measureBeats)
        self._registry = counterRegistry
        DBUtility.populateCounterCombo(self.countComboBox, beatCounter, counterRegistry)

    def getValues(self):
        cb = self.countComboBox
        beatCount = self._registry[cb.currentIndex()]
        mc = makeSimpleCount(beatCount, self.beatsSpinBox.value())
        return (self.numMeasuresSpinBox.value(),
                mc,
                self.beforeButton.isChecked())
