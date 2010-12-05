'''
Created on 2 Aug 2010

@author: Mike Thomas

'''
from PyQt4.QtGui import QTableView, QFontMetrics
from PyQt4 import QtCore, QtGui

#pylint: disable-msg=R0902
class ScoreTable(QTableView):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
        super(ScoreTable, self).__init__(parent)
        self.spaceFactor = 50
        self._colWidths = 0
        self._rowHeight = 0
        self._buttonMethods = {QtCore.Qt.LeftButton : self._leftClick,
                               QtCore.Qt.MidButton : self._midClick,
                               QtCore.Qt.RightButton : self._rightClick}
        self._noteHead = None
        self._fixedWidth = True
        self._desiredWidth = 80
        self._menuIsUp = False
        self._holdingForMenu = False

    def setColumnSizes(self):
        fm = QFontMetrics(self.font())
        spaceFactor = 1.25 + ((self.spaceFactor / 100.0) * 0.75)
        self._colWidths = spaceFactor * fm.width("X")
        self._rowHeight = 1.25 * fm.height()

    @QtCore.pyqtSlot(int)
    def spacingChanged(self, value):
        self.spaceFactor = value
        self.setColumnSizes()
        self.resizeTable()

    @QtCore.pyqtSlot()
    def resizeTable(self):
        for rowNum in xrange(0, self.model().rowCount()):
            self.setRowHeight(rowNum, self._rowHeight)
        for colNum in xrange(0, self.model().columnCount()):
            self.setColumnWidth(colNum, self._colWidths)
        self.reset()
        self.updateGeometry()

    @QtCore.pyqtSlot(QtCore.QString)
    def setNoteHead(self, noteHead):
        noteHead = str(noteHead)
        if noteHead == "":
            self._noteHead = None
        else:
            self._noteHead = noteHead[0]

    @QtCore.pyqtSlot(int)
    def setWidth(self, width):
        self.model().width = width
        self._desiredWidth = width

    @QtCore.pyqtSlot(bool)
    def setFixedWidth(self, value):
        self._fixedWidth = value
        if self._fixedWidth:
            self.model().width = self._desiredWidth
        else:
            self._setVariableWidth()

    def _setVariableWidth(self):
        self.model().width = int(max(10, (self.width() / self._colWidths) - 1))

    def resizeEvent(self, event):
        if not self._fixedWidth:
            self._setVariableWidth()
        super(ScoreTable, self).resizeEvent(event)

    def _leftClick(self, index):
        self.model().toggleNote(index, self._noteHead)

    def _rightClick(self, index):
        pass

    def _midClick(self, index):
        pass

    def mousePressEvent(self, event):
        self._startIndex = self.indexAt(event.pos())
        self._holdingForMenu = True
        QtCore.QTimer.singleShot(750, self.showContextMenu)
        super(ScoreTable, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        index = self.indexAt(event.pos())
        if index == self._startIndex:
            self.clearSelection()
            if self._holdingForMenu:
                button = event.button()
                self._buttonMethods[button](index)
        self._holdingForMenu = False
        super(ScoreTable, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        print "Mouse move"
        pos = event.pos()
        index = self.indexAt(pos)
        if self._holdingForMenu and index != self._startIndex:
            self._holdingForMenu = False
        else:
            print index.row(), index.column()
            super(ScoreTable, self).mouseMoveEvent(event)

    def showContextMenu(self):
        if self._holdingForMenu:
            qm = QtGui.QMenu()
            qm.addAction("Hi")
            self._menuIsUp = True
            qm.exec_(QtGui.QCursor.pos())
            self._menuIsUp = False
            self._holdingForMenu = False
