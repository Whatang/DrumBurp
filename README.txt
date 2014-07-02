DrumBurp Copyright (C) 2011-14 Michael Thomas

DrumBurp is a simple GUI for creating and editing music notation for drum kit.

DrumBurp's aim is to make the user-experience of writing drum music as quick
and intuitive as possible. The generality of many existing music notation
software packages means that there is an abundance of unnecessary complexity
involved in writing drum notation. While these packages can produce beautiful
output, and cope with everything you could ever possibly want to notate, they
can be slow and ponderous to use. By being very clear that the objective of
DrumBurp is restricted to writing *only* drum music, I hope to remove the
difficulties such generality can impose. 

DrumBurp will never have a Bagpipes mode. 

The fundamental philosophy of DrumBurp is as follows: when faced with a choice
between additional functionality/complexity in a specific case, or speed,
simplicity and intuitive user interaction in the general case, the general case
always wins. Simple, quick and stupid is better than complex, slow and clever.

DrumBurp is focussed around using a simple representation of drum music. For
each note you play it essentially cares about:
 - WHICH drum you hit,
 - WHEN you hit it,
 - and HOW you strike it.
 
These three pieces of information together are sufficient to write drum music
in tablature notation. DrumBurp aims to allow the drummer to get this
information into the computer as quickly and as painlessly as possible.

DrumBurp stores this information in it's own format in its saved score files.
However, it can export tablature as ASCII text files easily enough. A long-term
goal of DrumBurp is to be able to output "real" drum notation as aesthetically
pleasing and easy to read as that produced by Lilypond or Nted.

DrumBurp's fundamental data structures should rarely, if ever, change. The most
important part of DrumBurp is its interface with the user. It's goal for the
user is less time writing, more time drumming.

LICENSING INFORMATION

DrumBurp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

See the file COPYING for details of the GNU GPL.

Contact details: drumburp@whatang.org