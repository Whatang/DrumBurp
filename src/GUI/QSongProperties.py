'''
Created on 8 Jan 2011

@author: Mike Thomas
'''

from Data.TimeCounter import getCounters, counterMaker, TimeCounter

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

    def __repr__(self):
        "Return a string representation."
        return "<Null>"

    def __str__(self):
        "Convert to a string and return it."
        return "Null"

#pylint: disable-msg=R0902

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

    def __init__(self, settings = None, qScore = Null()):
        self._qScore = qScore
        self._xMargins = 20
        self._yMargins = 30
        self._xSpacing = self._START_NOTE_WIDTH
        self._ySpacing = self._START_NOTE_HEIGHT
        self._lineSpacing = self._START_LINE_SPACE
        self._noteFont = None
        self._head = None
        self._width = 80
        self.beatsPerMeasure = 4
        self._beatCounter = getCounters()[0][1]

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

    def proportionalSpacing(self):
        return ((float(self.xSpacing - self.MIN_NOTE_WIDTH)
                 / self.NOTE_WIDTH_RANGE * 100),
                (float(self.ySpacing - self.MIN_NOTE_HEIGHT)
                 / self.NOTE_HEIGHT_RANGE * 100),
                (float(self.lineSpacing - self.MIN_LINE_SPACE)
                 / self.LINE_SPACE_RANGE * 100))

    def maxColumns(self, widthInPixels):
        widthInPixels -= (2 * self.xMargins + self.LINELABELWIDTH)
        return int(widthInPixels / self.xSpacing)

    @staticmethod
    def allowedNoteHeads():
        return ("x", "X", "o", "O", "g", "f", "d", "+")

    def save(self, settings):
        pass

    def measureBeatsChanged(self, beats):
        self.beatsPerMeasure = beats

    def _getbeatCounter(self):
        return self._beatCounter
    def _setbeatCounter(self, value):
        if isinstance(value, int):
            value = counterMaker(value)
        assert(isinstance(value, TimeCounter))
        if self._beatCounter != value:
            self._beatCounter = value
    beatCounter = property(fget = _getbeatCounter, fset = _setbeatCounter)
