'''
Created on 19 Jan 2011

@author: Mike Thomas

'''

from PyQt4.QtGui import QMenu
from PyQt4 import QtCore

class QMenuIgnoreCancelClick(QMenu):
    '''
    classdocs
    '''


    def __init__(self, qScore, parent = None):
        '''
        Constructor
        '''
        super(QMenuIgnoreCancelClick, self).__init__(parent)
        self._qScore = qScore
        self.connect(self, QtCore.SIGNAL("aboutToHide()"),
                     self._checkGoodSelection)

    def _checkGoodSelection(self):
        if self.activeAction() == None:
            self._qScore.ignoreNextClick()

