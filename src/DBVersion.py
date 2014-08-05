'''
Created on 18 Mar 2012

@author: Mike Thomas
'''
APPNAME = "DrumBurp"
FULL_RELEASE = True
DB_VERSION = "0.8"
if not FULL_RELEASE:
    DB_VERSION += "a"

if __name__ == "__main__":
    print DB_VERSION
