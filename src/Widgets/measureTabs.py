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
Created on 17 Apr 2011

@author: Mike Thomas

'''
import copy
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignal
from ui_measureTabs import Ui_measureTabs

class measureTabs(QWidget, Ui_measureTabs):
    '''
    classdocs
    '''


    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(measureTabs, self).__init__(parent)
        self.setupUi(self)
        self._measureCount = None
        self._defaultBeats = None
        self._defaultCounter = None
        self._registry = None
        self._mcMaker = None
        self._currentCount = None
        self._complexDialog = None

    beatChanged = pyqtSignal()

    @property
    def simpleSelected(self):
        return self.counterTabs.currentWidget() == self.simpleTab

    def setup(self, measureCount,
              counterRegistry, mcMaker,
              complexDialog):
        self._measureCount = measureCount
        self._registry = counterRegistry
        self._currentCount = copy.copy(measureCount)
        self._mcMaker = mcMaker
        self._complexDialog = complexDialog
        self.beatCountComboBox.currentIndexChanged.connect(self.preview)
        self.beatsSpinBox.valueChanged.connect(self.preview)
        self._populateCombo(self.beatCountComboBox)
        self.complexEditButton.clicked.connect(self._editComplex)
        self.counterTabs.currentChanged.connect(self.preview)
        self.restoreOriginal()

    def restoreOriginal(self):
        self.setBeat(self._measureCount)

    def _populateCombo(self, combo):
        combo.clear()
        for (name, unusedCounter) in self._registry:
            combo.addItem(name)

    def _setCombo(self, combo, beatCount):
        setCounter = False
        for index, (unusedName, counter) in enumerate(self._registry):
            if str(beatCount) == str(counter):
                setCounter = True
                combo.setCurrentIndex(index)
        if not setCounter:
            combo.setCurrentIndex(0)

    def getCounter(self):
        return self._currentCount

    def _simpleCounter(self):
        beatCount = self._registry[self.beatCountComboBox.currentIndex()]
        mc = self._mcMaker.makeSimpleCount(beatCount,
                                           self.beatsSpinBox.value())
        return mc

    def setBeat(self, measureCount):
        if measureCount is None:
            measureCount = self._mcMaker.makeSimpleCount(self._registry[0], 4)
        self._currentCount = copy.copy(measureCount)
        if measureCount.isSimpleCount():
            self.beatsSpinBox.setValue(measureCount.numBeats())
            self._setCombo(self.beatCountComboBox,
                           measureCount[0].counter)
            self.counterTabs.setCurrentIndex(0)
        else:
            self.counterTabs.setCurrentIndex(1)

    def preview(self):
        if self.simpleSelected:
            self._currentCount = self._simpleCounter()
        else:
            pass
        if self._currentCount is not None:
            self.previewText.setText(self._currentCount.countString())
        self.beatChanged.emit()

    def _editComplex(self):
        dlg = self._complexDialog(self._registry, self._currentCount, self)
        if dlg.exec_():
            self._currentCount = dlg.getCount()
            self.preview()

