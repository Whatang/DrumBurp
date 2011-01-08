'''
Created on 4 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore
from QStaff import QStaff
from QNote import QNote
from Data.Score import ScoreFactory

scoreFactory = ScoreFactory()

class QScore(QtGui.QGraphicsScene):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        super(QScore, self).__init__(parent)
        self._qStaffs = []
        self._properties = parent.songProperties
        self._score = None
        score = scoreFactory(parent.filename)
        self._properties.setScore(self)
        self.setScore(score)

    def setScore(self, score):
        if score != self._score:
            score.gridFormatScore(self._properties.width)
            self._score = score
            self._score.setCallBack(self.noteChanged)
            self.build()

    def getScore(self):
        return self._score#

    def build(self):
        self.clearStaffs()
        for staff in self._score.iterStaffs():
            self.addStaff(staff)
        self.placeStaffs()
        self.populate()

    def __iter__(self):
        return iter(self._qStaffs)

    def clearStaffs(self):
        for qStaff in self._qStaffs:
            qStaff.clear()
            self.removeItem(qStaff)
        self._qStaffs = []

    def addStaff(self, staff):
        qStaff = QStaff(staff, parent = self)
        qStaff.setIndex(self.numStaffs())
        self._qStaffs.append(qStaff)

    def numStaffs(self):
        return len(self._qStaffs)

    def getProperties(self):
        return self._properties

    def placeStaffs(self):
        xMargins = self._properties.xMargins
        yMargins = self._properties.yMargins
        lineSpacing = self._properties.lineSpacing
        yOffset = yMargins
        maxWidth = 0
        for qStaff in self:
            qStaff.setPos(xMargins, yOffset)
            qStaff.placeMeasures()
            yOffset += qStaff.height() + lineSpacing
            maxWidth = max(maxWidth, qStaff.width())
        self.setSceneRect(0, 0,
                          maxWidth + 2 * xMargins,
                          yOffset - lineSpacing + yMargins)

    def xSpacingChanged(self):
        maxWidth = 0
        for qStaff in self:
            qStaff.xSpacingChanged()
            maxWidth = max(maxWidth, qStaff.width())
        self.setSceneRect(0, 0,
                          maxWidth + 2 * self._properties.xMargins,
                          self.height())

    def ySpacingChanged(self):
        xMargins = self._properties.xMargins
        yMargins = self._properties.yMargins
        lineSpacing = self._properties.lineSpacing
        yOffset = yMargins
        for qStaff in self:
            qStaff.setPos(xMargins, yOffset)
            qStaff.ySpacingChanged()
            yOffset += qStaff.height() + lineSpacing
        self.setSceneRect(0, 0,
                          self.width(),
                          yOffset - lineSpacing + yMargins)

    def lineSpacingChanged(self):
        xMargins = self._properties.xMargins
        yMargins = self._properties.yMargins
        lineSpacing = self._properties.lineSpacing
        yOffset = yMargins
        for qStaff in self:
            qStaff.setPos(xMargins, yOffset)
            yOffset += qStaff.height() + lineSpacing
        self.setSceneRect(0, 0,
                          self.width(),
                          yOffset - lineSpacing + yMargins)

    def populate(self):
        for notePosition, head in self._score.iterNotes():
            self.setNote(notePosition, head)

    def noteChanged(self, notePosition):
        head = self._score.getNote(notePosition)
        self.setNote(notePosition, head)

    def setNote(self, np, head):
        self._qStaffs[np.staffIndex].setNote(np, head)

    def mouseReleaseEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            event.ignore()
        else:
            item = self.itemAt(event.scenePos())
            if isinstance(item, QNote):
                item.toggleNote(self._properties.head)
                event.accept()
            else:
                event.ignore()

    def toggleNote(self, np, head):
        self._score.toggleNote(np, head)

class Null(object):
    def __init__(self, *args, **kwargs):
        "Ignore parameters."
        return None

    # object calling

    def __call__(self, *args, **kwargs):
        "Ignore method calls."
        return self

    # attribute handling

    def __getattr__(self, mname):
        "Ignore attribute requests."
        return self

    def __setattr__(self, name, value):
        "Ignore attribute setting."
        return self

    def __delattr__(self, name):
        "Ignore deleting attributes."
        return self

    # misc.

    def __repr__(self):
        "Return a string representation."
        return "<Null>"

    def __str__(self):
        "Convert to a string and return it."
        return "Null"


class QSongProperties(object):
    _START_NOTE_WIDTH = 12
    MIN_NOTE_WIDTH = 12
    MAX_NOTE_WIDTH = 20
    NOTE_WIDTH_RANGE = MAX_NOTE_WIDTH - MIN_NOTE_WIDTH

    _START_NOTE_HEIGHT = 12
    MIN_NOTE_HEIGHT = 11
    MAX_NOTE_HEIGHT = 20
    NOTE_HEIGHT_RANGE = MAX_NOTE_HEIGHT - MIN_NOTE_HEIGHT

    _START_LINE_SPACE = 20
    MIN_LINE_SPACE = 10
    MAX_LINE_SPACE = 80
    LINE_SPACE_RANGE = MAX_LINE_SPACE - MIN_LINE_SPACE

    LINELABELWIDTH = 30

    def __init__(self, qScore = Null()):
        self._qScore = qScore
        self._xMargins = 20
        self._yMargins = 30
        self._xSpacing = self._START_NOTE_WIDTH
        self._ySpacing = self._START_NOTE_HEIGHT
        self._lineSpacing = self._START_LINE_SPACE
        self._noteFont = None
        self._head = None
        self._width = 80

    def setScore(self, score):
        self._qScore = score

    def _getxSpacing(self):
        return self._xSpacing
    def _setxSpacing(self, value):
        if value < 0:
            value += 101
            value = int(0.5 + self.MIN_NOTE_WIDTH +
                        ((value / 100.0) * self.NOTE_WIDTH_RANGE))
        if self._xSpacing != value:
            self._xSpacing = value
            self._qScore.xSpacingChanged()
    xSpacing = property(fget = _getxSpacing, fset = _setxSpacing)

    def _getySpacing(self):
        return self._ySpacing
    def _setySpacing(self, value):
        if value < 0:
            value += 101
            value = int(0.5 + self.MIN_NOTE_HEIGHT +
                        ((value / 100.0) * self.NOTE_HEIGHT_RANGE))
        if self._ySpacing != value:
            self._ySpacing = value
            self._qScore.ySpacingChanged()
    ySpacing = property(fget = _getySpacing, fset = _setySpacing)

    def _getlineSpacing(self):
        return self._lineSpacing
    def _setlineSpacing(self, value):
        if value < 0:
            value += 101
            value = int(0.5 + self.MIN_LINE_SPACE +
                        ((value / 100.0) * self.LINE_SPACE_RANGE))
        if self._lineSpacing != value:
            self._lineSpacing = value
            self._qScore.lineSpacingChanged()
    lineSpacing = property(fget = _getlineSpacing, fset = _setlineSpacing)

    def _getxMargins(self):
        return self._xMargins
    def _setxMargins(self, value):
        if self._xMargins != value:
            self._xMargins = value
    xMargins = property(fget = _getxMargins, fset = _setxMargins)

    def _getyMargins(self):
        return self._yMargins
    def _setyMargins(self, value):
        if self._yMargins != value:
            self._yMargins = value
    yMargins = property(fget = _getyMargins, fset = _setyMargins)

    def _getnoteFont(self):
        return self._noteFont
    def _setnoteFont(self, value):
        if self._noteFont != value:
            self._noteFont = value
            self._qScore.update()
    noteFont = property(fget = _getnoteFont, fset = _setnoteFont)

    def _gethead(self):
        return self._head
    def _sethead(self, value):
        if self._head != value:
            self._head = value
    head = property(fget = _gethead, fset = _sethead)

    def _getwidth(self):
        return self._width
    def _setwidth(self, value):
        if self._width != value:
            self._width = value
    width = property(fget = _getwidth, fset = _setwidth)

    def proportionalSpacing(self):
        return (float(self.xSpacing - self.MIN_NOTE_WIDTH) / self.NOTE_WIDTH_RANGE * 100,
                float(self.ySpacing - self.MIN_NOTE_HEIGHT) / self.NOTE_HEIGHT_RANGE * 100,
                (float(self.lineSpacing - self.MIN_LINE_SPACE)
                 / self.LINE_SPACE_RANGE * 100))

