# Copyright 2011 Michael Thomas
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
Created on 17 Apr 2011

@author: Mike Thomas

'''

from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from measureTabs import measureTabs

class measureTabs_plugin(QPyDesignerCustomWidgetPlugin):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(measureTabs_plugin, self).__init__(parent)
        self.initialized = False

    def createWidget(self, parent):
        widget = measureTabs(parent)
        return widget

    def name(self):
        return "measureTabs"

    def group(self):
        return "DrumBurp Widgets"

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return True

    def domXml(self):
        return '<widget class="measureTabs" name="measureTabs" />\n'

    def includeFile(self):
        return "Widgets.measureTabs_plugin"
