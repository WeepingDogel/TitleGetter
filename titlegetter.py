#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import requests
from bs4 import BeautifulSoup
import toml
def print_as_markdown(a,b):
    print("["+a+"]"+"("+b+")")
def loadtoml(filename):
    # load the *.toml file 
    fileobj = open(filename)
    config = toml.load(fileobj)
    return config
# load config
config = loadtoml('config.toml')
# check Language config
if config['Language']['lang'] == "en-US":
    input_tip = "Please type an URL: "
    version = "Version: "
    requests_success = "Requested Successfully"
    requests_failure = "Failed to request"
    result = "Title: "
    filename_input = "Type a filename: "
    empty_line_warning = "WARN: empty line is forbidden."
elif config['Language']['lang'] == "zh-CN":
    input_tip = "请输入一个链接: "
    version = "版本："
    requests_success = "请求成功"
    requests_failure = "请求失败"
    result = "标题: "
    filename_input = "输入文件名: "
    empty_line_warning = "警告：禁止空行"
# sign of program
def sign():
    print('''
╭━━━━╮╭╮╭╮╱╱╱╱╭━━━╮╱╱╭╮╱╭╮
┃╭╮╭╮┣╯╰┫┃╱╱╱╱┃╭━╮┃╱╭╯╰┳╯╰╮
╰╯┃┃┣╋╮╭┫┃╭━━╮┃┃╱╰╋━┻╮╭┻╮╭╋━━┳━╮
╱╱┃┃┣┫┃┃┃┃┃┃━┫┃┃╭━┫┃━┫┃╱┃┃┃┃━┫╭╯
╱╱┃┃┃┃┃╰┫╰┫┃━┫┃╰┻━┃┃━┫╰╮┃╰┫┃━┫┃
╱╱╰╯╰╯╰━┻━┻━━╯╰━━━┻━━┻━╯╰━┻━━┻╯
    ''')
    print(version + "1.0.1\n")
sign()
# create a session of requesting.
session = requests.session()
# import the headers
headers = config['headers']
# check the working mode

if config['BatchMode'] == True:
    filename = input(filename_input)
    if config['AsMarkDown'] == True:
        file_format = ".md"
    else:
        file_format = ".txt"
    # Batch Mode
    with open('out/'+filename+ file_format,'x') as f:
         # load the URLs
        urlist = open('list.txt')
        for x in urlist:
            # .strip() : delete the blank line
            url = x.strip()
            # empty line checking
            if url == '':
                print(empty_line_warning)
                urlist.close()
                os.remove("./out/" + filename + file_format)
                os._exit(0)
                # mpty line checking
            response = session.get(url,headers=headers)
            if response.status_code == 200:
                print(requests_success)
            else:
                print(requests_failure)
            if config['EncodingFix'] == True:
                # check if the EncodingFix is true
                source = response.text.encode('ISO8859-1')
            else:
                source = response.text
            soup = BeautifulSoup(source,'lxml')
            a = soup.find('title')
            titles = a.string.strip()
            if config['AsMarkDown'] == True:
                f.write("* ["+titles+"]"+"("+url+")\n\n")
                print_as_markdown(titles,url)
            else:
                f.write(result+titles + "\n" + "URL: " + url + "\n\n")
                print(result + titles)
                print("URL: " +  url)
                print("-" * 20)
else:
    # not on batch mode
    # request the URL
    url = input(input_tip)
    response = session.get(url,headers=headers)
    if response.status_code == 200:
        print(requests_success)
        # parse the web source
        if config['EncodingFix'] == True:
            # check if the EncodingFix is true
            source = response.text.encode('ISO8859-1')
        else:
            source = response.text
        soup = BeautifulSoup(source,'lxml')
        title = soup.find('title') # get the title from the web source
        # check the handling mode
        if config['AsMarkDown'] == True:
            print(result)
            print_as_markdown(title.string.strip(),url)
        else:
            print(result + title.string.strip())
            print("URL: " + url)
    else:
        # end
        print(requests_failure)