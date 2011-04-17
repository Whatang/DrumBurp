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
