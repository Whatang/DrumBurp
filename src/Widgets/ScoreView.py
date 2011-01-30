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
        super(ScoreView, self).setScene(scene)
        self._props = scene.displayProperties
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
        self.scene().scoreWidth = width
        self.emit(QtCore.SIGNAL("widthChanged(int)"), width)
    widthChanged = QtCore.pyqtSignal(int)

    @QtCore.pyqtSlot(int)
    def setBPM(self, bpm):
        self.scene().bpm = bpm
        self.emit(QtCore.SIGNAL("bpmChanged(int)"), bpm)
    bpmChanged = QtCore.pyqtSignal(int)

    @QtCore.pyqtSlot(QtCore.QString)
    def setTitle(self, title):
        self.scene().title = title
        self.emit(QtCore.SIGNAL("titleChanged(QString)"), title)
    titleChanged = QtCore.pyqtSignal(QtCore.QString)

    @QtCore.pyqtSlot(QtCore.QString)
    def setArtist(self, artist):
        self.scene().artist = artist
        self.emit(QtCore.SIGNAL("artistChanged(QString)"), artist)
    artistChanged = QtCore.pyqtSignal(QtCore.QString)

    @QtCore.pyqtSlot(QtCore.QString)
    def setCreator(self, creator):
        self.scene().creator = creator
        self.emit(QtCore.SIGNAL("creatorChanged(QString)"), creator)
    creatorChanged = QtCore.pyqtSignal(QtCore.QString)

    @QtCore.pyqtSlot(QtGui.QFont)
    def setFont(self, font):
        self._props.noteFont = font
        self.scene().update()

    @QtCore.pyqtSlot(int)
    def setDefaultMeasureWidth(self, width):
        self._props.beatsPerMeasure = width

    def startUp(self):
        self.scene().startUp()

    def keyPressEvent(self, event):
        if isinstance(self.scene().focusItem(), QtGui.QGraphicsTextItem):
            event.ignore()
            return super(ScoreView, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Home:
            self.centerOn(0, 0)
        elif event.key() == QtCore.Qt.Key_End:
            self.centerOn(0, self.sceneRect().height())
        else:
            event.ignore()
            return super(ScoreView, self).keyPressEvent(event)
