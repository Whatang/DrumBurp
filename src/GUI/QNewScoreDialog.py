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
Created on 9 Jan 2011

@author: Mike Thomas

'''

from ui_newScoreDialog import Ui_newScoreDialog
from PyQt4.QtGui import QDialog
import Data.MeasureCount
from QComplexCountDialog import QComplexCountDialog
class QNewScoreDialog(QDialog, Ui_newScoreDialog):
    '''
    classdocs
    '''
    def __init__(self, parent = None,
                 counter = None, registry = None):
        '''
        Constructor
        '''
        super(QNewScoreDialog, self).__init__(parent)
        self.setupUi(self)
        self.measureTabs.setup(counter, registry,
                               Data.MeasureCount, QComplexCountDialog)

    def getValues(self):
        mc = self.measureTabs.getCounter()
        return (self.numMeasuresSpinBox.value(), mc)
