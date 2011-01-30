'''
Created on Jan 30, 2011

@author: Mike
'''

from PyQt4.QtGui import QDialog
from ui_repeatCountDialog import Ui_repeatCountDialog

class QRepeatCountDialog(QDialog, Ui_repeatCountDialog):
    '''
    classdocs
    '''


    def __init__(self, repeatCount, parent = None):
        '''
        Constructor
        '''
        super(QRepeatCountDialog, self).__init__(parent = parent)
        self._repeatCount = repeatCount
        self.setupUi(self)
        self.countBox.setValue(repeatCount)

    def getValue(self):
        return self.countBox.value()
