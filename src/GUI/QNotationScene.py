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
from Data.DefaultKits import STEM_DOWN, STEM_UP

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
STEM_LENGTH = 30
STEM_WIDTH = 1
EFFECTS_Z = -15
HEAD_Z = -10


class QNotationScene(QGraphicsScene):
    _heads = {}
    _effects = {}
    _flams = {}
    _drag = None
    _not_above_stem = set(["ghost"])

    def __init__(self, parent):
        super(QNotationScene, self).__init__(parent)
        self._headData = None
        self._loadHeads()
        self._linesAbove = []
        self._linesBelow = []
        self._stem = self.addRect(0, 0, STEM_WIDTH, STEM_LENGTH)

        for i in range(NUM_LINES):
            self.addLine(LEFT, TOP_LINE + i * PIXELS_PER_LINE,
                         LEFT + WIDTH, TOP_LINE + i * PIXELS_PER_LINE)
        for i in range(LINES_ABOVE):
            lineHeight = TOP_LINE - (i + 1) * PIXELS_PER_LINE
            line = self.addLine(LEFT + (WIDTH - EXT_WIDTH) / 2, lineHeight,
                                LEFT + (WIDTH + EXT_WIDTH) / 2, lineHeight)
            line.setVisible(False)
            self._linesAbove.append(line)
        for i in range(LINES_BELOW):
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
        self._head.setZValue(HEAD_Z)
        self._flamImage = self.addPixmap(self._flams[STEM_UP]["default"])
        self._flamImage.setZValue(EFFECTS_Z)
        self._flamImage.setVisible(False)
        self._effectImage = self.addPixmap(self._effects["ghost"])
        self._effectImage.setZValue(EFFECTS_Z)
        self._effectImage.setVisible(False)
        self._dragImage = self.addPixmap(self._drag)
        self._dragImage.setZValue(EFFECTS_Z)
        self._dragImage.setVisible(False)

    @classmethod
    def _loadNoteHead(cls, headname):
        imageName = headname.title()
        imageName = headname[0] + imageName[1:]
        imageName = imageName.replace(" ", "")
        image = QPixmap(":/heads/GUI/Notation/%sHead.png" % imageName)
        image.setMask(image.createHeuristicMask())
        cls._heads[headname] = image

    @classmethod
    def _loadEffect(cls, effectname):
        imageName = effectname.capitalize()
        image = QPixmap(":/heads/GUI/Notation/Effect_%s.png" % imageName)
        image.setMask(image.createHeuristicMask())
        cls._effects[effectname] = image

    @classmethod
    def _loadFlam(cls, headname):
        if STEM_UP not in cls._flams:
            cls._flams[STEM_UP] = {}
        if STEM_DOWN not in cls._flams:
            cls._flams[STEM_DOWN] = {}
        imageName = headname.capitalize()
        imageName = imageName.replace(" ", "")
        image = QPixmap(":/heads/GUI/Notation/Flam_Up_%s.png" % imageName)
        image.setMask(image.createHeuristicMask())
        cls._flams[STEM_UP][headname] = image
        image = QPixmap(":/heads/GUI/Notation/Flam_Down_%s.png" % imageName)
        image.setMask(image.createHeuristicMask())
        cls._flams[STEM_DOWN][headname] = image

    @classmethod
    def _loadHeads(cls):
        if cls._heads:
            return
        for headname in ("default", "cross", "diamond", "harmonic black",
                         "harmonic", "triangle", "xcircle"):
            cls._loadNoteHead(headname)
            cls._loadFlam(headname)
        for effectname in ("ghost", "accent", "stopped", "open", "choke"):
            cls._loadEffect(effectname)
        cls._drag = QPixmap(":/heads/GUI/Notation/Effect_Drag.png")

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
            for i in range(invisibleStart):
                self._linesAbove[i].setVisible(True)
        for i in range(invisibleStart, LINES_ABOVE):
            self._linesAbove[i].setVisible(False)
        invisibleStart = 0
        if offset <= -2 * NUM_LINES:
            invisibleStart = (-offset) / 2 - NUM_LINES + 1
            for i in range(invisibleStart):
                self._linesBelow[i].setVisible(True)
        for i in range(invisibleStart, LINES_BELOW):
            self._linesBelow[i].setVisible(False)
        if headData.stemDirection == STEM_DOWN:
            stemLeft = left
            self._stem.setY(middle + pixHeight / 2)
        else:
            stemLeft = left + pixWidth - 1
            self._stem.setY(middle - STEM_LENGTH + pixHeight / 2)
        self._stem.setX(stemLeft)
        # Draw effects
        if headData.notationEffect == "flam":
            self._effectImage.setVisible(False)
            self._dragImage.setVisible(False)
            # Draw flams
            flamHeads = self._flams[headData.stemDirection]
            image = flamHeads.get(headData.notationHead,
                                  self._heads["default"])
            self._flamImage.setPixmap(image)
            flamRect = self._flamImage.boundingRect()
            self._flamImage.setX(left - flamRect.width() - 2)
            self._flamImage.setY(middle)
            if headData.stemDirection == STEM_UP:
                self._flamImage.moveBy(0, -(flamRect.height() - pixHeight))
            self._flamImage.setVisible(True)
        elif headData.notationEffect in self._effects:
            self._flamImage.setVisible(False)
            self._dragImage.setVisible(False)
            # Draw effects
            self._effectImage.setPixmap(self._effects[headData.notationEffect])
            effectRect = self._effectImage.boundingRect()
            effectWidth = effectRect.width()
            effectHeight = effectRect.height()
            self._effectImage.setX(LEFT + (WIDTH - effectWidth) / 2)
            if headData.notationEffect in self._not_above_stem:
                self._effectImage.setY(middle - (effectHeight - pixHeight) / 2)
            elif headData.stemDirection == STEM_UP:
                self._effectImage.setY(middle - STEM_LENGTH - effectHeight - 2)
            else:
                self._effectImage.setY(
                    middle + STEM_LENGTH + pixHeight / 2 + 2)
            self._effectImage.setVisible(True)
        elif headData.notationEffect == "drag":
            self._flamImage.setVisible(False)
            self._effectImage.setVisible(False)
            dragRect = self._dragImage.boundingRect()
            self._dragImage.setX(stemLeft - dragRect.width() / 2)
            if headData.stemDirection == STEM_UP:
                self._dragImage.setY(self._stem.y() + 10
                                     - dragRect.height() / 2)
            else:
                self._dragImage.setY(self._stem.y() + STEM_LENGTH - 10
                                     - dragRect.height() / 2)
            self._dragImage.setVisible(True)
        else:
            self._dragImage.setVisible(False)
            self._flamImage.setVisible(False)
            self._effectImage.setVisible(False)

    @staticmethod
    def getCenter():
        return LEFT + WIDTH / 2, TOP_LINE + (ZERO * PIXELS_PER_LINE) / 2
