'''
Created on 17 Apr 2011

@author: Mike Thomas

'''

from PyQt4.QtGui import QDialog
from ui_dbLicense import Ui_dbLicense_dialog

class DBLicenseDialog(QDialog, Ui_dbLicense_dialog):
    '''
    classdocs
    '''


    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(DBLicenseDialog, self).__init__(parent)
        self.setupUi(self)
