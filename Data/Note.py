'''
Created on 1 Aug 2010

@author: Mike Thomas

'''

class Note(object):
    '''
    classdocs
    '''


    def __init__(self, time, lineIndex, head):
        '''
        Constructor
        '''
        self.time = time
        self.lineIndex = lineIndex
        self.head = head

    def __cmp__(self, other):
        '''
        Notes are compared on their time first, and then their lineIndex.
        
        If two Notes have the same time and lineIndex, they are considered
        equal, not matter what their 'head' value is.
        
        >>> n1 = Note(0,0,"x")
        >>> n2 = Note(1,0,"x")
        >>> n1 < n2
        True
        >>> n1 == Note(0,0,"o")
        True
        >>> Note(0,0,"x") < Note(0,1,"x")
        True
        '''
        return (cmp(self.time, other.time)
                or cmp(self.lineIndex, other.lineIndex))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
