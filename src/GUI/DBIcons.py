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
Created on 23 Jan 2011

@author: Mike Thomas
'''

from PyQt4 import QtGui

_ICON_CACHE = {"drumburp": "drumburp",
               "repeat": "view-refresh",
               "score": "audio-x-generic",
               "copy": "edit-copy",
               "paste": "edit-paste",
               "delete": "edit-delete"}


def initialiseIcons():
    for iconName, iconLocation in iter(_ICON_CACHE.items()):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Icons/" + iconLocation + ".png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _ICON_CACHE[iconName] = icon


def getIcon(iconName):
    return _ICON_CACHE[iconName.lower()]
