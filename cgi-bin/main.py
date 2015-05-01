#!/usr/bin/python

from likes import likesMain
from mosaic import mosaicMain
import cgi

args = cgi.FieldStorage()

if __name__ == "__main__":
    propic, imgpaths, _id = likesMain(args["token"].value)
    URL = "http://example.com/" + mosaicMain(propic, imgpaths, _id, 25, 25)
    print "Content-Type: application/json"
    print ""
    print {"url": URL}
