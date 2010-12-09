'''
Created on 5 Dec 2010

@author: Mike Thomas

'''

class DBTime(object):
    '''
    classdocs
    '''


    def __init__(self, scoreTime = None, systemTime = None, system = None):
        if scoreTime is None and systemTime is None:
            raise ValueError()
        self._system = system
        self._scoreTime = scoreTime
        self._systemTime = systemTime

    @property
    def scoreTime(self):
        if self._scoreTime is None:
            return self._system.startTime + self._systemTime
        else:
            return self._scoreTime

    @property
    def systemTime(self):
        if self._systemTime is None:
            return self._scoreTime - self._system.startTime
        else:
            return self._systemTime
