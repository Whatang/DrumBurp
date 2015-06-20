'''
Created on Feb 25, 2012

@author: Mike
'''

from GUI.ui_alternateRepeatWidget import Ui_AlternateWidget
from PyQt4.QtGui import QWidget

class QAlternateWidget(QWidget, Ui_AlternateWidget):
    def __init__(self, startVal, endVal, isRange, parent = None):
        super(QAlternateWidget, self).__init__(parent)
        self.setupUi(self)
        self.startBox.setValue(startVal)
        self.endBox.setValue(endVal)
        self.rangeCheck.setChecked(isRange)

    def getString(self):
        if self.rangeCheck.isChecked():
            return "%d-%d" % (self.startBox.value(), self.endBox.value())
        else:
            return "%d" % (self.startBox.value())

    def highValue(self):
        if self.rangeCheck.isChecked():
            return self.startBox.value()
        else:
            return max(self.startBox.value(), self.endBox.value())
