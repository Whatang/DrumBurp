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
        self.counterTabs.setTabEnabled(1, False)
        self.counterTabs.currentChanged.connect(self.preview)

    beatChanged = pyqtSignal()

    @property
    def simpleSelected(self):
        return self.counterTabs.currentWidget() == self.simpleTab

    def setup(self, measureCount,
              counterRegistry, mcMaker):
        self._measureCount = measureCount
        self._registry = counterRegistry
        self._currentCount = copy.copy(measureCount)
        self._mcMaker = mcMaker
        self.beatCountComboBox.currentIndexChanged.connect(self.preview)
        self.beatsSpinBox.valueChanged.connect(self.preview)
        self._populateCombo(self.beatCountComboBox)
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
        if measureCount.isSimpleCount():
            self.beatsSpinBox.setValue(measureCount.numBeats())
            self._setCombo(self.beatCountComboBox,
                           measureCount[0].counter)
            self.counterTabs.setCurrentIndex(0)
        else:
            pass

    def preview(self):
        if self.simpleSelected:
            self._currentCount = self._simpleCounter()
        else:
            pass
        if self._currentCount is not None:
            self.previewText.setText(self._currentCount.countString())
        self.beatChanged.emit()
