#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
This is master branch.
:)
'''
### Modules Importing ###
import os
import requests
from bs4 import BeautifulSoup
import toml
import argparse
### Modules Importing ###


class Main:
    '''
    Main Opertations
    Loading configuration files and languages, show the version and the logo, etc.
    The functions on this class will be ran as soon as the program started.
    '''

    def GetParser(self):
        '''
        This function is used to get the options the users give.
        '''
        parser = argparse.ArgumentParser(
            description='HELP', epilog='Have a nice day!')
        parser.add_argument('-f', '--format', help='The format of output')
        parser.add_argument('-o', '--output', help='The filename of output')
        parser.add_argument(
            '-u', '--url', help='The url from which you want to get the Title')
        parser.add_argument(
            '-i', '--input-file', help='The original url list. It may be a *.txt file.')
        parser.add_argument(
            '-b', '--batch-mode', help='Get titles from multi URLs, a list file(*.txt) and an output-file are required.', action="store_true")
        return parser

    def LoadTheConfig(self, filename):
        '''
        Configuration files will be loaded by this function.
        This parameter "filename" is required to be a name of a toml file (*.toml),
        In the source code library, you can find it in the directory 'config/'
        For the installed, usually, it will be moved to the '/usr/share/titlegetter/'
        And the file is "config.toml"
        When finished loading, the result including the content of the configuration file would be returned.
        And the other functions would use the result.
        '''
        config = toml.load(filename)
        return config

    def ShowLogo(self, config):
        '''
        The intention of this function is simple.
        Showing a LOGO composed of texts on a terminal is its final mission. LOL
        However, the LOGO was written to the configuration file by a foolish dog,
        So the parameter "config" is used to receive the result of the function "LoadTheConfig()".
        '''
        print(config['Sign']['LOGO'])
        '''
        Well, finished.
        But in order to read the LOGO correctly, the parameter "config" is required.
        such as:

        config = LoadTheConfig("config.toml")
        ShowLogo(config=config)
        
        Like this.
        '''

    def LoadOutputs(self, filename):
        '''
        The intention of this function is the same one as the function LoadTheConfig(),
        because the foolish dog doesn't know how to store the output texts of the different languages,
        he used the *.toml file to store them...
        This parameter "filename" is required to be a name of a toml file (*.toml),
        So...
        In the source code library, you can find it in the directory 'config/'.
        For the installed, usually, it will be moved to the '/usr/share/titlegetter/'.
        And the file is "lang.toml".
        Generally, we needn't to edit this file.
        '''
        lang = toml.load(filename)
        return lang

    def ShowVersion(self):
        Version = '2.2.1'
        print("V " + Version)
        # Get the version from the configuration file, and show it on the terminal.


class Process:
    def GetPage(self, headers, URL, session):
        # Get the webpage (HTML files).
        session = session
        response = session.get(url=URL, headers=headers)
        if response.status_code == 200:
            print('\n' + URL + " --> " + str(response.status_code) + " OK")
            return response.text
        else:
            print(URL + "Get Page Failed:" + response.status_code)
            os._exit(0)

    def GetTitle(self, page):
        # Get the title from the page.
        soup = BeautifulSoup(page, 'lxml')
        title = soup.find('title')
        return title.string.strip()

    def PrintAsPureText(self, title, URL):
        print('-' * 40)
        print('Title: ' + title)
        print('Link: ' + URL)
        print('-' * 40)

    def PrintAsMarkDown(self, title, URL):
        print('-' * 40)
        print('[' + title + ']' + '(' + URL + ')')
        print('-' * 40)

    def PrintAsHTML(self, title, URL):
        print('-' * 40)
        print("<ul><a href=" + "\"" + URL + "\"" + ">" + title + "</a></ul>")
        print('-' * 40)


'''
Here is the running aera for the classes, everything will be started from here.
'''
# Step Zero, initialize everything.
Starting = Main()
Do = Process()
if os.path.exists(str(os.getenv('XDG_CONFIG_HOME')) + '/titlegetter/config.toml') == True:
    config = Starting.LoadTheConfig(
        os.getenv('XDG_CONFIG_HOME')+'/titlegetter/config.toml')
elif os.path.exists(os.getenv('HOME') + '/.config/titlegetter/config.toml') == True:
    config = Starting.LoadTheConfig(
        os.getenv('HOME') + '/.config/titlegetter/config.toml')
elif os.path.exists('/etc/titlegetter/config.toml') == True:
    config = Starting.LoadTheConfig('/etc/titlegetter/config.toml')
elif os.path.exists('config/config.toml') == True:
    # Now it's time to load the config file. :)
    config = Starting.LoadTheConfig(filename="config/config.toml")
# if the LOGO is printed correctly, the configuration file has been loaded successfully.
Starting.ShowLogo(config=config)
Starting.ShowVersion()  # Show the version
parser = Starting.GetParser()
args = parser.parse_args()
headers = config['headers']  # import the headers
session = requests.session()  # start a session
# Step One, Check if the BatchMode opening.
# Now it's time to check the WorkMode.
if not args.batch_mode:
    # If it's zero, then we will work on single-url mode.
    # Now we just need to get the url.
    URL = args.url
    # then get the title
    if URL == None:
        print('[ERROR] URL is required!')
        os._exit(0)
    Page = Do.GetPage(headers=headers, URL=URL, session=session)
    Title = Do.GetTitle(page=Page)
    # Then got the format.
    if args.format == 'txt':
        Do.PrintAsPureText(URL=URL, title=Title)
    elif args.format == 'md':
        Do.PrintAsMarkDown(URL=URL, title=Title)
    elif args.format == 'html':
        Do.PrintAsHTML(URL=URL, title=Title)
    elif args.format == None:
        print('[ERROR] Format is required!\n')
        parser.print_help()
    else:
        print("'" + args.format + "'" +
              ' is not a legal format that TitleGetter supports.\n')
        parser.print_help()
elif args.batch_mode:
    # If the WorkMode is one, then it will be different.
    # at first we should read a text(*.txt) file which contains some URLs and the output-file.
    InputFileName = args.input_file
    # Then we need to get the name of output-file
    OutputFileName = args.output
    # And the format
    Format = args.format
    # If None, print the warn.
    if InputFileName == None:
        print('[ERROR]Filename is required!')
        parser.print_help()
        os._exit(0)
    if OutputFileName == None:
        print('[ERROR] Filename is required!')
        parser.print_help()
        os._exit(0)
    if Format == None:
        print('[ERROR] Format is required!')
        parser.print_help()
        os._exit(0)
    # If everything is ok.
    with open(OutputFileName, 'w', encoding='utf-8') as f:
        URLList = open(InputFileName)
        for URL in URLList:
            PureURL = URL.strip()
            if PureURL == '':
                print('[ERROR] URL can not be empty!')
                f.close()
                os.remove(OutputFileName)
                os._exit(0)
            print('[Loaded] ' + PureURL)
            Page = Do.GetPage(headers=headers, URL=PureURL, session=session)
            Title = Do.GetTitle(page=Page)
            if Format == 'txt':
                f.write('Title: ' + Title + '\n' + 'Link: ' + PureURL + '\n\n')
                Do.PrintAsPureText(title=Title, URL=PureURL)
            elif Format == 'md':
                f.write('[' + Title + ']' + '(' + PureURL + ')' + '\n\n')
                Do.PrintAsMarkDown(title=Title, URL=PureURL)
            elif Format == 'html':
                f.write("<ul><a href=" + "\"" + PureURL +
                        "\"" + ">" + Title + "</a></ul>" + "\n")
                Do.PrintAsHTML(title=Title, URL=PureURL)
        # Tell the file to the user
        print('\n\n\n\n File saved as:' + os.getcwd() + '/' + OutputFileName)
