# _*_ coding:utf-8 _*_

import urllib
import urllib2
import cookielib

filename = 'cookie1.txt'
# 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode({
	'stuid': '141006427',
	'pwd': ''
})
# 登录教务系统的URL
loginUrl = 'http://202.196.166.136/'
# 模拟登录，并把cookie保存到变量
result = opener.open(loginUrl, postdata)
# 保存cookie到cookie.txt中
cookie.save(ignore_discard=True, ignore_expires=True)
# 利用cookie请求访问另一个网址，此网址是成绩查询网址
gradeUrl = 'http://202.196.166.136/xs_main.aspx?xh=141006427'
# 请求访问成绩查询网址
result = opener.open(gradeUrl)
print result.read()