'''
Created on 5 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore

class QMeasureLine(QtGui.QGraphicsItem):
    '''
    classdocs
    '''


    def __init__(self, qScore, lastMeasure, nextMeasure, parent = None):
        '''
        Constructor
        '''
        super(QMeasureLine, self).__init__(parent)
        self._qScore = qScore
        self._score = self._qScore.getScore()
        self._props = self._qScore.getProperties()
        self._height = None
        self._rect = QtCore.QRectF(0, 0, 0, 0)
        self.setDimensions()
        self._index = None

    def setIndex(self, index):
        self._index = index

    def boundingRect(self):
        return self._rect

    def paint(self, painter, dummyOption, dummyWidget = None):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.scene().palette().base())
        painter.drawRect(self._rect)
        painter.setPen(QtCore.Qt.SolidLine)
        x = self._props.xSpacing / 2
        painter.drawLine(x, 0, x, self.height())

    def _setHeight(self):
        self._height = self._props.ySpacing * len(self._score.drumKit)

    def setDimensions(self):
        self.prepareGeometryChange()
        self._setHeight()
        self._rect.setBottomRight(QtCore.QPointF(self._props.xSpacing,
                                                 self._height))

    def xSpacingChanged(self):
        self.prepareGeometryChange()
        self._rect.setRight(self._props.xSpacing)

    def ySpacingChanged(self):
        self._setHeight()
        self.prepareGeometryChange()
        self._rect.setBottom(self._height)

    def height(self):
        return self._height

    def width(self):
        return self._props.xSpacing
