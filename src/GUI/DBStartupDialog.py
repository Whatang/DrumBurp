'''
Created on 17 Apr 2011

@author: Mike Thomas
'''
from ui_dbStartup import Ui_dbStartup
from PyQt4.QtGui import QDialog

class DBStartupDialog(QDialog, Ui_dbStartup):
    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(DBStartupDialog, self).__init__(parent)
        self.setupUi(self)
