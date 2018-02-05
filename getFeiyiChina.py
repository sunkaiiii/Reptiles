# coding=utf-8
import urllib2
import urllib
from bs4 import BeautifulSoup
import os

latest_news_url = """http://feiyi.china.com.cn/china/"""


def get_response(url):
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0"
    headers = {"User-Agent": user_agent}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    result = response.read()
    return result


def saveFile(text):
    file = open("newx.txt", "w")
    file.write(text.encode("utf-8"))
    file.close()


def generateNews():
    result = get_response(latest_news_url)
    soup = BeautifulSoup(result)
    text = ""
    for item in soup.find_all("div"):
        if (item.find("span") != None and item.find("span").text.encode("utf-8") == "要闻"):
            for item2 in item.find_all("li"):
                text += item2.find("a").get("href")
                text += "\n"
                text += item2.find("a").text
                text += "\n"
                if (item2.find("em") is not None):
                    text += item2.find("em").text
                    text += "\n"

                text += "\n\n"

    saveFile(text)


generateNews()
