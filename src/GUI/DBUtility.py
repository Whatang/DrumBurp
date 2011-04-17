'''
Created on 19 Jan 2011

@author: Mike Thomas
'''

def populateCounterCombo(combo, chosenCounter, registry):
    setCounter = False
    combo.clear()
    for index, (name, counter) in enumerate(registry):
        combo.addItem(name)
        if counter == chosenCounter:
            setCounter = True
            combo.setCurrentIndex(index)
    if not setCounter:
        combo.setCurrentIndex(0)
