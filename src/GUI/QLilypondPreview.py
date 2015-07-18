'''
Created on Feb 28, 2015

@author: mike_000
'''
from PyQt4.QtCore import pyqtSignal, QTimeLine
from PyQt4.QtGui import QMessageBox, QGraphicsScene, QPixmap
import tempfile
from StringIO import StringIO
import os.path
import os
import glob

from Notation.lilypond import LilypondScore, LilypondProblem
from GUI.LilypondExporter import LilypondExporter

class QLilypondPreview(QGraphicsScene):
    buildCompleted = pyqtSignal()

    def __init__(self, parent):
        super(QLilypondPreview, self).__init__(parent = parent)
        self.mainWindow = parent
        self._tempdir = tempfile.mkdtemp(prefix = "DrumBurpLilypondPreviewTemp_")
        self._exporter = None
        self.buildCompleted.connect(self._built)
        self._pageIndex = None
        self._pages = []
        self._pixmap = None
        self._waiting = self.addText("Building...")
        font = self._waiting.font()
        font.setPointSize(48)
        self._waiting.setFont(font)
        self._waiting.setOpacity(0.6)
        self._waiting.setVisible(False)
        self._waitingTimer = QTimeLine(2500, self)
        self._waitingTimer.setUpdateInterval(100)
        self._waitingTimer.setFrameRange(0, 5)
        self._waitingTimer.setLoopCount(0)
        self._waitingTimer.setCurveShape(self._waitingTimer.LinearCurve)
        self._waitingTimer.frameChanged.connect(self._updateWaitingText)
        self._noPreview = self.addText("No Preview")
        self._noPreview.setOpacity(0.6)
        self._noPreview.setVisible(False)
        self._noPreview.setFont(font)
        self._displayPage()
        self.mainWindow.refreshLilypond.setText("Preview")

    def _updateWaitingText(self, frameVal):
        if frameVal < 5:
            self._waiting.setPlainText("Building" + ("." * frameVal))

    @property
    def qscore(self):
        return self.mainWindow.scoreScene

    @property
    def score(self):
        return self.qscore.score

    def preview(self):
        # Make lilypond score string
        self.mainWindow.checkLilypondPath()
        lilyBuffer = StringIO()
        try:
            lyScore = LilypondScore(self.score)
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
        fname = os.path.join(self._tempdir, 'db.ly')
        # Check exporter is not already running
        if self._exporter is not None:
            if self._exporter.isRunning():
                QMessageBox.warning(self.parent(), "Still previewing",
                                    "Cannot preview now - previous preview build is still in progress")
                return
        # Disable controls
        self._setLilypondControlsEnabled(False)
        # Show waiting animation/message
        self._noPreview.setVisible(False)
        self._waiting.setVisible(True)
        self._waitingTimer.start()
        self._pageIndex = None
        if self._pixmap is not None:
            self.removeItem(self._pixmap)
        self._pixmap = None
        self.setSceneRect(self._waiting.boundingRect())
        # Send to exporter
        self._exporter = LilypondExporter(lilyBuffer.getvalue(), fname,
                                          self.mainWindow.lilyPath, 'png',
                                          self.buildCompleted.emit,
                                          self.mainWindow)
        pngFiles = glob.glob(os.path.join(self._tempdir, 'db*.png'))
        for pngFile in pngFiles:
            os.unlink(pngFile)
        self._exporter.start()

    def _setLilypondControlsEnabled(self, onOff):
        self.mainWindow.lilyPreviewControls.setEnabled(onOff)
        self.mainWindow.setLilypondControlsEnabled(onOff)

    def _built(self):
        try:
            # TODO: Remove waiting anim/message
            self._waiting.setVisible(False)
            self._waitingTimer.stop()
            # Check build results from exporter
            status = self._exporter.get_status()
            if status == self._exporter.SUCCESS:
                # Get pages of exported score & display them
                self._readPages()
                # Update button from 'Preview' to 'Refresh'
                self.mainWindow.refreshLilypond.setText("Refresh")
                return
            elif status == self._exporter.WROTE_LY:
                QMessageBox.warning(self.parent(), 'Build failed!',
                                    "DrumBurp exported this score to Lilypond format but could not find a Lilypond executable to run.")
            elif status == self._exporter.ERROR_IN_WRITING_LY:
                QMessageBox.warning(self.parent(), "Build failed!",
                                    "DrumBurp had a problem writing the Lilypond format to a temporary file.")
            elif status == self._exporter.ERROR_IN_RUNNING_LY:
                QMessageBox.warning(self.parent(), "Build failed!",
                                    "Lilypond had an error when trying to run on this score.")
            self.setNoPreview()
        finally:
            # Enable controls
            self._setLilypondControlsEnabled(True)

    def _readPages(self):
        pngFiles = glob.glob(os.path.join(self._tempdir, 'db*.png'))
        pngFiles.sort()
        self._pages = [QPixmap(pngFile) for pngFile in pngFiles]
        if self._pageIndex is None:
            self._pageIndex = 0
        self._pageIndex = min([self._pageIndex, len(self._pages) - 1])
        self._displayPage()

    def _displayPage(self):
        if len(self._pages) > 0:
            self._noPreview.setVisible(False)
            if self._pixmap is None:
                self._pixmap = self.addPixmap(self._pages[self._pageIndex])
            else:
                self._pixmap.setPixmap(self._pages[self._pageIndex])
            self.setSceneRect(self._pixmap.boundingRect())
        else:
            self._pageIndex = None
            if self._pixmap is not None:
                self.removeItem(self._pixmap)
            self._pixmap = None
            self._noPreview.setVisible(True)
            self.setSceneRect(self._noPreview.boundingRect())
        self._checkButtons()

    def setNoPreview(self):
        self._pages = []
        self.mainWindow.refreshLilypond.setText("Preview")
        self._displayPage()

    def cleanup(self):
        for toDelete in glob.glob(os.path.join(self._tempdir, '*')):
            os.unlink(toDelete)
        os.rmdir(self._tempdir)
        if self._exporter is not None and self._exporter.isRunning():
            self._exporter.exit()
            self._exporter.wait(1000)
            if self._exporter.isRunning():
                self._exporter.terminate()

    def _checkButtons(self):
        self.mainWindow.nextLilyPage.setEnabled(self._pageIndex is not None and
                                                self._pageIndex <
                                                len(self._pages) - 1)
        self.mainWindow.prevLilyPage.setEnabled(self._pageIndex is not None and
                                                self._pageIndex > 0)
        self.mainWindow.lastLilyPage.setEnabled(self._pageIndex is not None and
                                                self._pageIndex <
                                                len(self._pages) - 1)
        self.mainWindow.firstLilyPage.setEnabled(self._pageIndex is not None and
                                                 self._pageIndex > 0)

    def previousPage(self):
        if self._pageIndex > 0:
            self._pageIndex -= 1
            self._displayPage()

    def nextPage(self):
        if self._pageIndex < len(self._pages) - 1:
            self._pageIndex += 1
            self._displayPage()

    def firstPage(self):
        self._pageIndex = 0
        self._displayPage()

    def lastPage(self):
        self._pageIndex = len(self._pages) - 1
        self._displayPage()
