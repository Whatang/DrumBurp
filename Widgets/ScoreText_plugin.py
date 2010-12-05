'''
Created on 3 Nov 2010

@author: Mike Thomas

'''
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from ScoreText import ScoreText

#pylint: disable-msg=R0923

class ScoreTextPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent = None):

        super(ScoreTextPlugin, self).__init__(parent)
        self.initialized = False

    def createWidget(self, parent):
        widget = ScoreText(parent)
        return widget

    def name(self):
        return "ScoreText"

    def group(self):
        return "DrumBurp Widgets"

    def toolTip(self):
        return ""

    def isContainer(self):
        return False

    def whatsThis(self):
        return ""

    def domXml(self):
        return '<widget class="ScoreText" name="ScoreText" />\n'

    def includeFile(self):
        return "Widgets.ScoreText_plugin"
