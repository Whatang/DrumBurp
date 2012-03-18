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
Created on 31 Jul 2010

@author: Mike Thomas
'''
import sys
import optparse
from PyQt4.QtGui import QApplication
import GUI.DBMainwindow
import GUI.DBIcons
import GUI.DBStartupDialog
from DBVersion import APPNAME, DB_VERSION

def main():
    import ctypes
    parser = optparse.OptionParser()
    parser.add_option('--virgin', action = 'store_true')
    opts, args = parser.parse_args()
    filename = None
    if len(args) > 0:
        filename = args[0]
    myappid = 'Whatang.DrumBurp'
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except AttributeError:
        pass
    app = QApplication(sys.argv)
    app.setOrganizationName("Whatang Software")
    app.setOrganizationDomain("whatang.org")
    app.setApplicationName(APPNAME)
    splash = GUI.DBStartupDialog.DBStartupDialog(DB_VERSION)
    GUI.DBIcons.initialiseIcons()
    app.setWindowIcon(GUI.DBIcons.getIcon("drumburp"))
    splash.exec_()
    mainWindow = GUI.DBMainwindow.DrumBurp(fakeStartup = opts.virgin,
                                           filename = filename)
    mainWindow.setWindowTitle("DrumBurp v" + DB_VERSION)
    mainWindow.show()
    app.exec_()

if __name__ == '__main__':
    main()
