Set-PSDebug -Trace 1
Invoke-WebRequest "https://netcologne.dl.sourceforge.net/project/pyqt/PyQt4/PyQt-4.11.3/PyQt4-4.11.3-gpl-Py2.7-Qt4.8.6-x64.exe" -OutFile pyqt_installer.exe
& ./pyqt_installer.exe /S