# Copyright 2015 Michael Thomas
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
Created on Jul 19, 2015

@author: Mike Thomas
'''

from PyQt4.Qt import QFontDatabase, QFont
import Data.FontOptions


def initialiseFonts():
    fonts = [("NotCourierSans", "ncs.otf"),
             ('Inconsolata', 'inconsolata.otf'),
             ('BPmono', 'bpmono.ttf'),
             ('Liberation Mono', 'liberation.otf'),
             ('Oxygen Mono', 'oxygen.otf'),
             ('Open Sans', 'opensans.ttf'),
             ('Montserrat', 'montserrat.ttf'),
             ('Noto Sans', 'notosans.ttf'),
             ('PT Sans', 'ptsans.ttf'),
             ('Raleway', 'roboto.ttf'),
             ('Roboto', 'raleway.ttf')]
    for fontName, fontFile in fonts:
        if QFontDatabase.addApplicationFont(":/fonts/" + fontFile) == -1:
            print (fontName)
        else:
            font = QFont(fontName)
            Data.FontOptions.FontOptions.addFont(fontName, font)
            Data.FontOptions.FontOptions.addFont(fontName, font)
