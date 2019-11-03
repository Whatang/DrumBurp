Set-PSDebug -Trace 1
Set-Item Env:PYTHONIOENCODING UTF-8

# Download and install VS2008 C++ Redistributable
choco install vcredist2008

# Download and install PyQt
& ./install_pyqt.ps1

# Install NSIS installer tool
choco install nsis

# Install Python modules
& pip install -r build/requirements-windows.txt


