import facebook
import os
import json
import datetime
import requests
from config import token, IMGDIR, IMGCACHE, PROPICDIR
from progressbar import ProgressBar

def getProfile(graph):
    return graph.get_object("me")

def getLikes(graph):
    print "Getting your likes"
    ret = []
    likes = graph.get_connections("me", "likes", limit=100)
    ret += likes["data"]
    while "next" in likes["paging"]:
        print "after", likes["paging"]["cursors"]["after"]
        likes = graph.get_connections("me", "likes", limit=100,
                                      after=likes["paging"]["cursors"]["after"])
        ret += likes["data"]
    return ret

def downloadPictures(graph, arr):
    print "Downloading your pictures"
    # create image directory if necessary
    if not os.path.exists(IMGDIR):
        os.makedirs(IMGDIR)
    
    imgcache = {}
    # create image cache file if necessary, else read into dict
    if not os.path.exists(IMGCACHE):
        with open(IMGCACHE, "w") as f:
            f.write("{}")
    else:
        with open(IMGCACHE, "r") as f:
            imgcache = json.load(f)
    # TODO: make list of imagepaths
    progress = ProgressBar()
    for like in progress(arr):
        pageid = like["id"]
        pageinfo = graph.get_connections(pageid, "photos", fields="created_time")
        # omit blank/default profile pictures
        if len(pageinfo["data"]) > 0:
            imgtime = datetime.datetime.strptime(pageinfo["data"][0]["created_time"], "%Y-%m-%dT%H:%M:%S+0000")
            # execute if image hasn't been downloaded before OR if image has been updated on Facebook
            if pageid not in imgcache or imgtime > datetime.datetime.strptime(imgcache[pageid]["created_time"], "%Y-%m-%dT%H:%M:%S+0000"):
                pic = graph.get_connections(pageid, "picture")
                picurl = pic["url"]
                img = requests.get(picurl)
                with open(os.path.join(IMGDIR, pageid + ".jpg"), "wb") as imgfile:
                    imgfile.write(img.content)
                imgcache[pageid] = imgtime
    
    with open(IMGCACHE, "w+") as f:
        json.dump(imgcache, f)

def downloadProfilePicture(graph):
    print "Downloading your profile picture"
    # create propic directory if necessary
    if not os.path.exists(PROPICDIR):
        os.makedirs(PROPICDIR)
    
    me = getProfile(graph)
    myid = me["id"]
    propic = graph.get_connections("me", "picture", width=9999, height=9999)
    propicurl = propic["url"]
    img = requests.get(propicurl)
    with open(os.path.join(PROPICDIR, myid + ".jpg"), "wb") as f:
        f.write(img.content)

def main(token=token):
    graph = facebook.GraphAPI(token)
    likes = getLikes(graph)
    downloadPictures(graph, likes)
    downloadProfilePicture(graph)

if __name__ == "__main__":
    main()
