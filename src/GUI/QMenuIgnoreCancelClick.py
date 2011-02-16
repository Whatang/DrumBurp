'''
Created on 19 Jan 2011

@author: Mike Thomas

'''

from PyQt4.QtGui import QMenu

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
        self.aboutToHide.connect(self._checkGoodSelection)

    def _checkGoodSelection(self):
        if self.activeAction() == None:
            self._qScore.ignoreNextClick()

