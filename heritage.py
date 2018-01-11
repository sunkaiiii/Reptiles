#coding=utf-8
import urllib2
import urllib
from bs4 import BeautifulSoup
import os

heritage_url = """http://www.china.com.cn/culture/zhuanti/whycml/"""

def get_response(url):
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0"
    headers={"User-Agent":user_agent}
    request=urllib2.Request(url,headers=headers)
    response=urllib2.urlopen(request)
    result=response.read()
    return result

#爬取中央申报的非遗
def reptiles_center():
    url="""http://www.china.com.cn/culture/zhuanti/whycml/node_7021189.htm"""
    reptiles_data(url)

def reptiles_image(url,path):
    if not os.path.exists(path):
        os.mkdir(path)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    result = response.read()
    len2 = len(url.split("/"))
    name = url.split("/")[len2 - 1]
    f = open(path+"/"+name, "w")
    f.write(result)
    f.close()

#遍历每个网站，爬取信息
def reptiles_data(url):
    try:
        result = get_response(url)
        soup = BeautifulSoup(result)
        title = ""
        for item2 in soup.find_all("font"):
            title = unicode(item2.string).encode("utf-8")
            break
        if (len(title) > 0):
            print(title)
            for item in soup.body.find_all("a"):
                if ("node" not in str(item) and "jpg" not in str(item)):
                    this_url = heritage_url + unicode(item.get("href")).encode("utf-8")
                    result = get_response(this_url)
                    soup = BeautifulSoup(result)
                    path=os.getcwd() + u"/非遗/地方/".encode("utf-8") + title
                    heritage_name=""
                    for item2 in soup.find_all("td"):
                        if (item2.get("class") is not None) and ("f20_000000" in item2.get("class")):
                            if not os.path.exists(path):
                                os.mkdir(path)
                            heritage_name=unicode(item2.string).encode("utf-8")
                            if not os.path.exists(path + "/" +heritage_name):
                                os.mkdir(path + "/" +heritage_name)
                            f = open(path + "/" +heritage_name+"/"+heritage_name + ".txt", "w")
                            writeStr = ""
                            for item3 in soup.find_all("p"):
                                writeStr += unicode(item3.string).encode("utf-8") + "\n"
                            print(unicode(item2.string).encode("utf-8") + " " + writeStr)
                            f.write(writeStr)
                            f.close()
                            break
                    #如果有图片的话，爬取图片
                    for item2 in soup.find_all("img"):
                        if(item2.get("change") is not None):
                            if(item2.get("src") is not None):
                                print(item2.get("src"))
                                reptiles_image(item2.get("src"),path+"/"+heritage_name+"/img")
    except:
        return

#爬取全部分类的非遗
def repties_all_divide():
    url="http://www.china.com.cn/culture/zhuanti/whycml/node_7021179.htm"
    result=get_response(url)
    soup=BeautifulSoup(result)
    for item in soup.find_all("td"):
        if(item.a is not None):
            for item2 in item.find_all("a"):
                if(item2.string is not None):
                    url=heritage_url+unicode(item2.get("href")).encode("utf-8")
                    print(url)
                    reptiles_data(url)

if __name__=="__main__":
    # reptiles_center()
    repties_all_divide()