'''
Created on 5 Dec 2010

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore
from QSystem import QSystem
from DBSignals import LINESPACING_SIGNAL, XSPACING_SIGNAL, YSPACING_SIGNAL
from QNote import QNote

START_NOTE_WIDTH = 12
MIN_NOTE_WIDTH = 12
MAX_NOTE_WIDTH = 20
NOTE_WIDTH_RANGE = MAX_NOTE_WIDTH - MIN_NOTE_WIDTH

START_NOTE_HEIGHT = 12
MIN_NOTE_HEIGHT = 11
MAX_NOTE_HEIGHT = 20
NOTE_HEIGHT_RANGE = MAX_NOTE_HEIGHT - MIN_NOTE_HEIGHT

START_LINE_SPACE = 20
MIN_LINE_SPACE = 10
MAX_LINE_SPACE = 80
LINE_SPACE_RANGE = MAX_LINE_SPACE - MIN_LINE_SPACE



class ScoreScene(QtGui.QGraphicsScene):
    '''
    classdocs
    '''

    def __init__(self, score, parent = None):
        '''
        Constructor
        '''
        super(ScoreScene, self).__init__(parent)
        self._score = score
        self._systems = []
        self._xSpace = 0
        self._ySpace = 0
        self._sceneWidth = 0
        self._sceneHeight = 0
        self._interLineSpace = 20
        self._head = None
        self.xMargins = 10
        self.yMargins = 10
        self.noteFont = None

    def mouseReleaseEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            event.ignore()
        else:
            item = self.itemAt(event.scenePos())
            if isinstance(item, QNote):
                item.toggleNote(self.head)
                event.accept()
            else:
                event.ignore()

    def _gethead(self):
        return self._head
    def _sethead(self, value):
        if self._head != value:
            self._head = value
    head = property(fget = _gethead, fset = _sethead)

    def _getScore(self):
        return self._score
    def _setScore(self, score):
        self._score = score
    score = property(_getScore, _setScore)

    def _getxSpace(self):
        return self._xSpace
    def _setxSpace(self, value):
        if value != self._xSpace:
            self._xSpace = value
            self.emit(QtCore.SIGNAL(XSPACING_SIGNAL))
            if len(self._systems):
                self.sceneWidth = (max(s.width() for s in self._systems)
                                    + 2 * self.xMargins)
            else:
                self.sceneHeight = 200
    xSpace = property(fset = _setxSpace, fget = _getxSpace)

    def _getySpace(self):
        return self._ySpace
    def _setySpace(self, value):
        if self._ySpace != value:
            self._ySpace = value
            self.emit(QtCore.SIGNAL(YSPACING_SIGNAL))
            if len(self._systems):
                self.sceneHeight = (sum(s.height() + self.interLineSpace
                                        for s in self._systems)
                                    + 2 * self.yMargins)
            else:
                self.sceneHeight = 200
    ySpace = property(fget = _getySpace, fset = _setySpace)

    def _getinterLineSpace(self):
        return self._interLineSpace
    def _setinterLineSpace(self, value):
        if self._interLineSpace != value:
            self._interLineSpace = value
            self.emit(QtCore.SIGNAL(LINESPACING_SIGNAL))
    interLineSpace = property(fget = _getinterLineSpace,
                              fset = _setinterLineSpace)

    def _getsceneWidth(self):
        return self._sceneWidth
    def _setsceneWidth(self, value):
        if self._sceneWidth != value:
            self._sceneWidth = value
            self.setSceneRect(0, 0,
                          value,
                          self.sceneHeight)
    sceneWidth = property(fget = _getsceneWidth, fset = _setsceneWidth)

    def _getsceneHeight(self):
        return self._sceneHeight
    def _setsceneHeight(self, value):
        if self._sceneHeight != value:
            self._sceneHeight = value
            self.setSceneRect(0, 0,
                              self.sceneWidth,
                              value)
    sceneHeight = property(fget = _getsceneHeight, fset = _setsceneHeight)

    @property
    def numLines(self):
        return self.score.numLines

    def setSpacing(self, width = None,
                   height = None,
                   lineSpace = None):
        if width is not None:
            if width < 0:
                width += 101
                width = int(0.5 + MIN_NOTE_WIDTH +
                            ((width / 100.0) * NOTE_WIDTH_RANGE))
            self.xSpace = width
        if height is not None:
            if height < 0:
                height += 101
                height = int(0.5 + MIN_NOTE_HEIGHT +
                             ((height / 100.0) * NOTE_HEIGHT_RANGE))
            self.ySpace = height
        if lineSpace is not None:
            if lineSpace < 0:
                lineSpace += 101
                lineSpace = int(0.5 + MIN_LINE_SPACE +
                             ((lineSpace / 100.0) * LINE_SPACE_RANGE))
            self.interLineSpace = lineSpace

    def proportionalSpacing(self):
        return (float(self.xSpace - MIN_NOTE_WIDTH) / NOTE_WIDTH_RANGE * 100,
                float(self.ySpace - MIN_NOTE_HEIGHT) / NOTE_HEIGHT_RANGE * 100,
                (float(self.interLineSpace - MIN_LINE_SPACE)
                 / LINE_SPACE_RANGE * 100))

    def build(self):
        self._systems = []
        for index, system in enumerate(self.score.iterSystems()):
            if index >= len(self._systems):
                newSystem = QSystem(system,
                                    self.score.width,
                                    self.score.numLines,
                                    self,
                                    index)
                self._systems.append(newSystem)
            thisSystem = self._systems[-1]
            thisSystem.setSystem(system)
        self.xSpace = START_NOTE_WIDTH
        self.ySpace = START_NOTE_HEIGHT
