'''
Created on 19 Jan 2011

@author: Mike Thomas
'''

from QDBGridItem import QDBGridItem

class QLineLabel(QDBGridItem):
    def __init__(self, lineName, qScore, parent):
        super(QLineLabel, self).__init__(qScore, parent)
        self.setText(lineName)

    def cellHeight(self):
        return self._props.ySpacing

    def cellWidth(self):
        return self._props.LINELABELWIDTH

