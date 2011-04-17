'''
Created on 5 Dec 2010

@author: Mike Thomas
'''
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from ScoreView import ScoreView

#pylint: disable-msg=R0923

class ScoreViewPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent = None):
        super(ScoreViewPlugin, self).__init__(parent)
        self.initialized = False

    def createWidget(self, parent):
        widget = ScoreView(parent)
        return widget

    def name(self):
        return "ScoreView"

    def group(self):
        return "DrumBurp Widgets"

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return False

    def domXml(self):
        return '<widget class="ScoreView" name="ScoreView" />\n'

    def includeFile(self):
        return "Widgets.ScoreView_plugin"
