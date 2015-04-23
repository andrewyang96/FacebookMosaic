#!/usr/bin/python

from likes import likesMain
from mosaic import mosaicMain

if __name__ == "__main__":
    # TODO: get token from params
    imgpaths, propic = likesMain()
    print mosaicMain(propic, imgpaths)
