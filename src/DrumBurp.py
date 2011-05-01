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
    app.setWindowIcon(GUI.DBIcons.getIcon("drumburp"))
    mainWindow.show()
    app.exec_()

if __name__ == '__main__':
    main()
