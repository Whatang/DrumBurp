'''
Created on 5 Dec 2010

@author: Mike Thomas

'''
from PyQt4 import QtCore
from QMenuIgnoreCancelClick import QMenuIgnoreCancelClick
from QDBGridItem import QDBGridItem
from QRepeatDialog import QRepeatDialog
from Data import DBConstants
from Data.NotePosition import NotePosition
import DBIcons
import copy

class QNote(QDBGridItem):
    '''
    classdocs
    '''
    def __init__(self, qScore, parent):
        super(QNote, self).__init__(qScore, parent)
        self._qMeasure = parent
        self._notePosition = NotePosition()
        self._text = DBConstants.EMPTY_NOTE
        self.setAcceptsHoverEvents(True)

    def _getNotePosition(self):
        np = copy.copy(self._notePosition)
        return self._qMeasure.augmentNotePosition(np)

    def _score(self):
        return self.scene().score

    def toggleNote(self, head = None):
        if head is None:
            head = self._props.head
        self._score().toggleNote(self._getNotePosition(), head)


    def repeatNote(self):
        np = self._getNotePosition()
        head = self._text
        repeatDialog = QRepeatDialog(self.scene().parent())
        if repeatDialog.exec_():
            nRepeats, repInterval = repeatDialog.getValues()
            for dummyIndex in range(nRepeats):
                np = self._score().notePlus(np, repInterval)
                if np is None:
                    break
                self._score().addNote(np, head)

    def setIndex(self, drumIndex, noteTime):
        self._notePosition.noteTime = noteTime
        self._notePosition.drumIndex = drumIndex

    def cellWidth(self):
        return self._props.xSpacing

    def cellHeight(self):
        return self._props.ySpacing

    def mousePressEvent(self, event):
        menu = None
        if event.button() == QtCore.Qt.MiddleButton:
            event.ignore()
            menu = QMenuIgnoreCancelClick(self.scene())
            for noteHead in self._props.allowedNoteHeads():
                action = menu.addAction(noteHead)
                def noteAction(nh = noteHead):
                    self.toggleNote(nh)
                menu.connect(action, QtCore.SIGNAL("triggered()"), noteAction)
        elif event.button() == QtCore.Qt.RightButton:
            event.ignore()
            menu = QMenuIgnoreCancelClick(self.scene())
            actionText = "Repeat note"
            repeatNoteAction = menu.addAction(DBIcons.getIcon("repeat"),
                                              actionText)
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
            if self.scene().measureClipboard is None:
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
            deleteMenu = menu.addMenu("Delete...")
            deleteEmptyAction = deleteMenu.addAction("Empty Trailing Measures")
            menu.connect(deleteEmptyAction, QtCore.SIGNAL("triggered()"),
                         self._qMeasure.deleteEmptyMeasures)
        else:
            pass
        if menu is not None:
            menu.exec_(event.screenPos())

    def mouseReleaseEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton and
            self.scene().itemAt(event.scenePos()) == self):
            self.toggleNote()
        else:
            event.ignore()

    def hoverEnterEvent(self, dummyEvent):
        self.scene().highlightNote(self._getNotePosition())

    def hoverLeaveEvent(self, dummyEvent):
        self.scene().highlightNote(self._getNotePosition(), False)
