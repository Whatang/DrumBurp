# Copyright 2011 Michael Thomas
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
Created on 31 Jul 2010

@author: Mike Thomas
'''
import sys
from PyQt4.QtGui import QApplication
import GUI.DBMainwindow
import GUI.DBIcons

def main():
    import ctypes
    myappid = 'Whatang.DrumBurp'
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except AttributeError:
        pass
    app = QApplication(sys.argv)
    app.setOrganizationName("Whatang Software")
    app.setOrganizationDomain("whatang.org")
    app.setApplicationName(GUI.DBMainwindow.APPNAME)
    mainWindow = GUI.DBMainwindow.DrumBurp(fakeStartup = '--virgin' in sys.argv)
    mainWindow.setWindowTitle("DrumBurp v" + GUI.DBMainwindow.DB_VERSION)
    app.setWindowIcon(GUI.DBIcons.getIcon("drumburp"))
    mainWindow.show()
    app.exec_()

if __name__ == '__main__':
    main()
