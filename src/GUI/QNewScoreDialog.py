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
Created on 9 Jan 2011

@author: Mike Thomas

'''

from ui_newScoreDialog import Ui_newScoreDialog
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QSettings, QVariant
from cStringIO import StringIO
import Data.MeasureCount
from QComplexCountDialog import QComplexCountDialog
from Data import DefaultKits, DrumKit, fileUtils

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
        for name in DefaultKits.DEFAULT_KIT_NAMES:
            self.kitCombobox.addItem(name, userData = QVariant(False))
        self._settings = QSettings()
        self._settings.beginGroup("UserDefaultKits")
        for kitName in self._settings.allKeys():
            self.kitCombobox.addItem(kitName, userData = QVariant(True))

    def getValues(self):
        mc = self.measureTabs.getCounter()
        kitName = unicode(self.kitCombobox.currentText())
        kitIndex = self.kitCombobox.currentIndex()
        isUserKit = self.kitCombobox.itemData(kitIndex).toBool()
        if isUserKit:
            kitString = str(self._settings.value(kitName).toString())
            handle = StringIO(kitString)
            dbfile = fileUtils.dbFileIterator(handle)
            kit = DrumKit.DrumKit()
            kit.read(dbfile)
        else:
            kit = DrumKit.getNamedDefaultKit(kitName)
        return (self.numMeasuresSpinBox.value(), mc, kit)
