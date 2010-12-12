'''
Created on 31 Jul 2010

@author: Mike Thomas

'''

class Instrument(object):
    '''
    classdocs
    '''

    def __init__(self, name, head = "x", abbr = ""):
        '''
        Constructor
        
        @type name: str
        @type head: str
        @type abbr: str
        >>> instr = Instrument("test")
        >>> instr.name, instr.head, instr.abbr
        ('test', 'x', 'Te')
        >>> instr = Instrument("New Instrument", "o", "ne")
        >>> instr.name, instr.head, instr.abbr
        ('New Instrument', 'o', 'Ne')
        '''
        assert(len(head) == 1)
        assert(len(abbr) <= 2)
        self.name = name
        self.head = head
        if abbr == "":
            abbr = name[0:min(len(name), 2)]
        self.abbr = abbr.capitalize()
        assert(len(self.abbr) > 0)
        assert(len(self.name) > 0)
        assert(len(self.head) == 1)

