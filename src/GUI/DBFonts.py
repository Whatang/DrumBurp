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

from PyQt4.Qt import QFontDatabase


def initialiseFonts():
    fonts = ["ncs.otf", 'inconsolata.otf', 'bpmono.ttf', 'liberation.otf',
             'oxygen.otf', 'opensans.ttf', 'montserrat.ttf', 'notosans.ttf',
             'ptsans.ttf', 'roboto.ttf', 'raleway.ttf']
    for font in fonts:
        if QFontDatabase.addApplicationFont(":/fonts/" + font) == -1:
            print font
