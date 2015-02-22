# Copyright 2011-12 Michael Thomas
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
Created on 12 Mar 2011

@author: Mike Thomas

'''
from QMetaDataDialog import QMetadataDialog
from QGraphicsListData import QGraphicsListData

class QMetaData(QGraphicsListData):
    '''
    classdocs
    '''
    _editName = "score information."

    def _iterData(self):
        line = unicode(self._qScore.title)
        if self._qScore.artistVisible and self._qScore.artist:
            if line:
                line += ", by " + self._qScore.artist
            else:
                line = self._qScore.artist
        if self._qScore.bpmVisible and self._qScore.bpm:
            if line:
                line += " (%d bpm)" % self._qScore.bpm
            else:
                line += "%d bpm" % self._qScore.bpm
        yield line
        if self._qScore.creatorVisible and self._qScore.creator:
            yield "Tabbed by " + self._qScore.creator

    def _dataLen(self):
        if self._qScore.creatorVisible:
            return 2
        else:
            return 1

    def font(self):
        return self._props.metadataFont

    def mouseDoubleClickEvent(self, event_):
        dialog = QMetadataDialog(self._qScore, self.scene().parent())
        if dialog.exec_():
            changed = any((getattr(self._qScore, attribute) != value
                          for (attribute, value) in
                          dialog.getValues().iteritems()))
            if not changed:
                return
            self._qScore.beginMacro("Set Score Information", False)
            for attribute, value in dialog.getValues().iteritems():
                setattr(self._qScore, attribute, value)
            self._qScore.endMacro()
