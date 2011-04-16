'''
Created on 19 Jan 2011

@author: Mike Thomas
'''

from Data import MeasureCount
from PyQt4.QtCore import QVariant

def populateCounterCombo(combo, chosenCounter):
    setCounter = False
    combo.clear()
    for index, (beatTicks, counter) in enumerate(MeasureCount.getCounters()):
        combo.addItem(counter.description(),
                      userData = QVariant(beatTicks))
        if counter == chosenCounter:
            setCounter = True
            combo.setCurrentIndex(index)
    if not setCounter:
        combo.setCurrentIndex(0)
