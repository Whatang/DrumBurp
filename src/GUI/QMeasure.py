'''
Created on 5 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore
from Data.NotePosition import NotePosition
from QInsertMeasuresDialog import QInsertMeasuresDialog
from QEditMeasureDialog import QEditMeasureDialog
from QRepeatDialog import QRepeatDialog
from Data.TimeCounter import counterMaker
from Data import DBConstants
from DBCommands import (ToggleNote, RepeatNoteCommand,
                        InsertMeasuresCommand, SetRepeatCountCommand,
                        EditMeasurePropertiesCommand,
                        DeleteMeasureCommand,
                        InsertSectionCommand)
from QRepeatCountDialog import QRepeatCountDialog
from QMenuIgnoreCancelClick import QMenuIgnoreCancelClick
import DBIcons

import copy

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
        self._repeatCountRect = None
        self._startClick = None
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
            painter.setPen(self.scene().palette().text().color())
            repeatText = '%dx' % self._measure.repeatCount
            textWidth = QtGui.QFontMetrics(font).width(repeatText)
            textLocation = QtCore.QPointF(self.width() - textWidth,
                                          self._props.ySpacing)
            painter.drawText(textLocation, repeatText)
            if self._repeatCountRect is None:
                self._repeatCountRect = QtCore.QRectF(0, 0, 0, 0)
            self._repeatCountRect.setSize(QtCore.QSizeF(textWidth,
                                                        self._props.ySpacing))
            self._repeatCountRect.setTopRight(QtCore.QPointF(self.width(), 0))
        else:
            self._repeatCountRect = None


    def dataChanged(self, notePosition):
        if None not in (notePosition.noteTime, notePosition.drumIndex):
            self.update()
        else:
            self._setDimensions()
            self.update()
            self.parentItem().placeMeasures()

    def xSpacingChanged(self):
        self._setDimensions()
        self.update()

    def ySpacingChanged(self):
        self._setDimensions()
        self.update()

    def changeRepeatCount(self):
        repDialog = QRepeatCountDialog(self._measure.repeatCount,
                                       self.scene().parent())
        if (repDialog.exec_()
            and self._measure.repeatCount != repDialog.getValue()):
            command = SetRepeatCountCommand(self.scene(),
                                            self._measurePosition(),
                                            self._measure.repeatCount,
                                            repDialog.getValue())
            self.scene().addCommand(command)

    def _isOverNotes(self, point):
        return (1 <= (point.y() / self._props.ySpacing)
                < (1 + self.scene().kitSize))

    def _isOverCount(self, point):
        return (point.y() / self._props.ySpacing) >= self.scene().kitSize

    def _isOverRepeatCount(self, point):
        return (self._repeatCountRect is not None
                and self._repeatCountRect.contains(point))

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
        if self._isOverCount(point) or self._isOverRepeatCount(point):
            self.setCursor(QtCore.Qt.PointingHandCursor)
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)

    def hoverEnterEvent(self, event):
        self._hovering(event)

    def hoverMoveEvent(self, event):
        self._hovering(event)

    def hoverLeaveEvent(self, event_):
        self._highlight = None
        self.update()
        self.parentItem().clearHighlight()
        self.setCursor(QtCore.Qt.ArrowCursor)

    def toggleNote(self, noteTime, drumIndex, head = None):
        notePosition = self._makeNotePosition(noteTime, drumIndex)
        if head is None:
            head = self._props.head
        command = ToggleNote(self.scene(), notePosition, head)
        self.scene().addCommand(command)

    def repeatNote(self, noteTime, drumIndex):
        np = self._makeNotePosition(noteTime, drumIndex)
        head = self._measure.noteAt(noteTime, drumIndex)
        repeatDialog = QRepeatDialog(self.scene().parent())
        if repeatDialog.exec_():
            nRepeats, repInterval = repeatDialog.getValues()
            command = RepeatNoteCommand(self.scene(), np, nRepeats,
                                        repInterval, head)
            self.scene().addCommand(command)

    def mousePressEvent(self, event):
        point = self.mapFromScene(event.scenePos())
        if self._isOverNotes(point):
            noteTime, drumIndex = self._getNotePosition(point)
            self._notePressEvent(event, noteTime, drumIndex)
        else:
            event.ignore()

    def _notePressEvent(self, event, noteTime, drumIndex):
        score = self.scene().score
        menu = None
        if event.button() == QtCore.Qt.MiddleButton:
            event.ignore()
            menu = QMenuIgnoreCancelClick(self.scene())
            for noteHead in self._props.allowedNoteHeads():
                def noteAction(nh = noteHead):
                    self.toggleNote(noteTime, drumIndex, nh)
                menu.addAction(noteHead, noteAction)
        elif event.button() == QtCore.Qt.RightButton:
            event.ignore()
            menu = QMenuIgnoreCancelClick(self.scene())
            actionText = "Repeat note"
            repNote = lambda:self.repeatNote(noteTime, drumIndex)
            repeatNoteAction = menu.addAction(DBIcons.getIcon("repeat"),
                                              actionText, repNote)
            if (self._measure.noteAt(noteTime, drumIndex)
                == DBConstants.EMPTY_NOTE):
                repeatNoteAction.setEnabled(False)
            menu.addSeparator()
            menu.addAction(DBIcons.getIcon("copy"),
                           "Copy Measure",
                           self.copyMeasure)
            pasteAction = menu.addAction(DBIcons.getIcon("paste"),
                                         "Paste Measure",
                                         self.pasteMeasure)
            if self.scene().measureClipboard is None:
                pasteAction.setEnabled(False)
            menu.addSeparator()
            actionText = "Insert Default Measure"
            menu.addAction(actionText,
                           self.insertMeasureBefore)
            insertMenu = menu.addMenu("Insert...")
            insertMenu.addAction("Default Measure After",
                                 self.insertMeasureAfter)
            insertMenu.addAction("Other Measures", self.insertOtherMeasures)
            sectionCopyMenu = insertMenu.addMenu("Section Copy")
            sectionCopyMenu.setEnabled(score.numSections() > 0)
            for si, sectionTitle in enumerate(score.iterSections()):
                copyIt = lambda i = si: self._copySection(i)
                sectionCopyMenu.addAction(sectionTitle, copyIt)
            menu.addSeparator()
            deleteAction = menu.addAction(DBIcons.getIcon("delete"),
                                          "Delete Measure",
                                          self.deleteMeasure)
            deleteAction.setEnabled(score.numMeasures() > 1)
            deleteMenu = menu.addMenu("Delete...")
            deleteStaffAction = deleteMenu.addAction("Staff", self.deleteStaff)
            deleteStaffAction.setEnabled(score.numStaffs() > 1)
            deleteSectionAction = deleteMenu.addAction("Section",
                                                       self.deleteSection)
            deleteSectionAction.setEnabled(score.numSections() > 1)
            deleteEmptyAction = deleteMenu.addAction("Empty Trailing Measures",
                                                     self.deleteEmptyMeasures)
            deleteEmptyAction.setEnabled(score.numMeasures() > 1)
        else:
            self._startClick = (noteTime, drumIndex)
        if menu is not None:
            menu.exec_(event.screenPos())

    def mouseReleaseEvent(self, event):
        point = self.mapFromScene(event.scenePos())
        if self._isOverNotes(point):
            noteTime, drumIndex = self._getNotePosition(point)
            if (event.button() == QtCore.Qt.LeftButton and
                self._startClick == (noteTime, drumIndex)):
                self.toggleNote(noteTime, drumIndex)
            else:
                event.ignore()
        else:
            event.ignore()

    def mouseDoubleClickEvent(self, event):
        point = self.mapFromScene(event.scenePos())
        if self._isOverCount(point):
            self.editMeasureProperties()
        elif self._isOverRepeatCount(point):
            self.changeRepeatCount()
        else:
            event.ignore()

    def _makeNotePosition(self, noteTime, drumIndex):
        np = NotePosition(measureIndex = self._index,
                          noteTime = noteTime,
                          drumIndex = drumIndex)
        return self.parentItem().augmentNotePosition(np)

    def _measurePosition(self):
        np = NotePosition(measureIndex = self._index)
        return self.parentItem().augmentNotePosition(np)

    def deleteStaff(self):
        score = self.scene().score
        if score.numStaffs() == 1:
            QtGui.QMessageBox.warning(self.parent(),
                                      "Invalid delete",
                                      "Cannot delete last staff.")
            return
        msg = "Really delete this staff?"
        yesNo = QtGui.QMessageBox.question(self.scene().parent(),
                                           "Delete Staff?",
                                           msg,
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Cancel)
        if yesNo == QtGui.QMessageBox.Ok:
            np = self._measurePosition()
            np.measureIndex = None
            staff = score.getItemAtPosition(np)
            arguments = []
            np.measureIndex = staff.numMeasures() - 1
            while np.measureIndex >= 0:
                arguments.append((copy.copy(np),))
                np.measureIndex -= 1
            self.scene().addRepeatedCommand("Delete Staff",
                                            DeleteMeasureCommand, arguments)

    def deleteSection(self):
        score = self.scene().score
        if score.numSections() <= 1:
            QtGui.QMessageBox.warning(self.parent(),
                                      "Invalid delete",
                                      "Cannot delete last staff.")
            return
        msg = "Really delete this section?"
        yesNo = QtGui.QMessageBox.question(self.scene().parent(),
                                           "Delete Staff?",
                                           msg,
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Cancel)
        if yesNo == QtGui.QMessageBox.Ok:
            np = self._measurePosition()
            startIndex = score.getSectionStartStaffIndex(np)
            sectionIndex = score.getSectionIndex(np)
            sectionName = score.getSectionTitle(sectionIndex)
            np.staffIndex = startIndex
            while (np.staffIndex < score.numStaffs()
                   and not score.getStaff(np.staffIndex).isSectionEnd()):
                np.staffIndex += 1
            arguments = []
            for np.staffIndex in range(np.staffIndex, startIndex - 1, -1):
                staff = score.getStaff(np.staffIndex)
                for np.measureIndex in range(staff.numMeasures() - 1, -1, -1):
                    arguments.append((copy.copy(np),))
                np.staffIndex -= 1
            self.scene().addRepeatedCommand("Delete Section: " + sectionName,
                                            DeleteMeasureCommand, arguments)

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
            positions = score.trailingEmptyMeasures()
            if len(positions) == 0:
                return
            arguments = [(np,) for np in positions]
            self.scene().addRepeatedCommand("Delete Empty Measures",
                                            DeleteMeasureCommand, arguments)


    def _insertMeasure(self, np):
        counter = self._props.beatCounter
        command = InsertMeasuresCommand(self.scene(), np, 1,
                                        self._props.beatsPerMeasure *
                                        counter.beatLength,
                                        counter)
        self.scene().addCommand(command)

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
            command = InsertMeasuresCommand(self.scene(), np, nMeasures,
                                            measureWidth, counter)
            self.scene().addCommand(command)

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
            command = DeleteMeasureCommand(self.scene(),
                                           self._measurePosition())
            self.scene().addCommand(command)

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
            if (newCounter != counter
                or newTicks != numTicks):
                command = EditMeasurePropertiesCommand(self.scene(),
                                                       self._measurePosition(),
                                                       beats,
                                                       newCounter)
                self.scene().addCommand(command)

    def _copySection(self, sectionIndex):
        np = self._measurePosition()
        command = InsertSectionCommand(self.scene(), np, sectionIndex)
        self.scene().addCommand(command)
