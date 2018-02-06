# coding=utf-8
import urllib2
import urllib
from bs4 import BeautifulSoup
import os
import json
import writeheritageIntoSQL

latest_news_url = """http://feiyi.china.com.cn/china/index_"""

dir_name = "jsons"


def get_response(url):
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0"
    headers = {"User-Agent": user_agent}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    result = response.read()
    return result


def saveFile(resultList, category):
    if (not os.path.exists(dir_name)):
        os.mkdir(dir_name)
    file_name = "news_" + category + ".txt"
    file = open(os.path.join("jsons", file_name), "w")
    file.write(json.dumps(resultList))
    file.close()


def generateHTML(url, category):
    resultList=[]
    result = get_response(url)
    soup = BeautifulSoup(result)
    for item in soup.find_all("div"):
        if (item.find("span") != None and item.find("span").text.encode("utf-8") == category):
            for item2 in item.find_all("li"):
                urlInfo = {}
                urlInfo["url"] = item2.find("a").get("href")
                urlInfo["title"] = unicode(item2.find("a").text).encode("utf-8")
                urlInfo["category"] = category
                urlInfo["content"] = unicode(item2.text).encode("utf-8")
                resultList.append(urlInfo)
    return resultList


def generateYaoWen():
    resultList = []
    category = "要闻"
    for i in range(1, 16):
        if (i == 1):
            url = "http://feiyi.china.com.cn/china/"
        else:
            url = latest_news_url + str(i) + ".html"
        url_info = generateHTML(url, category)
        resultList.extend(url_info)
    saveFile(resultList, category)


def load_file(category):
    file_name = "news_"  + category+".txt"
    file = open(os.path.join(dir_name, file_name), "r")
    result = file.read()
    return result


def generateNews():
    result = load_file("要闻")
    resultList = json.loads(result)
    writeheritageIntoSQL.writeFolkNewsToSql(resultList)


generateYaoWen()
generateNews()
