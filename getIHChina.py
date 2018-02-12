# coding=utf-8
import util
from bs4 import BeautifulSoup
import json
import writeheritageIntoSQL as sql

ihChina = "http://www.ihchina.cn"
baseUrl = "http://www.ihchina.cn/8/8_"
form_url = "http://www.ihchina.cn/8/"
errorURL = "http://192.168.49.123:8090"
imgName = "bottom_news"
first_page = "http://www.ihchina.cn/8/8_1.html"
divide = "/bottom_news"
pure_divide = "bottom_news"


def generateInformation(url):
    resultList = []
    result = util.get_response(url)
    soup = BeautifulSoup(result)
    for divs in soup.find_all("div"):
        if divs.get("class") is not None and divs.get("class")[0] == "detailNews":
            for ps in divs.find_all("p"):
                data = {}
                if (ps.find("img") is not None):
                    img_data = ps.find("img")
                    imgUrl = ihChina + img_data.get("src").replace(errorURL, "")
                    if (util.reptiles_image(imgUrl, imgName, util.get_last_name(imgUrl)) == util.success):
                        data["type"] = "img"
                        data["info"] = divide + "/" + util.get_last_name(imgUrl)
                        print(data["info"])
                        resultList.append(data)
                else:
                    data["type"] = "text"
                    data["info"] = ps.text.strip()
                    resultList.append(data)
    print(resultList)
    return json.dumps(resultList, ensure_ascii=True).encode("utf-8").decode("utf-8")


def getProtectFormList(page):
    resultList = []
    result = util.get_response(page)
    soup = BeautifulSoup(result)
    for divs in soup.find_all("div"):
        if divs.get("class") is not None and divs.get("class")[0] == "main_bhlt_content_list":
            for lis in divs.find_all("li"):
                data = {}
                a = lis.a
                span = lis.find("span")
                data["title"] = a.get("title").strip()
                data["time"] = span.text.strip()
                data["content"] = generateInformation(form_url + a.get("href"))
                resultList.append(data)
    print(resultList)
    return resultList


def getALLProtectForm():
    last_page = baseUrl + "1.html"
    url = "http://www.ihchina.cn/8/8_1.html"
    result = util.get_response(url)
    soup = BeautifulSoup(result)
    for item in soup.find_all("div"):
        if item.get("class") is not None and item.get("class")[0] == "pageBox1":
            for a in item.find_all("a"):
                if (unicode(a.text).encode("utf-8") == "尾页"):
                    last_page = form_url + util.get_last_name(a.get("href"))
                    print(last_page)
    result = []
    ok = True
    count = 1
    while ok:
        page_url = baseUrl + str(count) + ".html"
        print(page_url)
        result.extend(getProtectFormList(page_url))
        count += 1
        if (page_url == last_page):
            ok = False
    util.saveFile(result, pure_divide)


def writeDataIntoSql():
    file=util.openFile(pure_divide)
    data = file.read()
    resultList = json.loads(data)
    sql.wirte_bottom_folk_news_to_sql(resultList)

# getALLProtectForm()
# writeDataIntoSql()
