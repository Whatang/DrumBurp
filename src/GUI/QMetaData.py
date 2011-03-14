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

    def _iterData(self):
        yield self._qScore.title + ", by " + self._qScore.artist + " (%d bpm)" % self._qScore.bpm
        yield "Tabbed by " + self._qScore.creator

    def _dataLen(self):
        return 2

    def font(self):
        return self._props.metadataFont

    def mouseDoubleClickEvent(self, event_):
        dialog = QMetadataDialog(self._qScore)
        if dialog.exec_():
            changed = any((getattr(self._qScore, attribute) != value
                          for (attribute, value) in dialog.getValues().iteritems()))
            if not changed:
                return
            self._qScore.beginMacro("Set Score Information")
            for attribute, value in dialog.getValues().iteritems():
                setattr(self._qScore, attribute, value)
            self._qScore.endMacro()
