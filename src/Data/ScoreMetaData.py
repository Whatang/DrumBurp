'''
Created on 23 Jan 2011

@author: Mike Thomas

'''
import time

class ScoreMetaData(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.title = ""
        self.artist = ""
        self.bpm = 120
        self.creator = ""
        self.width = 80

    def makeEmpty(self):
        self.title = "Untitled"
        self.artist = "Unknown"
        self.creator = "Nobody"

    def load(self, scoreIterator):
        for lineType, lineData in scoreIterator:
            if lineData is None:
                lineData = ""
            if lineType == "TITLE":
                self.title = lineData
            elif lineType == "ARTIST":
                self.artist = lineData
            elif lineType == "CREATOR":
                self.creator = lineData
            elif lineType == "BPM":
                self.bpm = int(lineData)
            elif lineType == "WIDTH":
                self.width = int(lineData)
            elif lineType == "END_SCORE_METADATA":
                break

    def save(self, handle, indenter):
        print >> handle, indenter("SCORE_METADATA")
        indenter.increase()
        print >> handle, indenter("TITLE", self.title)
        print >> handle, indenter("ARTIST", self.artist)
        print >> handle, indenter("CREATOR", self.creator)
        print >> handle, indenter("BPM", self.bpm)
        print >> handle, indenter("WIDTH", self.width)
        indenter.decrease()
        print >> handle, indenter("END_SCORE_METADATA")


    def exportASCII(self):
        metadataString = []
        metadataString.append("Title     : " + self.title)
        metadataString.append("Artist    : " + self.artist)
        metadataString.append("BPM       : " + str(self.bpm))
        metadataString.append("Tabbed by : " + self.creator)
        metadataString.append("Date      : " + time.strftime("%d %B %Y"))
        metadataString.append("")
        return metadataString
