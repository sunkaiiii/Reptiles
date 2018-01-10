#coding=utf-8
import urllib2
import urllib
from bs4 import BeautifulSoup
import data
#
# url="http://pandapia.com/panda/dictionary.html"
#
# user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0"
# headers={"User-Agent":user_agent}
# requset=urllib2.Request(url)
# response=urllib2.urlopen(requset)
# result=response.read()
# print(result)

# str2=""
# soup=BeautifulSoup(data.data)

# for item in soup.find_all("a"):
#     if("pandapia.com/panda" in str(item)):
#         str2=str2+unicode(item.string).encode("utf-8")+"\n"
# f=open("panda.txt","w")
# f.write(str2)
# f.close()
# for item in soup.find_all("div"):
#     if "panda_AZList" in item.get("class"):
#         print(item)

# for item in soup.find_all("p"):
#     if("出生" in str(item)):
#         str2 = str2 + unicode(item.string).encode("utf-8") + "\n"
#
# f=open("panda2.txt","w")
# f.write(str2)
# f.close()

# for item in soup.find_all("a"):
#     if ("pandapia.com/panda/view" in str(item)):
#         print(item.get("href"))

url="http://pandapia.com/panda/view.html?id=MjA2"
user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0"
headers={"User-Agent":user_agent}
requset=urllib2.Request(url)
response=urllib2.urlopen(requset)
result=response.read()
f=open("data2.txt","w")
f.write(result)

url="http://pandapia.com/panda/dictionary.html"


user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0"
headers={"User-Agent":user_agent}
requset=urllib2.Request(url)
response=urllib2.urlopen(requset)
result=response.read()
soup=BeautifulSoup(result)
count=0
str2=""
for i in soup.find_all("a"):
    if ("pandapia.com/panda/view" in str(i)):
        count+=1
        geturl=i.get("href")
        headers2 = {"User-Agent": user_agent}
        requset2 = urllib2.Request(geturl)
        response2 = urllib2.urlopen(requset2)
        result2 = response2.read()
        soup2=BeautifulSoup(result2)
        name=soup2.find_all("h4")[0].string
        str2=str2+unicode(name).encode("utf-8").replace("\n","")+"\t"
        for item in soup2.find_all("ul"):
            if(item.get("class")!=None and "menu_ul" in item.get("class")):
                for item2 in item.find_all("div"):
                    for item3 in item2.stripped_strings:
                        str2=str2+unicode(item3).encode("utf-8").replace("\n","")+"\t"
        str2 += "\n\n"
        # print(str2)
f=open("restewt.txt","w")
f.write(str2)
f.close()


