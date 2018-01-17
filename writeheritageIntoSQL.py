# coding=utf-8
import mysql.connector
import os

dir = "/img/classify_divide_img/"
config={
    'host':'127.0.0.1',
    'user':'root',
    'port':3306,
    'database':'heritage',
    'charset':'utf8'
}

def readDir():
    result = []
    rootpath = "/非遗/分类"
    os.listdir(os.getcwd() + "/非遗/分类")
    count = 0
    for dirname in os.listdir(os.getcwd() + "/非遗/分类"):
        if os.path.isdir(os.getcwd() + rootpath + "/" + dirname):
            dividedir = os.getcwd() + rootpath + "/" + dirname
            for itemdir in os.listdir(dividedir):
                if os.path.isdir(dividedir + "/" + itemdir):
                    readdir = dividedir + "/" + itemdir
                    class_activity = {}
                    count += 1
                    class_activity["id"] = count
                    class_activity["divide"]=dirname
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
                                    class_activity["content"] += txt
                            result.append(class_activity)
                        elif "img" == files:
                            imageDir = readdir + "/" + files
                            images = []
                            for imageName in os.listdir(imageDir):
                                images.append(dir + imageName)
                            class_activity["image"] = images
    for items in result:
        for key, value in items.iteritems():
            if key == "image":
                strs = ""
                for i in value:
                    strs += "{" + i + "}"
                # print(key + " " + str(i))
                continue
            # print(key + " " + str(value))
    return result


def writeToSql():
    sql = "insert into classify_activity_new(id,time,divide,category,location,apply_location,content,number) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    result=readDir()
    sqlData=[]
    imageData=[]
    imagesql="insert into classify_activity_image(classify_id,img) values(%s,%s)"
    for items in result:
        id=str(items["id"])
        divide=items["divide"]
        time=""
        category=""
        location=""
        apply_location=""
        content=""
        number=""
        if items.has_key("time"):
            time=items["time"]
        if items.has_key("category"):
            category=items["category"]
        if items.has_key("location"):
            location=items["location"]
        if items.has_key("apply_location"):
            apply_location=items["apply_location"]
        if items.has_key("content"):
            content=items["content"]
        if items.has_key("number"):
            number=items["number"]
        data=(id,time,divide,category,location,apply_location,content,number)
        sqlData.append(data)

        if items.has_key("image"):
            for image in items["image"]:
                data=(id,image)
                imageData.append(data)

    try:
        con=mysql.connector.connect(**config)
        cursor=con.cursor()
        cursor.executemany(sql,sqlData)
        cursor.executemany(imagesql,imageData)
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
