# Copyright 2011-2015 Michael Thomas
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
import copy

HAS_MIDI = False
_MIDI_INITIALIZED = False
_PERCUSSION_CHANNEL = 0x09
_NOTE_ON = 0x90
_NOTE_OFF = 0x80
_CHOKE = 0xB0
_CHOKE_MSG = 120
_CHOKE_VELOCITY = 0
_PERCUSSION_NOTE_ON = _PERCUSSION_CHANNEL | _NOTE_ON
_PERCUSSION_NOTE_OFF = _PERCUSSION_CHANNEL | _NOTE_OFF
_PERCUSSION_CHOKE = _PERCUSSION_CHANNEL | _CHOKE
_BUFSIZE = 1024
_LATENCY = 1

_FREQ = 44100  # audio CD quality
_BITSIZE = -16  # unsigned 16 bit
_CHANNELS = 2  # 1 is mono, 2 is stereo
_NUMSAMPLES = 4096  # number of samples

FLAM_TIME_CONSTANT = 32
FLAM_VOLUME_CONSTANT = 2
DRAG_TIME_CONSTANT = 96

from PyQt4.Qt import QThread
import atexit
import time
import StringIO

try:
    import pygame
    import pygame.midi
    _HAS_PYGAME = True

    def getDefaultId():
        return pygame.midi.get_default_output_id()

    def iterDeviceIds():
        return xrange(pygame.midi.get_count())

    def getDeviceInfo(deviceId):
        int_, name, isIn, isOut, isOpen = pygame.midi.get_device_info(deviceId)
        return name, isIn == 1, isOut == 1, isOpen == 1

    def cleanup():
        _PLAYER.cleanup()
        pygame.mixer.quit()
        pygame.midi.quit()
        pygame.quit()  # IGNORE:no-member

except ImportError:
    _HAS_PYGAME = False
    def getDefaultId():
        return -1

    def iterDeviceIds():
        return iter([])

    def getDeviceInfo(deviceId_):
        return None, False, False, False

    def cleanup():
        if _PLAYER is not None:
            _PLAYER.cleanup()

class MidiDevice(object):
    def __init__(self, deviceId):
        self.deviceId = deviceId
        self.name, in_, self._isOutput, self._isOpen = getDeviceInfo(deviceId)
        self._isValid = self.name is not None

    def isValid(self):
        return self._isValid

    def isOutput(self):
        return self._isOutput

    def isOpen(self):
        return getDeviceInfo(self.deviceId)[3]

_OUTPUT_DEVICES = []
def refreshOutputDevices():
    while _OUTPUT_DEVICES:
        _OUTPUT_DEVICES.pop()
    for devId in iterDeviceIds():
        device = MidiDevice(devId)
        if device.isOutput():
            _OUTPUT_DEVICES.append(device)

def iterMidiDevices():
    return iter(_OUTPUT_DEVICES)


from PyQt4.QtCore import QTimer, pyqtSignal, QObject
from Data.DBConstants import MIDITICKSPERBEAT

class _midi(QObject):
    def __init__(self):
        super(_midi, self).__init__()
        self._port = None
        self._midiOut = None
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

    def initialize(self):
        if not _MIDI_INITIALIZED:
            raise RuntimeError("MIDI not initialized yet!")
        if self._port is None:
            self._port = getDefaultId()
        if self._port != -1:
            self._midiOut = pygame.midi.Output(self._port, _LATENCY, _BUFSIZE)

    def setPort(self, port):
        if self._midiOut:
            self._midiOut.abort()
            del self._midiOut
            self._midiOut = None
        self._port = port
        self.initialize()

    def port(self):
        return self._port

    def isGood(self):
        return self._port != -1 and self._midiOut is not None

    def setMute(self, onOff):
        self._mute = onOff

    def isMuted(self):
        return self._mute

    highlightMeasure = pyqtSignal(int, int)

    def playNote(self, drumIndex, head):
        if self.kit is None or self._mute:
            return
        headData = self.kit[drumIndex].headData(head)
        self.playHeadData(headData)

    def playHeadData(self, headData, when = None):
        if not self._midiOut:
            return
        if when is None:
            when = pygame.midi.time()
        if headData.effect == "flam":
            self._midiOut.write([[[_PERCUSSION_NOTE_ON,
                                   headData.midiNote,
                                   headData.midiVolume / FLAM_VOLUME_CONSTANT],
                                  when]])
            self._midiOut.write([[[_PERCUSSION_NOTE_ON,
                                   headData.midiNote,
                                   headData.midiVolume],
                                  when + FLAM_TIME_CONSTANT]])
        elif headData.effect == "drag":
            self._midiOut.write([[[_PERCUSSION_NOTE_ON,
                                   headData.midiNote,
                                   headData.midiVolume ],
                                  when]])
            self._midiOut.write([[[_PERCUSSION_NOTE_ON,
                                   headData.midiNote,
                                   headData.midiVolume],
                                  when + DRAG_TIME_CONSTANT]])
        elif headData.effect == "choke":
            self._midiOut.write([[[_PERCUSSION_NOTE_ON,
                                   headData.midiNote,
                                   headData.midiVolume ],
                                  when]])
            self._midiOut.write([[[_PERCUSSION_CHOKE,
                                   _CHOKE_MSG,
                                   _CHOKE_VELOCITY],
                                  when + DRAG_TIME_CONSTANT]])
        else:
            self._midiOut.write([[[_PERCUSSION_NOTE_ON,
                                   headData.midiNote,
                                   headData.midiVolume],
                                  when]])

    def playScore(self, score):
        measureList = list(score.iterMeasuresWithRepeats())
        self._playMIDINow(measureList, score)

    def _playMIDINow(self, measureList, score):
        if self.kit is None or self._midiOut is None:
            return
        baseTime = 0
        bpm = score.scoreData.bpm
        msPerBeat = 60000.0 / bpm
        self._measureDetails = []
        lastMeasureIndex = None
        try:
            for measure, measureIndex in measureList:
                if lastMeasureIndex is None or measureIndex != lastMeasureIndex + 1:
                    bpm = score.bpmAtMeasureByIndex(measureIndex)
                elif measure.newBpm > 0 and bpm != measure.newBpm:
                    bpm = measure.newBpm
                if bpm == 0:
                    bpm = 120
                lastMeasureIndex = measureIndex
                msPerBeat = 60000.0 / bpm
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
        for index, (measure, measureIndex) in enumerate(measureList):
            if measure.simileDistance > 0:
                measure = score.getReferredMeasure(measureIndex)
                measureList[index] = (measure, measureIndex)
        self._playMIDINow(measureList, score)

    def shutUp(self):
        if self._musicPlaying:
            self.timer.stop()
            self._measureDetails = []
            self._measureTimer.stop()
            self.highlightMeasure.emit(-1, -1)
            if self._midiOut:
                del self._midiOut
                self._midiOut = None
            pygame.mixer.music.stop()
            self._midiOut = pygame.midi.Output(self._port, _LATENCY, _BUFSIZE)
            self._musicPlaying = False

    def cleanup(self):
        if self._midiOut is not None:
            self._midiOut.abort()
            del self._midiOut
            self._midiOut = None

    def _highlight(self):
        delay = -1
        measureIndex = None
        nextMeasure = -1
        while delay < 0 and self._measureDetails:
            measureIndex, measureEnd = self._measureDetails.pop()
            if self._measureDetails:
                nextMeasure = self._measureDetails[-1][0]
            delay = (measureEnd - 1000 * (time.clock() - self._songStart))
        if measureIndex is not None:
            self.highlightMeasure.emit(measureIndex, nextMeasure)
        else:
            self.highlightMeasure.emit(-1, -1)
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
    if delta <= 0:
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

def _makeMidiStart(score):
    signature = "Created with DrumBurp"
    midiData = []
    midiData.extend([0, 0xff, 0x1, len(signature)])
    midiData.extend([ord(ch) for ch in signature])
    return midiData

def _writeMidiNotes(midiObjects, baseTime):
    lastNoteTime = 0
    midiData = []
    for midiEvent in midiObjects:
        deltaTime = midiEvent.time - lastNoteTime
        lastNoteTime = midiEvent.time
        encodeSevenBitDelta(deltaTime, midiData)
        midiData.extend(midiEvent.write())
    # Turn off drum notes
    deltaTime = baseTime - lastNoteTime
    # Insert a delay before the end of the track.
    encodeSevenBitDelta(deltaTime + 4 * MIDITICKSPERBEAT, midiData)
    midiData.extend([_PERCUSSION_NOTE_OFF, 38, 0])
    encodeSevenBitDelta(0, midiData)
    midiData.extend([0xFF, 0x2F, 0])
    return midiData

def _finishMidiData(midiData):
    numBytes = len(midiData)
    lenBytes = [((numBytes >> i) & 0xff) for i in xrange(24, -8, -8)]
    return lenBytes + midiData

class MidiObject(object):
    def __init__(self, eventTime):
        self.time = eventTime

    def __cmp__(self, other):
        return cmp(self.time, other.time)

    def write(self):
        raise NotImplementedError()

class MidiTempoChange(MidiObject):
    def __init__(self, eventTime, bpm):
        super(MidiTempoChange, self).__init__(eventTime)
        self.bpm = bpm

    def write(self):
        msPerBeat = int(60000000 / self.bpm)
        return [0xff, 0x51, 03, (msPerBeat >> 16) & 0xff,
                (msPerBeat >> 8) & 0xff, msPerBeat & 0xff]

class MidiNote(MidiObject):
    def __init__(self, noteTime, headData):
        super(MidiNote, self).__init__(noteTime)
        self.headData = headData

    def write(self):
        return [_PERCUSSION_NOTE_ON, self.headData.midiNote,
                self.headData.midiVolume]

class MidiChoke(MidiObject):
    def write(self):
        return [_PERCUSSION_CHOKE, _CHOKE_MSG, _CHOKE_VELOCITY]

def _calculateMidiTimes(measureIterator, score):
    notes = []
    baseTime = 1
    lastBpm = None
    lastMeasureIndex = None
    for measure, measureIndex in measureIterator:
        measureNotes = []
        times = list(measure.counter.iterMidiTicks())
        if lastMeasureIndex is None or measureIndex != lastMeasureIndex + 1:
            bpm = score.bpmAtMeasureByIndex(measureIndex)
        elif measure.newBpm > 0 and bpm != measure.newBpm:
            bpm = measure.newBpm
        lastMeasureIndex = measureIndex
        if bpm == 0:
            bpm = 120
        if bpm != lastBpm:
            notes.append(MidiTempoChange(baseTime + times[0], bpm))
            lastBpm = bpm
        for notePos, head in measure:
            drumData = score.drumKit[notePos.drumIndex]
            headData = drumData.headData(head)
            if headData is not None:
                noteTime = baseTime + times[notePos.noteTime]
                divisionTicks = times[notePos.noteTime + 1] - times[notePos.noteTime]
                if headData.effect == "flam":
                    headCopy = copy.copy(headData)
                    headCopy.midiVolume = headData.midiVolume / FLAM_VOLUME_CONSTANT
                    measureNotes.append(MidiNote(noteTime - (MIDITICKSPERBEAT / FLAM_TIME_CONSTANT), headCopy))
                elif headData.effect == "drag":
                    measureNotes.append(MidiNote(noteTime + divisionTicks / 2, headData))
                elif headData.effect == "choke":
                    measureNotes.append(MidiChoke(noteTime + divisionTicks / 2))
                measureNotes.append(MidiNote(noteTime, headData))
        baseTime += times[-1]
        measureNotes.sort()
        notes.extend(measureNotes)
    return notes, baseTime

def exportMidi(measureIterator, score, handle):
    handle.write("MThd\x00\x00\x00\x06\x00\x00\x00\x01")
    handle.write("%c" % chr((MIDITICKSPERBEAT >> 8) & 0xFF))
    handle.write("%c" % chr((MIDITICKSPERBEAT >> 0) & 0xFF))
    notes, baseTime = _calculateMidiTimes(measureIterator, score)
    midiData = _makeMidiStart(score)
    midiData += _writeMidiNotes(notes, baseTime)
    midiData = _finishMidiData(midiData)
    handle.write("MTrk")
    for byte in midiData:
        handle.write("%c" % byte)

def selectMidiDevice(dev):
    _PLAYER.cleanup()
    _PLAYER.setPort(dev.deviceId)
    return _PLAYER.isGood()

def currentDevice():
    for dev in _OUTPUT_DEVICES:
        if dev.deviceId == _PLAYER.port():
            return dev
    return None

def _initialize():
    global HAS_MIDI, _MIDI_INITIALIZED
    if _MIDI_INITIALIZED:
        return
    if _HAS_PYGAME:
        pygame.init()  # IGNORE:no-member
        pygame.midi.init()
        pygame.mixer.init(_FREQ, _BITSIZE, _CHANNELS, _NUMSAMPLES)
        pygame.mixer.music.set_volume(0.8)
    _MIDI_INITIALIZED = True
    _PLAYER.initialize()
    atexit.register(cleanup)
    HAS_MIDI = _HAS_PYGAME and _PLAYER.isGood()

class MidiInit(QThread):
    def run(self):  # IGNORE:no-self-use
        _initialize()

def main():
    _initialize()
    refreshOutputDevices()
    for device in iterMidiDevices():
        print device.name

if __name__ == "__main__":
    main()
