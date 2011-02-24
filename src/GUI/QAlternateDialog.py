'''
Created on 22 Feb 2011

@author: Mike Thomas

'''
from PyQt4.QtGui import QDialog
from ui_alternateRepeats import Ui_AlternateDialog
class QAlternateDialog(QDialog, Ui_AlternateDialog):
    def __init__(self, alternate, parent = None):
        super(QAlternateDialog, self).__init__(parent = parent)
        self.setupUi(self)
        if alternate is not None:
            self.repeatText.setText(alternate)

    def getValue(self):
        text = unicode(self.repeatText.text())
        if len(text) == 0:
            text = None
        return text
