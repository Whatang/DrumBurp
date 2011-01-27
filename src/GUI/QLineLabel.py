'''
Created on 19 Jan 2011

@author: Mike Thomas
'''

from QDBGridItem import QDBGridItem
from QEditKitDialog import QEditKitDialog
from PyQt4.QtCore import Qt

class QLineLabel(QDBGridItem):
    def __init__(self, drum, qScore, parent):
        super(QLineLabel, self).__init__(qScore, parent)
        self.setText(drum.abbr)
        self.setToolTip(drum.name)
        self.setCursor(Qt.PointingHandCursor)

    def cellHeight(self):
        return self._props.ySpacing

    def cellWidth(self):
        return self._props.LINELABELWIDTH

    def mouseDoubleClickEvent(self, event_):
        editDialog = QEditKitDialog(self.scene().score.drumKit,
                                    self.scene().parent())
        if editDialog.exec_():
            newKit, changes = editDialog.getNewKit()
            self.scene().score.changeKit(newKit, changes)
            self.scene().reBuild()
            self.scene().dirty = True

