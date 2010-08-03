'''
Created on 2 Aug 2010

@author: Mike Thomas

'''
from PyQt4.QtGui import QTableView, QFontMetrics
from PyQt4 import QtCore

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
        self._width = 80

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
        self._width = width

    @QtCore.pyqtSlot(bool)
    def setFixedWidth(self, value):
        self._fixedWidth = value
        if self._fixedWidth:
            self.model().width = self._width
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

    def mouseReleaseEvent(self, event):
        pos = event.pos()
        index = self.indexAt(pos)
        button = event.button()
        self._buttonMethods[button](index)
        super(ScoreTable, self).mouseReleaseEvent(event)
