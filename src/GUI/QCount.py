'''
Created on 19 Jan 2011

@author: Mike Thomas

'''

from QDBGridItem import QDBGridItem
from PyQt4.QtCore import Qt

class QCount(QDBGridItem):
    '''
    classdocs
    '''


    def __init__(self, count, qScore, parent):
        '''
        Constructor
        '''
        super(QCount, self).__init__(qScore, parent)
        self._qMeasure = parent
        self._index = None
        self.setCursor(Qt.PointingHandCursor)
        self.setText(count)

    def setIndex(self, index):
        self._index = index

    def cellWidth(self):
        return self._props.xSpacing

    def cellHeight(self):
        return self._props.ySpacing

    def mouseDoubleClickEvent(self, dummyEvent):
        self._qMeasure.editMeasureProperties()
