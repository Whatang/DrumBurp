'''
Created on 18 Mar 2012

@author: Mike Thomas
'''
APPNAME = "DrumBurp"
FULL_RELEASE = False
DB_VERSION = "0.10"
if not FULL_RELEASE:
    DB_VERSION += "a"

if __name__ == "__main__":
    print DB_VERSION
