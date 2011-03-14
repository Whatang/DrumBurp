'''
Created on 12 Mar 2011

@author: Mike Thomas
'''

from ui_scorePropertiesDialog import Ui_ScoreDialog
from PyQt4.QtGui import QDialog

class QMetadataDialog(QDialog, Ui_ScoreDialog):
    def __init__(self, qscore, parent = None):
        super(QMetadataDialog, self).__init__(parent)
        self.setupUi(self)
        self._qscore = qscore
        self.titleEdit.setText(qscore.title)
        self.artistEdit.setText(qscore.artist)
        self.creatorEdit.setText(qscore.creator)
        self.bpmSpinBox.setValue(qscore.bpm)

    def getValues(self):
        return {"title" : self.titleEdit.text(),
                "artist" : self.artistEdit.text(),
                "creator": self.creatorEdit.text(),
                "bpm" : self.bpmSpinBox.value()}
