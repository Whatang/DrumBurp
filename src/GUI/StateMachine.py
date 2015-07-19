# Copyright 2015 Michael Thomas
#
# See www.whatang.org for more information.
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DrumBurp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DrumBurp.  If not, see <http://www.gnu.org/licenses/>
'''
Created on Jul 19, 2015

@author: Mike Thomas
'''

class _StateMachineMetaClass(type):
    def __new__(mcs, name, bases, attrs):
        # We want every sub-class of StateMachine to get its own set of states
        # and transitions.
        attrs["_states"] = set()
        attrs["_transitions"] = {}
        return super(_StateMachineMetaClass, mcs).__new__(mcs, name, bases, attrs)

class StateMachine(object):
    __metaclass__ = _StateMachineMetaClass
    _states = set()
    _transitions = {}
    SIMPLE = 0
    FACTORY = 1

    def __init__(self, initialStateType):
        assert initialStateType in self._states
        self._state = initialStateType(self, None)

    def set_state(self, stateType):
        assert stateType in self._states
        self._state = stateType(self, None)

    @classmethod
    def add_state(cls, state):
        cls._states.add(state)
        cls._transitions[state] = {}
        return state

    @classmethod
    def add_transition(cls, oldState, eventType, newState, function = None, guard = None):
        assert issubclass(oldState, State)
        assert issubclass(newState, State)
        assert oldState in cls._states
        cls._transitions[oldState][eventType] = (cls.SIMPLE, (newState, function, guard))

    @classmethod
    def add_factory_transition(cls, oldState, eventType, factory):
        assert issubclass(oldState, State)
        assert oldState in cls._states
        cls._transitions[oldState][eventType] = (cls.FACTORY, factory)

    def send_event(self, event):
        newState = self._getNewState(event)
        if newState is not None:
            # print type(newState).__name__
            assert type(newState) in self._states
            self._state = newState

    def _getNewState(self, event):
        # print type(self._state).__name__, type(event).__name__
        transitionLookup = self._transitions[type(self._state)]
        eventType = type(event)
        if eventType not in transitionLookup:
            return
        transType, transition = transitionLookup[eventType]
        if transType == self.SIMPLE:
            newState, function, guard = transition
            if function is not None:
                function(self._state, event)
            if guard is not None:
                if not guard(self._state, event):
                    return
            return newState(self, event)
        elif transType == self.FACTORY:
            return transition(self._state, event)
        else:
            return

class State(object):
    def __init__(self, machine, event):
        self.machine = machine
        self.event = event
        self.initialize()

    def initialize(self):
        pass
