import glob
import os
import sys
import numpy as np
from scipy.spatial import KDTree
from PIL import Image
from config import IMGDIR, PROPICDIR, MOSAICDIR
from likes import likesMain
from progressbar import ProgressBar

def listAllFiles():
    return [e.replace("\\", "/") for e in glob.glob(os.path.join(IMGDIR, "*.jpg"))]

def createKDTree(imagefiles):
    imgdict = {}
    print "Creating KDTree and color-image map"
    progress = ProgressBar()
    for imagefile in progress(imagefiles):
        img = Image.open(imagefile)
        imgdict[tuple(getAverageColor(img))] = imagefile
    return (KDTree(imgdict.keys()), imgdict)

def getAverageColor(img):
    width, height = img.size
    numPixels = width * height
    pixels = img.load()
    rgb = np.array([0,0,0])
    for x in xrange(width):
        for y in xrange(height):
            pixel = np.array(pixels[x, y])
            if pixel.size > 3: # discard alpha value
                pixel = pixel[:3]
            rgb = np.add(rgb, pixel)
    rgb = np.divide(rgb, numPixels)
    return rgb

def getAverageColorOfRegion(img, xbounds, ybounds):
    if len(xbounds) != 2 or len(ybounds) != 2:
        raise ValueError("xbounds {0} or ybounds {1} incorrectly configured".format(xbounds, ybounds))
    if xbounds[0] < 0 or ybounds[0] < 0 or xbounds[1] > img.size[0] or ybounds[1] > img.size[1]:
        raise ValueError("xbounds {0} or ybounds {1} out of bounds for image size {2}".format(xbounds, ybounds, img.size))
    numPixels = (xbounds[1] - xbounds[0]) * (ybounds[1] - ybounds[0])
    pixels = img.load()
    rgb = np.array([0,0,0])
    for x in xrange(*xbounds):
        for y in xrange(*ybounds):
            pixel = np.array(pixels[x, y])
            if pixel.size > 3: # discard alpha value
                pixel = pixel[:3]
            rgb = np.add(rgb, pixel)
    rgb = np.divide(rgb, numPixels)
    return rgb

def parseProfilePicture(propic, width=20, height=20):
    if width != height: # ensure square output image
        raise ValueError("Width ({0}) and height ({1}) must be the same".format(width, height))
    if width < 20 or height < 20: # ensure enough images
        raise ValueError("Width and height both must be >= 10")
    img = Image.open(propic)
    imgWidth, imgHeight = img.size
    widthInt, heightInt = float(imgWidth) / width, float(imgHeight) / height
    arr = np.ndarray((height, width, 3))
    print "Parsing profile picture"
    pbar = ProgressBar(maxval=width*height).start()
    for x in xrange(width):
        for y in xrange(height):
            xbounds = (int(x * widthInt), int((x+1) * widthInt))
            ybounds = (int(y * heightInt), int((y+1) * heightInt))
            arr[y][x] = getAverageColorOfRegion(img, xbounds, ybounds)
            pbar.update(x*height+y)
    pbar.finish()
    return arr

def getBestImages(arr, tree, d):
    height, width = arr.shape[:2]
    ret = [["" for i in xrange(width)] for j in xrange(height)]
    print "Getting best images for mosaic"
    pbar = ProgressBar(maxval=width*height).start()
    for y, row in enumerate(arr):
        for x, region in enumerate(row):
            dist, idx = tree.query(region)
            closest = tuple(tree.data[idx])
            ret[y][x] = d[closest]
            pbar.update(y*width+x)
    pbar.finish()
    return ret

def createMosaic(outfile, imgs, widthInt=50, heightInt=50):
    # create mosaic directory if necessary
    if not os.path.exists(MOSAICDIR):
        os.makedirs(MOSAICDIR)
    
    width, height = len(imgs), len(imgs[0])
    imgWidth, imgHeight = width*widthInt, height*heightInt
    output = Image.new("RGB", (imgWidth, imgHeight))
    print "Creating mosaic"
    pbar = ProgressBar(maxval=width*height).start()
    for y, row in enumerate(imgs):
        for x, region in enumerate(row):
            img = Image.open(imgs[y][x])
            box = (widthInt*x, heightInt*y, widthInt*(x+1), heightInt*(y+1))
            output.paste(img, box)
            pbar.update(y*width+x)
    pbar.finish()
    output.save(outfile)

def debugMosaic(outfile, colors, widthInt=50, heightInt=50):
    height, width = colors.shape[:2]
    imgWidth, imgHeight = width*widthInt, height*heightInt
    output = Image.new("RGB", (imgWidth, imgHeight))
    print "Creating debug mosaic"
    pbar = ProgressBar(maxval=width*height).start()
    for y, row in enumerate(colors):
        for x, region in enumerate(row):
            box = (widthInt*x, heightInt*y, widthInt*(x+1), heightInt*(y+1))
            output.paste(tuple(colors[y][x].astype(int)), box)
            pbar.update(y*width+x)
    pbar.finish()
    output.save(outfile)

def mosaicMain(propic, files, width=50, height=50):
    # files = listAllFiles()
    tree, d = createKDTree(files)
    arr = parseProfilePicture(propic, width, height)
    imgs = getBestImages(arr, tree, d)
    mosaicimgpath = os.path.join(MOSAICDIR, os.path.basename(propic))
    createMosaic(mosaicimgpath, imgs)
    return mosaicimgpath

def debug(propic, files, width=50, height=50):
    # files = listAllFiles()
    tree, d = createKDTree(files)
    arr = parseProfilePicture(propic, width, height)
    debugMosaic("debug_mosaic.jpg", arr)

def test():
    imgpaths, propic = likesMain()
    return mosaicMain(propic, imgpaths)
