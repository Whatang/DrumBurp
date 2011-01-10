'''
Created on 31 Jul 2010

@author: Mike Thomas

'''

from ui_drumburp import Ui_DrumBurpWindow
from PyQt4.QtGui import QMainWindow, QFontDatabase, QFileDialog, QMessageBox, QDialog
from PyQt4.QtCore import QTimer, pyqtSignature, SIGNAL
from QScore import QScore
from QSongProperties import QSongProperties
from QNewScoreDialog import QNewScoreDialog
import os

APPNAME = "DrumBurp"

class DrumBurp(QMainWindow, Ui_DrumBurpWindow):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(DrumBurp, self).__init__(parent)
        self.setupUi(self)
        self.filename = None
        self.songProperties = QSongProperties()
        self.scoreScene = QScore(self)
        self.scoreView.setScene(self.scoreScene)
        self.fontComboBox.setWritingSystem(QFontDatabase.Latin)
#        QTimer.singleShot(0, lambda: self.widthSpinBox.setValue(80))
        xValue, yValue, lValue = self.songProperties.proportionalSpacing()
        QTimer.singleShot(0, lambda: self.spaceSlider.setValue(xValue))
        QTimer.singleShot(0, lambda: self.verticalSlider.setValue(yValue))
        QTimer.singleShot(0, lambda: self.lineSpaceSlider.setValue(lValue))
        QTimer.singleShot(0, lambda: self.defaultMeasureWidthSpinBox.setValue(self.songProperties.defaultMeasureWidth))
        font = self.scoreScene.font()
        self.fontComboBox.setCurrentFont(font)
        self.connect(self.scoreScene, SIGNAL("dirty"), self.setWindowModified)
        self.updateStatus("Welcome to %s" % APPNAME)

    def updateStatus(self, message):
        self.statusBar().showMessage(message, 5000)
        if self.filename is not None:
            print repr(self.filename)
            self.setWindowTitle("DrumBurp - %s[*]"
                                % os.path.basename(self.filename))
        else:
            self.setWindowTitle("DrumBurp - Untitled[*]")
        self.setWindowModified(self.scoreScene.dirty)

    def okToContinue(self):
        if self.scoreScene.dirty:
            reply = QMessageBox.question(self,
                                         "DrumBurp - Unsaved Changes",
                                         "Save unsaved changes?",
                                         QMessageBox.Yes,
                                         QMessageBox.No,
                                         QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                if not self.fileSave():
                    failReply = QMessageBox.warning(self,
                                                    "Failed save!",
                                                    "DrumBurp could not save the file. "
                                                    + "\n\n" +
                                                    "Continue anyway? All unsaved changes will be lost!",
                                                    QMessageBox.Yes,
                                                    QMessageBox.No)
                    return failReply == QMessageBox.Yes
        return True

    def closeEvent(self, event):
        if self.okToContinue():
            pass
        else:
            event.ignore()

    @pyqtSignature("")
    def on_actionFitInWindow_triggered(self):
        widthInPixels = self.scoreView.width()
        maxColumns = self.songProperties.maxColumns(widthInPixels)
        self.widthSpinBox.setValue(maxColumns)

    @pyqtSignature("")
    def on_actionLoad_triggered(self):
        if not self.okToContinue():
            return
        fname = QFileDialog.getOpenFileName(parent = self,
                                            caption = "Choose a DrumBurp file to open",
                                            filter = "DrumBurp files (*.brp)")
        if len(fname) == 0:
            return
        if self.scoreScene.loadScore(fname):
            self.filename = unicode(fname)
            self.updateStatus("Successfully loaded %s" % self.filename)

    def getFileName(self):
        fname = QFileDialog.getSaveFileName(parent = self, caption = "Choose a DrumBurp file to save",
                                            directory = self.filename if self.filename is not None else "",
                                            filter = "DrumBurp files (*.brp)")
        if len(fname) == 0 :
            return False
        self.filename = unicode(fname)
        return True

    def fileSave(self):
        if self.filename is None:
            if not self.getFileName():
                return False
        return self.scoreScene.saveScore(self.filename)

    @pyqtSignature("")
    def on_actionSave_triggered(self):
        if self.fileSave():
            self.updateStatus("Successfully saved %s" % self.filename)

    @pyqtSignature("")
    def on_actionSaveAs_triggered(self):
        if self.getFileName():
            self.scoreScene.saveScore(self.filename)
            self.updateStatus("Successfully saved %s" % self.filename)

    @pyqtSignature("")
    def on_actionNew_triggered(self):
        if self.okToContinue():
            dialog = QNewScoreDialog()
            dialog.measureSizeSpinBox.setValue(self.songProperties.defaultMeasureWidth)
            if dialog.exec_():
                nMeasures = dialog.numMeasuresSpinBox.value()
                mWidth = dialog.measureSizeSpinBox.value()
                self.scoreScene.newScore(numMeasures = nMeasures,
                                         measureWidth = mWidth)
                self.filename = None
                self.defaultMeasureWidthSpinBox.setValue(mWidth)
                self.updateStatus("Created a new blank score")
