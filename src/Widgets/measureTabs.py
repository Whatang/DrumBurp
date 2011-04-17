'''
Created on 17 Apr 2011

@author: Mike Thomas

'''

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
        self.counterTabs.setTabEnabled(1, False)

    beatChanged = pyqtSignal()

    @property
    def simpleSelected(self):
        return self.counterTabs.currentWidget() == self.simpleTab

    def setup(self, measureCount,
              counterRegistry, mcMaker):
        self._measureCount = measureCount
        self._registry = counterRegistry
        self._mcMaker = mcMaker
        self.beatCountComboBox.currentIndexChanged.connect(self.preview)
        self.beatsSpinBox.valueChanged.connect(self.preview)
        self.restoreOriginal()

    def restoreOriginal(self):
        self.setBeat(self._measureCount)

    def populateCombo(self, combo, beatCount):
        setCounter = False
        combo.clear()
        for index, (name, counter) in enumerate(self._registry):
            combo.addItem(name)
            if str(beatCount) == str(counter):
                setCounter = True
                combo.setCurrentIndex(index)
        if not setCounter:
            combo.setCurrentIndex(0)

    def getCounter(self):
        if self.simpleSelected:
            return self._simpleCounter()
        else:
            pass

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
            self.populateCombo(self.beatCountComboBox,
                               measureCount[0].counter)
            self.counterTabs.setCurrentIndex(0)
        else:
            pass

    def preview(self):
        if self.simpleSelected:
            counter = self._simpleCounter()
            self.previewText.setPlainText(counter.countString())
        else:
            pass
        self.beatChanged.emit()
