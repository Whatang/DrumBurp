'''
Created on Feb 22, 2015

@author: mike_000
'''
import copy
from PyQt4.QtGui import QDialog, QColor, QLabel, QPushButton, QComboBox, QColorDialog
from PyQt4 import QtCore
from ui_dbColours import Ui_ColourPicker

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
    def _colourFromString(c_string):
        rgba = [int(x, 16) for x in c_string.split(",")]
        return QColor.fromRgb(*rgba)

    @staticmethod
    def _lineToString(name, line):
        return "%s:%s" % (name, REVERSE_STYLE_MAP[line])

    @staticmethod
    def _lineFromString(l_string):
        return STYLE_MAP[l_string]


    def toString(self):
        answer = "/".join([self._colourToString("backgroundColour", self.backgroundColour),
                          self._lineToString("borderStyle", self.borderStyle),
                          self._colourToString("borderColour", self.borderColour)])
        return answer

    def fromString(self, c_string):
        for item in str(c_string).split("/"):
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
                                      "Solid",
                                      QColor(QtCore.Qt.blue).lighter())
DEFAULT_SELECTED_MEASURE = ColouredItem(QColor(QtCore.Qt.gray).lighter(),
                                        "Solid",
                                        QColor(QtCore.Qt.gray).lighter())
DEFAULT_PLAYING_HIGHLIGHT = ColouredItem(QColor(QtCore.Qt.transparent),
                                         "Solid",
                                         QColor(QtCore.Qt.blue).lighter())

class ColourScheme(object):
    def __init__(self, noteHighlight = DEFAULT_NOTE_HIGHLIGHT, 
                 timeHighlight = DEFAULT_TIME_HIGHLIGHT,
                 selectedMeasure = DEFAULT_SELECTED_MEASURE,
                 playingHighlight = DEFAULT_PLAYING_HIGHLIGHT):
        self.noteHighlight = noteHighlight
        self.timeHighlight = timeHighlight
        self.selectedMeasure = selectedMeasure
        self.playingHighlight = playingHighlight
        
    @staticmethod
    def iterColourNames():
        yield "Note Highlight", "noteHighlight"
        yield "Time Highlight", "timeHighlight"
        yield "Selected Measure", "selectedMeasure"
        yield "Playing Highlight", "playingHighlight"

class DBColourPicker(QDialog, Ui_ColourPicker):
    
    def __init__(self, colour_scheme, parent = None):
        super(DBColourPicker, self).__init__(parent)
        self.setupUi(self)
        self._originalScheme = colour_scheme
        self._currentScheme = copy.deepcopy(colour_scheme)
        for row, (colourName, colourRef) in enumerate(ColourScheme.iterColourNames()):
            label = QLabel(self)
            label.setText(colourName)
            label.setAlignment(QtCore.Qt.AlignRight)
            self.gridLayout.addWidget(label, row + 1, 0, 1, 1)
            backgroundButton = self._makeBackgroundButton(colourRef)
            self.gridLayout.addWidget(backgroundButton, row + 1, 1, 1, 1)
            combo = self._makeLineCombo(colourRef)
            self.gridLayout.addWidget(combo, row + 1, 2, 1, 1)
            lineButton = self._makeLineButton(colourRef)
            self.gridLayout.addWidget(lineButton, row + 1, 3, 1, 1)
           
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
        colour = getattr(self._getColourItem(colourRef), colourType)
        self._styleButton(button, colour)

    def _makeBackgroundButton(self, colourRef):
        backgroundButton = QPushButton(self)
        backgroundButton.setObjectName(colourRef + "background_col")
        self._makeColourSelector(backgroundButton, colourRef, "backgroundColour")
        return backgroundButton

    def _makeLineCombo(self, colourRef):
        combo = QComboBox(self)
        combo.setObjectName(colourRef + "border_style")
        currentStyle = self._getColourItem(colourRef).borderStyle
        selected = 0
        for lineStyle in STYLES:
            if STYLE_MAP[lineStyle] == currentStyle:
                selected = combo.count()
            combo.addItem(lineStyle)
        combo.setCurrentIndex(selected)
        def setLineStyle(new_index):
            self._getColourItem(colourRef).borderStyle = STYLES[new_index]
        combo.currentIndexChanged.connect(setLineStyle)
        return combo

    def _makeLineButton(self, colourRef):
        lineButton = QPushButton(self)
        lineButton.setObjectName(colourRef + "border_col")
        self._makeColourSelector(lineButton, colourRef, "borderColour")
        return lineButton

    def getColourScheme(self):
        return self._currentScheme

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
