'''
Created on 23 Jan 2011

@author: Mike Thomas
'''

from PyQt4 import QtGui

_ICON_CACHE = {"drumburp":"drumburp",
               "repeat":"view-refresh",
               "score":"audio-x-generic",
               "copy":"edit-copy",
               "paste":"edit-paste",
               "delete":"edit-delete"}


def initialiseIcons():
    for iconName, iconLocation in _ICON_CACHE.iteritems():
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Icons/" + iconLocation + ".png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _ICON_CACHE[iconName] = icon

def getIcon(iconName):
    return _ICON_CACHE[iconName.lower()]
