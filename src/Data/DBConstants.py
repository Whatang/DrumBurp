# Copyright 2011-12 Michael Thomas
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
Created on 12 Dec 2010

@author: Mike Thomas
'''

# Storage & text constants

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

# MIDI
MIDITICKSPERBEAT = 192

# File format numbers
DBFF_0 = 0
CURRENT_FILE_FORMAT = DBFF_0
