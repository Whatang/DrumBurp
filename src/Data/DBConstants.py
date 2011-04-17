'''
Created on 12 Dec 2010

@author: Mike Thomas
'''

#pylint:disable-msg=C0301

EMPTY_NOTE = "-"
BAR_TYPES = {"NO_BAR": 0,
             "NORMAL_BAR": 1,
             "REPEAT_START": 2,
             "REPEAT_END":4,
             "SECTION_END":8,
             "LINE_BREAK":16}
BARLINE = "|"
REPEAT_STARTER = "/"
REPEAT_END = "\\"
REPEAT_EXTENDER = EMPTY_NOTE
ALTERNATE_EXTENDER = "_"
DRUM_ABBR_WIDTH = 2
BEAT_COUNT = "^"
