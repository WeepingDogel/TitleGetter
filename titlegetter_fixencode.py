#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import requests
from bs4 import BeautifulSoup
session = requests.session()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
print("网站标题获取器")
target = input('请输入链接:')
response = session.get(target,headers=headers)
if response.status_code == 200:
    print("请求成功")
    html = response.text.encode('ISO8859-1')
    soup = BeautifulSoup(html,'lxml')
    a = soup.find('title')
    print('目标的标题为:' + a.string)
else:
    print('请求失败')