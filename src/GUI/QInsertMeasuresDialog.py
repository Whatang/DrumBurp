'''
Created on 9 Jan 2011

@author: Mike Thomas
'''
from ui_insertMeasuresDialog import Ui_InsertMeasuresDialog
from PyQt4.QtGui import QDialog
import Data.MeasureCount
from QComplexCountDialog import QComplexCountDialog

class QInsertMeasuresDialog(QDialog, Ui_InsertMeasuresDialog):
    '''
    classdocs
    '''
    def __init__(self, parent, measureCount, counterRegistry):
        '''
        Constructor
        '''
        super(QInsertMeasuresDialog, self).__init__(parent)
        self.setupUi(self)
        self.measureTabs.setup(measureCount, counterRegistry,
                               Data.MeasureCount, QComplexCountDialog)
        restore = self.buttonBox.button(self.buttonBox.RestoreDefaults)
        restore.clicked.connect(self._restoreDefault)

    def getValues(self):
        mc = self.measureTabs.getCounter()
        return (self.numMeasuresSpinBox.value(),
                mc,
                self.beforeButton.isChecked())

    def _restoreDefault(self):
        self.measureTabs.restoreOriginal()
        self.numMeasuresSpinBox.setValue(1)
        self.beforeButton.setChecked(True)
