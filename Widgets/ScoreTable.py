'''
Created on 2 Aug 2010

@author: Mike Thomas

'''
from PyQt4.QtGui import QTableView, QFontMetrics, QFont
from PyQt4 import QtCore

class ScoreTable(QTableView):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
        super(ScoreTable, self).__init__(parent)
        self.spaceFactor = 50
        self._buttonMethods = {QtCore.Qt.LeftButton : self._leftClick,
                               QtCore.Qt.MidButton : self._midClick,
                               QtCore.Qt.RightButton : self._rightClick}
        self._noteHead = None

    @QtCore.pyqtSlot(int)
    def spacingChanged(self, value):
        self.spaceFactor = value
        self.resizeTable()

    @QtCore.pyqtSlot()
    def resizeTable(self):
        fm = QFontMetrics(self.font())
        for rowNum in xrange(0, self.model().rowCount()):
            self.setRowHeight(rowNum, 1.25 * fm.height())
        spaceFactor = 1.25 + ((self.spaceFactor / 100.0) * 0.75)
        for colNum in xrange(0, self.model().columnCount()):
            self.setColumnWidth(colNum, spaceFactor * fm.width("X"))
        self.reset()
        self.updateGeometry()

    @QtCore.pyqtSlot(QtCore.QString)
    def setNoteHead(self, noteHead):
        noteHead = str(noteHead)
        if noteHead == "":
            self._noteHead = None
        else:
            self._noteHead = noteHead[0]

    def _leftClick(self, index):
        self.model().addNote(index, self._noteHead)

    def _rightClick(self, index):
        print index.row(), index.column()

    def _midClick(self, index):
        self.model().delNote(index)

    def mouseReleaseEvent(self, event):
        pos = event.pos()
        index = self.indexAt(pos)
        button = event.button()
        self._buttonMethods[button](index)
        event.accept()

