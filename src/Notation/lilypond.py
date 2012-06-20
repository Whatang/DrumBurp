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
'''
Created on 4 Apr 2012

@author: Mike Thomas

'''
from __future__ import print_function
from contextlib import contextmanager
from Data.DrumKit import DrumKit

import sys

class Indenter(object):
    def __init__(self, spaces = 2):
        self._spaces = spaces
        self._level = 0
        self._handle = sys.stdout

    def __call__(self, *args, **kwargs):
        self.write(*args, **kwargs)

    def increase(self):
        self._level += self._spaces

    def decrease(self):
        self._level -= self._spaces

    def setHandle(self, handle):
        self._handle = handle

    def write(self, *args, **kwargs):
        print(" " * self._level, end = '', file = self._handle)
        kwargs['file'] = self._handle
        print(*args, **kwargs)

def makeLilyContext(opener, closer):
    def myLilyContext(indenter, context):
        indenter.write(" ".join(x for x in [context, opener] if x))
        indenter.increase()
        yield
        indenter.decrease()
        indenter.write(closer)
    return myLilyContext

LilyContext = contextmanager(makeLilyContext("{", "}"))
VoiceContext = contextmanager(makeLilyContext("<<", ">>"))

def lilyString(inString):
    return '"%s"' % inString

class LilyMeasure(object):
    def __init__(self, score, measure, kit):
        self.measure = measure
        self.score = score
        self.kit = kit
        self._beats = list(self.measure.counter.iterBeatTicks())
        self._voices = {DrumKit.UP:[], DrumKit.DOWN:[]}
        self._build()

    def _build(self):
        notes = {DrumKit.UP : [], DrumKit.DOWN : []}
        for notePos, head in self.measure:
            direction = self.kit.getDirection(notePos.drumIndex, head)
            notes[direction].append((notePos, head))
        noteTimes = {}
        for direction in notes:
            timeSet = set(notePos.noteTime  for (notePos, head)
                           in notes[direction])
            for tick in self.measure.counter.iterBeatTimes():
                timeSet.add(tick)
            timeSet.add(len(self._beats))
            noteTimes[direction] = list(timeSet)
            noteTimes[direction].sort()
        durations = {DrumKit.UP: {}, DrumKit.DOWN:{}}
        for direction, durationDict in durations.iteritems():
            for thisTime, nextTime in zip(noteTimes[direction][:-1],
                                          noteTimes[direction][1:]):
                unusedBeatNum, beat, tick = self._beats[thisTime]
                numTicks = nextTime - thisTime
                durationDict[thisTime] = beat.lilyDuration(numTicks)
        lilyNotes = {DrumKit.UP:{}, DrumKit.DOWN:{}}
        effects = {DrumKit.UP:{}, DrumKit.DOWN:{}}
        for direction, lilyDict in lilyNotes.iteritems():
            for (notePos, head) in notes[direction]:
                if notePos.noteTime not in lilyDict:
                    lilyDict[notePos.noteTime] = []
                noteIndicator, effect = self.kit.getLilyNote(notePos, head)
                lilyDict[notePos.noteTime].append(noteIndicator)
                effects[direction].setdefault(notePos.noteTime, []).append((noteIndicator, effect))
        wholeRests = {DrumKit.UP: {}, DrumKit.DOWN: {}}
        for direction, timeList in noteTimes.iteritems():
            lNotes = lilyNotes[direction]
            lEffects = effects[direction]
            voice = self._voices[direction]
            for noteTime in timeList[:-1]:
                dur = durations[direction][noteTime]
                accent = ""
                if noteTime in lEffects:
                    for noteIndicator, effect in lEffects[noteTime]:
                        if effect == "flam":
                            voice.append(r"\override Stem #'length = #4 \acciaccatura{%s8} \revert Stem #'length" % noteIndicator)
                        elif effect == "accent":
                            accent += r"\accent"
                        elif effect == "choke":
                            accent += r"\staccatissimo"
                        elif effect == "drag":
                            durString = str(int(dur.rstrip(".")) * 2)
                            if dur[-1] == ".":
                                durString += "."
                            tremolo = ":" + durString
                            accent = tremolo + accent
                        elif effect == "ghost":
                            noteIndex = lNotes[noteTime].index(noteIndicator)
                            lNotes[noteTime][noteIndex] = r"< \parenthesize " + noteIndicator + ">"
                if noteTime not in lNotes:
                    lNotes[noteTime] = ["r"]
                if len(lNotes[noteTime]) > 1:
                    voice.append("<" + " ".join(lNotes[noteTime]) + ">" + dur + accent)
                else:
                    voice.append(lNotes[noteTime][0] + dur + accent)
                    if lNotes[noteTime] == ["r"] and dur == "4":
                        wholeRests[direction][noteTime] = len(voice) - 1
        for direction, restTimes in wholeRests.iteritems():
            otherDirection = 1 - direction
            for (rest, index) in restTimes.iteritems():
                if rest not in wholeRests[otherDirection]:
                    self._voices[direction][index] = "s4"
        self._mergeRests(DrumKit.UP)
        self._mergeRests(DrumKit.DOWN)

    def _mergeRests(self, direction):
        resting = False
        start = None
        newRestLengths = {1: "4", 2: "2", 3:"2.", 4:"1"}
        newVoice = []
        for index, info in enumerate(self._voices[direction]):
            if info == "r4":
                if not resting:
                    resting = True
                    start = index
                elif index - start == 4:
                    newVoice.append("r1")
                    start = index
            elif resting:
                end = index
                restLength = end - start
                newLength = newRestLengths[restLength]
                newVoice.append("r" + newLength)
                newVoice.append(info)
                resting = False
            else:
                newVoice.append(info)
        if resting:
            end = len(self._voices[direction])
            restLength = end - start
            newLength = newRestLengths[restLength]
            newVoice.append("r" + newLength)
        self._voices[direction] = newVoice




    def voiceOne(self, indenter):
        voice = self._voices[DrumKit.UP]
        indenter(" ".join(voice))

    def voiceTwo(self, indenter):
        voice = self._voices[DrumKit.DOWN]
        indenter(" ".join(voice))

class LilyKit(object):
    _HEADS = {"default": "()",
              "harmonic black": "harmonic-black"}
    _EFFECTS = {"open":'"open"',
                "stopped":'"stopped"'}
    def __init__(self, kit):
        self._kit = kit
        self._lilyHeads = []
        self._lilyNames = []
        allLilyHeads = set()
        allLilyNames = set()
        headCount = 0
        for drum in kit:
            sanitized = "".join(ch.lower() for ch in drum.name if ch.isalpha())
            sanAbbr = "".join(ch.lower() for ch in drum.abbr if ch.isalpha())
            lilyHeads = {}
            lilyNames = {}
            headCount = 0
            for head in drum:
                ok = False
                headCount = -1
                lily = ""
                while not ok:
                    if headCount >= 0:
                        lily = chr(0x61 + headCount % 26)
                    elif headCount >= 26:
                        lily = chr(0x61 + headCount / 26) + chr(0x61 + headCount % 26)
                    headCount += 1
                    lHead = sanAbbr + lily
                    lName = sanitized + lily
                    ok = not(lHead in allLilyHeads or lName in allLilyNames)
                lilyHeads[head] = lHead
                lilyNames[head] = lName
                allLilyHeads.add(lHead)
                allLilyNames.add(lName)
            self._lilyHeads.append(lilyHeads)
            self._lilyNames.append(lilyNames)

    def _getLilyHead(self, notePos, head):
        return self._lilyHeads[notePos.drumIndex][head]

    def getLilyNote(self, notePos, head):
        lilyHead = self._getLilyHead(notePos, head)
        headData = self._kit[notePos.drumIndex].headData(head)
        effect = headData.notationEffect
        return lilyHead, effect

    def getDirection(self, drumIndex, head = None):
        headData = self._kit[drumIndex].headData(head)
        return headData.stemDirection

    def write(self, handle):
        print("drumPitchNames = #'(", end = '', file = handle)
        for drumIndex, drum in enumerate(self._kit):
            for head in drum:
                name = self._lilyNames[drumIndex][head]
                print("   (%s . %s)" % (name, name), file = handle)
        for drumIndex, drum in enumerate(self._kit):
            for head in drum:
                name = self._lilyNames[drumIndex][head]
                abbr = self._lilyHeads[drumIndex][head]
                print("   (%s . %s)" % (abbr, name), file = handle)
        print (")", file = handle)
        print("", file = handle)
        print("#(define dbdrums '(", file = handle)
        for drumIndex, drum in enumerate(self._kit):
            for head in drum:
                name = self._lilyNames[drumIndex][head]
                abbr = self._lilyHeads[drumIndex][head]
                headData = drum.headData(head)
                lilyNoteHead = self._HEADS.get(headData.notationHead,
                                               headData.notationHead)
                lilyEffect = self._EFFECTS.get(headData.notationEffect,
                                               "#f")
                print("   (%s %s %s %d)" % (name,
                                            lilyNoteHead,
                                            lilyEffect,
                                            headData.notationLine),
                      file = handle)
        print("))", file = handle)
        print ("", file = handle)


class LilypondScore(object):
    def __init__(self, score):
        self.score = score
        self._lilyKit = LilyKit(score.drumKit)
        self.scoreData = score.scoreData
        self.indenter = Indenter()

    def write(self, handle):
        self.indenter.setHandle(handle)
        self.indenter(r'\version "2.12.3"')
        with LilyContext(self.indenter, '\header'):
            self._writeHeader()
        self._writeMacros(handle)
        self._lilyKit.write(handle)
        with LilyContext(self.indenter, '\score'):
            self._writeScore()

    def _writeHeader(self):
        self.indenter('title = %s' % lilyString(self.scoreData.title))
        if self.scoreData.artistVisible:
            self.indenter('composer = %s' % lilyString(self.scoreData.artist))
        if self.scoreData.creatorVisible:
            self.indenter('arranger = %s' % lilyString(self.scoreData.creator))

    def _writeScore(self):
        with VoiceContext(self.indenter, r'\new DrumStaff'):
            self._writeDrumStaffInfo()
            with LilyContext(self.indenter, r'\drummode'):
                self._writeMusic()
        with LilyContext(self.indenter, r'\layout'):
            with LilyContext(self.indenter, r'\context'):
                self.indenter(r"\DrumStaff \override RestCollision #'positioning-done = #merge-rests-on-positioning")

    def _writeDrumStaffInfo(self):
        self.indenter(r'\set DrumStaff.drumStyleTable = #(alist->hash-table dbdrums)')
        self.indenter(r'\set Staff.instrumentName = #"Drums"')
        if self.scoreData.bpmVisible:
            self.indenter(r'\tempo 4 = %d' % self.scoreData.bpm)
        #self.indenter(r'\set DrumStaff.drumStyleTable = #(alist->hash-table mydrums)')
        self.indenter(r"\override Score.RehearsalMark #'self-alignment-X = #LEFT")

    def _writeMusic(self):
        measureIterator = self.score.iterMeasures()
        sectionTitle = self.score.getSectionTitle(0)
        sectionIndex = 0
        repeatCommands = []
        try:
            measure = measureIterator.next()
            hasAlternate = False
            while True:
                if sectionTitle:
                    self.indenter(r'\mark %s' % lilyString(sectionTitle))
                if measure.isRepeatStart():
                    repeatCommands.append("start-repeat")
                if measure.alternateText is not None:
                    if hasAlternate:
                        repeatCommands.append("(volta #f)")
                    repeatCommands.append("(volta %s)" % lilyString(measure.alternateText))
                    hasAlternate = True
                if repeatCommands:
                    self.indenter(r"\set Score.repeatCommands = #'(%s)" % " ".join(repeatCommands))
                    repeatCommands = []
                with VoiceContext(self.indenter, ""):
                    self._writeMeasure(measure)
                if measure.isRepeatEnd():
                    if measure.repeatCount > 2:
                        self.indenter(r"\once \override Score.RehearsalMark #'self-alignment-X = #right")
                        self.indenter(r'\mark %s' % lilyString("x%d" % measure.repeatCount))
                    repeatCommands.append("end-repeat")
                if measure.isSectionEnd():
                    sectionIndex += 1
                    if sectionIndex < self.score.numSections():
                        sectionTitle = self.score.getSectionTitle(sectionIndex)
                else:
                    sectionTitle = None
                if hasAlternate and (measure.isSectionEnd() or measure.isRepeatEnd()):
                    repeatCommands.append("(volta #f)")
                    hasAlternate = False
                if measure.isLineEnd() or measure.isSectionEnd():
                    self.indenter(r'\break')
                measure = measureIterator.next()
        except StopIteration:
            if repeatCommands:
                self.indenter(r"\set Score.repeatCommands = #'(%s)" % " ".join(repeatCommands))

    def _writeMeasure(self, measure):
        parsed = LilyMeasure(self.score, measure, self._lilyKit)
        with LilyContext(self.indenter, r'\new DrumVoice'):
            self.indenter(r'\voiceOne')
            parsed.voiceOne(self.indenter)
        with LilyContext(self.indenter, r'\new DrumVoice'):
            self.indenter(r'\voiceTwo')
            parsed.voiceTwo(self.indenter)

    def _writeMacros(self, handle):
        handle.write("""
#(define (rest-score r)
  (let ((score 0)
    (yoff (ly:grob-property-data r 'Y-offset))
    (sp (ly:grob-property-data r 'staff-position)))
    (if (number? yoff)
    (set! score (+ score 2))
    (if (eq? yoff 'calculation-in-progress)
        (set! score (- score 3))))
    (and (number? sp)
     (<= 0 2 sp)
     (set! score (+ score 2))
     (set! score (- score (abs (- 1 sp)))))
    score))

#(define (merge-rests-on-positioning grob)
  (let* ((can-merge #f)
     (elts (ly:grob-object grob 'elements))
     (num-elts (and (ly:grob-array? elts)
            (ly:grob-array-length elts)))
     (two-voice? (= num-elts 2)))
    (if two-voice?
    (let* ((v1-grob (ly:grob-array-ref elts 0))
           (v2-grob (ly:grob-array-ref elts 1))
           (v1-rest (ly:grob-object v1-grob 'rest))
           (v2-rest (ly:grob-object v2-grob 'rest)))
      (and
       (ly:grob? v1-rest)
       (ly:grob? v2-rest)                
       (let* ((v1-duration-log (ly:grob-property v1-rest 'duration-log))
          (v2-duration-log (ly:grob-property v2-rest 'duration-log))
          (v1-dot (ly:grob-object v1-rest 'dot))
          (v2-dot (ly:grob-object v2-rest 'dot))
          (v1-dot-count (and (ly:grob? v1-dot)
                     (ly:grob-property v1-dot 'dot-count -1)))
          (v2-dot-count (and (ly:grob? v2-dot)
                     (ly:grob-property v2-dot 'dot-count -1))))
         (set! can-merge
           (and 
            (number? v1-duration-log)
            (number? v2-duration-log)
            (= v1-duration-log v2-duration-log)
            (eq? v1-dot-count v2-dot-count)))
         (if can-merge
         ;; keep the rest that looks best:
         (let* ((keep-v1? (>= (rest-score v1-rest)
                      (rest-score v2-rest)))
            (rest-to-keep (if keep-v1? v1-rest v2-rest))
            (dot-to-kill (if keep-v1? v2-dot v1-dot)))
           ;; uncomment if you're curious of which rest was chosen:
           ;;(ly:grob-set-property! v1-rest 'color green)
           ;;(ly:grob-set-property! v2-rest 'color blue)
           (ly:grob-suicide! (if keep-v1? v2-rest v1-rest))
           (if (ly:grob? dot-to-kill)
               (ly:grob-suicide! dot-to-kill))
           (ly:grob-set-property! rest-to-keep 'direction 0)
           (ly:rest::y-offset-callback rest-to-keep)))))))
    (if can-merge
    #t
    (ly:rest-collision::calc-positioning-done grob))))
    
""")
