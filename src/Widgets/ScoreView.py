# Copyright 2011-12 Michael Thomas
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

class SmoothScroller(object):
    NUM_STEPS = 100

    def __init__(self, view):
        self.view = view
        self._timeline = None
        self._xStart = None
        self._xEnd = None
        self._yStart = None
        self._yEnd = None
        self._mutex = QtCore.QMutex()

    def scrollTo(self, xEnd, yEnd, timeInMs = 250):
        if not timeInMs:
            self.view.horizontalScrollBar().setValue(xEnd)
            self.view.verticalScrollBar().setValue(yEnd)
            return
        self._xStart = self.view.horizontalScrollBar().value()
        self._yStart = self.view.verticalScrollBar().value()
        self._xEnd = xEnd
        self._yEnd = yEnd
        self._timeline = QtCore.QTimeLine(duration = timeInMs)
        self._timeline.setFrameRange(0, self.NUM_STEPS)
        self._timeline.frameChanged.connect(self._frame)
        self._timeline.finished.connect(self._finished)
        self._timeline.start()

    def _frame(self, frameNum):
        deltaX = ((self._xEnd - self._xStart) * frameNum) / self.NUM_STEPS
        deltaY = ((self._yEnd - self._yStart) * frameNum) / self.NUM_STEPS
        self.view.horizontalScrollBar().setValue(self._xStart + deltaX)
        self.view.verticalScrollBar().setValue(self._yStart + deltaY)

    def _finished(self):
        del self._timeline
        self._timeline = None

class ScoreView(QtGui.QGraphicsView):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
        super(ScoreView, self).__init__(parent)
        self._props = None
        self._scroller = SmoothScroller(self)

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

    @QtCore.pyqtSlot(int)
    def setLilypondSize(self, size):
        self.scene().setLilypondSize(size)

    @QtCore.pyqtSlot(int)
    def setLilypondPages(self, numPages):
        self.scene().setLilypondPages(numPages)

    @QtCore.pyqtSlot(bool)
    def setLilyFill(self, lilyFill):
        self.scene().setLilyFill(lilyFill)

    @QtCore.pyqtSlot(QtGui.QFont)
    def setFont(self, font):
        self.scene().setScoreFont(font, "note")

    @QtCore.pyqtSlot(int)
    def setNoteFontSize(self, size):
        self.scene().setScoreFontSize(size, "note")

    @QtCore.pyqtSlot(QtGui.QFont)
    def setSectionFont(self, font):
        self.scene().setScoreFont(font, "section")

    @QtCore.pyqtSlot(int)
    def setSectionFontSize(self, size):
        self.scene().setScoreFontSize(size, "section")

    @QtCore.pyqtSlot(QtGui.QFont)
    def setMetadataFont(self, font):
        self.scene().setScoreFont(font, "metadata")

    @QtCore.pyqtSlot(int)
    def setMetadataFontSize(self, size):
        self.scene().setScoreFontSize(size, "metadata")

    @QtCore.pyqtSlot(bool)
    def setMetadataVisible(self, onOff):
        self.scene().setElementVisibility(onOff, "metadata",
                                          "score info")

    @QtCore.pyqtSlot(bool)
    def setBeatCountVisible(self, onOff):
        self.scene().setElementVisibility(onOff, "beatCount",
                                          "beat count")

    @QtCore.pyqtSlot(bool)
    def setEmptyLinesVisible(self, onOff):
        self.scene().setElementVisibility(onOff, "emptyLines",
                                          "empty lines")

    @QtCore.pyqtSlot(bool)
    def setKitDataVisible(self, onOff):
        self.scene().setElementVisibility(onOff, "kitData",
                                          "drum key")

    @QtCore.pyqtSlot(bool)
    def setMeasureCountsVisible(self, onOff):
        self.scene().setElementVisibility(onOff, "measureCounts",
                                          "measure counts")

    def startUp(self):
        self.scene().startUp()

    def keyPressEvent(self, event):
        if isinstance(self.scene().focusItem(), QtGui.QGraphicsTextItem):
            event.ignore()
            return super(ScoreView, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Home:
            self.setTopLeft(0, 0)
        elif event.key() == QtCore.Qt.Key_End:
            self.setTopLeft(0, self.sceneRect().height())
        else:
            event.ignore()
            return super(ScoreView, self).keyPressEvent(event)

    @QtCore.pyqtSlot(int)
    def showSection(self, sectionIndex):
        section = self.scene().getQSection(sectionIndex)
        self.showItemAtTop(section)

    def setTopLeft(self, left, top, timeInMs = 250):
        self._scroller.scrollTo(left, top, timeInMs)

    @QtCore.pyqtSlot(QtGui.QGraphicsItem)
    def showItemAtTop(self, item, timeInMs = 250, margins = 20):
        itemRect = item.sceneBoundingRect()
        left = max(0, itemRect.right() + margins - self.viewport().width())
        top = max(0, itemRect.top() - margins)
        self.setTopLeft(left, top, timeInMs)

    @QtCore.pyqtSlot(QtGui.QGraphicsItem, QtGui.QGraphicsItem)
    def showTwoItems(self, primary, secondary, timeInMs = 250, margins = 20):
        primRect = primary.sceneBoundingRect()
        secRect = secondary.sceneBoundingRect()
        top = min(primRect.top(), secRect.top())
        bottom = max(primRect.bottom(), secRect.bottom())
        left = min(primRect.left(), secRect.left())
        right = max(primRect.right(), secRect.right())
        vwidth = self.viewport().width()
        vheight = self.viewport().height()
        if (right - left - 2 * margins) > vwidth or (top - bottom - 2 * margins) > vheight:
            if (right - left) > vwidth or (top - bottom) > vheight:
                self.showItemAtTop(primary, timeInMs, margins)
            else:
                vleft = max(0, right - vwidth)
                vtop = max(0, top)
                self.setTopLeft(vleft, vtop, timeInMs)
        else:
            vleft = max(0, right + margins - vwidth)
            vtop = max(0, top - margins)
            self.setTopLeft(vleft, vtop, timeInMs)
