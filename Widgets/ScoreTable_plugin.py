'''
Created on 1 Aug 2010

@author: Mike Thomas
'''
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from ScoreTable import ScoreTable

class ScoreTablePlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent = None):

        super(ScoreTablePlugin, self).__init__(parent)
        self.initialized = False

    def createWidget(self, parent):
        widget = ScoreTable(parent)
        return widget

    def name(self):
        return "ScoreTable"

    def group(self):
        return "DrumBurp Widgets"

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return False

    def domXml(self):
        return '<widget class="ScoreTable" name="ScoreTable" />\n'

    def includeFile(self):
        return "Widgets.ScoreTable_plugin"
