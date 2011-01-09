'''
Created on 4 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui
from QStaff import QStaff
from Data.Score import ScoreFactory
_SCORE_FACTORY = ScoreFactory()

#pylint: disable-msg=R0904

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
        score = _SCORE_FACTORY(filename = parent.filename,
                               numMeasures = 16,
                               measureWidth = self._properties.defaultMeasureWidth)
        self._startMousePressItem = None
        self._properties.setScore(self)
        self.setScore(score)

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

    def reBuild(self):
        oldSceneRect = self.sceneRect()
        self.build()
        self.update(oldSceneRect)

    def setWidth(self):
        formatChanged = self._score.gridFormatScore(self._properties.width)
        if formatChanged:
            self.reBuild()

    def populate(self):
        for notePosition, head in self._score.iterNotes():
            self.setNote(notePosition, head)

    def noteChanged(self, notePosition):
        head = self._score.getNote(notePosition)
        self.setNote(notePosition, head)

    def setNote(self, np, head):
        self._qStaffs[np.staffIndex].setNote(np, head)

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos())
        if item is not None:
            self._startMousePressItem = item
            item.mousePressEvent(event)

    def getMousePressStartItem(self):
        return self._startMousePressItem

    def mouseReleaseEvent(self, event):
        item = self.itemAt(event.scenePos())
        if item is not None:
            item.mouseReleaseEvent(event)
        self._startMousePressItem = None

    def toggleNote(self, np, head):
        head = head if head is not None else self._properties.head
        self._score.toggleNote(np, head)

    def insertMeasure(self, np):
        width = self._properties.defaultMeasureWidth
        self._score.insertMeasureByPosition(width, np)
        self._score.gridFormatScore(self._properties.width)
        self.reBuild()

    def insertOtherMeasures(self, np):
        QtGui.QMessageBox.warning(self.parent(),
                                  "Not implemented",
                                  "Inserting multiple and/or non-standard "
                                  "measures is not yet supported.")

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
            self._score.gridFormatScore(self._properties.width)
            self.reBuild()

