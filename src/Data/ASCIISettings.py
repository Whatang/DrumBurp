'''
Created on Jan 30, 2011

@author: Mike
'''

class ASCIISettings(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._checkNames = []
        self._registerCheckName("metadata")
        self._registerCheckName("kitKey")
        self._registerCheckName("omitEmpty")
        self._registerCheckName("underline")
        self._registerCheckName("printCounts")
        self._registerCheckName("emptyLineBeforeSection")
        self._registerCheckName("emptyLineAfterSection")

    def _registerCheckName(self, name, defaultValue = True):
        setattr(self, name, defaultValue)
        self._checkNames.append(name)

    def checkNames(self):
        return self._checkNames
