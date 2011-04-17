'''
Created on 9 Jan 2011

@author: Mike Thomas

'''

from ui_newScoreDialog import Ui_newScoreDialog
from PyQt4.QtGui import QDialog
import Data.MeasureCount

class QNewScoreDialog(QDialog, Ui_newScoreDialog):
    '''
    classdocs
    '''
    def __init__(self, parent = None,
                 counter = None, registry = None):
        '''
        Constructor
        '''
        super(QNewScoreDialog, self).__init__(parent)
        self.setupUi(self)
        self.measureTabs.setup(counter, registry, Data.MeasureCount)

    def getValues(self):
        mc = self.measureTabs.getCounter()
        return (self.numMeasuresSpinBox.value(), mc)
