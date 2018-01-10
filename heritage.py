import urllib2
import urllib
from bs4 import BeautifulSoup

url="""http://www.china.com.cn/culture/zhuanti/whycml/node_7021189.htm"""

user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0"
headers={"User-Agent":user_agent}
request=urllib2.Request(url)
response=urllib2.urlopen(request)
result=response.read()
soup=BeautifulSoup(result)
for item in soup.body.find_all("a"):
    if("node" not in str(item) and "jpg" not in str(item)):
        print(item.get("href"))