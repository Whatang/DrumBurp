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
Created on 19 Jan 2011

@author: Mike Thomas

'''

from PyQt4.QtGui import QMenu

class QMenuIgnoreCancelClick(QMenu):
    '''
    classdocs
    '''


    def __init__(self, qScore, parent = None):
        '''
        Constructor
        '''
        super(QMenuIgnoreCancelClick, self).__init__(parent)
        self._qScore = qScore
        self.aboutToHide.connect(self._checkGoodSelection)

    def _checkGoodSelection(self):
        if self.activeAction() == None:
            self._qScore.ignoreNextClick()

