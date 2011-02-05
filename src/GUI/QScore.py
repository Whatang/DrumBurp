'''
Created on 4 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore
from QStaff import QStaff
from QSection import QSection
from Data.Score import ScoreFactory
import functools
_SCORE_FACTORY = ScoreFactory()

def _readOnly(method):
    return property(fget = method)

def delayCall(method):
    @functools.wraps(method)
    def delayer(*args, **kwargs):
        QtCore.QTimer.singleShot(0, lambda: method(*args, **kwargs))
    return delayer

def _metaDataProperty(varname, setName = None):
    if setName is None:
        setName = "set" + varname.capitalize()
    def _getData(self):
        return getattr(self.score.scoreData, varname)
    def _setData(self, value):
        if getattr(self, varname) != value:
            setattr(self.score.scoreData, varname, value)
            for view in self.views():
                getattr(view, setName)(value)
            self.dirty = True
    return property(fget = _getData, fset = _setData)


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
        self._qSections = []
        self._properties = parent.songProperties
        self._score = None
        self._highlightedNote = None
        self._dirty = None
        self._ignoreNext = False
        self.measureClipboard = None
        if parent.filename is not None:
            if not self.loadScore(parent.filename):
                parent.filename = None
                self.newScore()
        else:
            self.newScore()
        self._properties.connectScore(self)

    def startUp(self):
        for view in self.views():
            view.setWidth(self.scoreWidth)
            view.setArtist(self.artist)
            view.setTitle(self.title)
            view.setCreator(self.creator)
            view.setBPM(self.bpm)

    def _getscoreWidth(self):
        if self._score is not None:
            return self._score.scoreData.width
        else:
            return None
    def _setscoreWidth(self, value):
        if self._score is None:
            return
        if self.scoreWidth != value:
            self._score.scoreData.width = value
            for view in self.views():
                view.setWidth(value)
            if self._score is not None:
                self.checkFormatting()
            self.dirty = True
    scoreWidth = property(fget = _getscoreWidth,
                          fset = _setscoreWidth)

    artist = _metaDataProperty("artist")
    creator = _metaDataProperty("creator")
    title = _metaDataProperty("title")
    bpm = _metaDataProperty("bpm", "setBPM")

    @_readOnly
    def displayProperties(self):
        return self._properties

    def _gethighlightedNote(self):
        return self._highlightedNote
    def _sethighlightedNote(self, np):
        if self._highlightedNote != np:
            self._clearHighlight()
            self._makeHighlight(np)
            self._highlightedNote = np
    highlightedNote = property(fget = _gethighlightedNote,
                               fset = _sethighlightedNote)

    def _clearHighlight(self):
        if self.highlightedNote != None:
            qStaff = self._qStaffs[self.highlightedNote.staffIndex]
            qStaff.setHighlight(self.highlightedNote, False)

    def _makeHighlight(self, np):
        if np != None:
            qStaff = self._qStaffs[np.staffIndex]
            qStaff.setHighlight(np, True)

    def _getdirty(self):
        return self._dirty
    def _setdirty(self, value):
        if self._dirty != value:
            self._dirty = value
            self.emit(QtCore.SIGNAL("dirty"), self._dirty)
    dirty = property(fget = _getdirty, fset = _setdirty)

    @_readOnly
    def kitSize(self):
        return len(self._score.drumKit)

    @_readOnly
    def lineOffsets(self):
        yOffsets = [drumIndex * self._properties.ySpacing
                    for drumIndex in range(0, self.kitSize)]
        yOffsets.reverse()
        return yOffsets

    def _setScore(self, score):
        if score != self._score:
            score.gridFormatScore(None)
            self._score = score
            if score is not None:
                self.startUp()
            self._score.setCallBack(self._dataChanged)
            self._build()
            self.dirty = False

    @_readOnly
    def score(self):
        return self._score

    def _build(self):
        self._clearStaffs()
        for staff in self._score.iterStaffs():
            self._addStaff(staff)
        for title in self._score.iterSections():
            self._addSection(title)
        self._placeStaffs()
        self._populate()


    @delayCall
    def reBuild(self):
        self._score.gridFormatScore(None)
        oldSceneRect = self.sceneRect()
        self._build()
        self.update(oldSceneRect)

    def checkFormatting(self):
        if self._score.gridFormatScore(None):
            self.reBuild()

    def __iter__(self):
        return iter(self._qStaffs)

    def _clearStaffs(self):
        for qStaff in self._qStaffs:
            self.removeItem(qStaff)
        self._qStaffs = []
        for qSection in self._qSections:
            self.removeItem(qSection)
        self._qSections = []

    def _addStaff(self, staff):
        qStaff = QStaff(staff, self)
        qStaff.setIndex(len(self._qStaffs))
        self._qStaffs.append(qStaff)

    def _addSection(self, title):
        qSection = QSection(title, qScore = self)
        qSection.setIndex(len(self._qSections))
        self._qSections.append(qSection)

    def _placeStaffs(self):
        xMargins = self._properties.xMargins
        yMargins = self._properties.yMargins
        lineSpacing = self._properties.lineSpacing
        yOffset = yMargins
        newSection = True
        sectionIndex = 0
        maxWidth = 0
        for qStaff in self:
            if newSection:
                newSection = False
                if sectionIndex < len(self._qSections):
                    qSection = self._qSections[sectionIndex]
                    sectionIndex += 1
                    qSection.setPos(xMargins, yOffset)
                    yOffset += qSection.boundingRect().height()
                    yOffset += lineSpacing
            newSection = qStaff.isSectionEnd()
            qStaff.setPos(xMargins, yOffset)
            qStaff.placeMeasures()
            yOffset += qStaff.height() + lineSpacing
            maxWidth = max(maxWidth, qStaff.width())
            newSection = qStaff.isSectionEnd()
        self.setSceneRect(0, 0,
                          maxWidth + 2 * xMargins,
                          yOffset - lineSpacing + yMargins)

    def xSpacingChanged(self):
        for qStaff in self:
            qStaff.xSpacingChanged()
        maxWidth = max(qStaff.width() for qStaff in self)
        self.setSceneRect(0, 0,
                          maxWidth + 2 * self._properties.xMargins,
                          self.height())

    def ySpacingChanged(self):
        xMargins = self._properties.xMargins
        yMargins = self._properties.yMargins
        lineSpacing = self._properties.lineSpacing
        yOffset = yMargins
        newSection = True
        sectionIndex = 0
        for qStaff in self:
            if newSection:
                newSection = False
                if sectionIndex < len(self._qSections):
                    qSection = self._qSections[sectionIndex]
                    sectionIndex += 1
                    qSection.setPos(xMargins, yOffset)
                    yOffset += qSection.boundingRect().height()
                    yOffset += lineSpacing
            newSection = qStaff.isSectionEnd()
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
        sectionIndex = 0
        newSection = True
        for qStaff in self:
            if newSection:
                newSection = False
                if sectionIndex < len(self._qSections):
                    qSection = self._qSections[sectionIndex]
                    sectionIndex += 1
                    qSection.setPos(xMargins, yOffset)
                    yOffset += qSection.boundingRect().height()
                    yOffset += lineSpacing
            newSection = qStaff.isSectionEnd()
            qStaff.setPos(xMargins, yOffset)
            yOffset += qStaff.height() + lineSpacing
        self.setSceneRect(0, 0,
                          self.width(),
                          yOffset - lineSpacing + yMargins)

    def _populate(self):
        for notePosition, head_ in self._score.iterNotes():
            self._dataChanged(notePosition)

    def _dataChanged(self, notePosition):
        self.dirty = True
        staff = self._qStaffs[notePosition.staffIndex]
        staff.dataChanged(notePosition)

    def ignoreNextClick(self):
        self._ignoreNext = True

    def mousePressEvent(self, event):
        event.ignore()
        if self._ignoreNext:
            self._ignoreNext = False
        else:
            super(QScore, self).mousePressEvent(event)

    def highlightNote(self, np, onOff = True):
        if onOff:
            self.highlightedNote = np
        else:
            self.highlightedNote = None

    def copyMeasure(self, np):
        self.measureClipboard = self._score.copyMeasure(np)

    def pasteMeasure(self, np):
        self._score.pasteMeasure(np, self.measureClipboard)
        self.checkFormatting()
        self.dirty = True

    def changeRepeatCount(self, np):
        qStaff = self._qStaffs[np.staffIndex]
        qStaff.changeRepeatCount(np)

    def loadScore(self, filename):
        try:
            newScore = _SCORE_FACTORY(filename = filename)
        except IOError, exc:
            msg = "Error loading DrumBurp file %s" % filename
            QtGui.QMessageBox.warning(self.parent(),
                                      "Score load error",
                                      msg + "\n" + str(exc))
            return False
        self._setScore(newScore)
        return True

    def saveScore(self, filename):
        try:
            _SCORE_FACTORY.saveScore(self._score, filename)
        except StandardError, exc:
            msg = "Error loading DrumBurp file: %s" % str(exc)
            QtGui.QMessageBox.warning(self.parent(),
                                      "Score save error",
                                      msg)
            return False
        self.dirty = False
        return True

    def newScore(self, numMeasures = 16,
                 measureWidth = None,
                 counter = None):
        if counter is None:
            counter = self._properties.beatCounter
        if measureWidth is None:
            measureWidth = self._properties.beatsPerMeasure * counter.beatLength
        newScore = _SCORE_FACTORY(numMeasures = numMeasures,
                                  measureWidth = measureWidth,
                                  counter = counter)
        self._setScore(newScore)

    def printScore(self, qprinter):
        painter = QtGui.QPainter(qprinter)
        self.render(painter)
        painter.end()
