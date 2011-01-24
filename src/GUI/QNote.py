'''
Created on 5 Dec 2010

@author: Mike Thomas

'''
from PyQt4 import QtCore
from QMenuIgnoreCancelClick import QMenuIgnoreCancelClick
from QDBGridItem import QDBGridItem
from Data import DBConstants
from Data.NotePosition import NotePosition
import DBIcons

class QNote(QDBGridItem):
    '''
    classdocs
    '''
    def __init__(self, qScore, parent):
        super(QNote, self).__init__(qScore, parent)
        self._qMeasure = parent
        self._drumIndex = None
        self._noteTime = None
        self._notePosition = NotePosition()
        self._text = DBConstants.EMPTY_NOTE
        self.setAcceptsHoverEvents(True)

    def toggleNote(self, head = None):
        np = NotePosition(drumIndex = self._drumIndex,
                          noteTime = self._noteTime)
        self._qMeasure.toggleNote(np, head)

    def repeatNote(self):
        np = NotePosition(drumIndex = self._drumIndex,
                          noteTime = self._noteTime)
        self._qMeasure.repeatNote(np, self._text)

    def setIndex(self, drumIndex, noteTime):
        if (drumIndex, noteTime) != (self._drumIndex, self._noteTime):
            self._drumIndex = drumIndex
            self._noteTime = noteTime
            self._notePosition.drumIndex = drumIndex
            self._notePosition.noteTime = noteTime

    def cellWidth(self):
        return self._props.xSpacing

    def cellHeight(self):
        return self._props.ySpacing

    def mousePressEvent(self, event):
        menu = None
        if event.button() == QtCore.Qt.MiddleButton:
            event.ignore()
            menu = QMenuIgnoreCancelClick(self._qScore)
            for noteHead in self._props.allowedNoteHeads():
                action = menu.addAction(noteHead)
                def noteAction(nh = noteHead):
                    self.toggleNote(nh)
                menu.connect(action, QtCore.SIGNAL("triggered()"), noteAction)
        elif event.button() == QtCore.Qt.RightButton:
            event.ignore()
            menu = QMenuIgnoreCancelClick(self._qScore)
            actionText = "Repeat note"
            repeatNoteAction = menu.addAction(DBIcons.getIcon("repeat"), actionText)
            menu.connect(repeatNoteAction,
                         QtCore.SIGNAL("triggered()"),
                         self.repeatNote)
            if self._text == DBConstants.EMPTY_NOTE:
                repeatNoteAction.setEnabled(False)
            menu.addSeparator()
            copyAction = menu.addAction(DBIcons.getIcon("copy"),
                                        "Copy Measure")
            menu.connect(copyAction,
                         QtCore.SIGNAL("triggered()"),
                         self._qMeasure.copyMeasure)
            pasteAction = menu.addAction(DBIcons.getIcon("paste"),
                                         "Paste Measure")
            menu.connect(pasteAction,
                         QtCore.SIGNAL("triggered()"),
                         self._qMeasure.pasteMeasure)
            if self._qScore.measureClipboard is None:
                pasteAction.setEnabled(False)
            menu.addSeparator()
            actionText = "Insert Default Measure"
            insertDefaultMeasureAction = menu.addAction(actionText)
            menu.connect(insertDefaultMeasureAction,
                         QtCore.SIGNAL("triggered()"),
                         self._qMeasure.insertMeasureBefore)
            insertMenu = menu.addMenu("Insert...")
            insertAfterAction = insertMenu.addAction("Default Measure After")
            insertMenu.connect(insertAfterAction,
                               QtCore.SIGNAL("triggered()"),
                               self._qMeasure.insertMeasureAfter)
            insertOtherMeasures = insertMenu.addAction("Other Measures")
            insertMenu.connect(insertOtherMeasures,
                               QtCore.SIGNAL("triggered()"),
                               self._qMeasure.insertOtherMeasures)
            menu.addSeparator()
            deleteAction = menu.addAction(DBIcons.getIcon("delete"),
                                          "Delete Measure")
            menu.connect(deleteAction, QtCore.SIGNAL("triggered()"),
                         self._qMeasure.deleteMeasure)
        else:
            pass
        if menu is not None:
            menu.exec_(event.screenPos())

    def mouseReleaseEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton and
            self._qScore.itemAt(event.scenePos()) == self):
            self.toggleNote()
        else:
            event.ignore()

    def hoverEnterEvent(self, dummyEvent):
        np = NotePosition(drumIndex = self._drumIndex,
                          noteTime = self._noteTime)
        self._qMeasure.highlightNote(np)

    def hoverLeaveEvent(self, dummyEvent):
        np = NotePosition(drumIndex = self._drumIndex,
                          noteTime = self._noteTime)
        self._qMeasure.highlightNote(np, False)
