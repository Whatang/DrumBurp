'''
Created on 5 Dec 2010

@author: Mike Thomas

'''
from PyQt4 import QtGui, QtCore


class ScoreView(QtGui.QGraphicsView):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
        super(ScoreView, self).__init__(parent)
        self._fixedWidth = 80
        self._props = None

    def setScene(self, scene):
#        self.connect(self, QtCore.SIGNAL("itemClicked"), scene.itemClicked)
        super(ScoreView, self).setScene(scene)
        self._props = scene.getProperties()
        self.centerOn(0, 0)

    @QtCore.pyqtSlot(int)
    def horizontalSpacingChanged(self, value):
        self._props.xSpacing = value - 101

    @QtCore.pyqtSlot(int)
    def verticalSpacingChanged(self, value):
        self._props.ySpacing = value - 101

    @QtCore.pyqtSlot(int)
    def systemSpacingChanged(self, value):
        self._props.lineSpacing = value - 101

    @QtCore.pyqtSlot(QtCore.QString)
    def setNoteHead(self, noteHead):
        noteHead = str(noteHead)
        if noteHead == "":
            noteHead = None
        else:
            noteHead = noteHead[0]
        self._props.head = noteHead

    @QtCore.pyqtSlot(int)
    def setWidth(self, width):
        pass

    @QtCore.pyqtSlot(bool)
    def setFixedWidth(self, value):
        self._fixedWidth = value
        if self._fixedWidth:
            pass
        else:
            self._setVariableWidth()

    @QtCore.pyqtSlot(QtGui.QFont)
    def setFont(self, font):
        self.scene().getProperties().noteFont = font
        self.scene().update()

    def _setVariableWidth(self):
#        self.setWidth(int(max(10, (self.width() / self._colWidths) - 1)))
        pass
