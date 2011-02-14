'''
Created on 5 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore
from Data.NotePosition import NotePosition
from QInsertMeasuresDialog import QInsertMeasuresDialog
from QEditMeasureDialog import QEditMeasureDialog
from Data.TimeCounter import counterMaker
from Data import DBConstants
from QRepeatCountDialog import QRepeatCountDialog

_CHAR_PIXMAPS = {}
def _stringToPixMap(character, font, scene):
    key = (character, font.key())
    if key not in _CHAR_PIXMAPS:
        fm = QtGui.QFontMetrics(font)
        br = fm.tightBoundingRect(character)
        dx = -br.x() + 1
        dy = -br.y() + 1
        br.translate(dx, dy)
        pix = QtGui.QPixmap(br.width() + 2, br.height() + 2)
        painter = QtGui.QPainter(pix)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(scene.palette().base())
        painter.drawRect(0, 0, br.width() + 2, br.height() + 2)
        painter.setBrush(scene.palette().text())
        painter.setPen(QtCore.Qt.SolidLine)
        painter.setFont(font)
        painter.drawText(dx, dy, character)
        painter.end()
        _CHAR_PIXMAPS[key] = pix
    return _CHAR_PIXMAPS[key]


class QMeasure(QtGui.QGraphicsItem):
    '''
    classdocs
    '''


    def __init__(self, qScore, measure, parent):
        '''
        Constructor
        '''
        super(QMeasure, self).__init__(parent)
        self._props = qScore.displayProperties
        self._measure = None
        self._index = None
        self._width = 0
        self._height = 0
        self._highlight = None
        self._rect = QtCore.QRectF(0, 0, 0, 0)
        self.setAcceptsHoverEvents(True)
        self.setMeasure(measure)

    def _setDimensions(self):
        self.prepareGeometryChange()
        self._width = self._props.xSpacing * len(self._measure)
        self._height = (self.scene().kitSize + 2) * self._props.ySpacing
        self._rect.setBottomRight(QtCore.QPointF(self._width, self._height))

    def boundingRect(self):
        return self._rect

    def width(self):
        return self._width

    def height(self):
        return self._height

    def setMeasure(self, measure):
        if self._measure != measure:
            self._measure = measure
            self._setDimensions()
            self.update()

    def setIndex(self, index):
        self._index = index

    def paint(self, painter, dummyOption, dummyWidget = None):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.scene().palette().base())
        painter.drawRect(self._rect)
        painter.setPen(QtCore.Qt.SolidLine)
        font = self._props.noteFont
        if font is None:
            font = painter.font()
        xValues = [noteTime * self._props.xSpacing
                   for noteTime in range(0, len(self._measure))]
        for drumIndex in range(0, self.scene().kitSize):
            baseline = (self.scene().kitSize - drumIndex) * self._props.ySpacing
            lineHeight = baseline + (self._props.ySpacing / 2.0)
            for noteTime, x in enumerate(xValues):
                text = self._measure.noteAt(noteTime, drumIndex)
                if text == DBConstants.EMPTY_NOTE:
                    painter.drawLine(x + 1, lineHeight,
                                     x + self._props.xSpacing - 1, lineHeight)
                else:
                    pix = _stringToPixMap(text, font, self.scene())
                    left = x + (self._props.xSpacing - pix.width() + 2) / 2
                    top = baseline + (self._props.ySpacing
                                      - pix.height() + 2) / 2
                    painter.drawPixmap(left, top, pix)
                if self._highlight == (noteTime, drumIndex):
                    painter.setPen(self.scene().palette().highlight().color())
                    painter.setBrush(QtCore.Qt.NoBrush)
                    painter.drawRect(x, baseline,
                                     self._props.xSpacing - 1,
                                     self._props.ySpacing - 1)
                    painter.setPen(self.scene().palette().text().color())
        baseline = (self.scene().kitSize + 1) * self._props.ySpacing
        for noteTime, count in enumerate(self._measure.count()):
            x = xValues[noteTime]
            pix = _stringToPixMap(count, font, self.scene())
            left = x + (self._props.xSpacing - pix.width() + 2) / 2
            top = baseline + (self._props.ySpacing - pix.height() + 2) / 2
            painter.drawPixmap(left, top, pix)
            if self._highlight and noteTime == self._highlight[0]:
                painter.setPen(self.scene().palette().highlight().color())
                painter.setBrush(QtCore.Qt.NoBrush)
                painter.drawRect(x, baseline,
                                 self._props.xSpacing - 1,
                                 self._props.ySpacing - 1)
        if self._measure.isRepeatEnd() and self._measure.repeatCount > 2:
            repeatText = '%dx' % self._measure.repeatCount
            textWidth = QtGui.QFontMetrics(font).width(repeatText)
            textLocation = QtCore.QPointF(self.width() - textWidth,
                                          self._props.ySpacing)
            painter.drawText(textLocation, repeatText)


    def dataChanged(self, notePosition):
        if None not in (notePosition.noteTime, notePosition.drumIndex):
            self.update()
        else:
            self._setDimensions()
            self.update()
            self.parent().placeMeasures()

    def xSpacingChanged(self):
        self._setDimensions()
        self.update()

    def ySpacingChanged(self):
        self._setDimensions()
        self.update()

    def _countChanged(self):
        self.update()

    def _setRepeatCount(self, count):
        self._measure.repeatCount = count
        self.update()

    def _isOverNotes(self, point):
        return (1 <= (point.y() / self._props.ySpacing) < (1 + self.scene().kitSize))

    def _isOverCount(self, point):
        return (point.y() / self._props.ySpacing) >= self.scene().kitSize

    def _getNotePosition(self, point):
        x = self._getNoteTime(point)
        y = self.scene().kitSize - int(point.y() / self._props.ySpacing)
        return x, y

    def _getNoteTime(self, point):
        return int(point.x() / self._props.xSpacing)

    def _hovering(self, event):
        point = self.mapFromScene(event.scenePos())
        if self._isOverNotes(point):
            newPlace = self._getNotePosition(point)
            if newPlace != self._highlight:
                self._highlight = newPlace
                self.update()
                self.parentItem().setLineHighlight(newPlace[1])
        elif self._highlight != None:
            self._highlight = None
            self.parentItem().clearHighlight()
            self.update()

    def hoverEnterEvent(self, event):
        self._hovering(event)

    def hoverMoveEvent(self, event):
        self._hovering(event)

    def hoverLeaveEvent(self, event_):
        self._highlight = None
        self.update()
        self.parentItem().clearHighlight()

    def toggleNote(self, noteTime, drumIndex, head = None):
        notePosition = self._makeNotePosition(noteTime, drumIndex)
        if head is None:
            head = self._props.head
        self.scene().score.toggleNote(notePosition, head)

    def mousePressEvent(self, event):
        point = self.mapFromScene(event.scenePos())
        if self._isOverNotes(point):
            noteTime, drumIndex = self._getNotePosition(point)
            self.toggleNote(noteTime, drumIndex)

    def _makeNotePosition(self, noteTime, drumIndex):
        np = NotePosition(measureIndex = self._index, noteTime = noteTime, drumIndex = drumIndex)
        return self.parentItem().augmentNotePosition(np)

    def _measurePosition(self):
        return NotePosition(measureIndex = self._index)

    def _insertMeasure(self, np):
        qScore = self.scene()
        counter = self._props.beatCounter
        width = (self._props.beatsPerMeasure *
                 counter.beatLength)
        qScore.score.insertMeasureByPosition(width, np,
                                             counter = counter)
        qScore.reBuild()
        qScore.dirty = True

    def insertMeasureBefore(self):
        self._insertMeasure(self._measurePosition())

    def insertMeasureAfter(self):
        np = self._measurePosition()
        np.measureIndex += 1
        self._insertMeasure(np)

    def insertOtherMeasures(self):
        np = self._measurePosition()
        beats = self._props.beatsPerMeasure
        counter = self._props.beatCounter
        insertDialog = QInsertMeasuresDialog(self.scene().parent(),
                                             beats,
                                             counter)
        if insertDialog.exec_():
            nMeasures, beats, counter, insertBefore = insertDialog.getValues()
            counter = counterMaker(counter)
            measureWidth = beats * counter.beatLength
            if not insertBefore:
                np.measureIndex += 1
            score = self.scene().score
            for dummyMeasureIndex in range(nMeasures):
                score.insertMeasureByPosition(measureWidth, np,
                                              counter = counter)
            self.scene().reBuild()
            self.scene().dirty = True

    def deleteMeasure(self):
        score = self.scene().score
        if score.numMeasures() == 1:
            QtGui.QMessageBox.warning(self.parent(),
                                      "Invalid delete",
                                      "Cannot delete last measure.")
            return
        yesNo = QtGui.QMessageBox.question(self.scene().parent(),
                                           "Delete Measure",
                                           "Really delete this measure?",
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Cancel)
        if yesNo == QtGui.QMessageBox.Ok:
            score.deleteMeasureByPosition(self._measurePosition())
            self.scene().reBuild()
            self.scene().dirty = True

    def copyMeasure(self):
        self.scene().copyMeasure(self._measurePosition())

    def pasteMeasure(self):
        self.scene().pasteMeasure(self._measurePosition())

    def editMeasureProperties(self):
        numTicks = len(self._measure)
        counter = self._measure.counter
        defBeats = self._props.beatsPerMeasure
        defCounter = self._props.beatCounter
        editDialog = QEditMeasureDialog(self.scene().parent(),
                                        numTicks,
                                        counter,
                                        defBeats,
                                        defCounter)
        if editDialog.exec_():
            beats, newCounter = editDialog.getValues()
            newCounter = counterMaker(newCounter)
            newTicks = newCounter.beatLength * beats
            score = self.scene().score
            if (newCounter != counter
                or newTicks != numTicks):
                score.setMeasureBeatCount(self._measurePosition(),
                                          beats, newCounter)
                self.scene().dirty = True
                if newTicks != numTicks:
                    self.scene().reBuild()
                else:
                    self._countChanged()

    def changeRepeatCount(self):
        repDialog = QRepeatCountDialog(self._measure.repeatCount,
                                       self.scene().parent())
        if repDialog.exec_():
            self._setRepeatCount(repDialog.getValue())
