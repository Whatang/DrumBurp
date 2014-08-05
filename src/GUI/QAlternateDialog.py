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
Created on 22 Feb 2011

@author: Mike Thomas

'''
from PyQt4 import QtGui
from ui_alternateRepeats import Ui_AlternateDialog
from QAlternateWidget import QAlternateWidget

class QAlternateDialog(QtGui.QDialog, Ui_AlternateDialog):
    def __init__(self, alternate, parent = None):
        super(QAlternateDialog, self).__init__(parent = parent)
        self.setupUi(self)
        self._repeats = []
        if alternate is not None:
            self.populate(alternate)
        else:
            self.populate("1")
        self.addButton.clicked.connect(self._addClicked)


    def getValue(self):
        value = ", ".join(repeat.getString() for repeat in self._repeats)
        value += "."
        return value

    def populate(self, alternate):
        repeats = [repeat.strip() for repeat in alternate.split(",")]
        for repeat in repeats:
            if "-" in repeat:
                startVal, endVal = map(int,
                                       map(lambda x : x.strip("."),
                                           repeat.split("-")))
                isRange = True
            else:
                startVal = int(repeat.strip().strip("."))
                endVal = startVal
                isRange = False
            self._addRepeat(startVal, endVal, isRange)
            self._checkButtons()

    def _addRepeat(self, startVal, endVal, isRange):
        newWidget = QAlternateWidget(startVal, endVal,
                                     isRange, self.repeatsFrame)
        self._repeats.append(newWidget)
        self.repeatsLayout.addWidget(newWidget)
        callback = lambda value, widget = newWidget : self.deleteRepeat(widget)
        newWidget.deleteButton.clicked.connect(callback)

    def deleteRepeat(self, widget):
        if widget not in self._repeats:
            return
        self._repeats.remove(widget)
        self.repeatsLayout.removeWidget(widget)
        widget.close()
        self._checkButtons()

    def _checkButtons(self):
        if len(self._repeats) > 1:
            deleteOn = True
        else:
            deleteOn = False
        for widget in self._repeats:
            widget.deleteButton.setEnabled(deleteOn)

    def _addClicked(self):
        maxVal = max(widget.highValue() for widget in self._repeats)
        self._addRepeat(maxVal, maxVal, False)
        self._checkButtons()



def main():
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    dialog = QAlternateDialog("1,2-3, 4,5, 6,7-10")
    dialog.show()
    app.exec_()
    if dialog.result() == dialog.Accepted:
        print dialog.getValue()

if __name__ == "__main__":
    main()
