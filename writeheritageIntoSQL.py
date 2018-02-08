# coding=utf-8
import mysql.connector
import os

dir = "/img/folk_img/"
# config = {
#     'host': 'btbudinner.win',
#     'user': 'root',
#     'port': 3306,
#     'database': 'heritage',
#     'charset': 'utf8',
#     'password': "123456"
# }

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'port': 3306,
    'database': 'heritage',
    'charset': 'utf8',
    'password': ""
}


def writeFolkNewsToSql(resultList):
    sqlDatas=[]
    for item in resultList:
        category=item["category"]
        title=item["title"]
        content=item.get("content")
        detail=item.get("detail")
        img=item.get("img")
        data=(title,content,category,detail,img)
        sqlDatas.append(data)
    sql="insert into folk_news(title,content,category,details,img) values(%s,%s,%s,%s,%s)"
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        cursor.executemany(sql, sqlDatas)
        con.commit()
    except mysql.connector.Error as e:
        print("insert datas error!{}".format(e))
        return
    finally:
        cursor.close()
        con.close

def write_main_page_slide_page(result_list):
    sqlDatas=[]
    for item in result_list:
        url=item.get("url")
        content=item.get("content")
        img=item.get("img")
        detail=item.get("detail")
        data=(url,content,img,detail)
        sqlDatas.append(data)
    sql = "insert into main_page_slide(url,content,img,detail) values(%s,%s,%s,%s)"
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        cursor.executemany(sql, sqlDatas)
        con.commit()
        cursor.close()
        con.close()
    except mysql.connector.Error as e:
        print("insert datas error!{}".format(e))
        return



def readDir():
    result = []
    rootpath = "/非遗/地方"
    os.listdir(os.getcwd() + rootpath)
    count = 0
    for dirname in os.listdir(os.getcwd() + rootpath):
        if os.path.isdir(os.getcwd() + rootpath + "/" + dirname):
            dividedir = os.getcwd() + rootpath + "/" + dirname
            for itemdir in os.listdir(dividedir):
                if os.path.isdir(dividedir + "/" + itemdir):
                    readdir = dividedir + "/" + itemdir
                    class_activity = {}
                    count += 1
                    class_activity["id"] = count
                    class_activity["divide"] = dirname
                    class_activity["title"] = itemdir
                    for files in os.listdir(readdir):
                        if ".txt" == os.path.splitext(files)[1]:
                            file = open(readdir + "/" + files)
                            txts = file.read()
                            txts = txts.replace("：", ":")
                            for txt in txts.split("\n"):
                                if ("时间" == txt.split(":")[0]):
                                    class_activity["time"] = txt.split(":")[1]
                                elif ("类别" == txt.split(":")[0]):
                                    class_activity["category"] = txt.split(":")[1]
                                elif ("地区" == txt.split(":")[0]):
                                    class_activity["location"] = txt.split(":")[1]
                                elif ("编号" == txt.split(":")[0]):
                                    class_activity["number"] = txt.split(":")[1]
                                elif ("申报地区或单位" == txt.split(":")[0]):
                                    class_activity["apply_location"] = txt.split(":")[1]
                                else:
                                    if not class_activity.has_key("content"):
                                        class_activity["content"] = ""
                                    class_activity["content"] += txt + "\n"
                            result.append(class_activity)
                        elif "img" == files:
                            imageDir = readdir + "/" + files
                            images = []
                            for imageName in os.listdir(imageDir):
                                if not class_activity.has_key("image"):
                                    class_activity["image"] = dir + imageName
                                images.append(dir + imageName)
                            class_activity["images"] = images
    # for items in result:
    #     for key, value in items.iteritems():
    #         if key == "image":
    #             strs = ""
    #             for i in value:
    #                 strs += "{" + i + "}"
    #             print(key + " " + str(i))
    #             continue
    #         print(key + " " + str(value))
    return result


def writeToSql():
    sql = "insert into folk_activity_information(id,time,divide,category,title,location,apply_location,content,number,img) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    result = readDir()
    sqlData = []
    imageData = []
    imagesql = "insert into folk_activity_img(classify_id,img) values(%s,%s)"
    for items in result:
        id = str(items["id"])
        divide = items["divide"]
        title = items["title"]
        time = ""
        category = ""
        location = ""
        apply_location = ""
        content = ""
        number = ""
        img = ""
        if items.has_key("time"):
            time = items["time"]
        if items.has_key("category"):
            category = items["category"]
        if items.has_key("location"):
            location = items["location"]
        if items.has_key("apply_location"):
            apply_location = items["apply_location"]
        if items.has_key("content"):
            content = items["content"]
        if items.has_key("number"):
            number = items["number"]
        if items.has_key("image"):
            img = items["image"]
        data = (id, time, divide, category, title, location, apply_location, content, number, img)
        sqlData.append(data)

        if items.has_key("images"):
            for image in items["images"]:
                data = (id, image)
                imageData.append(data)

    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        cursor.executemany(sql, sqlData)
        cursor.executemany(imagesql, imageData)
        con.commit()
    except mysql.connector.Error as e:
        print("insert datas error!{}".format(e))
        return
    finally:
        cursor.close()
        con.close


if __name__ == "__main__":
    # readDir()
    writeToSql()
