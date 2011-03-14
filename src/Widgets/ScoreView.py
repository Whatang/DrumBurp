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
        scene.metadataChanged.connect(self.setMetadata)
        self.centerOn(0, 0)

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
        self.widthChanged.emit(width)
    widthChanged = QtCore.pyqtSignal(int)

    @QtCore.pyqtSlot(int)
    def setBPM(self, bpm):
        self.scene().bpm = bpm
        self.bpmChanged.emit(bpm)
    bpmChanged = QtCore.pyqtSignal(int)

    @QtCore.pyqtSlot(QtCore.QString)
    def setTitle(self, title):
        self.scene().title = title
        self.titleChanged.emit(title)
    titleChanged = QtCore.pyqtSignal(QtCore.QString)

    @QtCore.pyqtSlot(QtCore.QString)
    def setArtist(self, artist):
        self.scene().artist = artist
        self.artistChanged.emit(artist)
    artistChanged = QtCore.pyqtSignal(QtCore.QString)

    @QtCore.pyqtSlot(QtCore.QString)
    def setCreator(self, creator):
        self.scene().creator = creator
        self.creatorChanged.emit(creator)
    creatorChanged = QtCore.pyqtSignal(QtCore.QString)

    def setMetadata(self, name, value):
        signal = getattr(self, str(name) + "Changed")
        signal.emit(value)

    @QtCore.pyqtSlot(QtGui.QFont)
    def setFont(self, font):
        self._props.noteFont = font

    @QtCore.pyqtSlot(int)
    def setNoteFontSize(self, size):
        self._props.noteFont.setPointSize(size)
        fm = QtGui.QFontMetrics(self._props.noteFont)
        br = fm.tightBoundingRect("X")
        self._props.xSpacing = 1.2 * fm.width("X") + 2
        self._props.ySpacing = br.height() + 2

    @QtCore.pyqtSlot(QtGui.QFont)
    def setSectionFont(self, font):
        self._props.sectionFont = font

    @QtCore.pyqtSlot(int)
    def setSectionFontSize(self, size):
        self._props.sectionFontSize = size

    @QtCore.pyqtSlot(QtGui.QFont)
    def setMetadataFont(self, font):
        self._props.metadataFont = font

    @QtCore.pyqtSlot(int)
    def setMetadataFontSize(self, size):
        self._props.metadataFontSize = size

    @QtCore.pyqtSlot(int)
    def setDefaultMeasureWidth(self, width):
        self._props.beatsPerMeasure = width


    @QtCore.pyqtSlot(bool)
    def setMetadataVisible(self, onOff):
        self._props.metadataVisible = onOff

    @QtCore.pyqtSlot(bool)
    def setBeatCountVisible(self, onOff):
        self._props.beatCountVisible = onOff

    @QtCore.pyqtSlot(bool)
    def setEmptyLinesVisible(self, onOff):
        self._props.emptyLinesVisible = onOff

    @QtCore.pyqtSlot(bool)
    def setKitDataVisible(self, onOff):
        self._props.kitDataVisible = onOff

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
