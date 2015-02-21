'''
Created on 18 Mar 2012

@author: Mike Thomas
'''
import os
APPNAME = "DrumBurp"
_ALPHA_STRING = "a"

DB_VERSION_FILE = 'dbversion.txt'

def readVersion():
    try:
        filename = os.path.dirname(__file__)
        filename = os.path.join(filename, DB_VERSION_FILE)
        versionText = open(filename, 'rU').read().strip()
        return versionText, not versionText.endswith(_ALPHA_STRING)
    except IOError:
        return "Unknown", True

def versionStringToTuple(vstr):
    vstr = vstr.rstrip(_ALPHA_STRING)
    try:
        versionInfo = [int(x) for x in vstr.split(".")]
        return versionInfo[:2]
    except (ValueError, TypeError):
        return (0, 0)


def getLatestVersion():
    import urllib2
    try:
        versionUrl = urllib2.urlopen('http://github.com/Whatang/DrumBurp/raw/master/src/dbversion.txt',
                                     timeout = 10)
        versionString = versionUrl.read()
        newVersion = versionStringToTuple(versionString)
        return newVersion
    except urllib2.HTTPError:
        return (0, 0)

def doesNewerVersionExist():
    currentVersion = versionStringToTuple(DB_VERSION)
    newVersion = getLatestVersion()
    if currentVersion < newVersion:
        return newVersion
    else:
        return ""

DB_VERSION, FULL_RELEASE = readVersion()

if __name__ == "__main__":
    print DB_VERSION, FULL_RELEASE
    print getLatestVersion()
    print "'%s'" % doesNewerVersionExist()

