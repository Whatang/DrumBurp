'''
Created on 9 Jan 2011

@author: Mike Thomas
'''
from ui_insertMeasuresDialog import Ui_InsertMeasuresDialog
from PyQt4.QtGui import QDialog

class QInsertMeasuresDialog(QDialog, Ui_InsertMeasuresDialog):
    '''
    classdocs
    '''
    def __init__(self, parent = None, measureWidth = 16):
        '''
        Constructor
        '''
        super(QInsertMeasuresDialog, self).__init__(parent)
        self.setupUi(self)
        self.measureSizeSpinBox.setValue(measureWidth)

    def getValues(self):
        return (self.numMeasuresSpinBox.value(),
                self.measureSizeSpinBox.value(),
                self.beforeButton.isChecked())
