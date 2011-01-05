'''
Created on 3 Aug 2010

@author: Mike Thomas

'''

from PyQt4.QtGui import QRadioButton
from PyQt4 import QtCore


class RadioButtonTeller(QRadioButton):
    def __init__(self, parent = None):
        self._buttonValue = ""
        super(RadioButtonTeller, self).__init__(parent)
        self.connect(self, QtCore.SIGNAL("clicked()"), self._emitValueSignal)

    def _emitValueSignal(self):
        self.emit(QtCore.SIGNAL("emitValue(QString)"), self.buttonValue)

    def _setButtonValue(self, value):
        self._buttonValue = value

    def _getButtonValue(self):
        return self._buttonValue

    emitValue = QtCore.pyqtSignal(QtCore.QString)
    buttonValue = QtCore.pyqtProperty(QtCore.QString, fget = _getButtonValue,
                                      fset = _setButtonValue)

