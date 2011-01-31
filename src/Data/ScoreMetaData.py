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

    def save(self, handle):
        print >> handle, "SCORE_METADATA"
        print >> handle, "TITLE", self.title
        print >> handle, "ARTIST", self.artist
        print >> handle, "CREATOR", self.creator
        print >> handle, "BPM", self.bpm
        print >> handle, "WIDTH", self.width
        print >> handle, "END_SCORE_METADATA"

    def exportASCII(self):
        metadataString = []
        metadataString.append("Title     : " + self.title)
        metadataString.append("Artist    : " + self.artist)
        metadataString.append("BPM       : " + str(self.bpm))
        metadataString.append("Tabbed by : " + self.creator)
        metadataString.append("Date      : " + time.strftime("%d %B %Y"))
        metadataString.append("")
        return metadataString
