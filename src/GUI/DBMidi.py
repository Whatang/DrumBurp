'''
Created on 17 Sep 2011

@author: Mike Thomas

'''

import pygame
import pygame.midi
import atexit

pygame.init()
pygame.midi.init()
class _midi(object):
    def __init__(self):
        self._port = pygame.midi.get_default_output_id()
        self._midiOut = pygame.midi.Output(self._port, 0)
        self._midiOut.set_instrument(0, channel = 9)

    def playNote(self, note):
        self._midiOut.note_on(note, 127, channel = 9)

    def cleanup(self):
        del self._midiOut

_NOTEMAP = {}

_PLAYER = _midi()

def setKit(drumKit):
    _NOTEMAP.clear()
    for index, drum in enumerate(drumKit):
        _NOTEMAP[index] = drum.midiNote

def playNote(drumIndex):
    _PLAYER.playNote(_NOTEMAP.get(drumIndex, 36))

atexit.register(_PLAYER.cleanup)

