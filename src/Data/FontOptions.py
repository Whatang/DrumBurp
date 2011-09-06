'''
Created on 5 Sep 2011

@author: Mike Thomas

'''

class FontOptions(object):

    def __init__(self):
        self.noteFontSize = 10
        self.noteFont = None
        self.sectionFontSize = 14
        self.sectionFont = None
        self.metadataFontSize = 16
        self.metadataFont = None

    def write(self, handle, indenter):
        print >> handle, indenter("FONT_OPTIONS_START")
        indenter.increase()
        print >> handle, indenter("NOTEFONTSIZE %d"
                                  % self.noteFontSize)
        print >> handle, indenter("SECTIONFONTSIZE %d"
                                  % self.sectionFontSize)
        print >> handle, indenter("METADATAFONTSIZE %d"
                                  % self.metadataFontSize)
        indenter.decrease()
        print >> handle, indenter("FONT_OPTIONS_END")

    def read(self, scoreIterator):
        for lineType, lineData in scoreIterator:
            if  lineType == "FONT_OPTIONS_END":
                break
            elif lineType == "NOTEFONTSIZE":
                self.noteFontSize = int(lineData)
            elif lineType == "SECTIONFONTSIZE":
                self.sectionFontSize = int(lineData)
            elif lineType == "METADATAFONTSIZE":
                self.metadataFontSize = int(lineData)
            else:
                raise IOError("Font information not recognised.")
