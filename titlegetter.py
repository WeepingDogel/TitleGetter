#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import requests
from bs4 import BeautifulSoup
import toml
## classes
class Interactions:
    def ckbatch(self,config):
        if config['BatchMode']['Turn_on'] == False:
            print("Batch OFF")
            return 0
        elif config['BatchMode']['Turn_on'] == True:
            print("Batch ON")
            return 1
    def cklang(self,config):
        if config['Language']['lang'] == "en_US":
            return 0
        if config['Language']['lang'] == "zh_CN":
            return 1
    def sign(self,config):
        print(config['Sign']['LOGO'])
    def show_version(self,config,lang):
        if lang == 0:
            print(config['Language']['en_US']['version'] + config['Sign']['Version'])
        if lang == 1:
            print(config['Language']['zh_CN']['version'] + config['Sign']['Version'])
    def getURL(self,lang):
        if lang == 0:
            URL = input(config['Language']['en_US']['input_tip'])
        if lang == 1:
            URL = input(config['Language']['zh_CN']['input_tip'])
        return URL
    def output_asking(self,config,lang):
        if lang == 0:
            print(config['Language']['en_US']['output_asking'])
        if lang == 1:
            print(config['Language']['zh_CN']['output_asking'])
        print('''
(0) Pure TEXT
(1) MarkDown
(2) HTML
                ''')
        choose = int(input(":"))
        return choose
class Main:
    def loadconfig(self,filename):
        config = toml.load(filename)
        return config
    def getPage(self,headers,URL):
        session = requests.session()
        response = session.get(URL,headers=headers)
        if response.status_code == 200:
            print("200 OK")
            return response.text
        else:
            print(URL + "Get Page Failed")
            os._exit(0)
class Process:
    def getTitle(self,Page):
        soup = BeautifulSoup(Page,'lxml')
        title = soup.find('title')
        return title.string.strip()
    def print_as_pure_text(self,title,URL):
        print('-' * 20)
        print("Title:" + title)
        print("URL:" + URL)
    def print_as_markdown(self,title,URL):
        print("-" * 20)
        print("["+title+"]"+"("+URL+")")
    def print_as_html(self,title,URL):
        print("-" * 20)
        print("<a href=" + "\"" + URL + "\"" + ">" + title + "</a>")
    def get_filename(self, lang, config):
        if lang == 0:
            filename = input(config['Language']['en_US']['filename_input'])
        elif lang == 1:
            filename = input(config['Language']['zh_CN']['filename_input'])
        return filename
## classes

## Running
A = Main()
B = Process()
config = A.loadconfig('config.toml')
C = Interactions()
C.sign(config=config)
lang = C.cklang(config=config)
C.show_version(config=config,lang=lang)
if C.ckbatch(config=config) == 0:
    URL = C.getURL(lang=lang)
    page = A.getPage(headers=config['headers'],URL=URL)
    choose = C.output_asking(config=config,lang=lang)
    title = B.getTitle(page)
    if choose == 0:
        B.print_as_pure_text(title=title,URL=URL)
    if choose == 1:
        B.print_as_markdown(title=title,URL=URL)
    if choose == 2:
        B.print_as_html(title=title,URL=URL)
elif C.ckbatch(config=config) == 1:
    def ck_format():
        choose = C.output_asking(config=config,lang=lang)
        if choose == 0:
            file_format = '.txt'
        if choose == 1:
            file_format = '.md'
        if choose == 2:
            file_format = '.html'
        return file_format
    filename = B.get_filename(lang=lang,config=config)
    file_format = ck_format()
    with open('out/'+filename+ file_format,'x',encoding="utf8") as f:
        URLIST = open('list.txt')
        for URL in URLIST:
            pure_url = URL.strip()
            page = A.getPage(headers=config['headers'], URL=pure_url)
            title = B.getTitle(page)
            if file_format == '.txt':
                f.write('Title:' + title + '\n' + 'URL:' + pure_url + '\n\n')
                B.print_as_pure_text(title=title, URL=pure_url)
            elif file_format == '.md':
                f.write("["+title+"]"+"("+pure_url+")\n\n")
                B.print_as_markdown(title=title,URL=pure_url)
            elif file_format == '.html':
                f.write("<a href=" + "\"" + pure_url + "\"" + ">" + title + "</a>" + "\n" + "<br>" + "\n")
                B.print_as_html(title,URL=pure_url)
