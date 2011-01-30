'''
Created on 26 Jan 2011

@author: Mike Thomas

'''

from PyQt4.QtGui import QGraphicsTextItem, QTextCursor
from PyQt4.QtCore import Qt

class QSection(QGraphicsTextItem):
    '''
    classdocs
    '''


    def __init__(self, title, qScore = None, parent = None):
        '''
        Constructor
        '''
        super(QSection, self).__init__(parent = parent, scene = qScore)
        font = self.font()
        font.setPixelSize(30)
        font.setBold(True)
        self.setFont(font)
        self.setTextInteractionFlags(Qt.TextEditable | Qt.TextSelectableByMouse)
        self._title = title
        self.setPlainText(title)
        self._index = None
        self.setCursor(Qt.PointingHandCursor)

    def setIndex(self, index):
        self._index = index

    _keyMoves = {Qt.Key_Left:QTextCursor.Left,
                 Qt.Key_Right:QTextCursor.Right,
                 Qt.Key_Home:QTextCursor.Start,
                 Qt.Key_End:QTextCursor.End,
                 Qt.Key_Up:QTextCursor.NoMove,
                 Qt.Key_Down:QTextCursor.NoMove}
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            event.ignore()
            self.clearFocus()
        elif event.key() == Qt.Key_Escape:
            event.ignore()
            self.setPlainText(self._title)
            self.clearFocus()
        elif event.key() in self._keyMoves:
            cursor = self.textCursor()
            cursor.movePosition(self._keyMoves[event.key()])
            self.setTextCursor(cursor)
        else:
            super(QSection, self).keyPressEvent(event)

    def focusOutEvent(self, event):
        text = unicode(self.document().toPlainText())
        if text != self._title:
            self._title = text
            self.scene().score.setSectionTitle(self._index, text)
            self.scene().dirty = True
        super(QSection, self).focusOutEvent(event)
