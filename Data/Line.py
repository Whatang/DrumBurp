'''
Created on 31 Jul 2010

@author: Mike Thomas

'''


class Line(object):
    '''
    classdocs
    '''

    def __init__(self, instrument):
        '''
        Create a Line for the given Instrument.
        
        @param instrument: The Instrument for this Line.       
        @type instrument: Data.Instrument.Instrument
        
        >>> import Data.Instrument as Instrument
        >>> instr = Instrument.Instrument('test')
        >>> line = Line(instr)
        '''
        self._notes = {}
        self.instrument = instrument

    def __len__(self):
        '''
        The length of this line in ticks.
        
        @rtype: int
        
        >>> import Data.Instrument as Instrument
        >>> instr = Instrument.Instrument('test')
        >>> line = Line(instr)
        >>> len(line)
        0
        >>> line.addNote(0)
        >>> len(line)
        1
        >>> line.addNote(9)
        >>> len(line)
        10
        '''
        try:
            return 1 + max(self._notes.iterkeys())
        except ValueError:
            return 0

    def __iter__(self):
        '''
        Iterate over all the notes in this line, in random order.
        
        Each returned object is a 2-tuple of (note time, note head).
        
        >>> import Data.Instrument as Instrument
        >>> line = Line(Instrument.Instrument("test"))
        >>> list(iter(line))
        []
        >>> line.addNote(2)
        >>> list(iter(line))
        [(2, 'x')]
        >>> line.addNote(1,"o")
        >>> notes = list(iter(line))
        >>> notes.sort()
        >>> notes
        [(1, 'o'), (2, 'x')]
        '''
        noteTimes = self._notes.keys()
        noteTimes.sort()
        for t in noteTimes:
            yield (t, self._notes[t])

    def addNote(self, noteTime, head = None):
        '''
        Add a note with the given head at the given time.
        
        If no head is given the default for the Instrument associated with this
        line is used.
        
        @type noteTime: int
        @type head: str
        @invariant: head == None or len(head) == 1
        @invariant: noteTime >= 0
        
        >>> import Data.Instrument as Instrument
        >>> instr = Instrument.Instrument("test", "x")
        >>> line = Line(instr)
        >>> line.addNote(0)
        >>> line.noteAtTime(0)
        'x'
        >>> line.addNote(1, 'o')
        >>> line.noteAtTime(1)
        'o'
        >>> line.addNote(-1)
        Traceback (most recent call last):
        ...
        AssertionError
        >>> line.addNote(2, 'xxx')
        Traceback (most recent call last):
        ...
        AssertionError
        '''
        assert(noteTime >= 0)
        assert(head is None or len(head) == 1)
        if head is None:
            head = self.instrument.head
        self._notes[noteTime] = head

    def delNote(self, noteTime):
        '''
        Delete the note at the given time.
        @type noteTime: int
        @invariant: noteTime >= 0
        
        >>> import Data.Instrument as Instrument
        >>> instr = Instrument.Instrument("test", "x")
        >>> line = Line(instr)
        >>> line.addNote(1)
        >>> line.delNote(1)
        >>> len(line)
        0
        >>> line.delNote(1)
        >>> len(line)
        0
        '''
        assert(noteTime >= 0)
        self._notes.pop(noteTime, None)

    def noteAtTime(self, noteTime):
        '''
        Return the note head on this line at the given time.
        @type noteTime: int
        @invariant: noteTime >= 0 
        '''
        assert(noteTime >= 0)
        return self._notes.get(noteTime, None)
