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
Created on Jan 30, 2011

@author: Mike
'''

from PyQt4.QtGui import QDialog
from GUI.ui_repeatCountDialog import Ui_repeatCountDialog

class QRepeatCountDialog(QDialog, Ui_repeatCountDialog):
    '''
    classdocs
    '''


    def __init__(self, repeatCount, parent = None):
        '''
        Constructor
        '''
        super(QRepeatCountDialog, self).__init__(parent = parent)
        self._repeatCount = repeatCount
        self.setupUi(self)
        self.countBox.setValue(repeatCount)

    def getValue(self):
        return self.countBox.value()
