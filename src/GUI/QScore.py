'''
Created on 4 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore
from QStaff import QStaff
from QInsertMeasuresDialog import QInsertMeasuresDialog
from QEditMeasureDialog import QEditMeasureDialog
from QRepeatDialog import QRepeatDialog
from Data.Score import ScoreFactory
from Data.TimeCounter import counterMaker
import functools
_SCORE_FACTORY = ScoreFactory()

#pylint: disable-msg=R0904

def delayCall(method):
    @functools.wraps(method)
    def delayer(*args, **kwargs):
        QtCore.QTimer.singleShot(0, lambda: method(*args, **kwargs))
    return delayer

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
        self._properties.setScore(self)

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
            self.dirty = True
    scoreWidth = property(fget = _getscoreWidth,
                          fset = _setscoreWidth)

    def _getartist(self):
        return self._score.scoreData.artist
    def _setartist(self, value):
        if self.artist != value:
            self._score.scoreData.artist = value
            for view in self.views():
                view.setArtist(value)
            self.dirty = True
    artist = property(fget = _getartist, fset = _setartist)

    def _getcreator(self):
        return self._score.scoreData.creator
    def _setcreator(self, value):
        if self.creator != value:
            self._score.scoreData.creator = value
            for view in self.views():
                view.setCreator(value)
            self.dirty = True
    creator = property(fget = _getcreator, fset = _setcreator)

    def _gettitle(self):
        return self._score.scoreData.title
    def _settitle(self, value):
        if self.title != value:
            self._score.scoreData.title = value
            for view in self.views():
                view.setTitle(value)
            self.dirty = True
    title = property(fget = _gettitle, fset = _settitle)

    def _getbpm(self):
        return self._score.scoreData.bpm
    def _setbpm(self, value):
        if self.bpm != value:
            self._score.scoreData.bpm = value
            for view in self.views():
                view.setBPM(value)
            self.dirty = True
    bpm = property(fget = _getbpm, fset = _setbpm)

    def _gethighlightedNote(self):
        return self._highlightedNote
    def _sethighlightedNote(self, np):
        if self._highlightedNote != np:
            self.clearHighlight()
            self.makeHighlight(np)
            self._highlightedNote = np
    highlightedNote = property(fget = _gethighlightedNote,
                               fset = _sethighlightedNote)

    def clearHighlight(self):
        if self.highlightedNote != None:
            qStaff = self._qStaffs[self.highlightedNote.staffIndex]
            qStaff.setHighlight(self.highlightedNote, False)

    def makeHighlight(self, np):
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

    def _getkitSize(self):
        return len(self._score.drumKit)
    kitSize = property(fget = _getkitSize)

    def lineOffsets(self):
        yOffsets = [drumIndex * self._properties.ySpacing
                    for drumIndex in range(0, self.kitSize)]
        yOffsets.reverse()
        return yOffsets

    def iterLineLabels(self):
        return (drum.abbr for drum in self._score.drumKit)

    def setScore(self, score):
        if score != self._score:
            score.gridFormatScore(None)
            self._score = score
            if score is not None:
                self.startUp()
            self._score.setCallBack(self.noteChanged)
            self.build()
            self.dirty = False

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

    def reBuild(self):
        oldSceneRect = self.sceneRect()
        self.build()
        self.update(oldSceneRect)

    def setWidth(self, width):
        if self.scoreWidth != width:
            self.scoreWidth = width
            if self._score is not None:
                formatChanged = self._score.gridFormatScore(width)
                if formatChanged:
                    self.reBuild()
            for view in self.views():
                view.setWidth(width)
            self.dirty = True

    def populate(self):
        for notePosition, head in self._score.iterNotes():
            self.setNote(notePosition, head)

    def noteChanged(self, notePosition):
        self.dirty = True
        head = self._score.getNote(notePosition)
        self.setNote(notePosition, head)

    def setNote(self, np, head):
        self._qStaffs[np.staffIndex].setNote(np, head)

    def ignoreNextClick(self):
        self._ignoreNext = True

    def mousePressEvent(self, event):
        event.ignore()
        if self._ignoreNext:
            self._ignoreNext = False
        else:
            super(QScore, self).mousePressEvent(event)

    def toggleNote(self, np, head):
        head = head if head is not None else self._properties.head
        self._score.toggleNote(np, head)

    def repeatNote(self, np, head):
        repeatDialog = QRepeatDialog(self.parent())
        if repeatDialog.exec_():
            nRepeats, repInterval = repeatDialog.getValues()
            for dummyIndex in range(nRepeats):
                np = self._score.notePlus(np, repInterval)
                if np is None:
                    break
                self._score.addNote(np, head)

    def highlightNote(self, np, onOff):
        if onOff:
            self.highlightedNote = np
        else:
            self.highlightedNote = None

    @delayCall
    def insertMeasure(self, np):
        counter = self._properties.beatCounter
        width = (self._properties.beatsPerMeasure *
                 counter.beatLength)
        self._score.insertMeasureByPosition(width, np,
                                            counter = counter)
        self._score.gridFormatScore(None)
        self.reBuild()
        self.dirty = True

    @delayCall
    def insertOtherMeasures(self, np):
        beats = self._properties.beatsPerMeasure
        counter = self._properties.beatCounter
        insertDialog = QInsertMeasuresDialog(self.parent(),
                                             beats,
                                             counter)
        if insertDialog.exec_():
            nMeasures, beats, counter, insertBefore = insertDialog.getValues()
            counter = counterMaker(counter)
            measureWidth = beats * counter.beatLength
            if not insertBefore:
                np.measureIndex += 1
            for dummyMeasureIndex in range(nMeasures):
                self._score.insertMeasureByPosition(measureWidth, np,
                                                    counter = counter)
            self._score.gridFormatScore(None)
            self.reBuild()
            self.dirty = True

    @delayCall
    def deleteMeasure(self, np):
        if self._score.numMeasures() == 1:
            QtGui.QMessageBox.warning(self.parent(),
                                      "Invalid delete",
                                      "Cannot delete last measure.")
            return
        yesNo = QtGui.QMessageBox.question(self.parent(), "Delete Measure",
                                              "Really delete this measure?",
                                              QtGui.QMessageBox.Ok,
                                              QtGui.QMessageBox.Cancel)
        if yesNo == QtGui.QMessageBox.Ok:
            self._score.deleteMeasureByPosition(np)
            self._score.gridFormatScore(None)
            self.reBuild()
            self.dirty = True

    def copyMeasure(self, np):
        self.measureClipboard = self._score.copyMeasure(np)

    @delayCall
    def pasteMeasure(self, np):
        self._score.pasteMeasure(np, self.measureClipboard)
        if self._score.gridFormatScore(None):
            self.reBuild()
        self.dirty = True

    @delayCall
    def editMeasureProperties(self, np, numTicks, counter):
        defBeats = self._properties.beatsPerMeasure
        defCounter = self._properties.beatCounter
        editDialog = QEditMeasureDialog(self.parent(),
                                        numTicks,
                                        counter,
                                        defBeats,
                                        defCounter)
        if editDialog.exec_():
            beats, newCounter = editDialog.getValues()
            newCounter = counterMaker(newCounter)
            newTicks = newCounter.beatLength * beats
            if (newCounter != counter
                or newTicks != numTicks):
                self._score.setMeasureBeatCount(np, beats, newCounter)
                self.dirty = True
                if newTicks != numTicks:
                    self._score.gridFormatScore(None)
                    self.reBuild()
                else:
                    self._countChanged(np)

    def _countChanged(self, np):
        staff = self._qStaffs[np.staffIndex]
        staff.countChanged(np)

    @delayCall
    def setSectionEnd(self, np, onOff):
        self._score.setSectionEnd(np, onOff)
        self._score.gridFormatScore(None)
        self.reBuild()
        self.dirty = True

    def setRepeatEnd(self, np, onOff):
        self._score.setRepeatEnd(np, onOff)
        self.dirty = True

    def setRepeatStart(self, np, onOff):
        self._score.setRepeatStart(np, onOff)
        self.dirty = True

    def loadScore(self, filename):
        try:
            newScore = _SCORE_FACTORY(filename = filename)
        except IOError, exc:
            msg = "Error loading DrumBurp file %s" % filename
            QtGui.QMessageBox.warning(self.parent(),
                                      "Score load error",
                                      msg + "\n" + str(exc))
            return False
        self.setScore(newScore)
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
        self.setScore(newScore)

    def setAllBeats(self):
        self._score.setAllBeats(self._properties.beatsPerMeasure,
                                self._properties.beatCounter)
        self.reBuild()
        self.dirty = True

    def exportASCII(self, handle):
        self._score.exportASCII(handle)

    def printScore(self, qprinter):
        painter = QtGui.QPainter(qprinter)
        self.render(painter)
        painter.end()

