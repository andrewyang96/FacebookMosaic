import facebook
import os
import json
import datetime
import requests
from config import token, IMGDIR, IMGCACHE, PROPICDIR, ref

def getProfile(graph):
    return graph.get_object("me")

def getLikes(graph, _id):
    ret = []
    likes = graph.get_connections("me", "likes", limit=100)
    ret += likes["data"]
    
    message = "Fetching your likes"
    pbarmax = False
    pbarval = 0
    ref.put("/progress", _id, {"message": message, "max": pbarmax, "val": 0})
    while "next" in likes["paging"]:
        likes = graph.get_connections("me", "likes", limit=100,
                                      after=likes["paging"]["cursors"]["after"])
        ret += likes["data"]
    return ret

def downloadPictures(graph, arr, _id):
    # create image directory if necessary
    if not os.path.exists(IMGDIR):
        os.makedirs(IMGDIR)
    
    imgpaths = []
    message = "Downloading your likes' pictures"
    pbarmax = len(arr)
    pbarval = 0
    ref.put("/progress", _id, {"message": message, "max": pbarmax, "val": 0})
    for like in arr:
        pageid = like["id"]
        pageinfo = graph.get_connections(pageid, "photos", fields="created_time")
        # omit blank/default pictures
        if len(pageinfo["data"]) > 0:
            imgtime = datetime.datetime.strptime(pageinfo["data"][0]["created_time"], "%Y-%m-%dT%H:%M:%S+0000")
            imgpath = os.path.join(IMGDIR, pageid + ".jpg")
            # execute if image hasn't been downloaded before OR if image has been updated on Facebook
            # TODO: check if in firebase
        pbarval += 1
        ref.put("/progress", _id, {"message": message, "max": pbarmax, "val": pbarval})
    
    with open(IMGCACHE, "w+") as f:
        json.dump(imgcache, f)
    return imgpaths

def downloadProfilePicture(graph, _id):
    # print "Downloading your profile picture"
    # create propic directory if necessary
    if not os.path.exists(PROPICDIR):
        os.makedirs(PROPICDIR)

    message = "Downloading your profile picture"
    pbarmax = False
    pbarval = 0
    ref.put("/progress", _id, {"message": message, "max": pbarmax, "val": 0})
    # TODO: check if in firebase
    
    me = getProfile(graph)
    myid = me["id"]
    propic = graph.get_connections("me", "picture", width=9999, height=9999)
    propicurl = propic["url"]
    img = requests.get(propicurl)
    propicimgpath = os.path.join(PROPICDIR, myid + ".jpg")
    with open(propicimgpath, "wb") as f:
        f.write(img.content)
    return propicimgpath

def likesMain(token=token):
    graph = facebook.GraphAPI(token)
    _id = getProfile(graph)["id"]
    # likes = getLikes(graph, _id)
    # imgpaths = downloadPictures(graph, likes, _id)
    imgpaths = None # TODO: if Facebook privileges approved, then uncomment above lines
    propicpath = downloadProfilePicture(graph, _id)
    return (propicpath, imgpaths, _id)

if __name__ == "__main__":
    propicpath, imgpaths, _id = likesMain()
