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
import collections
from Data.DrumKit import DrumKit
from DBVersion import DB_VERSION

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

LILY_CONTEXT = contextmanager(makeLilyContext("{", "}"))
VOICE_CONTEXT = contextmanager(makeLilyContext("<<", ">>"))

class LilypondProblem(RuntimeError):
    pass

class TripletsProblem(LilypondProblem):
    "DrumBurp cannot yet set triplets in Lilypond"

class FiveSixthsProblem(LilypondProblem):
    "DrumBurp cannot set notes of length 5/6 beat."

class FiveEighthsProblem(LilypondProblem):
    "DrumBurp cannot set notes of length 5/8 beat."

class SevenEighthsProblem(LilypondProblem):
    "DrumBurp cannot set notes of length 7/8 beat."

class FiveTwelfthsProblem(LilypondProblem):
    "DrumBurp cannot set notes of length 5/12 beat."

class SevenTwelfthsProblem(LilypondProblem):
    "DrumBurp cannot set notes of length 7/12 beat."

class ElevenTwelfthsProblem(LilypondProblem):
    "DrumBurp cannot set notes of length 11/12 beat."

def lilyDuration(beat, ticks):
    dur = None
    if ticks == beat.numTicks:
        dur = "4"
    elif beat.numTicks % 3 == 0:
        if ticks * 6 == 5 * beat.numTicks:
            raise FiveSixthsProblem()
        elif ticks * 3 == 2 * beat.numTicks:
            dur = "@4"
        elif ticks * 2 == beat.numTicks:
            dur = "@8."
        elif ticks * 3 == beat.numTicks:
            dur = "@8"
        elif ticks * 6 == beat.numTicks:
            dur = "@16"
        elif ticks * 12 == beat.numTicks:
            dur = "@32"
        elif ticks * 4 == beat.numTicks:
            dur = "@16."
        elif ticks * 12 == 5 * beat.numTicks:
            raise FiveTwelfthsProblem()
        elif ticks * 12 == 7 * beat.numTicks:
            raise SevenTwelfthsProblem()
        elif ticks * 12 == 11 * beat.numTicks:
            raise ElevenTwelfthsProblem()
    else:
        if 2 * ticks == beat.numTicks:
            dur = "8"
        elif 4 * ticks == beat.numTicks:
            dur = "16"
        elif 4 * ticks == 3 * beat.numTicks:
            dur = "8."
        elif 8 * ticks == beat.numTicks:
            dur = "32"
        elif 8 * ticks == 3 * beat.numTicks:
            dur = "16."
        elif 8 * ticks == 5 * beat.numTicks:
            raise FiveEighthsProblem()
        elif 8 * ticks == 7 * beat.numTicks:
            raise SevenEighthsProblem()
    return dur


def lilyString(inString):
    return '"%s"' % inString

class LilyMeasure(object):
    _FLAM_STRING = (r"\override Stem #'length = #4 \acciaccatura{%s8} "
                    + r"\revert Stem #'length")
    _ACCENT_STRING = r"\accent"
    _CHOKE_STRING = r"\staccatissimo"

    def __init__(self, score, measure, kit):
        self.measure = measure
        self.score = score
        self.kit = kit
        self._beats = list(self.measure.counter.iterBeatTicks())
        self._voices = {DrumKit.UP:[], DrumKit.DOWN:[]}
        self._build()


    def _separateNotesByDirection(self):
        notes = {DrumKit.UP:[], DrumKit.DOWN:[]}
        for notePos, head in self.measure:
            direction = self.kit.getDirection(notePos.drumIndex, head)
            notes[direction].append((notePos, head))
        return notes


    def _calculateNoteTimes(self, notes):
        noteTimes = {}
        for direction in notes:
            timeSet = set(notePos.noteTime for (notePos, head) in
                notes[direction])
            for tick in self.measure.counter.iterBeatTimes():
                timeSet.add(tick)

            timeSet.add(len(self._beats))
            noteTimes[direction] = list(timeSet)
            noteTimes[direction].sort()
        return noteTimes

    def _calculateDurations(self, noteTimes):
        durations = {}
        for direction, timeList in noteTimes.iteritems():
            durationDict = {}
            for thisTime, nextTime in zip(timeList[:-1],
                timeList[1:]):
                unusedBeatNum, beat, tick_ = self._beats[thisTime]
                numTicks = nextTime - thisTime
                durationDict[thisTime] = lilyDuration(beat, numTicks)
            durations[direction] = durationDict
        return durations


    def _getLilyNotesAndEffects(self, notes):
        lilyNotes = {}
        effects = {DrumKit.UP:{}, DrumKit.DOWN:{}}
        for direction, timeList in notes.iteritems():
            lilyDict = {}
            effectsDict = collections.defaultdict(list)
            for notePos, head in timeList:
                if notePos.noteTime not in lilyDict:
                    lilyDict[notePos.noteTime] = []
                noteIndicator, effect = self.kit.getLilyNote(notePos, head)
                lilyDict[notePos.noteTime].append(noteIndicator)
                effectsDict[notePos.noteTime].append((noteIndicator, effect))
            lilyNotes[direction] = lilyDict
            effects[direction] = effectsDict
        return lilyNotes, effects


    @staticmethod
    def _makeDrag(dur):
        durString = str(int(dur.rstrip(".")) * 2)
        if dur[-1] == ".":
            durString += "."
        return ":" + durString

    @staticmethod
    def _makeNoteString(lNotes):
        if len(lNotes) > 1 or lNotes[0].startswith(r"\paren"):
            noteString = "<" + " ".join(lNotes) + ">"
        else:
            noteString = lNotes[0]
        return noteString


    def _buildVoices(self, noteTimes, durations, lilyNotes, effects):
        wholeRests = collections.defaultdict(dict)
        for direction, timeList in noteTimes.iteritems():
            lNotes = lilyNotes[direction]
            lEffects = effects[direction]
            voice = self._voices[direction]
            isTriplet = False
            for noteTime in timeList[:-1]:
                dur = durations[direction][noteTime]
                if dur.startswith("@"):
                    dur = dur[1:]
                    if not isTriplet:
                        if dur == "8.":
                            dur = "8"
                        else:
                            isTriplet = True
                            voice.append(r"\times 2/3 {")
                elif isTriplet:
                    voice.append("}")
                    isTriplet = False
                accent = ""
                if noteTime in lEffects:
                    for noteIndicator, effect in lEffects[noteTime]:
                        if effect == "flam":
                            voice.append(self._FLAM_STRING % noteIndicator)
                        elif effect == "accent":
                            accent += self._ACCENT_STRING
                        elif effect == "choke":
                            accent += self._CHOKE_STRING
                        elif effect == "drag":
                            accent = self._makeDrag(dur) + accent
                        elif effect == "ghost":
                            noteIndex = lNotes[noteTime].index(noteIndicator)
                            lNotes[noteTime][noteIndex] = (r"\parenthesize " +
                                                           noteIndicator)
                if noteTime not in lNotes:
                    lNotes[noteTime] = ["r"]
                if lNotes[noteTime] == ["r"] and dur == "4":
                    wholeRests[direction][noteTime] = len(voice)
                voice.append(self._makeNoteString(lNotes[noteTime])
                             + dur + accent)
            if isTriplet:
                voice.append("}")
        return wholeRests

    def _build(self):
        notes = self._separateNotesByDirection()
        noteTimes = self._calculateNoteTimes(notes)
        durations = self._calculateDurations(noteTimes)
        lilyNotes, effects = self._getLilyNotesAndEffects(notes)
        wholeRests = self._buildVoices(noteTimes, durations, lilyNotes, effects)
        for direction, restTimes in wholeRests.iteritems():
            otherDirection = 1 - direction
            for (rest, index) in restTimes.iteritems():
                if (otherDirection not in wholeRests
                    or rest not in wholeRests[otherDirection]):
                    self._voices[direction][index] = "s4"
        self._mergeWholeRests(DrumKit.UP)
        self._mergeWholeRests(DrumKit.DOWN)

    def _mergeWholeRests(self, direction):
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
        reservedNames = set(["s", "r"])
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
                        lily = (chr(0x61 + headCount / 26)
                                + chr(0x61 + headCount % 26))
                    headCount += 1
                    lHead = sanAbbr + lily
                    lName = sanitized + lily
                    ok = not(lHead in allLilyHeads or lName in allLilyNames
                             or lHead in reservedNames)
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

_PAPER_SIZES = { "A0" : "a0",
                 "A1" : "a1",
                 "A2" : "a2",
                 "A3" : "a3",
                 "A4" : "a4",
                 "A5" : "a5",
                 "A6" : "a6",
                 "A7" : "a7",
                 "A8" : "a8",
                 "A9" : "a9",
                 "B0" : "b0",
                 "B1" : "b1",
                 "B10" : "b10",
                 "B2" : "b2",
                 "B3" : "b3",
                 "B4" : "b4",
                 "B5" : "b5",
                 "B6" : "b6",
                 "B7" : "b7",
                 "B8" : "b8",
                 "B9" : "b9",
                 "C5E" : "c5",
                 "Executive" : "executive",
                 "Folio" : "folio",
                 "Ledger" : "ledger",
                 "Legal" : "legal",
                 "Letter" : "letter",
                 "Tabloid" : "tabloid" }

class BadPaperSize(LilypondProblem):
    "DrumBurp cannot create a Lilypond score on this paper size."
class LilypondScore(object):
    def __init__(self, score):
        self.score = score
        self._lilyKit = LilyKit(score.drumKit)
        self._paperSize = str(score.paperSize)
        self.scoreData = score.scoreData
        self._lilysize = score.lilysize
        self._numPages = score.lilypages
        self._lilyFill = score.lilyFill
        self.indenter = Indenter()
        self._timeSig = None
        self._lastTimeSig = None
        self._hadRepeatCount = False

    def write(self, handle):
        self.indenter.setHandle(handle)
        self.indenter(r'\version "2.12.3"')
        with LILY_CONTEXT(self.indenter, r"\paper"):
            self._writePaper()
        with LILY_CONTEXT(self.indenter, r'\header'):
            self._writeHeader()
        with LILY_CONTEXT(self.indenter, r'\layout'):
            self._writeLayout()
        self._writeMacros(handle)
        self._lilyKit.write(handle)
        with LILY_CONTEXT(self.indenter, '\score'):
            self._writeScore()

    def _writePaper(self):
        paperSize = _PAPER_SIZES.get(self._paperSize, None)
        if paperSize is None:
            raise BadPaperSize(self._paperSize)
        self.indenter(r'#(set-paper-size %s)' % lilyString(paperSize))
        if self._numPages != 0:
            self.indenter(r'page-count = #%d' % self._numPages)
        if self._lilyFill:
            self.indenter(r'ragged-last-bottom = ##f')

    def _writeHeader(self):
        self.indenter('title = %s' % lilyString(self.scoreData.title))
        self.indenter(r'tagline = #(string-append "Score created using DrumBurp %s, engraved with Lilypond " (lilypond-version))' % DB_VERSION)
        if self.scoreData.artistVisible:
            self.indenter('composer = %s' % lilyString(self.scoreData.artist))
        if self.scoreData.creatorVisible:
            self.indenter('arranger = %s' % lilyString(self.scoreData.creator))

    def _writeLayout(self):
        self.indenter(r'#(layout-set-staff-size %d)' % self._lilysize)

    def _writeScore(self):
        with VOICE_CONTEXT(self.indenter, r'\new DrumStaff'):
            self._writeDrumStaffInfo()
            with LILY_CONTEXT(self.indenter, r'\drummode'):
                self._writeMusic()
        with LILY_CONTEXT(self.indenter, r'\layout'):
            with LILY_CONTEXT(self.indenter, r'\context'):
                self.indenter(r"\DrumStaff \override RestCollision " +
                              r"#'positioning-done = " +
                              r"#merge-rests-on-positioning")

    def _writeDrumStaffInfo(self):
        self.indenter(r'\set DrumStaff.drumStyleTable ' +
                      r'= #(alist->hash-table dbdrums)')
        self.indenter(r'\set Staff.instrumentName = #"Drums"')
        if self.scoreData.bpmVisible:
            self.indenter(r'\tempo 4 = %d' % self.scoreData.bpm)
        self.indenter(r"\override Score.RehearsalMark " +
                      r"#'self-alignment-X = #LEFT")


    @staticmethod
    def _getNextRepeats(repeatCommands, hasAlternate, measure):
        if measure.isRepeatStart():
            repeatCommands.append("start-repeat")
        if measure.alternateText is not None:
            if hasAlternate:
                repeatCommands.append("(volta #f)")
            repeatCommands.append("(volta %s)" %
                                  lilyString(measure.alternateText))
            hasAlternate = True
        return hasAlternate


    def _writeSectionTitle(self, sectionTitle):
        if sectionTitle:
            if self._hadRepeatCount:
                self._hadRepeatCount = False
                self.indenter(r'\bar "|"')
                self.indenter(r"\cadenzaOn")
                self.indenter(r"\once \override Score.TimeSignature #'stencil = ##f")
                self.indenter(r"\time 1/32")
                self.indenter(r"s32")
                self.indenter(r'\bar ""')
                self.indenter(r"\cadenzaOff")
                if self._timeSig == self._lastTimeSig:
                    self.indenter(r"\once \override Score.TimeSignature #'stencil = ##f")
                self.indenter(r"\time %s" % self._timeSig)
                self._lastTimeSig = self._timeSig
            self.indenter(r'\mark %s' % lilyString(sectionTitle))
            sectionTitle = None
        return sectionTitle


    def _getLastRepeats(self, repeatCommands, hasAlternate, measure):
        self._hadRepeatCount = False
        if measure.isRepeatEnd():
            if measure.repeatCount > 2:
                self._hadRepeatCount = True
                self.indenter(r"\once \override Score.RehearsalMark " +
                              r"#'break-visibility = #begin-of-line-invisible")
                self.indenter(r"\once \override Score.RehearsalMark " +
                              r"#'self-alignment-X = #right")
                self.indenter(r'\mark %s'
                              % lilyString("x%d" % measure.repeatCount))
            repeatCommands.append("end-repeat")
        if hasAlternate and (measure.isSectionEnd() or
            measure.isRepeatEnd()):
            repeatCommands.append("(volta #f)")
            hasAlternate = False
        return hasAlternate


    def _getNextSectionTitle(self, sectionIndex):
        sectionIndex += 1
        sectionTitle = None
        if sectionIndex < self.score.numSections():
            sectionTitle = self.score.getSectionTitle(sectionIndex)
        return sectionIndex, sectionTitle

    @staticmethod
    def _getTimeSig(measure):
        counter = measure.counter
        return "%d/%d" % counter.timeSig()

    def _writeMusic(self):
        secIndex, secTitle = self._getNextSectionTitle(-1)
        repeatCommands = []
        hasAlternate = False
        self._lastTimeSig = None
        for measure in self.score.iterMeasures():
            hasAlternate = self._getNextRepeats(repeatCommands,
                                                hasAlternate, measure)
            if repeatCommands:
                self.indenter(r"\set Score.repeatCommands = #'(%s)" %
                              " ".join(repeatCommands))
                repeatCommands = []
            self._timeSig = self._getTimeSig(measure)
            secTitle = self._writeSectionTitle(secTitle)
            if self._timeSig != self._lastTimeSig:
                self.indenter(r"\time %s" % self._timeSig)
                self._lastTimeSig = self._timeSig
            with VOICE_CONTEXT(self.indenter, ""):
                self._writeMeasure(measure)
            hasAlternate = self._getLastRepeats(repeatCommands,
                                                hasAlternate, measure)
            if measure.isSectionEnd():
                secIndex, secTitle = self._getNextSectionTitle(secIndex)
            if measure.isLineEnd() or measure.isSectionEnd():
                self.indenter(r'\break')
        if repeatCommands:
            self.indenter(r"\set Score.repeatCommands = #'(%s)"
                          % " ".join(repeatCommands))

    def _writeMeasure(self, measure):
        parsed = LilyMeasure(self.score, measure, self._lilyKit)
        with LILY_CONTEXT(self.indenter, r'\new DrumVoice'):
            self.indenter(r'\voiceOne')
            parsed.voiceOne(self.indenter)
        with LILY_CONTEXT(self.indenter, r'\new DrumVoice'):
            self.indenter(r'\voiceTwo')
            parsed.voiceTwo(self.indenter)

    @staticmethod
    def _writeMacros(handle):
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
