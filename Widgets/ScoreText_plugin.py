'''
Created on 3 Nov 2010

@author: Mike Thomas

'''
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from ScoreText import ScoreText

class ScoreTextPlugin(QPyDesignerCustomWidgetPlugin):
    '''
    classdocs
    '''
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
