#coding=utf-8
import urllib2
import urllib
import ssl
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context
data={}
data["tz_offset"]="480"
data["username"]="1204010825"
data["password"]="ILOVEKIMI"
data["realm"]="教师"
data["btnSubmit"]="登陆"
user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0"
headers={"User-Agent":user_agent}

ctx = ssl.create_default_context(purpose = ssl.Purpose.SERVER_AUTH,)
data=urllib.urlencode(data)
url="https://vpn.btbu.edu.cn/dana-na/auth/url_default/login.cgi"
request=urllib2.Request(url,data,headers)
response=urllib2.urlopen(request)
result=response.read()
soup=BeautifulSoup(result)
for item in soup.find_all("input"):
    if("FormDataStr" in str(item)):
        value= item.get("value")
        data={}
        data["btnContinue"]="继续会话"
        data["FormDataStr"]=value
        data=urllib.urlencode(data)


