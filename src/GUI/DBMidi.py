'''
Created on 17 Sep 2011

@author: Mike Thomas

'''

import pygame
import pygame.midi
import atexit
import time
from PyQt4.QtCore import QTimer, pyqtSignal, QObject

pygame.init()
pygame.midi.init()

_PERCUSSION = 0x99
_BUFSIZE = 8192
_NOTESPERSEND = 1024
_LATENCYPERNOTE = 1
_VELOCITY = 127

class _midi(QObject):
    def __init__(self):
        super(_midi, self).__init__()
        self._port = pygame.midi.get_default_output_id()
        self._midiOut = pygame.midi.Output(self._port, 0, _BUFSIZE)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.shutUp)
        self._measureDetails = []
        self._measureTimer = QTimer()
        self._measureTimer.setSingleShot(True)
        self._measureTimer.timeout.connect(self._highlight)
        self._songStart = None
        self._mute = False

    def setMute(self, onOff):
        self._mute = onOff

    highlightMeasure = pyqtSignal(int)

    def playNote(self, note):
        if not self._mute:
            self._midiOut.write([[[_PERCUSSION, note, _VELOCITY],
                                  pygame.midi.time()]])

    def playScore(self, score):
        start = time.clock()
        baseTime = 0
        msPerBeat = 60000.0 / score.scoreData.bpm
        notes = []
        for measureIndex, measure in enumerate(score.iterMeasures()):
            times = list(measure.counter.iterFloatBeat())
            for notePos, unusedHead in measure:
                drumIndex = _NOTEMAP.get(notePos.drumIndex, 71)
                if drumIndex is not None:
                    noteTime = (baseTime + times[notePos.noteTime]) * msPerBeat
                    notes.append((noteTime, drumIndex))
            baseTime += measure.counter.floatBeats()
            self._measureDetails.append((measureIndex, baseTime * msPerBeat))

        self._measureDetails.reverse()
#        print "Built notes", time.clock() - start
        numNotes = len(notes)
        index = 0
        latency = numNotes * _LATENCYPERNOTE
        del self._midiOut
        self._midiOut = pygame.midi.Output(self._port, latency, _BUFSIZE)
#        print "Ready to send notes", time.clock() - start
        midiTime = pygame.midi.time()
        self._songStart = time.clock() + latency / 1000.0
        while index < numNotes:
            midiNotes = [[[_PERCUSSION, drumIndex, _VELOCITY], midiTime + noteTime]
                         for (noteTime, drumIndex) in
                         notes[index:index + _NOTESPERSEND]]
#            print "Made notes", time.clock() - start
            self._midiOut.write(midiNotes)
            index += _NOTESPERSEND
#            print "Sent notes", time.clock() - start, index
#        print "Sent %d notes" % numNotes, time.clock() - start
        self.timer.start(baseTime * msPerBeat + latency)
        self._measureTimer.start(latency)


    def shutUp(self):
        self.timer.stop()
        self._measureTimer.stop()
        del self._midiOut
        self.highlightMeasure.emit(-1)
        self._midiOut = pygame.midi.Output(self._port, 0, _BUFSIZE)

    def cleanup(self):
        self._midiOut.abort()
        del self._midiOut

    def _highlight(self):
        measureIndex, measureEnd = self._measureDetails.pop()
        self._measureTimer.start(measureEnd -
                                 1000 * (time.clock() - self._songStart))
        self.highlightMeasure.emit(measureIndex)
#        print measureIndex, measureEnd, measureEnd - 1000 * (time.clock() - self._songStart)

_NOTEMAP = {}

_PLAYER = _midi()

SONGEND_SIGNAL = _PLAYER.timer.timeout
HIGHLIGHT_SIGNAL = _PLAYER.highlightMeasure

def setKit(drumKit):
    _NOTEMAP.clear()
    for index, drum in enumerate(drumKit):
        _NOTEMAP[index] = drum.midiNote

def playNote(drumIndex):
    note = _NOTEMAP.get(drumIndex, 71)
    if note is not None:
        _PLAYER.playNote(note)

def playScore(score):
    _PLAYER.playScore(score)

def shutUp():
    _PLAYER.shutUp()

def setMute(onOff):
    _PLAYER.setMute(onOff)

atexit.register(_PLAYER.cleanup)

