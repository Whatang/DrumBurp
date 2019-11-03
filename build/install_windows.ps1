Set-PSDebug -Trace 1
Set-Item Env:PYTHONIOENCODING UTF-8

# Download and install VS2008 C++ Redistributable

Invoke-WebRequest https://download.microsoft.com/download/d/2/4/d242c3fb-da5a-4542-ad66-f9661d0a8d19/vcredist_x64.exe -OutFile vcredist_x64.exe
& vcredist_x64.exe /quiet /install

Invoke-WebRequest https://netcologne.dl.sourceforge.net/project/pyqt/PyQt4/PyQt-4.11.3/PyQt4-4.11.3-gpl-Py2.7-Qt4.8.6-x64.exe -OutFile pyqt_installer.exe
& pyqt_installer.exe /S

# Install NSIS installer tool
Invoke-WebRequest "https://downloads.sourceforge.net/project/nsis/NSIS%203/3.04/nsis-3.04-setup.exe?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fnsis%2Ffiles%2FNSIS%25203%2F3.04%2Fnsis-3.04-setup.exe%2Fdownload%3Fuse_mirror%3Dnetcologne%26download%3D&ts=1572714477" -OutFile nsis-setup.exe
& nsis-setup.exe /S

# Install Python modules
& pip install -r build/requirements-windows.txt


