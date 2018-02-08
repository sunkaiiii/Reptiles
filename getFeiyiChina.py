# coding=utf-8
import urllib2
import urllib
from bs4 import BeautifulSoup
import os
import json
import writeheritageIntoSQL
from textrank4zh import TextRank4Sentence

latest_news_url = """http://feiyi.china.com.cn/china/index_"""
tese_url = """http://feiyi.china.com.cn/tese/index_"""
zhisheng_url = """http://feiyi.china.com.cn/zhisheng/index_"""
wenhua_url = """http://feiyi.china.com.cn/wenhua/index_"""
dashi_url = """http://feiyi.china.com.cn/dashi/index_"""
gushi_url = """http://feiyi.china.com.cn/gushi/index_"""
yingxiang_url = """http://feiyi.china.com.cn/yingxiang/index_"""
zhanguan_url = """http://feiyi.china.com.cn/zhanguan/index_"""
zaixian_url = """http://feiyi.china.com.cn/zaixian/index_"""
faxian_url = """http://feiyi.china.com.cn/faxian/index_"""

main_page_url = """http://feiyi.china.com.cn/"""

path = "img"
imagedir = "folk_news"
main_slide_page_dir="main_news_img"

feiyiwang = """http://feiyi.china.com.cn"""

dir_name = "jsons"


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
        if not os.path.exists(os.path.join(path,pathname)):
            os.mkdir(os.path.join(path,pathname))
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        result = response.read()
        f = open(os.path.join(os.getcwd(), path, pathname, spiltfilename), "w")
        f.write(result)
        f.close()



def find_range(url):
    result = get_response(url)
    soup = BeautifulSoup(result)
    for item in soup.find_all("div"):
        if (item.get("class")[0] == "page"):
            for item2 in item.find_all("a"):
                if (item2.text == "尾页"):
                    return feiyiwang + item2.get("href")


def saveFile(resultList, category):
    if (not os.path.exists(dir_name)):
        os.mkdir(dir_name)
    file_name = "news_" + category + ".txt"
    file = open(os.path.join("jsons", file_name), "w")
    file.write(json.dumps(resultList))
    file.close()


def generateHTML(url, category):
    resultList = []
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
                if (len(urlInfo.get("title")) < 2):
                    tr4s = TextRank4Sentence()
                    tr4s.analyze(urlInfo["content"], lower=True)
                    for item in tr4s.get_key_sentences(num=3):
                        urlInfo["title"] = item.sentence
                        break
                resultList.append(urlInfo)
    return resultList


def generate_main_page():
    result=get_response(main_page_url)
    soup=BeautifulSoup(result)
    result_list=[]
    for item in soup.find_all("div"):
        if(item.get("class") is not None and item.get("class")[0]=="feature-slide-preview"):
            info={}
            info["url"]=item.a.get("href")
            info["content"]=item.text
            image_url=feiyiwang+item.find("img").get("src")
            split_url=image_url.split("/")
            split_url=split_url[len(split_url)-1]
            path="main_news_img"
            reptiles_image(image_url,path,split_url)
            info["detail"]=generate_main_page_html(feiyiwang+info.get("url"))
            info["img"]="btbudinner.win:8080/img/main_news_img/"+split_url
            result_list.append(info)

    saveFile(result_list,"首页轮播")

def generate_main_page_html(url):
    result=get_response(url)
    soup=BeautifulSoup(result)
    result_list=[]
    for item in soup.find_all("div"):
        if(item.get("class") is not None and item.get("class")[0]=="article-zhu"):
            for text_item in item.find_all("p"):
                info={}
                if(text_item.find("img") is not None):
                    info["type"]="img"
                    image_url=text_item.find("img").get("src")
                    split_url=image_url.split("/")
                    split_url=split_url[len(split_url)-1]
                    reptiles_image(feiyiwang+image_url,main_slide_page_dir,split_url)
                    info["info"]="btbudinner.win:8080/"+main_slide_page_dir+"/"+split_url
                else:
                    info["type"]="text"
                    info["info"]=text_item.text
                result_list.append(info)
    return json.dumps(result_list,ensure_ascii=False).decode("utf-8")




def generate_ALL_INFO(first_url, scan_url, category):
    resultList = []
    url = first_url
    endUrl = find_range(url)
    print(endUrl)
    category = category
    for i in range(1, 500):
        if (i == 1):
            url = first_url
        else:
            url = scan_url + str(i) + ".html"
        url_info = generateHTML(url, category)
        resultList.extend(url_info)
        if (url == endUrl):
            break
    saveFile(resultList, category)


def generateYaoWen_ALL():
    url = "http://feiyi.china.com.cn/china/"
    category = "要闻"
    generate_ALL_INFO(url, latest_news_url, category)


def generateTeSe_ALL():
    url = "http://feiyi.china.com.cn/tese/index.html"
    category = "中国特色"
    generate_ALL_INFO(url, tese_url, category)


def generatezhisheng_ALL():
    url = """http://feiyi.china.com.cn/zhisheng/"""
    category = "传统村落"
    generate_ALL_INFO(url, zhisheng_url, category)


def generatewenhua_ALL():
    url = """http://feiyi.china.com.cn/wenhua/index.html"""
    category = "特色小镇"
    generate_ALL_INFO(url, wenhua_url, category)


def generatedashi_ALL():
    url = """http://feiyi.china.com.cn/dashi/"""
    category = "魅力中国"
    generate_ALL_INFO(url, dashi_url, category)


def generategushi_ALL():
    url = """http://feiyi.china.com.cn/gushi/"""
    category = "非遗中国"
    generate_ALL_INFO(url, gushi_url, category)


def generateyingxiang_ALL():
    url = """http://feiyi.china.com.cn/yingxiang/"""
    category = "时代影像"
    generate_ALL_INFO(url, yingxiang_url, category)


def generatezhanguan_ALL():
    url = """http://feiyi.china.com.cn/zhanguan/"""
    category = "发现之旅"
    generate_ALL_INFO(url, zhanguan_url, category)


def generatezaixian_ALL():
    url = """http://feiyi.china.com.cn/zaixian/"""
    category = "一带一路"
    generate_ALL_INFO(url, zaixian_url, category)


def generatefaxian_ALL():
    url = """http://feiyi.china.com.cn/faxian/"""
    category = "民风民俗"
    generate_ALL_INFO(url, faxian_url, category)


def load_file(category):
    file_name = "news_" + category + ".txt"
    file = open(os.path.join(dir_name, file_name), "r")
    result = file.read()
    return result


def generateeachNews(urlInfos):
    result = get_response(feiyiwang + urlInfos["url"])
    soup = BeautifulSoup(result)
    for title in soup.find_all("h1"):
        print(title.text)
        urlInfos["title"] = title.text
    detail = []
    for item in soup.findAll("div"):
        if (item.get("class") is not None and item.get("class")[0] == "article"):
            for item2 in item.find_all("p"):
                info = {}
                if (item2.find("img") is not None):
                    img_url = item2.find("img").get("src")
                    filename = img_url.split("/")
                    filename = filename[len(filename) - 1]
                    info["type"] = "img"
                    info["info"] = "btbudinner.win:8080/img/folk_news/" + filename
                    reptiles_image(feiyiwang + img_url, imagedir, filename)
                else:
                    info["type"] = "text"
                    info["info"] = item2.text
                detail.append(info)
    urlInfos["detail"] = json.dumps(detail, ensure_ascii=False).decode("utf-8")
    return urlInfos


def generateNews():
    categories = ["要闻", "中国特色", "传统村落", "特色小镇", "魅力中国", "非遗中国", "时代影像", "发现之旅", "一带一路", "民风民俗"]
    for category in categories:
        print(category)
        result = load_file(category)
        resultList = json.loads(result)
        for index in range(0, len(resultList)):
            resultList[index] = generateeachNews(resultList[index])
        writeheritageIntoSQL.writeFolkNewsToSql(resultList)

def read_main_page_slide_info():
    category="首页轮播"
    result=load_file(category)
    result_list=json.loads(result)
    writeheritageIntoSQL.write_main_page_slide_page(result_list)


# generateYaoWen_ALL()
# generateTeSe_ALL()
# generatezhisheng_ALL()
# generatewenhua_ALL()
# generatedashi_ALL()
# generategushi_ALL()
# generateyingxiang_ALL()
# generatezhanguan_ALL()
# generatezaixian_ALL()
# generatefaxian_ALL()

# generate_main_page()


# generateNews()
# read_main_page_slide_info()
