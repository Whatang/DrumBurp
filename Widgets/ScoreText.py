'''
Created on 3 Nov 2010

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore

class ScoreText(QtGui.QTextEdit):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(ScoreText, self).__init__(parent)
        self.model = None
        self._buttonMethods = {QtCore.Qt.LeftButton : self._leftClick,
                               QtCore.Qt.MidButton : self._midClick,
                               QtCore.Qt.RightButton : self._rightClick}
        self._noteHead = None
        self._fixedWidth = True
        self._desiredWidth = 80
        self._holdingForMenu = False
        cursor = self.textCursor()
        cursor.insertText("hi")

    @QtCore.pyqtSlot(int)
    def setWidth(self, width):
        self.model.width = width
        self._desiredWidth = width

    @QtCore.pyqtSlot(QtCore.QString)
    def setNoteHead(self, noteHead):
        noteHead = str(noteHead)
        if noteHead == "":
            self._noteHead = None
        elif isinstance(noteHead, basestring):
            self._noteHead = noteHead[0]
        else:
            self._noteHead = noteHead

    def _leftClick(self, index):
        print index
        print dir(index)
#        self.model.toggleNote(index, self._noteHead)

    def _rightClick(self, index):
        pass

    def _midClick(self, index):
        pass

    def mouseReleaseEvent(self, event):
        print event.pos()
        index = self.cursorForPosition(event.pos())
        button = event.button()
        self._buttonMethods[button](index)
        super(ScoreText, self).mouseReleaseEvent(event)
