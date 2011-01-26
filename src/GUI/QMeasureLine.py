'''
Created on 5 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore
from Data.NotePosition import NotePosition
from QMenuIgnoreCancelClick import QMenuIgnoreCancelClick

class QMeasureLine(QtGui.QGraphicsItem):
    '''
    classdocs
    '''


    def __init__(self, qScore, lastMeasure, nextMeasure, parent = None):
        '''
        Constructor
        '''
        super(QMeasureLine, self).__init__(parent)
        self._qStaff = parent
        self._props = qScore.displayProperties
        self._height = None
        self._rect = QtCore.QRectF(0, 0, 0, 0)
        self._lastMeasure = lastMeasure
        self._nextMeasure = nextMeasure
        self._painter = None
        self._setPainter()
        self.setDimensions()
        self._index = None

    def setIndex(self, index):
        self._index = index

    def boundingRect(self):
        return self._rect

    def _setPainter(self):
        self._painter = PAINTER_FACTORY(self._lastMeasure, self._nextMeasure)

    def paint(self, painter, dummyOption, dummyWidget = None):
        self._painter(self, painter, dummyOption, dummyWidget = None)

    def _setHeight(self):
        self._height = self._props.ySpacing * self.scene().kitSize

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

    def _getEndNotePosition(self):
        assert(self._index > 0)
        np = NotePosition(measureIndex = self._index - 1)
        return self._qStaff.augmentNotePosition(np)

    def _getStartNotePosition(self):
        np = NotePosition(measureIndex = self._index)
        return self._qStaff.augmentNotePosition(np)

    def _setSectionEnd(self, onOff):
        self.scene().score.setSectionEnd(self._getEndNotePosition(), onOff)
        self.scene().dirty = True
        self.scene().reBuild()
        self._setPainter()

    def _setRepeatEnd(self, onOff):
        self.scene().score.setRepeatEnd(self._getEndNotePosition(), onOff)
        self.scene().dirty = True
        self._setPainter()
        self.update()

    def _setRepeatStart(self, onOff):
        self.scene().score.setRepeatStart(self._getStartNotePosition(), onOff)
        self.scene().dirty = True
        self._setPainter()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            event.accept()
            menu = QMenuIgnoreCancelClick(self.scene())
            # Repeat Start
            if self._nextMeasure is not None:
                repeatStartAction = QtGui.QAction("Repeat Start", menu)
                repeatStartAction.setCheckable(True)
                repeatStartAction.setChecked(self._nextMeasure.isRepeatStart())
                menu.connect(repeatStartAction, QtCore.SIGNAL("toggled(bool)"),
                             self._setRepeatStart)
                menu.addAction(repeatStartAction)
            # Repeat End
            if self._lastMeasure is not None:
                repeatEndAction = QtGui.QAction("Repeat End", menu)
                repeatEndAction.setCheckable(True)
                repeatEndAction.setChecked(self._lastMeasure.isRepeatEnd())
                menu.connect(repeatEndAction, QtCore.SIGNAL("toggled(bool)"),
                             self._setRepeatEnd)
                menu.addAction(repeatEndAction)
            # Section Ending
            if self._lastMeasure is not None:
                sectionEndAction = QtGui.QAction("Section End", menu)
                sectionEndAction.setCheckable(True)
                sectionEndAction.setChecked(self._lastMeasure.isSectionEnd())
                menu.connect(sectionEndAction, QtCore.SIGNAL("toggled(bool)"),
                            self._setSectionEnd)
                menu.addAction(sectionEndAction)
            menu.exec_(event.screenPos())
        else:
            pass

class BarLinePainter(object):
    THICK_LINE_WIDTH = 3
    THICK_LINE_OFFSET = 1
    EXTRA_LINE_OFFSET = 3
    DOT_OFFSET = 5
    DOT_RADIUS = 2

    def __call__(self, qMeasureLine, painter, dummyOption, dummyWidget = None):
        raise NotImplementedError()

    @classmethod
    def _clearBase(cls, painter, palette, boundingRect):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(palette.base())
        painter.drawRect(boundingRect)

    @classmethod
    def _drawThickLine(cls, painter, xCenter, height, palette):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(palette.text())
        painter.drawRect(xCenter - cls.THICK_LINE_OFFSET, 0,
                         cls.THICK_LINE_WIDTH, height + 1)

    @classmethod
    def _drawDot(cls, painter, x, y, palette):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(palette.text())
        painter.drawEllipse(QtCore.QPointF(x, y),
                            cls.DOT_RADIUS, cls.DOT_RADIUS)

    @classmethod
    def _drawExtraLineBefore(cls, painter, xCenter, height, palette):
        painter.setPen(QtCore.Qt.SolidLine)
        painter.setBrush(palette.text())
        painter.drawLine(xCenter - cls.EXTRA_LINE_OFFSET, 0,
                         xCenter - cls.EXTRA_LINE_OFFSET, height)

    @classmethod
    def _drawExtraLineAfter(cls, painter, xCenter, height, palette):
        painter.setPen(QtCore.Qt.SolidLine)
        painter.setBrush(palette.text())
        painter.drawLine(xCenter + cls.EXTRA_LINE_OFFSET, 0,
                         xCenter + cls.EXTRA_LINE_OFFSET, height)

    @classmethod
    def _drawRepeatBefore(cls, painter, xCenter, height, palette):
        cls._drawExtraLineBefore(painter, xCenter, height, palette)
        y = height / 3
        cls._drawDot(painter, xCenter - cls.DOT_OFFSET, y, palette)
        cls._drawDot(painter, xCenter - cls.DOT_OFFSET, 2 * y, palette)

    @classmethod
    def _drawRepeatAfter(cls, painter, xCenter, height, palette):
        cls._drawExtraLineAfter(painter, xCenter, height, palette)
        y = height / 3
        cls._drawDot(painter, xCenter + cls.DOT_OFFSET, y, palette)
        cls._drawDot(painter, xCenter + cls.DOT_OFFSET, 2 * y, palette)

class NormalBarLinePainter(BarLinePainter):
    def __call__(self, qMeasureLine, painter, dummyOption, dummyWidget = None):
        palette = qMeasureLine.scene().palette()
        self._clearBase(painter, palette, qMeasureLine.boundingRect())
        painter.setPen(QtCore.Qt.SolidLine)
        x = qMeasureLine.width() / 2
        painter.drawLine(x, 0, x, qMeasureLine.height())

class RepeatStartLinePainter(BarLinePainter):
    def __call__(self, qMeasureLine, painter, dummyOption, dummyWidget = None):
        palette = qMeasureLine.scene().palette()
        self._clearBase(painter, palette, qMeasureLine.boundingRect())
        x = qMeasureLine.width() / 2
        self._drawThickLine(painter, x, qMeasureLine.height(), palette)
        self._drawRepeatAfter(painter, x, qMeasureLine.height(), palette)


class RepeatEndLinePainter(BarLinePainter):
    def __call__(self, qMeasureLine, painter, dummyOption, dummyWidget = None):
        palette = qMeasureLine.scene().palette()
        self._clearBase(painter, palette, qMeasureLine.boundingRect())
        x = qMeasureLine.width() / 2
        self._drawThickLine(painter, x, qMeasureLine.height(), palette)
        self._drawRepeatBefore(painter, x, qMeasureLine.height(), palette)

class RepeatStartEndLinePainter(BarLinePainter):
    def __call__(self, qMeasureLine, painter, dummyOption, dummyWidget = None):
        palette = qMeasureLine.scene().palette()
        self._clearBase(painter, palette, qMeasureLine.boundingRect())
        x = qMeasureLine.width() / 2
        self._drawThickLine(painter, x, qMeasureLine.height(), palette)
        self._drawRepeatBefore(painter, x, qMeasureLine.height(), palette)
        self._drawRepeatAfter(painter, x, qMeasureLine.height(), palette)

class SectionEndLinePainter(BarLinePainter):
    def __call__(self, qMeasureLine, painter, dummyOption, dummyWidget = None):
        palette = qMeasureLine.scene().palette()
        self._clearBase(painter, palette, qMeasureLine.boundingRect())
        x = qMeasureLine.width() / 2
        self._drawThickLine(painter, x, qMeasureLine.height(), palette)
        self._drawExtraLineBefore(painter, x, qMeasureLine.height(), palette)

class BarLinePainterFactory(object):
    def __init__(self):
        self._painterCache = {}
        self._normalLinePainter = NormalBarLinePainter()
        self._painterCache[(True, False, False)] = RepeatStartLinePainter()
        self._painterCache[(False, True, False)] = RepeatEndLinePainter()
        self._painterCache[(True, True, False)] = RepeatStartEndLinePainter()
        self._painterCache[(False, False, True)] = SectionEndLinePainter()
        self._painterCache[(False, True, True)] = RepeatEndLinePainter()

    @staticmethod
    def _pairKey(lastMeasure, nextMeasure):
        key = (nextMeasure is not None and nextMeasure.isRepeatStart(),
               lastMeasure is not None and lastMeasure.isRepeatEnd(),
               lastMeasure is not None and lastMeasure.isSectionEnd())
        return key

    def __call__(self, lastMeasure, nextMeasure):
        pairKey = self._pairKey(lastMeasure, nextMeasure)
        return self._painterCache.get(pairKey, self._normalLinePainter)

PAINTER_FACTORY = BarLinePainterFactory()

