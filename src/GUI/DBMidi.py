'''
Created on 17 Sep 2011

@author: Mike Thomas

'''

import pygame
import pygame.midi
import atexit
import time
from PyQt4 import QtGui
from PyQt4.QtCore import QTimer, pyqtSignal, QObject
from Data.MeasureCount import MIDITICKSPERBEAT

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
        self.kit = None

    def setMute(self, onOff):
        self._mute = onOff

    highlightMeasure = pyqtSignal(int)

    def playNote(self, drumIndex, head):
        if self.kit is None or self._mute:
            return
        headData = self.kit[drumIndex].headData(head)
        self.playHeadData(headData)

    def playHeadData(self, headData):
        self._midiOut.write([[[_PERCUSSION, headData.midiNote,
                               headData.midiVolume],
                              pygame.midi.time()]])

    def playScore(self, score):
        if self.kit is None:
            return
        baseTime = 0
        msPerBeat = 60000.0 / score.scoreData.bpm
        notes = []
        self._measureDetails = []
        for measureIndex, measure in enumerate(score.iterMeasures()):
            times = list(measure.counter.iterFloatBeat())
            for notePos, head in measure:
                drumData = self.kit[notePos.drumIndex]
                headData = drumData.headData(head)
                if headData is not None:
                    noteTime = (baseTime + times[notePos.noteTime]) * msPerBeat
                    notes.append((noteTime, headData))
            baseTime += measure.counter.floatBeats()
            self._measureDetails.append((measureIndex, baseTime * msPerBeat))
        self._measureDetails.reverse()
        numNotes = len(notes)
        index = 0
        latency = numNotes * _LATENCYPERNOTE
        del self._midiOut
        self._midiOut = pygame.midi.Output(self._port, latency, _BUFSIZE)
        midiTime = pygame.midi.time()
        self._songStart = time.clock() + latency / 1000.0
        while index < numNotes:
            midiNotes = [[[_PERCUSSION, headData.midiNote, headData.midiVolume],
                          midiTime + noteTime]
                         for (noteTime, headData) in
                         notes[index:index + _NOTESPERSEND]]
            self._midiOut.write(midiNotes)
            index += _NOTESPERSEND
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
        delay = -1
        measureIndex = None
        while delay < 0 and self._measureDetails:
            measureIndex, measureEnd = self._measureDetails.pop()
            delay = (measureEnd - 1000 * (time.clock() - self._songStart))
        if measureIndex is not None:
            self.highlightMeasure.emit(measureIndex)
        if delay > 0:
            self._measureTimer.start(delay)


_PLAYER = _midi()

SONGEND_SIGNAL = _PLAYER.timer.timeout
HIGHLIGHT_SIGNAL = _PLAYER.highlightMeasure

def setKit(drumKit):
    _PLAYER.kit = drumKit

def playNote(drumIndex, head):
    _PLAYER.playNote(drumIndex, head)

def playHeadData(headData):
    _PLAYER.playHeadData(headData)

def playScore(score):
    _PLAYER.playScore(score)

def shutUp():
    _PLAYER.shutUp()

def setMute(onOff):
    _PLAYER.setMute(onOff)

def encodeSevenBitDelta(delta, midiData):
    values = []
    lastByte = True
    if delta == 0:
        midiData.append(0)
        return
    while delta:
        thisValue = (delta & 0x7F)
        delta >>= 7
        if lastByte:
            lastByte = False
        else:
            delta |= 0x80
        values.append(thisValue)
    values.reverse()
    midiData.extend(values)

def exportMidi(score, handle):
    handle.write("MThd\x00\x00\x00\x06\x00\x00\x00\x01")
    handle.write("%c" % chr((MIDITICKSPERBEAT >> 8) & 0xFF))
    handle.write("%c" % chr((MIDITICKSPERBEAT >> 0) & 0xFF))
    notes = []
    baseTime = 0
    for measure in score.iterMeasures():
        times = list(measure.counter.iterMidiTicks())
        for notePos, head in measure:
            drumData = score.drumKit[notePos.drumIndex]
            headData = drumData.headData(head)
            if headData is not None:
                noteTime = baseTime + times[notePos.noteTime]
                notes.append((noteTime, headData))
        baseTime += times[-1]
    lastNoteTime = 0
    msPerBeat = int(60000000 / score.scoreData.bpm)
    midiData = [0, 0xff, 0x51, 03, (msPerBeat >> 16) & 0xff,
                (msPerBeat >> 8) & 0xff, msPerBeat & 0xff]
    signature = "Created with DrumBurp"
    midiData.extend([0, 0xff, 0x1, len(signature)])
    midiData.extend([ord(ch) for ch in signature])
    for noteTime, headData in notes:
        deltaTime = noteTime - lastNoteTime
        lastNoteTime = noteTime
        encodeSevenBitDelta(deltaTime, midiData)
        midiData.extend([0x99, headData.midiNote, headData.midiVolume])
    midiData.extend([0, 0xFF, 0x2F, 0])
    numBytes = len(midiData)
    lenBytes = [((numBytes >> i) & 0xff) for i in xrange(24, -8, -8)]
    midiData = lenBytes + midiData
    handle.write("MTrk")
    for byte in midiData:
        handle.write("%c" % byte)

atexit.register(_PLAYER.cleanup)

