# Copyright 2011-2012 Michael Thomas
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
import webbrowser
from StringIO import StringIO
from ui_drumburp import Ui_DrumBurpWindow
from PyQt4.QtGui import (QMainWindow, QFontDatabase,
                         QFileDialog, QMessageBox,
                         QPrintPreviewDialog, QWhatsThis,
                         QPrinterInfo, QLabel, QFrame,
                         QPrinter, QDesktopServices)
from PyQt4.QtCore import pyqtSignature, QSettings, QVariant, QTimer, QThread
from QScore import QScore
from QDisplayProperties import QDisplayProperties
from QNewScoreDialog import QNewScoreDialog
from QAsciiExportDialog import QAsciiExportDialog
from QEditMeasureDialog import QEditMeasureDialog
from QVersionDownloader import QVersionDownloader
from DBInfoDialog import DBInfoDialog
import DBColourPicker
import DBIcons
import os
import DBMidi
from Data.Score import InconsistentRepeats
from DBFSMEvents import StartPlaying, StopPlaying
from DBVersion import APPNAME, DB_VERSION, doesNewerVersionExist
from Notation.lilypond import LilypondScore, LilypondProblem
from Notation import AsciiExport
# pylint:disable-msg=R0904

class FakeQSettings(object):
    def value(self, key_):  # IGNORE:R0201
        return QVariant()

    def setValue(self, key_, value_):  # IGNORE:R0201
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
        self._printer = None
        self.setupUi(self)
        self.scoreScene = None
        self.paperBox.blockSignals(True)
        self.paperBox.clear()
        self._knownPageHeights = []
        self.colourScheme = DBColourPicker.ColourScheme()
        printer = QPrinter()
        printer.setOutputFileName("invalid.pdf")
        for name in dir(QPrinter):
            attr = getattr(QPrinter, name)
            if (isinstance(attr, QPrinter.PageSize)
                and name != "Custom"):
                self.paperBox.addItem(name)
                printer.setPaperSize(attr)
                self._knownPageHeights.append(printer.pageRect().height())
        self._pageHeight = printer.paperRect().height()
        self.paperBox.blockSignals(False)
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
        errored_files = []
        try:
            self.scoreScene = QScore(self)
        except:
            errored_files.append(self.filename)
            try:
                self.recentFiles.remove(self.filename)
            except ValueError:
                pass
            self.filename = None
            self.scoreScene = QScore(self)

        self.restoreGeometry(settings.value("Geometry").toByteArray())
        self.restoreState(settings.value("MainWindow/State").toByteArray())
        self._readColours(settings)
        self.statusbar.addPermanentWidget(QFrame())
        self.availableNotesLabel = QLabel()
        self.availableNotesLabel.setMinimumWidth(250)
        self.statusbar.addPermanentWidget(self.availableNotesLabel)
        self._infoBar = QLabel()
        self.statusbar.addPermanentWidget(self._infoBar)
        self._initializeState()
        self.setSections()
        self._versionThread = VersionCheckThread()
        self._versionThread.finished.connect(self._finishedVersionCheck)
        QTimer.singleShot(0, lambda : self._startUp(errored_files))
        self.actionCheckOnStartup.setChecked(settings.value("CheckOnStartup").toBool())

    def _connectSignals(self, props, scene):
        # Connect signals
        props.fontChanged.connect(self._setNoteFont)
        props.noteSizeChanged.connect(self.noteSizeSpinBox.setValue)
        props.sectionFontChanged.connect(self._setSectionFont)
        props.sectionFontSizeChanged.connect(self._setSectionFontSize)
        props.metadataFontChanged.connect(self._setMetadataFont)
        props.metadataFontSizeChanged.connect(self._setMetadataSize)
        scene.dirtySignal.connect(self.setWindowModified)
        scene.dragHighlight.connect(self.actionLoopBars.setEnabled)
        scene.dragHighlight.connect(self.actionPlayOnce.setEnabled)
        scene.dragHighlight.connect(self.actionCopyMeasures.setEnabled)
        scene.dragHighlight.connect(self.checkPasteMeasure)
        scene.dragHighlight.connect(self.actionClearMeasures.setEnabled)
        scene.dragHighlight.connect(self.actionDeleteMeasures.setEnabled)
        scene.sceneFormatted.connect(self.sceneFormatted)
        scene.playing.connect(self._scorePlaying)
        scene.currentHeadsChanged.connect(self.availableNotesLabel.setText)
        scene.statusMessageSet.connect(self._setStatusFromScene)
        scene.lilysizeChanged.connect(self._setLilySize)
        scene.lilypagesChanged.connect(self._setLilyPages)
        scene.lilyFillChanged.connect(self._setLilyFill)
        self.paperBox.currentIndexChanged.connect(self._setPaperSize)
        props.kitDataVisibleChanged.connect(self._setKitDataVisible)
        props.emptyLinesVisibleChanged.connect(self._setEmptyLinesVisible)
        props.measureCountsVisibleChanged.connect(self._setMeasureCountsVisible)
        props.metadataVisibilityChanged.connect(self._setMetadataVisible)
        props.beatCountVisibleChanged.connect(self._setBeatCountVisible)
        DBMidi.SONGEND_SIGNAL.connect(self.musicDone)
        DBMidi.HIGHLIGHT_SIGNAL.connect(self.highlightPlayingMeasure)

    def _initializeState(self):
        props = self.songProperties
        scene = self.scoreScene
        self.scoreView.setScene(scene)
        self._connectSignals(props, scene)
        # Fonts
        self.fontComboBox.setWritingSystem(QFontDatabase.Latin)
        self.sectionFontCombo.setWritingSystem(QFontDatabase.Latin)
        self.sectionFontCombo.setWritingSystem(QFontDatabase.Latin)
        self.lineSpaceSlider.setValue(scene.systemSpacing)
        font = props.noteFont
        if font is None:
            font = scene.font()
        font.setPointSize(props.noteFontSize)
        self.fontComboBox.setCurrentFont(font)
        self.noteSizeSpinBox.setValue(props.noteFontSize)
        font = props.sectionFont
        if font is None:
            font = scene.font()
        font.setPointSize(props.sectionFontSize)
        self.sectionFontCombo.setCurrentFont(font)
        self.sectionFontSizeSpinbox.setValue(props.sectionFontSize)
        font = props.metadataFont
        if font is None:
            font = scene.font()
        font.setPointSize(props.metadataFontSize)
        self.metadataFontCombo.setCurrentFont(font)
        self.metadataFontSizeSpinbox.setValue(props.metadataFontSize)
        # Visibility toggles
        self.actionShowDrumKey.setChecked(props.kitDataVisible)
        self.actionShowEmptyLines.setChecked(props.emptyLinesVisible)
        self.actionShowScoreInfo.setChecked(props.metadataVisible)
        self.actionShowBeatCount.setChecked(props.beatCountVisible)
        self.actionShowMeasureCounts.setChecked(props.measureCountsVisible)
        # Set doable actions
        self.actionPlayOnce.setEnabled(False)
        self.actionLoopBars.setEnabled(False)
        self.actionCopyMeasures.setEnabled(False)
        self.actionPasteMeasures.setEnabled(False)
        self.actionFillPasteMeasures.setEnabled(False)
        self.actionClearMeasures.setEnabled(False)
        self.actionDeleteMeasures.setEnabled(False)
        self.MIDIToolBar.setEnabled(DBMidi.HAS_MIDI)
        # Undo/redo
        self.actionUndo.setEnabled(False)
        self.actionRedo.setEnabled(False)
        scene.canUndoChanged.connect(self.actionUndo.setEnabled)
        changeUndoText = lambda txt:self.actionUndo.setText("Undo " + txt)
        scene.undoTextChanged.connect(changeUndoText)
        scene.canRedoChanged.connect(self.actionRedo.setEnabled)
        changeRedoText = lambda txt:self.actionRedo.setText("Redo " + txt)
        scene.redoTextChanged.connect(changeRedoText)
        # Default beat
        self._beatChanged(scene.defaultCount)
        self.widthSpinBox.setValue(scene.scoreWidth)
        self.lilypondSize.setValue(scene.score.lilysize)
        self.lilyPagesBox.setValue(scene.score.lilypages)
        self.lilyFillButton.setChecked(scene.score.lilyFill)


    def _startUp(self, errored_files):
        self.scoreView.startUp()
        self.updateStatus("Welcome to %s v%s" % (APPNAME, DB_VERSION))
        self.scoreView.setFocus()
        if self.actionCheckOnStartup.isChecked():
#             self.on_actionCheckForUpdates_triggered()
            self._versionThread.start()
        if errored_files:
            QMessageBox.warning(self, "Problem during startup",
                                "Error opening files:\n %s" % "\n".join(errored_files))


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

    def _setMeasureCountsVisible(self):
        props = self.songProperties
        if props.measureCountsVisible != self.actionShowMeasureCounts.isChecked():
            self.actionShowMeasureCounts.setChecked(props.measureCountsVisible)

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
            settings.setValue("CheckOnStartup",
                              QVariant(self.actionCheckOnStartup.isChecked()))
            self._writeColours(settings)
            self.songProperties.save(settings)
            self._versionThread.exit()
            self._versionThread.wait(1000)
            if not self._versionThread.isFinished():
                self._versionThread.terminate()
        else:
            event.ignore()

    def _writeColours(self, settings):
        for unusedName, colourRef in self.colourScheme.iterColourNames():
            colourItem = getattr(self.colourScheme, colourRef)
            settings.setValue("Colours/" + colourRef,
                              QVariant(colourItem.toString()))
                
    def _readColours(self, settings):
        for unusedName, colourRef in self.colourScheme.iterColourNames():
            colourItem = getattr(self.colourScheme, colourRef)
            if not settings.contains("Colours/" + colourRef):
                continue
            colourItem.fromString(settings.value("Colours/" + colourRef).toString())

    @pyqtSignature("")
    def on_actionFitInWindow_triggered(self):
        widthInPixels = self.scoreView.width()
        maxColumns = self.songProperties.maxColumns(widthInPixels)
        self.widthSpinBox.setValue(maxColumns)
        self.scoreScene.reBuild()

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
            self.lilypondSize.setValue(self.scoreScene.score.lilysize)
            self.lilyPagesBox.setValue(self.scoreScene.score.lilypages)
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
                directory = unicode(QDesktopServices.storageLocation(home))
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
            dialog = QNewScoreDialog(self,
                                     counter,
                                     registry)
            if dialog.exec_():
                nMeasures, counter, kit = dialog.getValues()
                self.scoreScene.newScore(kit,
                                         numMeasures = nMeasures,
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
        asciiDialog = QAsciiExportDialog(fname, parent = self,
                                         settings = self._asciiSettings)
        if not asciiDialog.exec_():
            return
        fname = asciiDialog.getFilename()
        self._asciiSettings = asciiDialog.getOptions()
        try:
            asciiBuffer = StringIO()
            exporter = AsciiExport.Exporter(self.scoreScene.score,
                                            self._asciiSettings)
            exporter.export(asciiBuffer)
        except StandardError:
            QMessageBox.warning(self.parent(), "ASCII generation failed!",
                                "Could not generate ASCII for this score!")
            raise
        try:
            with open(fname, 'w') as txtHandle:
                txtHandle.write(asciiBuffer.getvalue())
        except StandardError:
            QMessageBox.warning(self.parent(), "Export failed!",
                                "Could not export to " + fname)
            raise
        else:
            self.updateStatus("Successfully exported ASCII to " + fname)

    @pyqtSignature("")
    def on_actionPrint_triggered(self):
        if self._printer is None:
            self._printer = QPrinter()
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

    @pyqtSignature("")
    def on_actionExportLilypond_triggered(self):
        lilyBuffer = StringIO()
        try:
            lyScore = LilypondScore(self.scoreScene.score)
            lyScore.write(lilyBuffer)
        except LilypondProblem, exc:
            QMessageBox.warning(self.parent(), "Lilypond impossible",
                                "Cannot export Lilypond for this score: %s"
                                % exc.__doc__)
        except StandardError, exc:
            QMessageBox.warning(self.parent(), "Export failed!",
                                "Error generating Lilypond for this score: %s"
                                % exc.__doc__)
            raise
        else:
            try:
                if self.filename:
                    filestem = os.path.splitext(self.filename)[:-1]
                    outfileName = os.path.extsep.join(filestem)
                    directory = os.path.abspath(outfileName)
                else:
                    outfileName = "Untitled.ly"
                    loc = QDesktopServices.HomeLocation
                    home = unicode(QDesktopServices.storageLocation(loc))
                    directory = os.path.join(home, outfileName)
                caption = "Choose a Lilypond input file to write to"
                fname = QFileDialog.getSaveFileName(parent = self,
                                                    caption = caption,
                                                    directory = directory,
                                                    filter = "(*.ly)")
                if len(fname) == 0:
                    return
                fname = unicode(fname)
                with open(fname, 'w') as handle:
                    handle.write(lilyBuffer.getvalue())
            except StandardError:
                QMessageBox.warning(self.parent(), "Export failed!",
                                    "Could not export Lilypond")
                raise
            else:
                self.updateStatus("Successfully exported Lilypond to " + fname)

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

    @pyqtSignature("")
    def on_actionAboutDrumBurp_triggered(self):
        dlg = DBInfoDialog(DB_VERSION, self)
        dlg.exec_()

    @staticmethod
    @pyqtSignature("")
    def on_actionOnlineManual_triggered():
        webbrowser.open_new_tab("www.whatang.org/drumburp-manual")

    def _getPaperSize(self):
        try:
            return getattr(QPrinter, str(self.paperBox.currentText()))
        except AttributeError:
            return QPrinter.Letter

    @pyqtSignature("")
    def on_actionFitPage_triggered(self):
        papersize = self._getPaperSize()
        printer = QPrinter()
        printer.setPaperSize(papersize)
        widthInPixels = printer.pageRect().width()
        maxColumns = self.songProperties.maxColumns(widthInPixels)
        self.widthSpinBox.setValue(maxColumns)
        self.scoreScene.reBuild()

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
            unused = list(self.scoreScene.score.iterMeasuresWithRepeats())
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
            self.musicStart()
        else:
            self.musicDone()
            DBMidi.shutUp()

    def highlightPlayingMeasure(self, index):
        if index == -1:
            self.scoreScene.highlightPlayingMeasure(None)
        else:
            position = self.scoreScene.score.getMeasurePosition(index)
            self.scoreScene.highlightPlayingMeasure(position)
            measure = self.scoreScene.getQMeasure(position)
            self.scoreView.ensureVisible(measure)

    @staticmethod
    @pyqtSignature("bool")
    def on_actionMuteNotes_toggled(onOff):
        DBMidi.setMute(onOff)

    @pyqtSignature("")
    def on_actionExportMIDI_triggered(self):
        if not self._canPlayback():
            return
        try:
            midiBuffer = StringIO()
            DBMidi.exportMidi(self.scoreScene.score.iterMeasuresWithRepeats(),
                              self.scoreScene.score, midiBuffer)
        except StandardError, exc:
            QMessageBox.warning(self.parent(), "Error generating MIDI!",
                                "Failed to generate MIDI for this score: %s"
                                % exc.__doc__)
            raise
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
        try:
            with open(fname, 'wb') as handle:
                handle.write(midiBuffer.getvalue())
        except StandardError:
            QMessageBox.warning(self.parent(), "File error",
                                "Error writing MIDI to file %s" % fname)

    @pyqtSignature("bool")
    def on_actionLoopBars_toggled(self, onOff):
        if onOff:
            if not self.scoreScene.hasDragSelection():
                self.actionLoopBars.toggle()
                return
            DBMidi.loopBars(self.scoreScene.iterDragSelection(),
                            self.scoreScene.score)
            self.musicStart()
        else:
            self.musicDone()
            DBMidi.shutUp()

    @pyqtSignature("bool")
    def on_actionPlayOnce_toggled(self, onOff):
        if onOff:
            if not self.scoreScene.hasDragSelection():
                self.actionPlayOnce.toggle()
                return
            DBMidi.loopBars(self.scoreScene.iterDragSelection(),
                            self.scoreScene.score,
                            loopCount = 1)
            self.musicStart()
        else:
            self.musicDone()
            DBMidi.shutUp()

    @pyqtSignature("")
    def on_actionCopyMeasures_triggered(self):
        self.scoreScene.copyMeasures()

    def checkPasteMeasure(self):
        onOff = (self.scoreScene.hasDragSelection() and
                 len(self.scoreScene.measureClipboard) > 0)
        self.actionPasteMeasures.setEnabled(onOff)
        self.actionFillPasteMeasures.setEnabled(onOff)

    @pyqtSignature("")
    def on_actionPasteMeasures_triggered(self):
        self.scoreScene.pasteMeasuresOver()

    @pyqtSignature("")
    def on_actionFillPasteMeasures_triggered(self):
        self.scoreScene.pasteMeasuresOver(repeating = True)

    @pyqtSignature("")
    def on_actionClearMeasures_triggered(self):
        self.scoreScene.clearMeasures()

    @pyqtSignature("")
    def on_actionDeleteMeasures_triggered(self):
        self.scoreScene.deleteMeasures()

    def musicStart(self):
        self.scoreScene.sendFsmEvent(StartPlaying())

    def musicDone(self):
        players = [self.actionPlayScore, self.actionPlayOnce,
                   self.actionLoopBars]
        for playButton in players:
            if playButton.isChecked():
                playButton.setChecked(False)
        self.scoreScene.sendFsmEvent(StopPlaying())

    def _scorePlaying(self, playing):
        self.fileToolBar.setDisabled(playing)
        self.exportToolBar.setDisabled(playing)
        self.displayToolBar.setDisabled(playing)
        self.helpToolBar.setDisabled(playing)
        self.fontDock.setDisabled(playing)
        self.scorePropertiesGroup.setDisabled(playing)
        self.menubar.setDisabled(playing)
        self.actionExportMIDI.setDisabled(playing)
        self.actionMuteNotes.setDisabled(playing)
        self.lilypondGroupBox.setDisabled(playing)

    @pyqtSignature("int")
    def on_paperBox_currentIndexChanged(self, index):
        self._pageHeight = self._knownPageHeights[index]
        self.sceneFormatted()

    def sceneFormatted(self):
        if self.scoreScene:
            numMeasures = self.scoreScene.score.numMeasures()
            measureText = "%d Measure" % numMeasures
            if numMeasures > 1:
                measureText += "s"
            numStaffs = self.scoreScene.score.numStaffs()
            staffText = "%d Staff" % numStaffs
            if numStaffs > 1:
                staffText += "s"
            numPages = self.scoreScene.numPages(self._pageHeight)
            pagetext = "%d Page" % numPages
            if numPages > 1:
                pagetext += "s"
            self._infoBar.setText(", ".join([measureText, staffText, pagetext]))

    def _setStatusFromScene(self, msg):
        self.statusbar.showMessage(msg)

    def _setLilySize(self, size):
        if size != self.lilypondSize.value():
            self.lilypondSize.setValue(size)

    def _setLilyPages(self, numPages):
        if numPages != self.lilyPagesBox.value():
            self.lilyPagesBox.setValue(numPages)

    def _setLilyFill(self, lilyFill):
        if lilyFill != self.lilyFillButton.isChecked():
            self.lilyFillButton.setChecked(lilyFill)

    @pyqtSignature("")
    def on_actionCheckForUpdates_triggered(self):
        dialog = QVersionDownloader(newer = None, parent = self)
        dialog.exec_()
        
    def _finishedVersionCheck(self):
        newer = self._versionThread.newVersionInfo
        if newer:
            dialog = QVersionDownloader(newer = newer, parent = self)
            dialog.exec_()
        elif newer is None:
            self.statusbar.showMessage("Failed to get latest version info from www.whatang.org", 5000)
        else:
            self.statusbar.showMessage("Check successful: You have the latest version of DrumBurp", 5000)

    @pyqtSignature("")
    def on_actionEditColours_triggered(self):
        dialog = DBColourPicker.DBColourPicker(self.colourScheme, self)
        if not dialog.exec_():
            return
        self.colourScheme = dialog.getColourScheme()

class VersionCheckThread(QThread):
    def __init__(self, parent = None):
        super(VersionCheckThread, self).__init__(parent = parent)
        self.newVersionInfo = None

    def run(self):
        self.newVersionInfo = doesNewerVersionExist()
