'''
Created on 5 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui
from QNote import QNote
from QCount import QCount
from Data.NotePosition import NotePosition
from QInsertMeasuresDialog import QInsertMeasuresDialog
from QEditMeasureDialog import QEditMeasureDialog
from Data.TimeCounter import counterMaker

class QMeasure(QtGui.QGraphicsItemGroup):
    '''
    classdocs
    '''


    def __init__(self, qScore, measure, parent):
        '''
        Constructor
        '''
        super(QMeasure, self).__init__(parent)
        self._qStaff = parent
        self._props = qScore.displayProperties
        self._measure = None
        self._index = None
        self._notes = []
        self._counts = []
        self._width = 0
        self._height = 0
        self.setMeasure(measure)
        self.setHandlesChildEvents(False)

    def width(self):
        return self._width

    def height(self):
        return self._height

    def setMeasure(self, measure):
        if self._measure != measure:
            self._measure = measure
            self._build()

    def setIndex(self, index):
        self._index = index

    def _clear(self):
        self._counts = []

    def _build(self):
        self._clear()
        for drumIndex in range(0, self.scene().kitSize):
            noteLine = []
            self._notes.append(noteLine)
            for noteTime in range(0, len(self._measure)):
                qNote = QNote(self.scene(), parent = self)
                qNote.setIndex(drumIndex, noteTime)
                noteLine.append(qNote)
                self.addToGroup(qNote)
        for noteTime, count in enumerate(self._measure.count()):
            qCount = QCount(count, self.scene(), parent = self)
            qCount.setIndex(noteTime)
            self._counts.append(qCount)
            self.addToGroup(qCount)

    def placeNotes(self):
        yOffsets = self.scene().lineOffsets
        countOffset = self.scene().kitSize * self._props.ySpacing
        for noteTime in range(0, len(self._measure)):
            xOffset = noteTime * self._props.xSpacing
            for drumIndex, yOffset in enumerate(yOffsets):
                qNote = self._notes[drumIndex][noteTime]
                qNote.setDimensions()
                qNote.setPos(xOffset, yOffset)
            qCount = self._counts[noteTime]
            qCount.setDimensions()
            qCount.setPos(xOffset, countOffset)
        self._setWidth()
        self._setHeight()

    def _setWidth(self):
        self._width = len(self._measure) * self._props.xSpacing

    def _setHeight(self):
        self._height = (self.scene().kitSize + 1) * self._props.ySpacing

    def _makeNotePosition(self):
        np = NotePosition()
        return self.augmentNotePosition(np)

    def augmentNotePosition(self, np):
        np.measureIndex = self._index
        return self._qStaff.augmentNotePosition(np)

    def setHighlight(self, np, onOff):
        qCount = self._counts[np.noteTime]
        qCount.setHighlight(onOff)
        qNote = self._notes[np.drumIndex][np.noteTime]
        qNote.setHighlight(onOff)

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
        self._insertMeasure(self._makeNotePosition())

    def insertMeasureAfter(self):
        np = self._makeNotePosition()
        np.measureIndex += 1
        self._insertMeasure(np)

    def insertOtherMeasures(self):
        np = self._makeNotePosition()
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
            score.deleteMeasureByPosition(self._makeNotePosition())
            self.scene().reBuild()
            self.scene().dirty = True

    def deleteEmptyMeasures(self):
        score = self.scene().score
        if score.numMeasures() == 1:
            QtGui.QMessageBox.warning(self.parent(),
                                      "Invalid delete",
                                      "Cannot delete last measure.")
            return
        msg = "This will delete all empty trailing measures.\nContinue?"
        yesNo = QtGui.QMessageBox.question(self.scene().parent(),
                                           "Delete Empty Measures",
                                           msg,
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Cancel)
        if yesNo == QtGui.QMessageBox.Ok:
            score.deleteEmptyMeasures()
            self.scene().reBuild()
            self.scene().dirty = True

    def copyMeasure(self):
        self.scene().copyMeasure(self._makeNotePosition())

    def pasteMeasure(self):
        self.scene().pasteMeasure(self._makeNotePosition())

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
                score.setMeasureBeatCount(self._makeNotePosition(),
                                          beats, newCounter)
                self.scene().dirty = True
                if newTicks != numTicks:
                    self.scene().reBuild()
                else:
                    self._countChanged()

    def _countChanged(self):
        for qCount, count in zip(self._counts, self._measure.count()):
            qCount.setText(count)

    def setNote(self, np, head):
        self._notes[np.drumIndex][np.noteTime].setText(head)

    def xSpacingChanged(self):
        yOffsets = self.scene().lineOffsets
        for noteTime in range(0, len(self._measure)):
            xOffset = noteTime * self._props.xSpacing
            for drumIndex, dummyyOffset in enumerate(yOffsets):
                qNote = self._notes[drumIndex][noteTime]
                qNote.setX(xOffset)
                qNote.xSpacingChanged()
            qCount = self._counts[noteTime]
            qCount.setX(xOffset)
            qCount.xSpacingChanged()
        self._setWidth()

    def ySpacingChanged(self):
        yOffsets = self.scene().lineOffsets
        countOffset = self.scene().kitSize * self._props.ySpacing
        for noteTime in range(0, len(self._measure)):
            for drumIndex, yOffset in enumerate(yOffsets):
                qNote = self._notes[drumIndex][noteTime]
                qNote.setY(yOffset)
                qNote.ySpacingChanged()
            qCount = self._counts[noteTime]
            qCount.setY(countOffset)
            qCount.ySpacingChanged()
        self._setHeight()
