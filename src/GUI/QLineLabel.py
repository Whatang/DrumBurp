'''
Created on 19 Jan 2011

@author: Mike Thomas
'''

from QDBGridItem import QDBGridItem

class QLineLabel(QDBGridItem):
    def __init__(self, drum, qScore, parent):
        super(QLineLabel, self).__init__(qScore, parent)
        self.setText(drum.abbr)
        self.setToolTip(drum.name)

    def cellHeight(self):
        return self._props.ySpacing

    def cellWidth(self):
        return self._props.LINELABELWIDTH

