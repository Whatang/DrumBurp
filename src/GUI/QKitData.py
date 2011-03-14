'''
Created on 13 Mar 2011

@author: Mike Thomas
'''

from QGraphicsListData import QGraphicsListData

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
