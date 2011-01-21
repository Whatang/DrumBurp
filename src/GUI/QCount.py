'''
Created on 19 Jan 2011

@author: Mike Thomas

'''

from QDBGridItem import QDBGridItem

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
        self.setText(count)

    def setIndex(self, index):
        self._index = index

    def cellWidth(self):
        return self._props.xSpacing

    def cellHeight(self):
        return self._props.ySpacing

    def mouseDoubleClickEvent(self, event):
        self._qMeasure.editMeasureProperties()
