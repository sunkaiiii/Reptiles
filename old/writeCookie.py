#coding=utf-8
import urllib2
import cookielib

#声明一个CookieJar对象实例来保存cookie
cookie=cookielib.CookieJar()
#利用urlib2库的HTTPCookieProcessor对象来创建cookie处理器
handler=urllib2.HTTPCookieProcessor(cookie)
#通过handler来构建opener
opener=urllib2.build_opener(handler)
#此处的open方法同urlib2的urlopen方法， 也可以传入request
response=opener.open("http://www.baidu.com")
for item in cookie:
    print("Name="+item.name)
    print("Value="+item.value)


#cookie保存在文件中
filename="cookie.txt"
#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie=cookielib.MozillaCookieJar(filename)
handler=urllib2.HTTPCookieProcessor(cookie)
opener=urllib2.build_opener(handler)
response=opener.open("http://www.baidu.com")

#ignore_discard意思是即是cookie将被丢弃也将他保存下来
#ignore_expires的意思是如果在该文件中cookie已经存在，则覆盖源文件写入
cookie.save(ignore_discard=True,ignore_expires=True)


