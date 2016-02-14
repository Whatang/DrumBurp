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
DEFAULT_VOLUME = 96
GHOST_VOLUME = 50
DEFAULT_NOTE = 71

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

NAMED_DEFAULTS = {"Default": DEFAULT_KIT_INFO}
DEFAULT_KIT_NAMES = ["Default"]

_CLASSIC_DRUMS = [(("Hi hat w/foot", "Hf", "x", False), 44, "cross", -5, STEM_DOWN),
                  (("Bass Drum", "B", "o", False), 35, "default", -3, STEM_DOWN),
                  (("Floor Tom 2", "F2", "o", False), 41, "default", -2, STEM_DOWN),
                  (("Floor Tom", "F", "o", False), 43, "default", -1, STEM_UP),
                  (("Snare", "S", "o", False), 38, "default", 1, STEM_DOWN),
                  (("Mid Tom", "T", "o", False), 47, "default", 2, STEM_UP),
                  (("Small Tom", "t", "o", False), 50, "default", 3, STEM_UP),
                  (("Ride", "Rd", "x", False), 51, "cross", 4, STEM_UP),
                  (("Hihat", "H", "x", False), 42, "cross", 5, STEM_UP),
                  (("Cymbal", "C", "x", False), 49, "cross", 6, STEM_UP)]
_CLASSIC_HEADS = {"Hf" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "a")],
                  "B" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                         ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "c"),
                         ("d", None, None, "drag", "default", "drag", "d")],
                  "F2" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                          ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                          ("f", None, None, "flam", "default", "flam", "f"),
                          ("d", None, None, "drag", "default", "drag", "d")],
                  "F" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                         ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                         ("f", None, None, "flam", "default", "flam", "f"),
                         ("d", None, None, "drag", "default", "drag", "d")],
                  "S" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                         ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                         ("f", None, None, "flam", "default", "flam", "c"),
                         ("d", None, None, "drag", "default", "drag", "d"),
                         ("x", 37, None, "normal", "cross", "none", "x")],
                  "T" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                         ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                         ("f", None, None, "flam", "default", "flam", "f"),
                         ("d", None, None, "drag", "default", "drag", "d")],
                  "t" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                         ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                         ("f", None, None, "flam", "default", "flam", "f"),
                         ("d", None, None, "drag", "default", "drag", "d")],
                  "Rd" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "a"),
                          ("d", None, None, "drag", "cross", "drag", "d"),
                          ("g", None, GHOST_VOLUME, "ghost", "cross", "ghost", "g"),
                          ("b", 53, None, "normal", "triangle", "none", "b"),
                          ("B", 53, ACCENT_VOLUME, "accent", "triangle", "accent", "c"),
                          ("f", None, None, "flam", "cross", "flam", "f"),
                          ("#", None, None, "choke", "cross", "choke", "s")],
                  "H" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "a"),
                         ("o", 46, None, "normal", "cross", "open", "o"),
                         ("O", 46, ACCENT_VOLUME, "accent", "cross", "open", "b"),
                         ("+", 44, None, "choke", "cross", "stopped", "s"),
                         ("d", None, None, "drag", "cross", "drag", "c")],
                  "C" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "a"),
                         ("#", None, None, "choke", "cross", "choke", "c")]}
_CLASSIC_KIT = {"drums":_CLASSIC_DRUMS, "heads":_CLASSIC_HEADS}
NAMED_DEFAULTS["Classic"] = _CLASSIC_KIT
DEFAULT_KIT_NAMES.append("Classic")


_TTABS_COM_DRUMS = [(("Bass drum", "B", "o", True), 36, "default", -3, STEM_DOWN),
                    (("Floor Tom", "FT", "o", False), 43, "default", -1, STEM_DOWN),
                    (("Mid Tom", "T", "o", False), 47, "default", 2, STEM_DOWN),
                    (("Snare", "S", "o", True), 38, "default", 1, STEM_DOWN),
                    (("Hi-Hat with foot", "Hf", "x", False), 44, "cross", -5, STEM_DOWN),
                    (("HiHat", "HH", "x", False), 42, "cross", 5, STEM_UP),
                    (("Ride Cymbal", "Rd", "x", False), 51, "cross", 4, STEM_UP),
                    (("Crash-ride cymbal", "CR", "x", False), 57, "cross", 7, STEM_UP),
                    (("Crash cymbal", "CC", "x", False), 49, "cross", 6, STEM_UP)]
_TTABS_COM_HEADS = {"B" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "o"),
                           ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                           ("d", None, None, "drag", "default", "drag", "d")],
                    "FT" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "o"),
                            ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                            ("f", None, None, "flam", "default", "flam", "f"),
                            ("b", None, GHOST_VOLUME, "none", "default", "none", "b"),
                            ("B", None, ACCENT_VOLUME, "none", "default", "accent", "r"),
                            ("d", None, None, "drag", "default", "drag", "d")],
                    "T" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "o"),
                           ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                           ("f", None, None, "flam", "default", "flam", "f"),
                           ("b", None, GHOST_VOLUME, "none", "default", "none", "b"),
                           ("B", None, ACCENT_VOLUME, "none", "default", "accent", "r"),
                           ("d", None, None, "drag", "default", "drag", "d")],
                    "S" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "o"),
                           ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                           ("@", 37, None, "normal", "cross", "none", "x"),
                           ("f", None, None, "flam", "default", "flam", "f"),
                           ("b", None, GHOST_VOLUME, "none", "default", "none", "b"),
                           ("B", None, ACCENT_VOLUME, "none", "default", "accent", "r"),
                           ("d", None, None, "drag", "default", "drag", "d")],
                    "HH" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "x"),
                            ("o", 46, None, "normal", "cross", "open", "o"),
                            ("d", None, None, "drag", "cross", "drag", "d"),
                            ("#", None, None, "choke", "cross", "choke", "c")],
                    "Rd" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "x"),
                            ("b", 53, None, "normal", "triangle", "none", "b"),
                            ("d", None, None, "drag", "cross", "drag", "d")],
                    "CR" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "x"),
                            ("b", 53, None, "normal", "triangle", "none", "b"),
                            ("#", None, None, "choke", "cross", "stopped", "c")],
                    "CC" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "x"),
                            ("b", 53, None, "normal", "triangle", "none", "b"),
                            ("#", None, None, "choke", "cross", "stopped", "c")]}
_TTABS_COM_KIT = {"drums":_TTABS_COM_DRUMS, "heads":_TTABS_COM_HEADS}
NAMED_DEFAULTS["Ttabs.com"] = _TTABS_COM_KIT
DEFAULT_KIT_NAMES.append("Ttabs.com")

_MVK_DRUMS = [(("Hihat w/foot", "Hf", "o", False), 44, "cross", -5, STEM_DOWN),
              (("Bass drum", "BD", "o", True), 35, "default", -3, STEM_DOWN),
              (("Floor Tom 2", "F2", "o", False), 41, "default", -2, STEM_DOWN),
              (("Floor Tom 1", "F", "o", False), 43, "default", -1, STEM_DOWN),
              (("Second snare", "S2", "o", False), 40, "default", 0, STEM_DOWN),
              (("Snare", "S", "o", True), 38, "default", 1, STEM_DOWN),
              (("Tom 4", "T4", "o", False), 45, "default", 2, STEM_UP),
              (("Tom 3", "T3", "o", False), 47, "default", 3, STEM_UP),
              (("Tom 2", "T2", "o", False), 48, "default", 4, STEM_UP),
              (("Tom 1", "T1", "o", False), 50, "default", 5, STEM_UP),
              (("Hihat", "H", "x", False), 42, "cross", 5, STEM_UP),
              (("Ride Cymbal", "Rd", "x", False), 51, "cross", 4, STEM_UP),
              (("Crash Cymbal", "C", "x", False), 49, "cross", 6, STEM_UP),
              (("Percussion Line 2", "P2", "o", False), 68, "diamond", 7, STEM_UP),
              (("Percussion Line 1", "P1", "o", False), 67, "diamond", 8, STEM_UP)]
_MVK_HEADS = {"BD" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                      ("g", None, None, "ghost", "default", "ghost", "g"),
                      ("d", None, None, "drag", "default", "drag", "d")],
              "F2" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                      ("g", None, 55, "ghost", "default", "ghost", "g"),
                      ("f", None, None, "flam", "default", "flam", "f"),
                      ("d", None, None, "drag", "default", "drag", "d")],
              "F" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                     ("g", None, 55, "ghost", "default", "ghost", "g"),
                     ("f", None, None, "flam", "default", "flam", "f"),
                     ("d", None, None, "drag", "default", "drag", "d")],
              "S2" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                      ("g", None, 55, "ghost", "default", "ghost", "g"),
                      ("f", None, None, "flam", "default", "flam", "f"),
                      ("d", None, None, "drag", "default", "drag", "d"),
                      ("x", 39, None, "normal", "cross", "none", "x")],
              "S" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                     ("g", None, 54, "ghost", "default", "ghost", "g"),
                     ("f", None, None, "flam", "default", "flam", "f"),
                     ("d", None, None, "drag", "default", "drag", "d"),
                     ("x", 37, None, "normal", "cross", "none", "x")],
              "T4" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                      ("g", None, 53, "ghost", "default", "ghost", "g"),
                      ("f", None, None, "flam", "default", "flam", "f"),
                      ("d", None, None, "drag", "default", "drag", "d")],
              "T3" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                      ("g", None, 53, "ghost", "default", "ghost", "g"),
                      ("f", None, None, "flam", "default", "flam", "f"),
                      ("d", None, None, "drag", "default", "drag", "d")],
              "T2" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                      ("g", None, 55, "ghost", "default", "ghost", "g"),
                      ("f", None, None, "flam", "default", "flam", "f"),
                      ("d", None, None, "drag", "default", "drag", "d")],
              "T1" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                      ("g", None, 53, "ghost", "default", "ghost", "g"),
                      ("f", None, None, "flam", "default", "flam", "f"),
                      ("d", None, None, "drag", "default", "drag", "d")],
              "H" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "a"),
                     ("o", 46, None, "normal", "cross", "open", "o"),
                     ("O", 46, ACCENT_VOLUME, "accent", "cross", "open", "b"),
                     ("+", 44, None, "normal", "cross", "stopped", "c")],
              "Rd" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "a"),
                      ("#", None, None, "choke", "cross", "choke", "c"),
                      ("b", 53, None, "normal", "diamond", "none", "b")],
              "C" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "a"),
                     ("#", None, None, "choke", "cross", "choke", "c")]}
_MVK_KIT = {"drums":_MVK_DRUMS, "heads":_MVK_HEADS}
NAMED_DEFAULTS["MvK"] = _MVK_KIT
DEFAULT_KIT_NAMES.append("MvK")

_DRUMTABBER_COM_DRUMS = [(("High hat foot", "Hf", "x", False), 44, "cross", -5, STEM_DOWN),
                         (("Bass Drum 2", "B2", "o", False), 36, "default", -4, STEM_DOWN),
                         (("Bass Drum 1", "B1", "o", True), 35, "default", -3, STEM_DOWN),
                         (("Snare Drum", "SD", "o", True), 38, "default", 1, STEM_DOWN),
                         (("Floor Tom 2", "F2", "o", False), 41, "default", -2, STEM_DOWN),
                         (("Floor Tom 1", "F1", "o", False), 43, "default", -1, STEM_DOWN),
                         (("Tom 4", "T4", "o", False), 45, "default", 2, STEM_UP),
                         (("Tom 3", "T3", "o", False), 47, "default", 3, STEM_UP),
                         (("Tom 2", "T2", "o", False), 48, "default", 4, STEM_UP),
                         (("Tom 1", "T1", "o", False), 50, "default", 5, STEM_UP),
                         (("Hihat", "HH", "x", False), 42, "cross", 5, STEM_UP),
                         (("Ride Cymbal", "Rd", "x", False), 51, "cross", 4, STEM_UP),
                         (("Crash Cymbal 2", "C2", "x", False), 57, "cross", 7, STEM_UP),
                         (("Crash Cymbal 1", "C1", "x", False), 49, "cross", 6, STEM_UP)]
_DRUMTABBER_COM_HEADS = {"Hf" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "a")],
                         "B2" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a")],
                         "B1" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a")],
                         "SD" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a"),
                                 ("x", 37, None, "normal", "cross", "none", "x"),
                                 ("X", 37, ACCENT_VOLUME, "accent", "cross", "accent", "s"),
                                 ("@", 40, None, "normal", "xcircle", "none", "r"),
                                 ("g", None, GHOST_VOLUME, "ghost", "default", "ghost", "g"),
                                 ("f", None, None, "flam", "default", "flam", "f"),
                                 ("d", None, None, "drag", "default", "drag", "d"),
                                 ("b", None, None, "drag", "default", "drag", "b")],
                         "F2" : [("?", None, ACCENT_VOLUME, "accent", "default", "accent", "a")],
                         "F1" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a")],
                         "T4" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a")],
                         "T3" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a")],
                         "T2" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a")],
                         "T1" : [("O", None, ACCENT_VOLUME, "accent", "default", "accent", "a")],
                         "HH" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "a"),
                                 ("o", 46, None, "normal", "cross", "open", "o"),
                                 ("O", 46, ACCENT_VOLUME, "accent", "cross", "open", "c")],
                         "Rd" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "a"),
                                 ("b", None, None, "normal", "triangle", "none", "b"),
                                 ("B", None, ACCENT_VOLUME, "accent", "triangle", "accent", "c")],
                         "C2" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "a")],
                         "C1" : [("X", None, ACCENT_VOLUME, "accent", "cross", "accent", "a"),
                                 ("S", 55, None, "normal", "harmonic", "none", "s"),
                                 ("C", 52, None, "normal", "triangle", "none", "c")]}
_DRUMTABBER_COM_KIT = {"drums":_DRUMTABBER_COM_DRUMS, "heads":_DRUMTABBER_COM_HEADS}
NAMED_DEFAULTS["Drumtabber.com"] = _DRUMTABBER_COM_KIT
DEFAULT_KIT_NAMES.append("Drumtabber.com")
