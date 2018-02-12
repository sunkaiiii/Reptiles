import urllib2
import os
import json
path = "img"
imagedir = "folk_news"
success = "success"
error = "error"
dir_name = "jsons"


def get_last_name(img_url):
    filename = img_url.split("/")
    filename = filename[len(filename) - 1]
    return filename

def get_response(url):
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0"
    headers = {"User-Agent": user_agent}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    result = response.read()
    return result


def reptiles_image(url, pathname, spiltfilename):
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(os.path.join(path, imagedir)):
        os.mkdir(os.path.join(path, imagedir))
    if not os.path.exists(os.path.join(path, pathname)):
        os.mkdir(os.path.join(path, pathname))
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        result = response.read()
        f = open(os.path.join(os.getcwd(), path, pathname, spiltfilename), "w")
        f.write(result)
        f.close()
        return success
    except:
        return error

def saveFile(resultList, category):
    if (not os.path.exists(dir_name)):
        os.mkdir(dir_name)
    file_name = "news_" + category + ".txt"
    file = open(os.path.join("jsons", file_name), "w")
    file.write(json.dumps(resultList))
    file.close()

def openFile(divide):
    filename="news_"+divide+".txt"
    file=open(os.path.join("jsons",filename),"r")
    print(os.path.join("jsons",filename))
    return file
