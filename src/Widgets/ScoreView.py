# Copyright 2011 Michael Thomas
#
# See www.whatang.org for more information.
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DrumBurp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DrumBurp.  If not, see <http://www.gnu.org/licenses/>
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
        self._props = None

    def setScene(self, scene):
        super(ScoreView, self).setScene(scene)
        self._props = scene.displayProperties
        self.centerOn(0, 0)

    @QtCore.pyqtSlot(int)
    def systemSpacingChanged(self, value):
        self.scene().systemSpacing = value

    @QtCore.pyqtSlot(int)
    def setWidth(self, width):
        self.scene().scoreWidth = width
        self.widthChanged.emit(width)
    widthChanged = QtCore.pyqtSignal(int)

    @QtCore.pyqtSlot(QtGui.QFont)
    def setFont(self, font):
        self._props.noteFont = font
        self.setNoteFontSize(self._props.noteFont.pointSize())

    @QtCore.pyqtSlot(int)
    def setNoteFontSize(self, size):
        self.scene().setNoteFontSize(size)

    @QtCore.pyqtSlot(QtGui.QFont)
    def setSectionFont(self, font):
        self._props.sectionFont = font

    @QtCore.pyqtSlot(int)
    def setSectionFontSize(self, size):
        self.scene().setSectionFontSize(size)

    @QtCore.pyqtSlot(QtGui.QFont)
    def setMetadataFont(self, font):
        self._props.metadataFont = font

    @QtCore.pyqtSlot(int)
    def setMetadataFontSize(self, size):
        self.scene().setMetadataFontSize(size)

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

    @QtCore.pyqtSlot(int)
    def showSection(self, sectionIndex):
        section = self.scene().getQSection(sectionIndex)
        self.centerOn(section)

