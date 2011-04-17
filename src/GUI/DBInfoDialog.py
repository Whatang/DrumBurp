'''
Created on 17 Apr 2011

@author: Mike Thomas
'''

from ui_dbInfo import Ui_InfoDialog
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature
from DBLicense import DBLicenseDialog

class DBInfoDialog(QDialog, Ui_InfoDialog):
    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(DBInfoDialog, self).__init__(parent)
        self.setupUi(self)

    @pyqtSignature("")
    def on_licenseButton_clicked(self):
        dlg = DBLicenseDialog()
        dlg.exec_()
