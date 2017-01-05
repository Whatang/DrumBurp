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
Created on 12 Mar 2011

@author: Mike Thomas
'''

from GUI.ui_scorePropertiesDialog import Ui_ScoreDialog
from PyQt4.QtGui import QDialog

class QMetadataDialog(QDialog, Ui_ScoreDialog):
    _SWING_TO_INDEXES = {0:0, 8:1, 16:2, 32:3}
    _INDEXES_TO_SWING = {0:0, 1:8, 2:16, 3:32}
    def __init__(self, qscore, parent = None):
        super(QMetadataDialog, self).__init__(parent)
        self.setupUi(self)
        self._qscore = qscore
        self.titleEdit.setText(qscore.title)
        self.artistEdit.setText(qscore.artist)
        self.artistVisible.setChecked(qscore.artistVisible)
        self.creatorEdit.setText(qscore.creator)
        self.creatorVisible.setChecked(qscore.creatorVisible)
        self.bpmSpinBox.setValue(qscore.bpm)
        self.bpmVisible.setChecked(qscore.bpmVisible)
        index = self._SWING_TO_INDEXES.get(qscore.swing, 0)
        self.swingComboBox.setCurrentIndex(index)

    def getValues(self):
        return {"title" : self.titleEdit.text(),
                "artist" : self.artistEdit.text(),
                "artistVisible" : self.artistVisible.isChecked(),
                "creator": self.creatorEdit.text(),
                "creatorVisible": self.creatorVisible.isChecked(),
                "bpm" : self.bpmSpinBox.value(),
                "bpmVisible":self.bpmVisible.isChecked(),
                "swing":self._INDEXES_TO_SWING[self.swingComboBox.currentIndex()]}
