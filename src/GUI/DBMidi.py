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
Created on 17 Sep 2011

@author: Mike Thomas

'''

HAS_MIDI = True
_PERCUSSION = 0x99
_BUFSIZE = 1024

_FREQ = 44100    # audio CD quality
_BITSIZE = -16   # unsigned 16 bit
_CHANNELS = 2    # 1 is mono, 2 is stereo
_NUMSAMPLES = 4096    # number of samples

try:
    import pygame
    import pygame.midi
    pygame.init()
    pygame.midi.init()
    pygame.mixer.init(_FREQ, _BITSIZE, _CHANNELS, _NUMSAMPLES)
    pygame.mixer.music.set_volume(0.8)

    def get_default_id():
        return pygame.midi.get_default_output_id()

    def cleanup():
        _PLAYER.cleanup()
        pygame.mixer.quit()
        pygame.midi.quit()
        pygame.quit()

except ImportError:
    HAS_MIDI = False
    def get_default_id():
        return -1

    def cleanup():
        _PLAYER.cleanup()

import atexit
atexit.register(cleanup)
import time
import StringIO

from PyQt4.QtCore import QTimer, pyqtSignal, QObject
from Data.MeasureCount import MIDITICKSPERBEAT

class _midi(QObject):
    def __init__(self):
        super(_midi, self).__init__()
        self._port = get_default_id()
        self._midiOut = None
        if self._port != -1:
            self._midiOut = pygame.midi.Output(self._port, 0, _BUFSIZE)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self._measureDetails = []
        self._measureTimer = QTimer()
        self._measureTimer.setSingleShot(True)
        self._measureTimer.timeout.connect(self._highlight)
        self._songStart = None
        self._mute = False
        self._musicPlaying = False
        self.kit = None

    def isGood(self):
        return self._port != -1 and self._midiOut is not None

    def setMute(self, onOff):
        self._mute = onOff

    def isMuted(self):
        return self._mute

    highlightMeasure = pyqtSignal(int)

    def playNote(self, drumIndex, head):
        if self.kit is None or self._mute:
            return
        headData = self.kit[drumIndex].headData(head)
        self.playHeadData(headData)

    def playHeadData(self, headData):
        if self._midiOut:
            self._midiOut.write([[[_PERCUSSION, headData.midiNote,
                                   headData.midiVolume],
                                  pygame.midi.time()]])

    def playScore(self, score):
        measureList = list(score.iterMeasuresWithRepeats())
        self._playMIDINow(measureList, score)

    def _playMIDINow(self, measureList, score):
        if self.kit is None or self._midiOut is None:
            return
        baseTime = 0
        msPerBeat = 60000.0 / score.scoreData.bpm
        self._measureDetails = []
        try:
            for measure, measureIndex in measureList:
                times = list(measure.counter.iterTimesMs(msPerBeat))
                baseTime += times[-1]
                self._measureDetails.append((measureIndex, baseTime))
            self._measureDetails.reverse()
            del self._midiOut
            self._midiOut = None
            midi = StringIO.StringIO()
            exportMidi(measureList, score, midi)
            midi.seek(0, 0)
            pygame.mixer.music.load(midi)
            pygame.mixer.music.play()
            self._songStart = time.clock()
            self._musicPlaying = True
        except:
            self.timer.timeout.emit()
            raise
        self.timer.start(baseTime + 500)
        self._measureTimer.start(0)

    def loopBars(self, measureIterator, score, loopCount = 100):
        measureList = [(measure, measureIndex) for
                       (measure, measureIndex, unused)
                       in measureIterator] * loopCount
        self._playMIDINow(measureList, score)

    def shutUp(self):
        if self._musicPlaying:
            self.timer.stop()
            self._measureDetails = []
            self._measureTimer.stop()
            self.highlightMeasure.emit(-1)
            if self._midiOut:
                del self._midiOut
            pygame.mixer.music.stop()
            self._midiOut = pygame.midi.Output(self._port, 0, _BUFSIZE)
            self._musicPlaying = False

    def cleanup(self):
        if self._midiOut is not None:
            self._midiOut.abort()
            del self._midiOut
            self._midiOut = None

    def _highlight(self):
        delay = -1
        measureIndex = None
        while delay < 0 and self._measureDetails:
            measureIndex, measureEnd = self._measureDetails.pop()
            delay = (measureEnd - 1000 * (time.clock() - self._songStart))
        if measureIndex is not None:
            self.highlightMeasure.emit(measureIndex)
        else:
            self.highlightMeasure.emit(-1)
        if delay > 0:
            self._measureTimer.start(delay)


_PLAYER = _midi()
HAS_MIDI = HAS_MIDI and _PLAYER.isGood()

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

def loopBars(measureIterator, score, loopCount = 100):
    _PLAYER.loopBars(measureIterator, score, loopCount)

def shutUp():
    _PLAYER.shutUp()

def setMute(onOff):
    _PLAYER.setMute(onOff)

def isMuted():
    return _PLAYER.isMuted()

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
            thisValue |= 0x80
        values.append(thisValue)
    values.reverse()
    midiData.extend(values)

def exportMidi(measureIterator, score, handle):
    handle.write("MThd\x00\x00\x00\x06\x00\x00\x00\x01")
    handle.write("%c" % chr((MIDITICKSPERBEAT >> 8) & 0xFF))
    handle.write("%c" % chr((MIDITICKSPERBEAT >> 0) & 0xFF))
    notes = []
    baseTime = 1
    for measure, unusedIndex in measureIterator:
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
        midiData.extend([_PERCUSSION,
                         headData.midiNote,
                         headData.midiVolume])
    # Turn off drum notes
    deltaTime = baseTime - lastNoteTime
    encodeSevenBitDelta(deltaTime + 4 * MIDITICKSPERBEAT, midiData)
    midiData.extend([0x89, 38, 0])
    # Insert a delay before the end of the track.
    encodeSevenBitDelta(0, midiData)
    midiData.extend([0xFF, 0x2F, 0])
    numBytes = len(midiData)
    lenBytes = [((numBytes >> i) & 0xff) for i in xrange(24, -8, -8)]
    midiData = lenBytes + midiData
    handle.write("MTrk")
    for byte in midiData:
        handle.write("%c" % byte)
