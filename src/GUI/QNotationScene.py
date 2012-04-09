'''
Created on 8 Apr 2012

@author: Mike Thomas

'''

from PyQt4.QtGui import QGraphicsScene, QPixmap

PIXELS_PER_LINE = 8
BASE = 10
WIDTH = 50
EXTRA = 0


class QNotationScene(QGraphicsScene):
    '''
    classdocs
    '''


    def __init__(self, parent):
        super(QNotationScene, self).__init__(parent)
        self._headData = None
        self._heads = {}
        self._loadHeads()
        for i in xrange(5):
            self.addLine(BASE, BASE + (EXTRA + i) * PIXELS_PER_LINE, BASE + WIDTH, BASE + (EXTRA + i) * PIXELS_PER_LINE)
        self._zero = BASE + PIXELS_PER_LINE * (1 + EXTRA)
        self.setSceneRect(0, 0, 2 * BASE + WIDTH, 2 * BASE + 2 * EXTRA * PIXELS_PER_LINE)
        self._head = self.addPixmap(self._heads["default"])
        # TODO: Fix graphics positioning

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
        self._head.setPos(BASE + (WIDTH - self._head.boundingRect().width()) / 2,
                          self._zero - (PIXELS_PER_LINE * headData.notationLine - self._head.boundingRect().height()) / 2)
        # TODO: Draw stem
        # TODO: Draw effects

    def getCenter(self):
        return BASE + WIDTH / 2, self._zero
