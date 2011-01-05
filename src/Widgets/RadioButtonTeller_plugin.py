'''
Created on 3 Aug 2010

@author: Mike Thomas
'''
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from RadioButtonTeller import RadioButtonTeller

#pylint: disable-msg=R0923

class RadioButtonTellerPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent = None):

        super(RadioButtonTellerPlugin, self).__init__(parent)

        self.initialized = False

    def createWidget(self, parent):
        widget = RadioButtonTeller(parent)
        return widget

    def name(self):
        return "RadioButtonTeller"

    def group(self):
        return "DrumBurp Widgets"

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return False

    def domXml(self):
        return '<widget class="RadioButtonTeller" name="RadioButtonTeller" />\n'

    def includeFile(self):
        return "Widgets.RadioButtonTeller_plugin"
