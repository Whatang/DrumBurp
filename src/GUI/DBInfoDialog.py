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

from ui_dbInfo import Ui_InfoDialog
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature
from DBLicense import DBLicenseDialog

class DBInfoDialog(QDialog, Ui_InfoDialog):
    def __init__(self, version, parent = None):
        '''
        Constructor
        '''
        super(DBInfoDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("DrumBurp v%s Information" % version)
        text = unicode(self.copyrightLabel.text())
        text += ' This is version %s.' % version
        self.copyrightLabel.setText(text)

    @pyqtSignature("")
    def on_licenseButton_clicked(self): #IGNORE:R0201
        dlg = DBLicenseDialog()
        dlg.exec_()
