'''
Created on 16 Apr 2011

@author: Mike Thomas

'''


from DBConstants import BEAT_COUNT
class Counter(object):
    '''
    classdocs
    '''


    def __init__(self, counts):
        '''
        Constructor
        '''
        self._counts = counts

    def __iter__(self):
        return iter(self._counts)

    def __len__(self):
        return len(self._counts)

    def __str__(self):
        return self._counts

    def write(self, handle, indenter):
        print >> handle, indenter("COUNT", "|" + self._counts + "|")

_COUNTER_BEAT = Counter(BEAT_COUNT)
_EIGHTH_COUNT = Counter(BEAT_COUNT + "+")
_TRIPLET_COUNT = Counter(BEAT_COUNT + "ea")
_SIXTEENTH_COUNT = Counter(BEAT_COUNT + "e+a")
_SIXTEENTH_COUNT_SPARSE = Counter(BEAT_COUNT + ' + ')
_SIXTEENTH_TRIPLETS = Counter(BEAT_COUNT + 'ea+ea')
_SIXTEENTH_TRIPLETS_SPARSE = Counter(BEAT_COUNT + '  +  ')

class CounterRegistry(object):
    def __init__(self, defaults = True):
        self._names = []
        self._counts = {}
        if defaults:
            self.restoreDefaults()

    def clear(self):
        self._names = []
        self._counts = {}

    def restoreDefaults(self):
        self.register('Quarter Notes', _COUNTER_BEAT)
        self.register('8ths', _EIGHTH_COUNT)
        self.register('Triplets', _TRIPLET_COUNT)
        self.register('16ths', _SIXTEENTH_COUNT)
        self.register('Sparse 16ths', _SIXTEENTH_COUNT_SPARSE)
        self.register('16th Triplets', _SIXTEENTH_TRIPLETS)
        self.register('Sparse 16th Triplets', _SIXTEENTH_TRIPLETS_SPARSE)

    def register(self, name, count):
        if count not in self._counts:
            self._names.append(name)
            self._counts[name] = count
        else:
            raise KeyError('%s already exists' % name)

    def __iter__(self):
        for name in self._names:
            yield (name, self._counts[name])

    def countsByTicks(self, countLength):
        for name, count in self:
            if len(count) == countLength:
                yield name, count

    def getCounterByName(self, name):
        return self._counts[name]

    def __getitem__(self, index):
        return self._counts[self._names[index]]




