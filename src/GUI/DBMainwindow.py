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

from ui_drumburp import Ui_DrumBurpWindow
from PyQt4.QtGui import (QMainWindow, QFontDatabase,
                         QFileDialog, QMessageBox,
                         QPrintPreviewDialog, QWhatsThis,
                         QPrinterInfo,
                         QPrinter, QDesktopServices)
from PyQt4.QtCore import pyqtSignature, QSettings, QVariant, QTimer
from QScore import QScore
from QDisplayProperties import QDisplayProperties
from QNewScoreDialog import QNewScoreDialog
from QAsciiExportDialog import QAsciiExportDialog
from QEditMeasureDialog import QEditMeasureDialog
from DBInfoDialog import DBInfoDialog
from DBStartupDialog import DBStartupDialog
import DBIcons
import os
import DBMidi
from Data.Score import InconsistentRepeats

APPNAME = "DrumBurp"
DB_VERSION = "0.4"
#pylint:disable-msg=R0904

class FakeQSettings(object):
    def value(self, key_): #IGNORE:R0201
        return QVariant()

    def setValue(self, key_, value_): #IGNORE:R0201
        return


class DrumBurp(QMainWindow, Ui_DrumBurpWindow):
    '''
    classdocs
    '''

    def __init__(self, parent = None, fakeStartup = False, filename = None):
        '''
        Constructor
        '''
        self._fakeStartup = fakeStartup
        super(DrumBurp, self).__init__(parent)
        self._state = None
        self._asciiSettings = None
        self._printer = QPrinter()
        self.setupUi(self)
        DBIcons.initialiseIcons()
        self.paperBox.clear()
        for name in dir(QPrinter):
            if isinstance(getattr(QPrinter, name), QPrinter.PageSize):
                self.paperBox.addItem(name)
        settings = self._makeQSettings()
        self.recentFiles = [unicode(fname) for fname in
                            settings.value("RecentFiles").toStringList()
                            if os.path.exists(unicode(fname))]
        if filename is None:
            filename = (None
                        if len(self.recentFiles) == 0
                        else self.recentFiles[0])
        self.filename = filename
        self.addToRecentFiles()
        self.updateRecentFiles()
        self.songProperties = QDisplayProperties()
        # Create scene
        self.scoreScene = QScore(self)
        self.restoreGeometry(settings.value("Geometry").toByteArray())
        self.restoreState(settings.value("MainWindow/State").toByteArray())
        self._initializeState()
        self.setSections()
        QTimer.singleShot(0, self._startUp)

    def _initializeState(self):
        self.scoreView.setScene(self.scoreScene)
        # Connect signals
        props = self.songProperties
        props.fontChanged.connect(self._setNoteFont)
        props.noteSizeChanged.connect(self.noteSizeSpinBox.setValue)
        props.sectionFontChanged.connect(self._setSectionFont)
        props.sectionFontSizeChanged.connect(self._setSectionFontSize)
        props.metadataFontChanged.connect(self._setMetadataFont)
        props.metadataFontSizeChanged.connect(self._setMetadataSize)
        self.scoreScene.dirtySignal.connect(self.setWindowModified)
        self.paperBox.currentIndexChanged.connect(self._setPaperSize)
        props.kitDataVisibleChanged.connect(self._setKitDataVisible)
        props.emptyLinesVisibleChanged.connect(self._setEmptyLinesVisible)
        props.metadataVisibilityChanged.connect(self._setMetadataVisible)
        props.beatCountVisibleChanged.connect(self._setBeatCountVisible)
        DBMidi.SONGEND_SIGNAL.connect(self.musicDone)
        DBMidi.HIGHLIGHT_SIGNAL.connect(self.highlightPlayingMeasure)
        # Fonts
        self.fontComboBox.setWritingSystem(QFontDatabase.Latin)
        self.sectionFontCombo.setWritingSystem(QFontDatabase.Latin)
        self.sectionFontCombo.setWritingSystem(QFontDatabase.Latin)
        self.lineSpaceSlider.setValue(self.scoreScene.systemSpacing)
        font = self.songProperties.noteFont
        if font is None:
            font = self.scoreScene.font()
        font.setPointSize(self.songProperties.noteFontSize)
        self.fontComboBox.setCurrentFont(font)
        self.noteSizeSpinBox.setValue(self.songProperties.noteFontSize)
        font = self.songProperties.sectionFont
        if font is None:
            font = self.scoreScene.font()
        font.setPointSize(self.songProperties.sectionFontSize)
        self.sectionFontCombo.setCurrentFont(font)
        self.sectionFontSizeSpinbox.setValue(props.sectionFontSize)
        font = self.songProperties.metadataFont
        if font is None:
            font = self.scoreScene.font()
        font.setPointSize(self.songProperties.metadataFontSize)
        self.metadataFontCombo.setCurrentFont(font)
        self.metadataFontSizeSpinbox.setValue(props.metadataFontSize)
        # Visibility toggles
        self.actionShowDrumKey.setChecked(props.kitDataVisible)
        self.actionShowEmptyLines.setChecked(props.emptyLinesVisible)
        self.actionShowScoreInfo.setChecked(props.metadataVisible)
        self.actionShowBeatCount.setChecked(props.beatCountVisible)
        # Undo/redo
        self.actionUndo.setEnabled(False)
        self.actionRedo.setEnabled(False)
        self.scoreScene.canUndoChanged.connect(self.actionUndo.setEnabled)
        changeUndoText = lambda txt:self.actionUndo.setText("Undo " + txt)
        self.scoreScene.undoTextChanged.connect(changeUndoText)
        self.scoreScene.canRedoChanged.connect(self.actionRedo.setEnabled)
        changeRedoText = lambda txt:self.actionRedo.setText("Redo " + txt)
        self.scoreScene.redoTextChanged.connect(changeRedoText)
        # Default beat
        self._beatChanged(self.scoreScene.defaultCount)


    def _startUp(self):
        self.scoreView.startUp()
        dlg = DBStartupDialog(DB_VERSION)
        dlg.exec_()
        self.updateStatus("Welcome to %s v%s" % (APPNAME, DB_VERSION))


    def _makeQSettings(self):
        if self._fakeStartup:
            return FakeQSettings()
        else:
            return QSettings()

    def _setPaperSize(self, unusedIndex):
        self.scoreScene.setPaperSize(self.paperBox.currentText())

    def _setNoteFont(self):
        props = self.songProperties
        self.fontComboBox.setCurrentFont(props.noteFont)

    def _setSectionFont(self):
        props = self.songProperties
        self.sectionFontCombo.setCurrentFont(props.sectionFont)

    def _setSectionFontSize(self):
        props = self.songProperties
        self.sectionFontSizeSpinbox.setValue(props.sectionFontSize)

    def _setMetadataFont(self):
        props = self.songProperties
        self.metadataFontCombo.setCurrentFont(props.metadataFont)

    def _setMetadataSize(self):
        props = self.songProperties
        self.metadataFontSizeSpinbox.setValue(props.metadataFontSize)

    def _setKitDataVisible(self):
        props = self.songProperties
        if props.kitDataVisible != self.actionShowDrumKey.isChecked():
            self.actionShowDrumKey.setChecked(props.kitDataVisible)

    def _setMetadataVisible(self):
        props = self.songProperties
        if props.metadataVisible != self.actionShowScoreInfo.isChecked():
            self.actionShowScoreInfo.setChecked(props.metadataVisible)

    def _setEmptyLinesVisible(self):
        props = self.songProperties
        if props.emptyLinesVisible != self.actionShowEmptyLines.isChecked():
            self.actionShowEmptyLines.setChecked(props.emptyLinesVisible)

    def _setBeatCountVisible(self):
        props = self.songProperties
        if props.beatCountVisible != self.actionShowBeatCount.isChecked():
            self.actionShowBeatCount.setChecked(props.beatCountVisible)

    def updateStatus(self, message):
        self.statusBar().showMessage(message, 5000)
        if self.filename is not None:
            self.setWindowTitle("DrumBurp v%s - %s[*]"
                                % (DB_VERSION, os.path.basename(self.filename)))
        else:
            self.setWindowTitle("DrumBurp v%s - Untitled[*]" % DB_VERSION)
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
                    msg = ("DrumBurp could not save the file."
                           "\n\n"
                           "Continue anyway? "
                           "All unsaved changes will be lost!")
                    failReply = QMessageBox.warning(self,
                                                    "Failed Save!",
                                                    msg,
                                                    QMessageBox.Yes,
                                                    QMessageBox.No)
                    return failReply == QMessageBox.Yes
        return True

    def closeEvent(self, event):
        if self.okToContinue():
            settings = self._makeQSettings()
            settings.setValue("RecentFiles",
                              QVariant(self.recentFiles))
            settings.setValue("Geometry",
                              QVariant(self.saveGeometry()))
            settings.setValue("MainWindow/State",
                              QVariant(self.saveState()))
            self.songProperties.save(settings)
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
        caption = "Choose a DrumBurp file to open"
        directory = self.filename
        if len(self.recentFiles) > 0:
            directory = os.path.dirname(self.recentFiles[-1])
        else:
            loc = QDesktopServices.HomeLocation
            directory = QDesktopServices.storageLocation(loc)
        fname = QFileDialog.getOpenFileName(parent = self,
                                            caption = caption,
                                            directory = directory,
                                            filter = "DrumBurp files (*.brp)")
        if len(fname) == 0:
            return
        if self.scoreScene.loadScore(fname):
            self._beatChanged(self.scoreScene.defaultCount)
            self.filename = unicode(fname)
            self.updateStatus("Successfully loaded %s" % self.filename)
            self.addToRecentFiles()
            self.updateRecentFiles()

    def _getFileName(self):
        directory = self.filename
        if directory is None:
            suggestion = unicode(self.scoreScene.title)
            if len(suggestion) == 0:
                suggestion = "Untitled"
            suggestion = os.extsep.join([suggestion, "brp"])
            if len(self.recentFiles) > 0:
                directory = os.path.dirname(self.recentFiles[-1])
            else:
                home = QDesktopServices.HomeLocation
                directory = str(QDesktopServices.storageLocation(home))
            directory = os.path.join(directory,
                                     suggestion)
        if os.path.splitext(directory)[-1] == os.extsep + 'brp':
            directory = os.path.splitext(directory)[0]
        caption = "Choose a DrumBurp file to save"
        fname = QFileDialog.getSaveFileName(parent = self,
                                            caption = caption,
                                            directory = directory,
                                            filter = "DrumBurp files (*.brp)")
        if len(fname) == 0 :
            return False
        self.filename = unicode(fname)
        return True

    def fileSave(self):
        if self.filename is None:
            if not self._getFileName():
                return False
            self.addToRecentFiles()
            self.updateRecentFiles()
        return self.scoreScene.saveScore(self.filename)

    @pyqtSignature("")
    def on_actionSave_triggered(self):
        if self.fileSave():
            self.updateStatus("Successfully saved %s" % self.filename)

    @pyqtSignature("")
    def on_actionSaveAs_triggered(self):
        if self._getFileName():
            self.scoreScene.saveScore(self.filename)
            self.updateStatus("Successfully saved %s" % self.filename)
            self.addToRecentFiles()
            self.updateRecentFiles()

    @pyqtSignature("")
    def on_actionNew_triggered(self):
        if self.okToContinue():
            counter = self.scoreScene.defaultCount
            registry = self.songProperties.counterRegistry
            dialog = QNewScoreDialog(self.parent(),
                                     counter,
                                     registry)
            if dialog.exec_():
                nMeasures, counter = dialog.getValues()
                self.scoreScene.newScore(numMeasures = nMeasures,
                                         counter = counter)
                self.filename = None
                self.updateRecentFiles()
                self._beatChanged(counter)
                self.updateStatus("Created a new blank score")

    def addToRecentFiles(self):
        if self.filename is not None:
            if self.filename in self.recentFiles:
                self.recentFiles.remove(self.filename)
            self.recentFiles.insert(0, self.filename)
            if len(self.recentFiles) > 10:
                self.recentFiles.pop()

    def updateRecentFiles(self):
        self.menuRecentScores.clear()
        for fname in self.recentFiles:
            if fname != self.filename and os.path.exists(fname):
                def openRecentFile(bool_, filename = fname):
                    if not self.okToContinue():
                        return
                    if self.scoreScene.loadScore(filename):
                        self.filename = filename
                        self.updateStatus("Successfully loaded %s" % filename)
                        self.addToRecentFiles()
                        self.updateRecentFiles()
                action = self.menuRecentScores.addAction(fname)
                action.setIcon(DBIcons.getIcon("score"))
                action.triggered.connect(openRecentFile)

    def _beatChanged(self, counter):
        if counter != self.scoreScene.defaultCount:
            self.scoreScene.defaultCount = counter
        self.defaultMeasureButton.setText(counter.countString())

    def _systemSpacingChanged(self, value):
        if value != self.scoreScene.systemSpacing:
            self.scoreScene.systemSpacing = value
        self.lineSpaceSlider.setValue(value)

    def hideEvent(self, event):
        self._state = self.saveState()
        super(DrumBurp, self).hideEvent(event)

    def showEvent(self, event):
        if self._state is not None:
            self.restoreState(self._state)
            self._state = None
        super(DrumBurp, self).showEvent(event)

    @pyqtSignature("")
    def on_actionExportASCII_triggered(self):
        fname = self.filename
        if self.filename is None:
            home = QDesktopServices.HomeLocation
            fname = QDesktopServices.storageLocation(home)
            fname = os.path.join(str(fname), 'Untitled.txt')
        if os.path.splitext(fname)[-1] == '.brp':
            fname = os.path.splitext(fname)[0] + '.txt'
        props = self.songProperties
        self._asciiSettings = props.generateAsciiSettings(self._asciiSettings)
        asciiDialog = QAsciiExportDialog(fname, self,
                                         settings = self._asciiSettings)
        if not asciiDialog.exec_():
            return
        fname = asciiDialog.getFilename()
        self._asciiSettings = asciiDialog.getOptions()
        try:
            with open(fname, 'w') as txtHandle:
                self.scoreScene.score.exportASCII(txtHandle,
                                                  self._asciiSettings)
        except StandardError:
            QMessageBox.warning(self.parent(), "Export failed!",
                                "Could not export to " + fname)
            raise
        else:
            self.updateStatus("Successfully exported ASCII to " + fname)

    @pyqtSignature("")
    def on_actionPrint_triggered(self):
        self._printer = QPrinter(QPrinterInfo(self._printer),
                                 QPrinter.HighResolution)
        self._printer.setPaperSize(self._getPaperSize())
        dialog = QPrintPreviewDialog(self._printer, parent = self)
        def updatePages(qprinter):
            self.scoreScene.printScore(qprinter, self.scoreView)
        dialog.paintRequested.connect(updatePages)
        dialog.exec_()

    @pyqtSignature("")
    def on_actionExportPDF_triggered(self):
        try:
            printer = QPrinter(mode = QPrinter.HighResolution)
            printer.setPaperSize(self._getPaperSize())
            printer.setOutputFormat(QPrinter.PdfFormat)
            if self.filename:
                outfileName = list(os.path.splitext(self.filename)[:-1])
                outfileName = os.extsep.join(outfileName + ["pdf"])
            else:
                outfileName = "Untitled.pdf"
            printer.setOutputFileName(outfileName)
            printer.setPaperSize(self._getPaperSize())
            dialog = QPrintPreviewDialog(printer, parent = self)
            def updatePages(qprinter):
                self.scoreScene.printScore(qprinter, self.scoreView)
            dialog.paintRequested.connect(updatePages)
            dialog.exec_()
            self.updateStatus("Exported to PDF %s" % outfileName)
        except StandardError:
            QMessageBox.warning(self.parent(), "Export failed!",
                                "Could not export PDF to " + outfileName)


    @staticmethod
    @pyqtSignature("")
    def on_actionWhatsThis_triggered():
        QWhatsThis.enterWhatsThisMode()

    @pyqtSignature("")
    def on_actionUndo_triggered(self):
        self.scoreScene.undo()

    @pyqtSignature("")
    def on_actionRedo_triggered(self):
        self.scoreScene.redo()

    @staticmethod
    @pyqtSignature("")
    def on_actionAboutDrumBurp_triggered():
        dlg = DBInfoDialog(DB_VERSION)
        dlg.exec_()

    def _getPaperSize(self):
        return getattr(QPrinter, str(self.paperBox.currentText()))

    @pyqtSignature("")
    def on_actionFitPage_triggered(self):
        papersize = self._getPaperSize()
        printer = QPrinter()
        printer.setPaperSize(papersize)
        widthInPixels = printer.pageRect().width()
        maxColumns = self.songProperties.maxColumns(widthInPixels)
        self.widthSpinBox.setValue(maxColumns)

    @pyqtSignature("")
    def on_defaultMeasureButton_clicked(self):
        counter = self.scoreScene.defaultCount
        dlg = QEditMeasureDialog(counter, counter,
                                 self.songProperties.counterRegistry,
                                 self)
        if dlg.exec_():
            counter = dlg.getValues()
            self._beatChanged(counter)

    def setPaperSize(self, paperSize):
        index = self.paperBox.findText(paperSize)
        if index > -1 and index != self.paperBox.currentIndex():
            self.paperBox.setCurrentIndex(index)
        elif index == -1:
            self.paperBox.setCurrentIndex(0)

    def setDefaultCount(self, count):
        self._beatChanged(count)

    def setSystemSpacing(self, value):
        self._systemSpacingChanged(value)

    def setSections(self):
        score = self.scoreScene.score
        self.sectionNavigator.blockSignals(True)
        self.sectionNavigator.clear()
        for sectionTitle in score.iterSections():
            self.sectionNavigator.addItem(sectionTitle)
        self.sectionNavigator.blockSignals(False)

    def _canPlayback(self):
        try:
            measures = list(self.scoreScene.score.iterMeasuresWithRepeats())
        except InconsistentRepeats, exc:
                QMessageBox.warning(self, "Playback error",
                                    "There are inconsistent repeat markings.")
                position = self.scoreScene.score.getMeasurePosition(exc[0])
                measure = self.scoreScene.getQMeasure(position)
                self.scoreView.ensureVisible(measure)
                return False
        return True

    @pyqtSignature("bool")
    def on_actionPlayScore_toggled(self, onOff):
        if onOff:
            if not self._canPlayback():
                self.actionPlayScore.toggle()
                return
            DBMidi.playScore(self.scoreScene.score)
        else:
            DBMidi.shutUp()

    def highlightPlayingMeasure(self, index):
        if index == -1:
            self.scoreScene.highlightPlayingMeasure(None)
        else:
            position = self.scoreScene.score.getMeasurePosition(index)
            self.scoreScene.highlightPlayingMeasure(position)
            measure = self.scoreScene.getQMeasure(position)
            self.scoreView.ensureVisible(measure)

    @pyqtSignature("bool")
    def on_actionMuteNotes_toggled(self, onOff):
        DBMidi.setMute(onOff)

    @pyqtSignature("")
    def on_actionExportMIDI_triggered(self):
        if not self._canPlayback():
            return
        directory = self.filename
        if directory is None:
            suggestion = unicode(self.scoreScene.title)
            if len(suggestion) == 0:
                suggestion = "Untitled"
            suggestion = os.extsep.join([suggestion, "brp"])
            if len(self.recentFiles) > 0:
                directory = os.path.dirname(self.recentFiles[-1])
            else:
                home = QDesktopServices.HomeLocation
                directory = str(QDesktopServices.storageLocation(home))
            directory = os.path.join(directory,
                                     suggestion)
        if os.path.splitext(directory)[-1] == os.extsep + 'brp':
            directory = os.path.splitext(directory)[0]
        caption = "Export to MIDI"
        fname = QFileDialog.getSaveFileName(parent = self,
                                            caption = caption,
                                            directory = directory,
                                            filter = "DrumBurp files (*.mid)")
        if len(fname) == 0 :
            return
        with open(fname, 'wb') as handle:
            DBMidi.exportMidi(self.scoreScene.score.iterMeasuresWithRepeats(),
                              self.scoreScene.score, handle)

    @pyqtSignature("bool")
    def on_actionLoopBars_toggled(self, onOff):
        if onOff:
            if not self.scoreScene.hasDragSelection():
                self.actionLoopBars.toggle()
                return
            DBMidi.loopBars(self.scoreScene.iterDragSelection(),
                            self.scoreScene.score)
        else:
            DBMidi.shutUp()

    def musicDone(self):
        self.actionPlayScore.setChecked(False)
        self.actionLoopBars.setChecked(False)
