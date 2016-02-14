'''
Created on Feb 22, 2015

@author: mike_000
'''
import copy
from PyQt4.QtGui import (QDialog, QColor, QLabel, QPushButton,
                         QComboBox, QColorDialog, QPen)
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

class TextColouredItem(ColouredItem):
    def __init__(self, textColour):
        super(TextColouredItem, self).__init__(QColor(QtCore.Qt.transparent),
                                               "None",
                                               textColour)

class BorderColouredItem(ColouredItem):
    def __init__(self, borderStyle, borderColour):
        super(BorderColouredItem, self).__init__(QColor(QtCore.Qt.transparent),
                                                 borderStyle,
                                                 borderColour)

class ColAttrs(object):
    KNOWN_COLOURS = []

    def __init__(self, longName, attrName, default, background = True, border = True, text = False):
        self.longName = longName
        self.attrName = attrName
        self.default = default
        self.background = background
        self.border = border
        self.text = text
        self.KNOWN_COLOURS.append(self)

    def makeInstance(self, scheme):
        inst = ColourInstance(self)
        setattr(scheme, self.attrName, inst)

    def setPainter(self, painter, colour):
        raise NotImplementedError()

    def getInstance(self, scheme):
        return getattr(scheme, self.attrName)

class TextColAttrs(ColAttrs):
    def __init__(self, longName, attrName, default):
        super(TextColAttrs, self).__init__(longName, attrName, default,
                                           False, False, True)

    def setPainter(self, painter, colour):
        pen = QPen()
        pen.setColor(colour.borderColour)
        painter.setPen(pen)

class SolidBoxAttrs(ColAttrs):
    def __init__(self, longName, attrName, default):
        super(SolidBoxAttrs, self).__init__(longName, attrName, default,
                                            True, True, False)

    def setPainter(self, painter, colour):
        pen = QPen(colour.borderStyle)
        pen.setColor(colour.borderColour)
        painter.setPen(pen)
        painter.setBrush(colour.backgroundColour)

class BorderAttrs(ColAttrs):
    def __init__(self, longName, attrName, default):
        super(BorderAttrs, self).__init__(longName, attrName, default,
                                          False, True, False)

    def setPainter(self, painter, colour):
        pen = QPen(colour.borderStyle)
        pen.setColor(colour.borderColour)
        painter.setPen(pen)
        painter.setBrush(QColor(QtCore.Qt.transparent))

_TEXT_ATTRS = TextColAttrs("Text", "text",
                           TextColouredItem(QColor(QtCore.Qt.black)))
_POTENTIAL_ATTRS = TextColAttrs("New notes", "potential",
                                TextColouredItem(QColor(QtCore.Qt.blue)))
_DELETE_ATTRS = TextColAttrs("Notes to delete", "delete",
                             TextColouredItem(QColor(QtCore.Qt.red)))
_NOTE_HIGHLIGHT_ATTRS = SolidBoxAttrs("Note Highlight", "noteHighlight",
                                      ColouredItem(QColor(QtCore.Qt.yellow).lighter(),
                                                   "None",
                                                   QColor(QtCore.Qt.black)))
_TIME_HIGHLIGHT_ATTRS = BorderAttrs("Time Highlight", "timeHighlight",
                                    BorderColouredItem("Dashed",
                                                       QColor(QtCore.Qt.blue).lighter()))
_SEL_MEASURE_ATTRS = SolidBoxAttrs("Selected Measure", "selectedMeasure",
                                   ColouredItem(QColor(QtCore.Qt.gray).lighter(),
                                                "Solid",
                                                QColor(QtCore.Qt.gray).lighter()))
_PLAY_HL_ATTRS = BorderAttrs("Playing Highlight", "playingHighlight",
                             BorderColouredItem("Solid",
                                                QColor(QtCore.Qt.blue).lighter()))
_NEXT_PLAY_HL_ATTRS = BorderAttrs("Next Playing Highlight", "nextPlayingHighlight",
                                  BorderColouredItem("Dashed",
                                                     QColor(QtCore.Qt.blue).lighter()))
_STICKING_ATTRS = SolidBoxAttrs("Sticking Display", "sticking",
                                ColouredItem(QColor(QtCore.Qt.white),
                                             "Dashed",
                                             QColor(QtCore.Qt.gray)))

class ColourInstance(object):
    def __init__(self, colourAttrs):
        self.colour = copy.deepcopy(colourAttrs.default)
        self.colourAttrs = colourAttrs

    def setPainter(self, painter):
        self.colourAttrs.setPainter(painter, self)

    @property
    def borderStyle(self):
        return self.colour.borderStyle
    @borderStyle.setter
    def borderStyle(self, value):
        self.colour.borderStyle = value

    @property
    def borderColour(self):
        return self.colour.borderColour
    @borderColour.setter
    def borderColour(self, value):
        self.colour.borderColour = value

    @property
    def backgroundColour(self):
        return self.colour.backgroundColour
    @backgroundColour.setter
    def backgroundColour(self, value):
        self.colour.backgroundColour = value

    def toString(self):
        return self.colour.toString()

    def fromString(self, colString):
        return self.colour.fromString(colString)

class ColourScheme(object):
    def __init__(self):
        for colAttr in ColAttrs.KNOWN_COLOURS:
            colAttr.makeInstance(self)

    def iterColours(self):
        for colour in ColAttrs.KNOWN_COLOURS:
            yield getattr(self, colour.attrName)

    def iterTextColours(self):
        for colour in ColAttrs.KNOWN_COLOURS:
            if colour.text:
                yield getattr(self, colour.attrName)

    def iterAreaColours(self):
        for colour in ColAttrs.KNOWN_COLOURS:
            if not colour.text:
                yield getattr(self, colour.attrName)

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
        for row, colour in enumerate(self._currentScheme.iterTextColours()):
            colourAttr = colour.colourAttrs
            label = QLabel(self.frame)
            label.setText(colourAttr.longName)
            label.setAlignment(QtCore.Qt.AlignRight)
            self.textGrid.addWidget(label, row + 1, 0, 1, 1)
            textButton = self._makeLineButton(colourAttr)
            self.textGrid.addWidget(textButton, row + 1, 1, 1, 1)
        for row, colour in enumerate(self._currentScheme.iterAreaColours()):
            colourAttr = colour.colourAttrs
            label = QLabel(self.frame_2)
            label.setText(colourAttr.longName)
            label.setAlignment(QtCore.Qt.AlignRight)
            self.areaGrid.addWidget(label, row + 1, 0, 1, 1)
            if colourAttr.background:
                backgroundButton = self._makeBackgroundButton(colourAttr)
                self.areaGrid.addWidget(backgroundButton, row + 1, 1, 1, 1)
            if colourAttr.border:
                combo = self._makeLineCombo(colourAttr)
                self.areaGrid.addWidget(combo, row + 1, 2, 1, 1)
                lineButton = self._makeLineButton(colourAttr)
                self.areaGrid.addWidget(lineButton, row + 1, 3, 1, 1)
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
        }

        QPushButton:hover {
        border-width:2px;
        border-color: red;
        }"""
        ss %= colour.getRgb()
        if colour.getRgb()[3] == 0:
            button.setText("Transparent")
        button.setStyleSheet(ss)

    def _makeColourSelector(self, button, colourAttr, colourType):
        def selectColour():
            colour = colourAttr.getInstance(self._currentScheme)
            currentColour = getattr(colour, colourType)
            colourDialog = QColorDialog(currentColour, self)
            if colourDialog.exec_():
                selected = colourDialog.selectedColor()
                if selected != currentColour:
                    self._styleButton(button, selected)
                    setattr(colour, colourType, selected)
        button.clicked.connect(selectColour)
        self._colourSelectors.append((button, colourAttr,
                                      colourType))

    def _makeBackgroundButton(self, colourAttr):
        backgroundButton = QPushButton(self)
        backgroundButton.setObjectName(colourAttr.attrName + "background_col")
        self._makeColourSelector(backgroundButton, colourAttr, "backgroundColour")
        return backgroundButton

    def _makeLineCombo(self, colourAttr):
        combo = QComboBox(self)
        combo.setObjectName(colourAttr.attrName + "border_style")
        for lineStyle in STYLES:
            combo.addItem(lineStyle)
        def setLineStyle(newIndex):
            colour = colourAttr.getInstance(self._currentScheme)
            colour.borderStyle = STYLES[newIndex]
        combo.currentIndexChanged.connect(setLineStyle)
        self._lineSelectors.append((combo, colourAttr))
        return combo

    def _makeLineButton(self, colourAttr):
        lineButton = QPushButton(self)
        lineButton.setObjectName(colourAttr.attrName + "border_col")
        self._makeColourSelector(lineButton, colourAttr, "borderColour")
        return lineButton

    def getColourScheme(self):
        return self._currentScheme

    def _setColourValues(self):
        for button, colourAttr, colourType in self._colourSelectors:
            colour = colourAttr.getInstance(self._currentScheme)
            colourVal = getattr(colour, colourType)
            self._styleButton(button, colourVal)
        for combo, colourAttr in self._lineSelectors:
            colour = colourAttr.getInstance(self._currentScheme)
            currentStyle = colour.borderStyle
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
        scheme = dialog.getColourScheme()
        for col in scheme.iterColours():
            print col.colourAttrs.longName, col.toString()

if __name__ == "__main__":
    main()
