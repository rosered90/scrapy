# _*_ coding:utf-8 _*_
import json

import requests


r = requests.get('http://cuiqingcai.com')
print type(r)
# print r.text

# load1 = {'some':'data'}
r1 = requests.get("http://127.0.0.1:8000/purchase/main/")
print r1.cookies
print r1.cookies['csrftoken']


