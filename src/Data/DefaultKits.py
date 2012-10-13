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
Created on 17 Sep 2011

@author: Mike Thomas
'''
STEM_UP = 0
STEM_DOWN = 1

# [((Drum name, abbreviation, default head, locked), Midi note, lilypond symbol, lilypond position, lilypond stem direction)*]
DEFAULT_KIT = [(("Foot pedal", "Hf", "x", False), 44, "cross", -5 , STEM_DOWN),
               (("Kick", "Bd", "o", True), 36, "default", -3, STEM_DOWN),
               (("Floor Tom", "FT", "o", False), 43, "default", -1, STEM_DOWN),
               (("Snare", "Sn", "o", True), 38, "default", 1, STEM_DOWN),
               (("Mid Tom", "MT", "o", False), 47, "default", 2, STEM_DOWN),
               (("High Tom", "HT", "o", False), 50, "default", 3, STEM_DOWN),
               (("Ride", "Ri", "x", False), 51, "cross", 4, STEM_UP),
               (("HiHat", "Hh", "x", False), 42, "cross", 5, STEM_UP),
               (("Crash", "Cr", "x", False), 49, "cross", 6, STEM_UP)]

ACCENT_VOLUME = 127
GHOST_VOLUME = 50
#pylint:disable-msg=C0301
# {Abbr: [(Head, MIDI note or None for default, MIDI volume or None for default, Midi effect, lilypond symbol, lilypond effect, keyboard shortcut)*]}
DEFAULT_EXTRA_HEADS = {"FT": [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "o"),
                              ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                              ("f", None, None, "flam", "default", "flam", "f"),
                              ("d", None, None, "drag", "default", "drag", "d")],
                       "Sn": [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "o"),
                              ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                              ("x", 37, None, "normal", "cross", "none", "x"),
                              ("f", None, None, "flam", "default", "flam", "f"),
                              ("d", None, None, "drag", "default", "drag", "d")],
                       "MT": [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "o"),
                              ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                              ("f", None, None, "flam", "default", "flam", "f"),
                              ("d", None, None, "drag", "default", "drag", "d")],
                       "HT": [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "o"),
                              ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                              ("f", None, None, "flam", "default", "flam", "f"),
                              ("d", None, None, "drag", "default", "drag", "d")],
                       "Ri": [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "x"),
                              ("b", 53, None, "normal", "triangle", "none", "b"),
                              ("d", None, None, "drag", "cross", "drag", "d")],
                       "Hh": [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "x"),
                              ("o", 46, None, "normal", "cross", "open", "o"),
                              ("O", 46, ACCENT_VOLUME, "accent", "cross", "accent", "a"),
                              ("d", None, None, "drag", "cross", "drag", "d"),
                              ("+", None, None, "choke", "cross", "stopped", "s"),
                              ("#", None, None, "choke", "cross", "choke", "c")],
                       "Cr": [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "x"),
                              ("#", None, None, "choke", "cross", "stopped", "c")],
                       "Bd": [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "o"),
                              ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                              ("d", None, None, "drag", "default", "drag", "d")],
                       "Hf" : []}

DEFAULT_KIT_INFO = {"drums":DEFAULT_KIT,
                    "heads":DEFAULT_EXTRA_HEADS}

TTABS_DRUMS = [(("Bass drum", "B", "o", True), 36, "default", -3, STEM_DOWN),
               (("Floor Tom", "FT", "o", False), 43, "default", -1, STEM_DOWN),
               (("Mid Tom", "T", "o", False), 47, "default", 2, STEM_DOWN),
               (("Snare", "S", "o", True), 38, "default", 1, STEM_DOWN),
               (("Hi-Hat with foot", "Hf", "x", False), 44, "cross", -5 , STEM_DOWN),
               (("HiHat", "HH", "x", False), 42, "cross", 5, STEM_UP),
               (("Ride Cymbal", "Rd", "x", False), 51, "cross", 4, STEM_UP),
               (("Crash-ride cymbal", "CR", "x", False), 57, "cross", 7, STEM_UP),
               (("Crash cymbal", "CC", "x", False), 49, "cross", 6, STEM_UP)]

TTABS_EXTRA = {"B": [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "o"),
                     ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                     ("d", None, None, "drag", "default", "drag", "d")],
               "FT": [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "o"),
                      ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                      ("f", None, None, "flam", "default", "flam", "f"),
                      ("b", None, GHOST_VOLUME, "default", "none", "b"),
                      ("B", None, ACCENT_VOLUME, "default", "accent", "r"),
                      ("d", None, None, "drag", "default", "drag", "d")],
               "S": [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "o"),
                     ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                     ("@", 37, None, "normal", "cross", "none", "x"),
                     ("f", None, None, "flam", "default", "flam", "f"),
                     ("b", None, GHOST_VOLUME, "default", "none", "b"),
                     ("B", None, ACCENT_VOLUME, "default", "accent", "r"),
                     ("d", None, None, "drag", "default", "drag", "d")],
               "T": [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "o"),
                     ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                     ("f", None, None, "flam", "default", "flam", "f"),
                     ("b", None, GHOST_VOLUME, "default", "none", "b"),
                     ("B", None, ACCENT_VOLUME, "default", "accent", "r"),
                     ("d", None, None, "drag", "default", "drag", "d")],
               "HH": [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "x"),
                      ("o", 46, None, "normal", "cross", "open", "o"),
                      ("d", None, None, "drag", "cross", "drag", "d"),
                      ("#", None, None, "choke", "cross", "choke", "c")],
               "Rd": [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "x"),
                      ("b", 53, None, "normal", "triangle", "none", "b"),
                      ("d", None, None, "drag", "cross", "drag", "d")],
               "CR": [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "x"),
                      ("b", 53, None, "normal", "triangle", "none", "b"),
                      ("#", None, None, "choke", "cross", "stopped", "c")],
               "CC": [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "x"),
                      ("b", 53, None, "normal", "triangle", "none", "b"),
                      ("#", None, None, "choke", "cross", "stopped", "c")], }

TTABS_KIT = {"drums":TTABS_DRUMS, "heads":TTABS_EXTRA}

NAMED_DEFAULTS = {"Default": DEFAULT_KIT_INFO, "TTabs.com": TTABS_KIT}
DEFAULT_KIT_NAMES = ["Default", "TTabs.com"]

MVK_DRUMS = [(("Hihat w/foot", "Hf", "o", False), 44, "normal", -5, STEM_DOWN),
             (("Bass drum", "BD", "o", True), 35, "normal", -3, STEM_DOWN),
             (("Floor Tom 2", "F2", "o", False), 41, "normal", -2, STEM_DOWN),
             (("Floor Tom 1", "F", "o", False), 43, "normal", -1, STEM_DOWN),
             (("Second snare", "S2", "o", False), 40, "normal", 0, STEM_DOWN),
             (("Snare", "S", "o", True), 38, "normal", 1, STEM_DOWN),
             (("Tom 4", "T4", "o", False), 45, "normal", 2, STEM_UP),
             (("Tom 3", "T3", "o", False), 47, "normal", 3, STEM_UP),
             (("Tom 2", "T2", "o", False), 48, "normal", 4, STEM_UP),
             (("Tom 1", "T1", "o", False), 50, "normal", 5, STEM_UP),
             (("Hihat", "H", "x", False), 42, "normal", 5, STEM_UP),
             (("Ride Cymbal", "Rd", "x", False), 51, "normal", 4, STEM_UP),
             (("Crash Cymbal", "C", "x", False), 49, "normal", 6, STEM_UP),
             (("Percussion Line 2", "P2", "o", False), 68, "normal", 7, STEM_UP),
             (("Percussion Line 1", "P1", "o", False), 67, "normal", 8, STEM_UP)]
MVK_HEADS = {"BD" : [("O", None, 127, "accent", "default", "accent", "a"),
                     ("g", None, None, "ghost", "default", "ghost", "g"),
                     ("d", None, None, "drag", "default", "drag", "d")],
             "F2" : [("O", None, 127, "accent", "default", "accent", "a"),
                     ("g", None, 55, "ghost", "default", "ghost", "g"),
                     ("f", None, None, "flam", "default", "flam", "f"),
                     ("d", None, None, "drag", "default", "drag", "d")],
             "F" : [("O", None, 127, "accent", "default", "accent", "a"),
                    ("g", None, 55, "ghost", "default", "ghost", "g"),
                    ("f", None, None, "flam", "default", "flam", "f"),
                    ("d", None, None, "drag", "default", "drag", "d")],
             "S2" : [("O", None, 127, "accent", "default", "accent", "a"),
                     ("g", None, 55, "ghost", "default", "ghost", "g"),
                     ("f", None, None, "flam", "default", "flam", "f"),
                     ("d", None, None, "drag", "default", "drag", "d"),
                     ("x", 39, None, "normal", "cross", "none", "x")],
             "S" : [("O", None, 127, "accent", "default", "accent", "a"),
                    ("g", None, 54, "ghost", "default", "ghost", "g"),
                    ("f", None, None, "flam", "default", "flam", "f"),
                    ("d", None, None, "drag", "default", "drag", "d"),
                    ("x", 37, None, "normal", "cross", "none", "x")],
             "T4" : [("O", None, 127, "accent", "default", "accent", "a"),
                     ("g", None, 53, "ghost", "default", "ghost", "g"),
                     ("f", None, None, "flam", "default", "flam", "f"),
                     ("d", None, None, "drag", "default", "drag", "d")],
             "T3" : [("O", None, 127, "accent", "default", "accent", "a"),
                     ("g", None, 53, "ghost", "default", "ghost", "g"),
                     ("f", None, None, "flam", "default", "flam", "f"),
                     ("d", None, None, "drag", "default", "drag", "d")],
             "T2" : [("O", None, 127, "accent", "default", "accent", "a"),
                     ("g", None, 55, "ghost", "default", "ghost", "g"),
                     ("f", None, None, "flam", "default", "flam", "f"),
                     ("d", None, None, "drag", "default", "drag", "d")],
             "T1" : [("O", None, 127, "accent", "default", "accent", "a"),
                     ("g", None, 53, "ghost", "default", "ghost", "g"),
                     ("f", None, None, "flam", "default", "flam", "f"),
                     ("d", None, None, "drag", "default", "drag", "d")],
             "H" : [("X", None, 127, "accent", "cross", "accent", "a"),
                    ("o", 46, None, "normal", "cross", "open", "o"),
                    ("O", 46, 127, "accent", "cross", "open", "b"),
                    ("+", 44, None, "normal", "cross", "stopped", "c")],
             "Rd" : [("X", None, 127, "accent", "cross", "accent", "a"),
                     ("#", None, None, "choke", "cross", "choke", "c"),
                     ("b", 53, None, "normal", "diamond", "none", "b")],
             "C" : [("X", None, 127, "accent", "cross", "accent", "a"),
                    ("#", None, None, "choke", "cross", "choke", "c")]}
MVK_KIT = {"drums":MVK_DRUMS, "heads":MVK_HEADS}
NAMED_DEFAULTS["MvK"] = MVK_KIT
DEFAULT_KIT_NAMES.append("MvK")

DEFAULT_LILYPOND = {"Hf":"hhp",
                    "Bd": "bd",
                    "FT": "toml",
                    "Sn":"sn",
                    "MT":"tomml",
                    "HT": "tomh",
                    "Ri": "cymr",
                    "Hh":"hh",
                    "Cr":"cymc"}
