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

DEFAULT_EXTRA_HEADS = {"FT": [("O", None, ACCENT_VOLUME, "accent", "default", "accent"),
                              ("g", None, GHOST_VOLUME, "ghost", "default", "ghost"),
                              ("f", None, None, "flam", "default", "flam"),
                              ("d", None, None, "drag", "default", "drag")],
                       "Sn": [("O", None, ACCENT_VOLUME, "accent", "default", "accent"),
                              ("g", None, GHOST_VOLUME, "ghost", "default", "ghost"),
                              ("x", 37, None, "normal", "cross", "none"),
                              ("f", None, None, "flam", "default", "flam"),
                              ("d", None, None, "drag", "default", "drag")],
                       "MT": [("O", None, ACCENT_VOLUME, "accent", "default", "accent"),
                              ("g", None, GHOST_VOLUME, "ghost", "default", "ghost"),
                              ("f", None, None, "flam", "default", "flam"),
                              ("d", None, None, "drag", "default", "drag")],
                       "HT": [("O", None, ACCENT_VOLUME, "accent", "default", "accent"),
                              ("g", None, GHOST_VOLUME, "ghost", "default", "ghost"),
                              ("f", None, None, "flam", "default", "flam"),
                              ("d", None, None, "drag", "default", "drag")],
                       "Ri": [("X", None, ACCENT_VOLUME, "accent", "cross", "accent"),
                              ("b", 53, None, "normal", "triangle", "none"),
                              ("d", None, None, "drag", "cross", "drag")],
                       "Hh": [("X", None, ACCENT_VOLUME, "accent", "cross", "accent"),
                              ("o", 46, None, "normal", "cross", "open"),
                              ("O", 46, ACCENT_VOLUME, "accent", "cross", "accent"),
                              ("d", None, None, "drag", "cross", "drag"),
                              ("+", None, None, "choke", "cross", "stopped"),
                              ("#", None, None, "choke", "cross", "stopped")],
                       "Cr": [("X", None, ACCENT_VOLUME, "accent", "cross", "accent"),
                              ("#", None, None, "choke", "cross", "stopped")],
                       "Bd": [("O", None, ACCENT_VOLUME, "accent", "default", "accent"),
                              ("g", None, GHOST_VOLUME, "ghost", "default", "ghost"),
                              ("d", None, None, "drag", "default", "drag")]}

DEFAULT_LILYPOND = {"Hf":"hhp",
                    "Bd": "bd",
                    "FT": "toml",
                    "Sn":"sn",
                    "MT":"tomml",
                    "HT": "tomh",
                    "Ri": "cymr",
                    "Hh":"hh",
                    "Cr":"cymc"}
