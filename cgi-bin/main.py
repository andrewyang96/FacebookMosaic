#!/usr/bin/python

from likes import likesMain
from mosaic import mosaicMain

if __name__ == "__main__":
    propic, imgpaths, _id = likesMain()
    URL = "http://example.com/" + mosaicMain(propic, imgpaths, _id, 25, 25)
    print "Content-Type: application/json"
    print ""
    print {"url": URL}
