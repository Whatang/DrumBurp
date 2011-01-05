'''
Created on 12 Dec 2010

@author: Mike Thomas
'''

class BadTimeError(StandardError):
    "The given note position is invalid."

class BadNoteSpecification(StandardError):
    "The given note index is not valid for this DrumKit."

class DuplicateDrumError(StandardError):
    "This drum already appears in this drum kit."

class NoSuchDrumError(StandardError):
    "The specified drum was not found."

class OverSizeMeasure(StandardError):
    "The Score contains a Measure which is too large to format for this width."
