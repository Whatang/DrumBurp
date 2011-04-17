'''
Created on 13 Mar 2011

@author: Mike Thomas

'''


from PyQt4.QtGui import QGraphicsItem, QFontMetrics
from PyQt4.QtCore import QPoint, QRectF, QPointF, Qt

class QGraphicsListData(QGraphicsItem):
    '''
    classdocs
    '''


    def __init__(self, qScore, parent = None):
        '''
        Constructor
        '''
        super(QGraphicsListData, self).__init__(parent = parent, scene = qScore)
        self._qScore = qScore
        self._props = qScore.displayProperties
        self._rect = QRectF(0, 0, 0, 0)
        self._setRect()
        self.setCursor(Qt.PointingHandCursor)

    def _iterData(self):
        raise NotImplementedError()

    def _dataLen(self):
        raise NotImplementedError()

    def font(self):
        raise NotImplementedError()

    def _setRect(self, font = None):
        if font is None:
            font = self.font()
        if font is None:
            return
        fm = QFontMetrics(font)
        lineHeight = fm.height()
        height = lineHeight * self._dataLen() * 1.1
        width = max(fm.width(data) for data in self._iterData()) + 10
        if height != self._rect.height() or width != self._rect.width():
            self.prepareGeometryChange()
            self._rect.setBottomRight(QPointF(width, height))

    def boundingRect(self):
        return self._rect

    def paint(self, painter, dummyOption, dummyWidget = None):
        painter.save()
        try:
            font = self.font()
            if font is None:
                font = painter.font()
            self._setRect(font)
            painter.setFont(font)
            fm = QFontMetrics(font)
            lineHeight = fm.height()
            for index, data in enumerate(self._iterData()):
                painter.drawText(QPoint(5, (index + 1) * lineHeight), data)
        finally:
            painter.restore()

    def fontChanged(self):
        self._setRect()
        self.update()
