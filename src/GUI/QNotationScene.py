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

from PyQt4.QtGui import QGraphicsScene, QPixmap
import Data.DrumKit

PIXELS_PER_LINE = 8
LEFT = 10
TOP_LINE = 10
WIDTH = 100
NUM_LINES = 5
LINES_ABOVE = 2
LINES_BELOW = 1
EXTRA = 0
ZERO = 4
EXT_WIDTH = 10
STEM_LENGTH = 20

class QNotationScene(QGraphicsScene):
    '''
    classdocs
    '''


    def __init__(self, parent):
        super(QNotationScene, self).__init__(parent)
        self._headData = None
        self._heads = {}
        self._loadHeads()
        self._linesAbove = []
        self._linesBelow = []
        self._stem = self.addLine(0, 0, 0, STEM_LENGTH)
        for i in xrange(NUM_LINES):
            self.addLine(LEFT, TOP_LINE + i * PIXELS_PER_LINE,
                         LEFT + WIDTH, TOP_LINE + i * PIXELS_PER_LINE)
        for i in xrange(LINES_ABOVE):
            lineHeight = TOP_LINE - (i + 1) * PIXELS_PER_LINE
            line = self.addLine(LEFT + (WIDTH - EXT_WIDTH) / 2, lineHeight,
                                LEFT + (WIDTH + EXT_WIDTH) / 2, lineHeight)
            line.setVisible(False)
            self._linesAbove.append(line)
        for i in xrange(LINES_BELOW):
            lineHeight = TOP_LINE + (NUM_LINES + i) * PIXELS_PER_LINE
            line = self.addLine(LEFT + (WIDTH - EXT_WIDTH) / 2, lineHeight,
                                LEFT + (WIDTH + EXT_WIDTH) / 2, lineHeight)
            line.setVisible(False)
            self._linesBelow.append(line)
        self.setSceneRect(0,
                          TOP_LINE - LINES_ABOVE * PIXELS_PER_LINE,
                          2 * LEFT + WIDTH,
                          TOP_LINE
                          + (NUM_LINES + LINES_BELOW) * PIXELS_PER_LINE)
        self._head = self.addPixmap(self._heads["default"])
        self._head.setZValue(-1)

    def _loadHeads(self):
        defaultHead = QPixmap("GUI/defaultHead.png")
        defaultHead.setMask(defaultHead.createHeuristicMask())
        self._heads["default"] = defaultHead
        crossHead = QPixmap("GUI/crossHead.png")
        crossHead.setMask(crossHead.createHeuristicMask())
        self._heads["cross"] = crossHead
        diamondHead = QPixmap("GUI/diamondHead.png")
        diamondHead.setMask(diamondHead.createHeuristicMask())
        self._heads["diamond"] = diamondHead
        harmonicBlackHead = QPixmap("GUI/harmonicBlackHead.png")
        harmonicBlackHead.setMask(harmonicBlackHead.createHeuristicMask())
        self._heads["harmonic black"] = harmonicBlackHead
        harmonicHead = QPixmap("GUI/harmonicHead.png")
        harmonicHead.setMask(harmonicHead.createHeuristicMask())
        self._heads["harmonic"] = harmonicHead
        triangleHead = QPixmap("GUI/triangleHead.png")
        triangleHead.setMask(triangleHead.createHeuristicMask())
        self._heads["triangle"] = triangleHead
        xcircleHead = QPixmap("GUI/xcircleHead.png")
        xcircleHead.setMask(xcircleHead.createHeuristicMask())
        self._heads["xcircle"] = xcircleHead


    def setHeadData(self, headData):
        self._head.setPixmap(self._heads.get(headData.notationHead,
                                             self._heads["default"]))
        pixRect = self._head.boundingRect()
        pixWidth = pixRect.width()
        pixHeight = pixRect.height()
        left = LEFT + (WIDTH - pixWidth) / 2
        middle = (TOP_LINE
                  - (PIXELS_PER_LINE * (headData.notationLine - ZERO)
                     + pixHeight) / 2)
        self._head.setPos(left,
                          middle)
        offset = headData.notationLine - ZERO
        invisibleStart = 0
        if offset > 0:
            invisibleStart = offset / 2
            for i in xrange(invisibleStart):
                self._linesAbove[i].setVisible(True)
        for i in xrange(invisibleStart, LINES_ABOVE):
            self._linesAbove[i].setVisible(False)
        invisibleStart = 0
        if offset <= -2 * NUM_LINES:
            invisibleStart = (-offset) / 2 - NUM_LINES + 1
            for i in xrange(invisibleStart):
                self._linesBelow[i].setVisible(True)
        for i in xrange(invisibleStart, LINES_BELOW):
            self._linesBelow[i].setVisible(False)
        if headData.stemDirection == Data.DrumKit.DrumKit.DOWN:
            self._stem.setX(left)
            self._stem.setY(middle + pixHeight / 2)
        else:
            self._stem.setX(left + pixWidth - 1)
            self._stem.setY(middle - STEM_LENGTH + pixHeight / 2)
        # TODO: Draw effects

    def getCenter(self):
        return LEFT + WIDTH / 2, TOP_LINE + (ZERO * PIXELS_PER_LINE) / 2
