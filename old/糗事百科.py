#coding=utf-8
import urllib2
import urllib
from bs4 import BeautifulSoup

list = []
for i in range(1,13,1):
    url="https://www.qiushibaike.com/text/page/"+str(i)

    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0"
    headers={"User-Agent":user_agent}
    request=urllib2.Request(url,headers=headers)
    response=urllib2.urlopen(request)
    result=response.read()
    soup=BeautifulSoup(result)
    for item in soup.find_all("div"):
        if("content" in item.get("class")):
            for item2 in item.find_all("span"):
                strs=""
                for string in item2.strings:
                    strs+=unicode(string).encode("utf-8")+"\n"
                if len(strs)>0:
                    list.append(strs)
                    print(strs)

strs=""
for item in list:
    strs+=item
f=open("糗百.txt","w")
f.write(strs)
f.close()