# Copyright 2016 Michael Thomas
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
Created on Feb 25, 2012

@author: Mike
'''

from GUI.ui_alternateRepeatWidget import Ui_AlternateWidget
from PyQt4.QtGui import QWidget


class QAlternateWidget(QWidget, Ui_AlternateWidget):
    def __init__(self, startVal, endVal, isRange, parent=None):
        super(QAlternateWidget, self).__init__(parent)
        self.setupUi(self)
        self.startBox.setValue(startVal)
        self.endBox.setValue(endVal)
        self.rangeCheck.setChecked(isRange)

    def getString(self):
        if self.rangeCheck.isChecked():
            return "%d-%d" % (self.startBox.value(), self.endBox.value())
        else:
            return "%d" % (self.startBox.value())

    def highValue(self):
        if self.rangeCheck.isChecked():
            return self.startBox.value()
        else:
            return max(self.startBox.value(), self.endBox.value())
