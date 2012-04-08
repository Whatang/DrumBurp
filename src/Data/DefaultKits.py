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
DEFAULT_KIT = [(("Foot pedal", "Hf", "x", False), 44),
               (("Kick", "Bd", "o", True), 36),
               (("Floor Tom", "FT", "o", False), 43),
               (("Snare", "Sn", "o", True), 38),
               (("Mid Tom", "MT", "o", False), 47),
               (("High Tom", "HT", "o", False), 50),
               (("Ride", "Ri", "x", False), 51),
               (("HiHat", "Hh", "x", False), 42),
               (("Crash", "Cr", "x", False), 49)]

ACCENT_VOLUME = 127
GHOST_VOLUME = 50

DEFAULT_EXTRA_HEADS = {"FT": [("O", None, ACCENT_VOLUME, "accent"),
                              ("g", None, GHOST_VOLUME, "ghost"),
                              ("f", None, None, "flam"),
                              ("d", None, None, "drag")],
                       "Sn": [("O", None, ACCENT_VOLUME, "accent"),
                              ("g", None, GHOST_VOLUME, "ghost"),
                              ("x", 37, None, "normal"),
                              ("f", None, None, "flam"),
                              ("d", None, None, "drag")],
                       "MT": [("O", None, ACCENT_VOLUME, "accent"),
                              ("g", None, GHOST_VOLUME, "ghost"),
                              ("f", None, None, "flam"),
                              ("d", None, None, "drag")],
                       "HT": [("O", None, ACCENT_VOLUME, "accent"),
                              ("g", None, GHOST_VOLUME, "ghost"),
                              ("f", None, None, "flam"),
                              ("d", None, None, "drag")],
                       "Ri": [("X", None, ACCENT_VOLUME, "accent"),
                              ("b", 53, None, "normal"),
                              ("d", None, None, "drag")],
                       "Hh": [("X", None, ACCENT_VOLUME, "accent"),
                              ("o", 46, None, "normal"),
                              ("O", 46, ACCENT_VOLUME, "accent"),
                              ("d", None, None, "drag"),
                              ("+", None, None, "choke"),
                              ("#", None, None, "choke")],
                       "Cr": [("X", None, ACCENT_VOLUME, "accent"),
                              ("#", None, None, "choke")],
                       "Bd": [("O", None, ACCENT_VOLUME, "accent"),
                              ("g", None, GHOST_VOLUME, "ghost"),
                              ("d", None, None, "drag")]}

DEFAULT_LILYPOND = {"Hf":"hhp",
                    "Bd": "bd",
                    "FT": "toml",
                    "Sn":"sn",
                    "MT":"tomml",
                    "HT": "tomh",
                    "Ri": "cymr",
                    "Hh":"hh",
                    "Cr":"cymc"}
