'''
Created on Jan 27, 2011

@author: Mike
'''

from ui_asciiDialog import Ui_asciiDialog
from PyQt4.QtGui import QDialog, QFileDialog, QMessageBox
from PyQt4.QtCore import pyqtSignature
from Data.ASCIISettings import ASCIISettings
import os

class QAsciiExportDialog(QDialog, Ui_asciiDialog):
    '''
    classdocs
    '''

    def __init__(self, filename, parent = None, settings = None):
        '''
        Constructor
        '''
        super(QAsciiExportDialog, self).__init__(parent)
        self.setupUi(self)
        if settings is None:
            settings = ASCIISettings()
        self._filename = None
        self._setInitialState(filename, settings)

    def _setInitialState(self, filename, settings):
        self._filename = filename
        self.filenameLabel.setText(self._filename
                                   if self._filename is not None
                                   else "")
        for checkName in settings.checkNames():
            getattr(self, checkName + "Check").setChecked(getattr(settings, checkName))

    @pyqtSignature("")
    def on_filenameButton_clicked(self):
        options = QFileDialog.DontConfirmOverwrite
        filters = "Text file (*.txt);;All files (*.*)"
        directory = self._filename
        if directory is None:
            directory = ""
        fname = QFileDialog.getSaveFileName(parent = self.parent(),
                                            caption = "Export to text file",
                                            directory = directory,
                                            options = options,
                                            filter = filters)
        if len(fname) != 0:
            self._filename = os.path.abspath(fname)
            self.filenameLabel.setText(self._filename)

    def getFilename(self):
        if self.result() != self.Accepted:
            return None
        return self._filename

    def getOptions(self):
        settings = ASCIISettings()
        for checkName in settings.checkNames():
            value = getattr(self, checkName + "Check").isChecked()
            setattr(settings, checkName, value)
        return settings

    def accept(self):
        if not os.path.exists(self._filename):
            super(QAsciiExportDialog, self).accept()
            return
        buttons = (QMessageBox.Yes | QMessageBox.No | QMessageBox.Abort)
        yesNo = QMessageBox.question(self, "Overwrite?",
                                     ("%s already exists - overwrite?"
                                      % self._filename),
                                     buttons = buttons,
                                     defaultButton = QMessageBox.Yes)
        if yesNo == QMessageBox.Abort:
            self.reject()
            return
        elif yesNo == QMessageBox.No:
            return
        else:
            super(QAsciiExportDialog, self).accept()

def main():
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    dialog = QAsciiExportDialog("myfile.txt")
    dialog.show()
    app.exec_()
    if dialog.result() == dialog.Accepted:
        print dialog.getFilename()
        print dialog.getOptions()

if __name__ == "__main__":
    main()
