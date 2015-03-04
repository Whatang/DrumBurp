'''
Created on Feb 22, 2015

@author: mike_000
'''
import copy
from PyQt4.QtGui import (QDialog, QColor, QLabel, QPushButton,
                         QComboBox, QColorDialog)
from PyQt4 import QtCore
from GUI.ui_dbColours import Ui_ColourPicker

STYLE_MAP = {"None":QtCore.Qt.NoPen,
             "Solid":QtCore.Qt.SolidLine,
             "Dashed":QtCore.Qt.DashLine}
STYLES = ["None", "Dashed", "Solid"]
REVERSE_STYLE_MAP = dict((x, y) for (y, x) in STYLE_MAP.iteritems())

class ColouredItem(object):
    def __init__(self, backgroundColour, borderStyle, borderColour):
        self._borderStyle = None
        self.backgroundColour = backgroundColour
        self.borderStyle = borderStyle
        self.borderColour = borderColour

    @property
    def borderStyle(self):
        return self._borderStyle

    @borderStyle.setter
    def borderStyle(self, value):
        if not isinstance(value, QtCore.Qt.PenStyle):
            value = STYLE_MAP.get(value, QtCore.Qt.NoPen)
        self._borderStyle = value

    @staticmethod
    def _colourToString(name, colour):
        return name + ":%02x,%02x,%02x,%02x" % colour.getRgb()

    @staticmethod
    def _colourFromString(colString):
        rgba = [int(x, 16) for x in colString.split(",")]
        return QColor.fromRgb(*rgba)

    @staticmethod
    def _lineToString(name, line):
        return "%s:%s" % (name, REVERSE_STYLE_MAP[line])

    @staticmethod
    def _lineFromString(lineString):
        return STYLE_MAP[lineString]

    def toString(self):
        answer = "/".join([self._colourToString("backgroundColour",
                                                self.backgroundColour),
                          self._lineToString("borderStyle",
                                             self.borderStyle),
                          self._colourToString("borderColour",
                                               self.borderColour)])
        return answer

    def fromString(self, colString):
        for item in str(colString).split("/"):
            if ":" not in item:
                continue
            name, detail = item.split(":")
            if name.endswith("Colour"):
                setattr(self, name, self._colourFromString(detail))
            elif name.endswith("Style"):
                setattr(self, name, self._lineFromString(detail))

DEFAULT_NOTE_HIGHLIGHT = ColouredItem(QColor(QtCore.Qt.yellow).lighter(),
                                      "None",
                                      QColor(QtCore.Qt.NoPen))
DEFAULT_TIME_HIGHLIGHT = ColouredItem(QColor(QtCore.Qt.transparent),
                                      "Dashed",
                                      QColor(QtCore.Qt.blue).lighter())
DEFAULT_SELECTED_MEASURE = ColouredItem(QColor(QtCore.Qt.gray).lighter(),
                                        "Solid",
                                        QColor(QtCore.Qt.gray).lighter())
DEFAULT_PLAYING_HIGHLIGHT = ColouredItem(QColor(QtCore.Qt.transparent),
                                         "Solid",
                                         QColor(QtCore.Qt.blue).lighter())
DEFAULT_NEXTPLAY_HIGHLIGHT = ColouredItem(QColor(QtCore.Qt.transparent),
                                          "Dashed",
                                          QColor(QtCore.Qt.blue).lighter())

class ColAttrs(object):
    def __init__(self, background = True, border = True):
        self.background = background
        self.border = border

class ColourScheme(object):
    noteHighlightAttrs = ColAttrs(True, True)
    timeHighlightAttrs = ColAttrs(False, True)
    selectedMeasureAttrs = ColAttrs(True, True)
    playingHighlightAttrs = ColAttrs(False, True)
    nextPlayingHighlightAttrs = ColAttrs(False, True)

    def __init__(self, noteHighlight = DEFAULT_NOTE_HIGHLIGHT,
                 timeHighlight = DEFAULT_TIME_HIGHLIGHT,
                 selectedMeasure = DEFAULT_SELECTED_MEASURE,
                 playingHighlight = DEFAULT_PLAYING_HIGHLIGHT,
                 nextHighlight = DEFAULT_NEXTPLAY_HIGHLIGHT):
        self.noteHighlight = copy.deepcopy(noteHighlight)
        self.timeHighlight = copy.deepcopy(timeHighlight)
        self.selectedMeasure = copy.deepcopy(selectedMeasure)
        self.playingHighlight = copy.deepcopy(playingHighlight)
        self.nextPlayingHighlight = copy.deepcopy(nextHighlight)

    @staticmethod
    def iterColourNames():
        yield "Note Highlight", "noteHighlight"
        yield "Time Highlight", "timeHighlight"
        yield "Selected Measure", "selectedMeasure"
        yield "Playing Highlight", "playingHighlight"
        yield "Next Playing Highlight", "nextPlayingHighlight"

class DBColourPicker(QDialog, Ui_ColourPicker):

    def __init__(self, colour_scheme, parent = None):
        super(DBColourPicker, self).__init__(parent)
        self.setupUi(self)
        self._originalScheme = copy.deepcopy(colour_scheme)
        self._currentScheme = copy.deepcopy(colour_scheme)
        reset = self.buttonBox.button(self.buttonBox.Reset)
        reset.clicked.connect(self.reset)
        restore = self.buttonBox.button(self.buttonBox.RestoreDefaults)
        restore.clicked.connect(self.restoreDefaults)
        self._colourSelectors = []
        self._lineSelectors = []
        for row, (colourName, colourRef) in enumerate(ColourScheme.iterColourNames()):
            label = QLabel(self)
            label.setText(colourName)
            label.setAlignment(QtCore.Qt.AlignRight)
            self.gridLayout.addWidget(label, row + 1, 0, 1, 1)
            if self._getColourAttrs(colourRef).background:
                backgroundButton = self._makeBackgroundButton(colourRef)
                self.gridLayout.addWidget(backgroundButton, row + 1, 1, 1, 1)
            if self._getColourAttrs(colourRef).border:
                combo = self._makeLineCombo(colourRef)
                self.gridLayout.addWidget(combo, row + 1, 2, 1, 1)
                lineButton = self._makeLineButton(colourRef)
                self.gridLayout.addWidget(lineButton, row + 1, 3, 1, 1)
        self._setColourValues()

    @staticmethod
    def _styleButton(button, colour):
        button.setText("")
        button.setAutoFillBackground(True)
        ss = """QPushButton {
        background: rgba(%d, %d, %d, %d);
        border-color: black;
        border-width:1px;
        color: black;
        border-style: ridge;
        }"""
        ss %= colour.getRgb()
        if colour.getRgb()[3] == 0:
            button.setText("Transparent")
        button.setStyleSheet(ss)

    def _getColourItem(self, colourRef):
        return getattr(self._currentScheme, colourRef)

    def _getColourAttrs(self, colourRef):
        return getattr(self._currentScheme, colourRef + "Attrs")

    def _makeColourSelector(self, button, colourRef, colourType):
        def selectColour():
            currentColour = getattr(self._getColourItem(colourRef), colourType)
            colourDialog = QColorDialog(currentColour, self)
            if colourDialog.exec_():
                selected = colourDialog.selectedColor()
                if selected != currentColour:
                    self._styleButton(button, selected)
                    setattr(self._getColourItem(colourRef), colourType, selected)
        button.clicked.connect(selectColour)
        self._colourSelectors.append((button, colourRef, colourType))

    def _makeBackgroundButton(self, colourRef):
        backgroundButton = QPushButton(self)
        backgroundButton.setObjectName(colourRef + "background_col")
        self._makeColourSelector(backgroundButton, colourRef, "backgroundColour")
        return backgroundButton

    def _makeLineCombo(self, colourRef):
        combo = QComboBox(self)
        combo.setObjectName(colourRef + "border_style")
        for lineStyle in STYLES:
            combo.addItem(lineStyle)
        def setLineStyle(newIndex):
            self._getColourItem(colourRef).borderStyle = STYLES[newIndex]
        combo.currentIndexChanged.connect(setLineStyle)
        self._lineSelectors.append((combo, colourRef))
        return combo

    def _makeLineButton(self, colourRef):
        lineButton = QPushButton(self)
        lineButton.setObjectName(colourRef + "border_col")
        self._makeColourSelector(lineButton, colourRef, "borderColour")
        return lineButton

    def getColourScheme(self):
        return self._currentScheme

    def _setColourValues(self):
        for button, colourRef, colourType in self._colourSelectors:
            colour = getattr(self._getColourItem(colourRef), colourType)
            self._styleButton(button, colour)
        for combo, colourRef in self._lineSelectors:
            currentStyle = self._getColourItem(colourRef).borderStyle
            for selected, lineStyle in enumerate(STYLES):
                if STYLE_MAP[lineStyle] == currentStyle:
                    combo.setCurrentIndex(selected)

    def reset(self):
        self._currentScheme = copy.deepcopy(self._originalScheme)
        self._setColourValues()

    def restoreDefaults(self):
        self._currentScheme = copy.deepcopy(ColourScheme())
        self._setColourValues()

def main():
    from PyQt4.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    scheme = ColourScheme()
    dialog = DBColourPicker(scheme)
    dialog.show()
    app.exec_()
    if dialog.result():
        print dialog.getColourScheme()

if __name__ == "__main__":
    main()
