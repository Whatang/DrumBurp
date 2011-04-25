'''
Created on 20 Jan 2011

@author: Mike Thomas

'''

from ui_measurePropertiesDialog import Ui_measurePropertiesDialog
from PyQt4.QtGui import QDialog
import Data.MeasureCount
from QComplexCountDialog import QComplexCountDialog

class QEditMeasureDialog(QDialog, Ui_measurePropertiesDialog):
    '''
    classdocs
    '''


    def __init__(self, measureCount,
                 defaultCounter,
                 counterRegistry,
                 parent = None):
        '''
        Constructor
        '''
        super(QEditMeasureDialog, self).__init__(parent = parent)
        self.setupUi(self)
        self.measureTabs.setup(measureCount,
                               counterRegistry,
                               Data.MeasureCount,
                               QComplexCountDialog)
        self._original = measureCount
        self._defaultCounter = defaultCounter
        reset = self.buttonBox.button(self.buttonBox.Reset)
        reset.clicked.connect(self.measureTabs.restoreOriginal)
        restore = self.buttonBox.button(self.buttonBox.RestoreDefaults)
        restore.clicked.connect(self.restoreDefaults)
        reset = self.buttonBox.button(self.buttonBox.Reset)
        reset.clicked.connect(self.resetCount)

    def getValues(self):
        return self.measureTabs.getCounter()

    def restoreDefaults(self):
        self.measureTabs.setBeat(self._defaultCounter)

    def resetCount(self):
        self.measureTabs.setBeat(self._original)
