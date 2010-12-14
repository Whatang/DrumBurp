'''
Created on 12 Dec 2010

@author: Mike Thomas

'''

class Drum(object):
    '''
    classdocs
    '''
    def __init__(self, name, abbr, head):
        self.name = name
        self.abbr = abbr
        self.head = head
        assert(len(name) > 0)
        assert(1 <= len(abbr) <= 2)
        assert(len(head) == 1)

    def __eq__(self, other):
        return self.name == other.name or self.abbr == other.abbr
