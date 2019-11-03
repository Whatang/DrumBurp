Set-PSDebug -Trace 1
Set-Item Env:PYTHONIOENCODING UTF-8

# Download and install VS2008 C++ Redistributable

choco install vcredist2008

Invoke-WebRequest "https://netcologne.dl.sourceforge.net/project/pyqt/PyQt4/PyQt-4.11.3/PyQt4-4.11.3-gpl-Py2.7-Qt4.8.6-x64.exe" -OutFile pyqt_installer.exe
& ./pyqt_installer.exe /S

# Install NSIS installer tool
choco install nsis

# Install Python modules
& pip install -r build/requirements-windows.txt


