'''
Created on 12 Dec 2010

@author: Mike Thomas

'''

from DBConstants import DRUM_ABBR_WIDTH

class Drum(object):
    '''
    classdocs
    '''
    def __init__(self, name, abbr, head, locked = False):
        self.name = name
        self.abbr = abbr
        self.head = head
        self.locked = locked
        assert(len(name) > 0)
        assert(1 <= len(abbr) <= DRUM_ABBR_WIDTH)
        assert(len(head) == 1)

    def __eq__(self, other):
        return self.name == other.name or self.abbr == other.abbr

    def exportASCII(self):
        return "%2s - %s" % (self.abbr, self.name)
