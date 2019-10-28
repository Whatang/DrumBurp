# Copyright 2016 Michael Thomas
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
Created on 18 Mar 2012

@author: Mike Thomas
'''
import re
import versionflow
import DBVersionNum
APPNAME = "DrumBurp"

DB_VERSION_FILE = 'DBVersionNum.py'

DB_VERSION_STRING = versionflow.get_current_version(
    DBVersionNum, "DB_VERSION_STRING")


def versionStringToTuple(vstr):
    try:
        if '+' in vstr:
            vstr = vstr[:vstr.index('+')]
        versionInfo = list(int(x) for x in vstr.split("."))
        v = versionInfo[:3]
        while len(v) < 3:
            v.append(0)
    except (ValueError, TypeError):
        v = [0, 0, 0]
    return tuple(v)


def readVersion(text):
    finder = re.compile(r"DB_VERSION_STRING\s*=\s*'(.*)'")
    for line in text.splitlines():
        line = line.strip()
        match = finder.match(line)
        if match:
            versionText = match.groups(1)
            return versionStringToTuple(versionText[0])
    return (0, 0, 0)


def getLatestVersion():
    import urllib2
    try:
        versionUrl = urllib2.urlopen('http://github.com/Whatang/DrumBurp/raw/master/src/' + DB_VERSION_FILE,
                                     timeout=10)
        versionText = versionUrl.read()
        return readVersion(versionText)
    except urllib2.HTTPError:
        return (0, 0, 0)


def doesNewerVersionExist():
    currentVersion = versionStringToTuple(DB_VERSION)
    newVersion = getLatestVersion()
    if currentVersion < newVersion:
        return "v" + ".".join(newVersion)
    else:
        return ""


def _is_full_release(vstr):
    return not '+' in vstr


DB_VERSION, FULL_RELEASE = (DB_VERSION_STRING,
                            _is_full_release(DB_VERSION_STRING))

if __name__ == "__main__":
    print DB_VERSION, FULL_RELEASE
    print getLatestVersion()
    print versionStringToTuple(DB_VERSION)
    print "'%s'" % str(doesNewerVersionExist())
