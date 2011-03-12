'''
Created on 4 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore
from QStaff import QStaff
from QSection import QSection
from Data.Score import ScoreFactory
from DBCommands import MetaDataCommand, ScoreWidthCommand, PasteMeasure
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
            command = MetaDataCommand(self, varname, setName, value)
            self.addCommand(command)
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
        self._dirty = None
        self._ignoreNext = False
        self.measureClipboard = None
        self._undoStack = QtGui.QUndoStack(self)
        self._undoStack.canUndoChanged.connect(self.canUndoChanged)
        self._undoStack.undoTextChanged.connect(self.undoTextChanged)
        self._undoStack.canRedoChanged.connect(self.canRedoChanged)
        self._undoStack.redoTextChanged.connect(self.redoTextChanged)
        if parent.filename is not None:
            if not self.loadScore(parent.filename):
                parent.filename = None
                self.newScore()
        else:
            self.newScore()
        self._properties.connectScore(self)

    canUndoChanged = QtCore.pyqtSignal(bool)
    canRedoChanged = QtCore.pyqtSignal(bool)
    undoTextChanged = QtCore.pyqtSignal(str)
    redoTextChanged = QtCore.pyqtSignal(str)

    def addCommand(self, command):
        self._undoStack.push(command)
        self.dirty = not self._undoStack.isClean()

    def addRepeatedCommand(self, name, command, arguments):
        self._undoStack.beginMacro(name)
        for args in arguments:
            self.addCommand(command(self, *args))
        self._undoStack.endMacro()

    def undo(self):
        self._undoStack.undo()
        self.dirty = not self._undoStack.isClean()

    def redo(self):
        self._undoStack.redo()
        self.dirty = not self._undoStack.isClean()

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
            command = ScoreWidthCommand(self, value)
            self.addCommand(command)
    scoreWidth = property(fget = _getscoreWidth,
                          fset = _setscoreWidth)

    artist = _metaDataProperty("artist")
    creator = _metaDataProperty("creator")
    title = _metaDataProperty("title")
    bpm = _metaDataProperty("bpm", "setBPM")

    @_readOnly
    def displayProperties(self):
        return self._properties

    def _getdirty(self):
        return self._dirty
    def _setdirty(self, value):
        if self._dirty != value:
            self._dirty = value
            self.dirtySignal.emit(self._dirty)
    dirty = property(fget = _getdirty, fset = _setdirty)
    dirtySignal = QtCore.pyqtSignal(bool)

    @_readOnly
    def kitSize(self):
        return len(self._score.drumKit)

    @_readOnly
    def lineOffsets(self):
        yOffsets = [(drumIndex + 1) * self._properties.ySpacing
                    for drumIndex in range(0, self.kitSize)]
        yOffsets.reverse()
        return yOffsets

    def _setScore(self, score):
        if score != self._score:
            score.gridFormatScore(None)
            self._score = score
            if score is not None:
                self.startUp()
            self._score.setCallBack(self.dataChanged)
            self._build()
            self.dirty = False
            self._undoStack.clear()
            self._undoStack.setClean()

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
        qStaff = QStaff(staff, len(self._qStaffs), self)
        self._qStaffs.append(qStaff)

    def _addSection(self, title):
        qSection = QSection(title, qScore = self)
        qSection.setIndex(len(self._qSections))
        self._qSections.append(qSection)

    def setSectionTitle(self, index, title):
        qSection = self._qSections[index]
        qSection.setTitle(title)

    def _placeStaffs(self, staffCall = QStaff.placeMeasures):
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
            newSection = qStaff.isSectionEnd()
            qStaff.setPos(xMargins, yOffset)
            if staffCall is not None:
                staffCall(qStaff)
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
#                    yOffset += lineSpacing
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
#                    yOffset += lineSpacing
            newSection = qStaff.isSectionEnd()
            qStaff.setPos(xMargins, yOffset)
            yOffset += qStaff.height() + lineSpacing
        self.setSceneRect(0, 0,
                          self.width(),
                          yOffset - lineSpacing + yMargins)

    def sectionFontChanged(self):
        for qsection in self._qSections:
            qsection.setFont(self._properties.sectionFont)

    def sectionFontSizeChanged(self):
        self.sectionFontChanged()
        self.lineSpacingChanged()


    def dataChanged(self, notePosition):
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

    def copyMeasure(self, np):
        self.measureClipboard = self._score.copyMeasure(np)

    @delayCall
    def pasteMeasure(self, np):
        command = PasteMeasure(self, np, self.measureClipboard)
        self.addCommand(command)

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
        self._undoStack.setClean()
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
        rect = qprinter.pageRect()
        topLeft = QtCore.QPointF(self._properties.xMargins, self._properties.yMargins)
        bottomRight = QtCore.QPointF(self.sceneRect().right() - self._properties.xMargins,
                                     self._properties.yMargins)
        for staff in self._qStaffs:
            newY = staff.y() + staff.height()
            if newY - topLeft.y() > rect.height():
                sceneRect = QtCore.QRectF(topLeft, bottomRight)
                if sceneRect.width() > rect.width():
                    sceneRect.setWidth(rect.width())
                pageRect = QtCore.QRectF(0, 0, sceneRect.width(), sceneRect.height())
                self.render(painter, pageRect, sceneRect)
                qprinter.newPage()
                topLeft.setY(bottomRight.y() + self._properties.lineSpacing)
            bottomRight.setY(newY)
        sceneRect = QtCore.QRectF(topLeft, bottomRight)
        if sceneRect.width() > rect.width():
            sceneRect.setWidth(rect.width())
        pageRect = QtCore.QRectF(0, 0, sceneRect.width(), sceneRect.height())
        self.render(painter, pageRect, sceneRect)
        painter.end()
