'''
Created on 31 Jul 2010

@author: Mike Thomas
'''
import sys
from PyQt4.QtGui import QApplication
import GUI.DBMainwindow

def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Whatang Software")
    app.setOrganizationDomain("whatang.org")
    app.setApplicationName(GUI.DBMainwindow.APPNAME)
    mainWindow = GUI.DBMainwindow.DrumBurp()
    mainWindow.show()
    app.exec_()

if __name__ == '__main__':
    main()
