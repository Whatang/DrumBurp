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

DEFAULT_LILYPOND = {"Hf":"hhp",
                    "Bd": "bd",
                    "FT": "toml",
                    "Sn":"sn",
                    "MT":"tomml",
                    "HT": "tomh",
                    "Ri": "cymr",
                    "Hh":"hh",
                    "Cr":"cymc"}
