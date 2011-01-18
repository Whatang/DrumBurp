'''
Created on 17 Jan 2011

@author: Mike Thomas
'''

from ui_repeatDialog import Ui_RepeatDialog
from PyQt4.QtGui import QDialog

class QRepeatDialog(QDialog, Ui_RepeatDialog):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(QRepeatDialog, self).__init__(parent)
        self.setupUi(self)

    def getValues(self):
        return (self.numRepeatsSpinBox.value(),
                self.repeatIntervalSpinBox.value())
