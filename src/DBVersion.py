'''
Created on 18 Mar 2012

@author: Mike Thomas
'''
APPNAME = "DrumBurp"
FULL_RELEASE = False
_ALPHA_STRING = "a"
DB_VERSION = "0.10"
if not FULL_RELEASE:
    DB_VERSION += _ALPHA_STRING

def versionStringToTuple(vstr):
    vstr = vstr.rstrip(_ALPHA_STRING)
    try:
        versionInfo = map(int, vstr.split("."))
        return versionInfo[:2]
    except (ValueError, TypeError):
        return (0, 0)


def doesNewerVersionExist():
    import urllib2
    currentVersion = versionStringToTuple(DB_VERSION)
    try:
        versionUrl = urllib2.urlopen('http://www.whatang.org/latest_version',
                                      timeout = 10)
        versionString = versionUrl.read()
        newVersion = versionStringToTuple(versionString)
        if currentVersion < newVersion:
            return newVersion
        else:
            return ""
    except urllib2.HTTPError:
        return None

if __name__ == "__main__":
    print DB_VERSION
    print doesNewerVersionExist()

