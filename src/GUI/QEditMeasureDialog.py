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
Created on 20 Jan 2011

@author: Mike Thomas

'''

from PyQt4.QtGui import QDialog
from GUI.ui_measurePropertiesDialog import Ui_measurePropertiesDialog
from GUI.QComplexCountDialog import QComplexCountDialog
import Data.MeasureCount


class QEditMeasureDialog(QDialog, Ui_measurePropertiesDialog):
    def __init__(self, measureCount,
                 defaultCounter,
                 counterRegistry,
                 parent=None):
        super(QEditMeasureDialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.measureTabs.setup(measureCount,
                               counterRegistry,
                               Data.MeasureCount,
                               QComplexCountDialog)
        self._original = measureCount
        self._defaultCounter = defaultCounter
        reset = self.buttonBox.button(self.buttonBox.Reset)
        reset.clicked.connect(self.measureTabs.restoreOriginal)
        restore = self.buttonBox.button(self.buttonBox.RestoreDefaults)
        restore.clicked.connect(self.restoreDefaults)
        reset = self.buttonBox.button(self.buttonBox.Reset)
        reset.clicked.connect(self.resetCount)

    def getValues(self):
        return self.measureTabs.getCounter()

    def restoreDefaults(self):
        self.measureTabs.setBeat(self._defaultCounter)

    def resetCount(self):
        self.measureTabs.setBeat(self._original)
