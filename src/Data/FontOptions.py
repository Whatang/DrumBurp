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
Created on 5 Sep 2011

@author: Mike Thomas

'''



class FontOptions(object):
    DEFAULT_FONT = "Noto Sans"

    _ALLOWED_FONTS = {}

    def __init__(self):
        self.noteFontSize = 10
        self.noteFont = self.DEFAULT_FONT
        self.sectionFontSize = 14
        self.sectionFont = self.DEFAULT_FONT
        self.metadataFontSize = 16
        self.metadataFont = self.DEFAULT_FONT

    @classmethod
    def addFont(cls, fontName, font):
        cls._ALLOWED_FONTS[unicode(fontName)] = font

    @classmethod
    def iterAllowedFonts(cls):
        return cls._ALLOWED_FONTS.iteritems()

    @classmethod
    def isAllowedFont(cls, fontName):
        return unicode(fontName) in cls._ALLOWED_FONTS
