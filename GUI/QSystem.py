'''
Created on 5 Dec 2010

@author: Mike Thomas

'''
from PyQt4 import QtGui, QtCore
import QNote
from DBSignals import LINESPACING_SIGNAL, YSPACING_SIGNAL

class QSystem(QtGui.QGraphicsItemGroup):
    '''
    classdocs
    '''

    def __init__(self, system, width, numLines,
                 scoreScene, systemIndex, parent = None):
        '''
        Constructor
        '''
        super(QSystem, self).__init__(parent, scoreScene)
        self._scene = scoreScene
        self._system = None
        self._width = width
        self._numLines = numLines
        self._notes = []
        self._index = systemIndex
        self.setSystem(system)
        self._catcher = QtCore.QObject()
        self._catcher.connect(scoreScene, QtCore.SIGNAL(LINESPACING_SIGNAL),
                              self._rePosition)
        self._catcher.connect(scoreScene, QtCore.SIGNAL(YSPACING_SIGNAL),
                              self._rePosition)

    def setSystem(self, system):
        self._system = system
        self.build()
        self._rePosition()
        system.connect(system, QtCore.SIGNAL("dataChanged"),
                       self.drawNoteHead)

    def width(self):
        return (((self._system.lastTime - self._system.startTime)
                 * self._scene.xSpace)
                 + QNote.OFFSET)

    def height(self):
        return self._system.numLines * self._scene.ySpace

    def yPosition(self):
        return self._scene.yMargins + self._index * (self._scene.interLineSpace + self.height())

    def _rePosition(self):
        self.setPos(self._scene.xMargins, self.yPosition())

    def build(self):
        self._notes = []
        for lineIndex in range(0, self._numLines):
            self._notes.append([])
            thisLine = self._notes[-1]
            instr = self._system.getLine(lineIndex).instrument
            QNote.QLineLabel(instr.abbr, lineIndex,
                             self._scene, parent = self)
            for timeIndex in range(0, self._width):
                newNote = QNote.QNote(timeIndex,
                                      lineIndex,
                                      self._scene,
                                      self)
                self.addToGroup(newNote)
                thisLine.append(newNote)
        self.reset()

    def reset(self):
        for lineIndex in range(0, self._numLines):
            for timeIndex in range(0, self._width):
                self.drawNoteHead(self._system.startTime + timeIndex,
                                  lineIndex)

    def drawNoteHead(self, timeIndex, lineIndex):
        note = self._notes[lineIndex][self._system.systemTime(timeIndex)]
        noteHead = self._system.getNoteHead(timeIndex, lineIndex)
        note.setText(noteHead)

    def toggleNote(self, timeIndex, lineIndex, head):
        self._system.toggleNote(self._system.startTime + timeIndex,
                                lineIndex, head)
