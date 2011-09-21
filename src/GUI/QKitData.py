# Copyright 2011 Michael Thomas
#
# See www.whatang.org for more information.
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DrumBurp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DrumBurp.  If not, see <http://www.gnu.org/licenses/>
'''
Created on 13 Mar 2011

@author: Mike Thomas
'''

from QGraphicsListData import QGraphicsListData
from QEditKitDialog import QEditKitDialog

class QKitData(QGraphicsListData):
    '''
    classdocs
    '''

    def _iterData(self):
        kit = self._qScore.score.drumKit
        for drum in kit:
            yield "%-2s = %s" % (drum.abbr, drum.name)

    def font(self):
        return self._props.noteFont

    def _dataLen(self):
        return self._qScore.kitSize

    def mouseDoubleClickEvent(self, event_):
        editDialog = QEditKitDialog(self.scene().score.drumKit,
                                    self.scene().parent())
        if editDialog.exec_():
            newKit, changes = editDialog.getNewKit()
            self.scene().changeKit(newKit, changes)
