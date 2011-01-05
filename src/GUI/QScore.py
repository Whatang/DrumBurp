'''
Created on 4 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore

class QScore(QtGui.QGraphicsScene):
    '''
    classdocs
    '''


    def __init__(self, score, parent = None):
        '''
        Constructor
        '''
        super(QScore, self).__init__(parent)
