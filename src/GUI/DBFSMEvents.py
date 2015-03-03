# Copyright 2011-12 Michael Thomas
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
'''Created on Feb 26, 2012

@author: Mike
'''
class FsmEvent(object):
    pass

class _MouseEvent(FsmEvent):
    def __init__(self, measure, note, screenPos = None):
        super(_MouseEvent, self).__init__()
        self.measure = measure
        self.note = note
        self.screenPos = screenPos

class LeftPress(_MouseEvent):
    pass

class RightPress(_MouseEvent):
    pass

class MidPress(_MouseEvent):
    pass

class MouseMove(_MouseEvent):
    pass

class MouseRelease(_MouseEvent):
    pass

class Escape(FsmEvent):
    pass

class MenuSelect(FsmEvent):
    def __init__(self, data = None):
        super(MenuSelect, self).__init__()
        self.data = data

class MenuCancel(FsmEvent):
    pass

class RepeatNotes(FsmEvent):
    pass

class MeasureLineContext(FsmEvent):
    def __init__(self, prevMeasure, nextMeasure, endNote, startNote, screenPos):
        super(MeasureLineContext, self).__init__()
        self.prevMeasure = prevMeasure
        self.nextMeasure = nextMeasure
        self.endNote = endNote
        self.startNote = startNote
        self.screenPos = screenPos

class MeasureCountContext(_MouseEvent):
    pass

class StartPlaying(FsmEvent):
    pass

class StopPlaying(FsmEvent):
    pass

class _MeasureEvents(FsmEvent):
    def __init__(self, measurePosition):
        super(_MeasureEvents, self).__init__()
        self.measurePosition = measurePosition

class EditMeasureProperties(_MeasureEvents):
    def __init__(self, counter, counterRegistry, measurePosition):
        super(EditMeasureProperties, self).__init__(measurePosition)
        self.counter = counter
        self.counterRegistry = counterRegistry

class SetAlternateEvent(_MeasureEvents):
    def __init__(self, alternateText, measurePosition):
        super(SetAlternateEvent, self).__init__(measurePosition)
        self.alternateText = alternateText

class ChangeRepeatCount(_MeasureEvents):
    def __init__(self, repeatCount, measurePosition):
        super(ChangeRepeatCount, self).__init__(measurePosition)
        self.repeatCount = repeatCount
