#!/usr/bin/python
# -*- coding: UTF-8 -*-


'''
This is Aur version
:)
'''

### Modules Importing ###
import os
import requests
from bs4 import BeautifulSoup
import toml
### Modules Importing ###

class Main:
    '''
    Main Opertations
    Loading configuration files and languages, show the version and the logo, etc.
    The functions on this class will be ran as soon as the program started.
    '''
    def LoadTheConfig(self,filename):
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
    def ShowLogo(self,config):
        '''
        The intention of this function is simple.
        Showing a LOGO composed of texts on a terminal is its final mission. LOL
        However, the LOGO was written to the configuration file by a foolish dog,
        So the parameter "config" is used to receive the result of the function "LoadTheConfig()".
        '''
        print(config['Sign']['LOGO'])
        '''
        Well, finished.
        But in order to read the LOGO currectly, the parameter "config" is required.
        such as:

        config = LoadTheConfig("config.toml")
        ShowLogo(config=config)
        
        Like this.
        '''
    def LoadOutputs(self,filename):
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
    def ShowVersion(self,config):
        print(config['Sign']['Version'])
        # Get the version from the configuration file, and show it on the terminal.
class Interactions:
    #This class is in order to deal with languages and outputs.
    def CheckLanguage(self,config):
        # Check the language type from configuration file.
        if config['Language']['lang'] == "en_US":
            lang = 0
        elif config['Language']['lang'] == "zh_CN":
            lang = 1
        return lang
    def InputTip(self,lang,Outputs):
        # Out put a tip to get a URL.
        if lang == 0:
            URL = input(Outputs['en_US']['input_tip'])
        if lang == 1:
            URL = input(Outputs['zh_CN']['input_tip'])
        return URL
    def RequestsSuccess(self,lang, Outputs):
        # print a sentence 
        # "Requested Successfully"
        if lang == 0:
            print(Outputs['en_US']['requests_success'])
        if lang == 1:
            print(Outputs['zh_CN']['requests_success'])
    def RequestsFailure(self,lang, Outputs):
        # print a sentence 
        # "Requested Successfully"
        if lang == 0:
            print(Outputs['en_US']['requests_failure'])
        if lang == 1:
            print(Outputs['zh_CN']['requests_failure'])
    def FileNameInput(self,lang,Outputs):
        # Output a tip to get a file name.
        if lang == 0:
            FileName = input(Outputs['en_US']['filename_input'])
        if lang == 1:
            FileName = input(Outputs['zh_CN']['filename_input'])
        return FileName
    def EmptyLineWarning(self,lang,Outputs):
        # Output a warn
        if lang == 0:
            print(Outputs['en_US']['empty_line_warning'])
        if lang == 1:
            print(Outputs['zh_CN']['empty_line_warning'])
    def OutputAsking(self,lang,Outputs):
        # Output three tips to ask the user...
        if lang == 0:
            print(Outputs['en_US']['output_asking'])
        if lang == 1:
            print(Outputs['zh_CN']['output_asking'])
        print('''
(0) Pure TEXT
(1) MarkDown
(2) HTML
                ''')
        choose = int(input(':'))
        return choose
class Process:
    def CheckBatch(self,config):
        # check if the BatchMode opened
        if config['BatchMode']['Turn_on'] == False:
            print("Batch OFF")
            return 0
        if config['BatchMode']['Turn_on'] == True:
            print("Batch On")
            return 1
    def GetPage(self,headers,URL,session):
        # Get the webpage (HTML files).
        session = session
        response = session.get(url=URL, headers=headers)
        if response.status_code == 200:
            print('\n' + URL + " --> 200 OK")
            return response.text
        else:
            print(URL + "Get Page Failed")
            os._exit(0)
    def GetTitle(self,page):
        # Get the title from the page.
        soup = BeautifulSoup(page,'lxml')
        title = soup.find('title')
        return title.string.strip()
    def PrintAsPureText(self,title,URL):
        print('-' * 40)
        print('Title: ' + title)
        print('Link: ' + URL)
        print('-' * 40)
    def PrintAsMarkDown(self,title,URL):
        print('-' * 40)
        print('['+ title + ']' + '(' + URL + ')')
        print('-' * 40)
    def PrintAsHTML(self,title,URL):
        print('-' * 40)
        print("<a href=" + "\"" + URL + "\"" + ">" + title + "</a>")
        print('-' * 40)
        
##Running##
'''
Here is the running aera for the classes, everything will be started from here.
'''

## Step Zero, initialize everything.
Starting = Main()
OutPut = Interactions()
Do = Process()
if os.path.exists(str(os.getenv('XDG_CONFIG_HOME')) + '/titlegetter/config.toml') == True:
    config = Starting.LoadTheConfig(os.getenv('XDG_CONFIG_HOME')+'/titlegetter/config.toml')
elif os.path.exists(os.getenv('HOME') + '/.config/titlegetter/config.toml') == True:
    config = Starting.LoadTheConfig(os.getenv('HOME') + '/.config/titlegetter/config.toml')
else:
    config = Starting.LoadTheConfig('/etc/titlegetter/config.toml')
# config = Starting.LoadTheConfig(filename="config/config.toml") # Now it's time to load the config file. :)
Starting.ShowLogo(config=config) # if the LOGO is printed currectly, the configuration file has been loaded successfully.
Starting.ShowVersion(config=config) # Show the version
Outputs = Starting.LoadOutputs(filename="/usr/share/titlegetter/lang.toml") # Load the output texts
lang = OutPut.CheckLanguage(config=config) # get the langauge
headers = config['headers'] # import the headers
session = requests.session() # start a session 
## Step One, Check if the BatchMode opening.

if Do.CheckBatch(config=config) == 0:
    ## Step Two, When the BatchMode is closed, try to get the single URL which is offered by the user.
    URL = OutPut.InputTip(lang=lang, Outputs=Outputs)
    ## Then Get the Page.
    Page = Do.GetPage(headers=headers,URL=URL,session=session)
    ## When we get the page, then get the title
    Title = Do.GetTitle(page=Page)
    ## Then ask the user how to output the result.
    choose = OutPut.OutputAsking(lang=lang,Outputs=Outputs)
    ## Finally output the result by following the choose.
    if choose == 0:
        Do.PrintAsPureText(title=Title,URL=URL)
    if choose == 1:
        Do.PrintAsMarkDown(title=Title,URL=URL)
    if choose == 2:
        Do.PrintAsHTML(title=Title,URL=URL)
elif Do.CheckBatch(config=config) == 1:
    # Step Two
    # When the BatchMode is turned on
    # Ask the user how to output the result at first.
    choose = OutPut.OutputAsking(lang=lang, Outputs=Outputs)
    if choose == 0:
        FileFormat = '.txt'
    if choose == 1:
        FileFormat = '.md'
    if choose == 2:
        FileFormat = '.html'
    FileName = OutPut.FileNameInput(lang=lang,Outputs=Outputs) ## Get the filename
    with open(os.getenv('HOME') + '/Documents/' + FileName + FileFormat, 'x', encoding='utf-8') as f: # Create a file to save the result.
        URLLIST = open(config['Main']['URLLIST']) # Get the URLLIST from the configuration file
        for URL in URLLIST: # Get the URL from the URLLIST
            PureURL = URL.strip() # Remove the blanks 
            Page = Do.GetPage(headers=headers,URL=PureURL,session=session) # Get the Title
            Title = Do.GetTitle(Page) # Get the Page
            if FileFormat == '.txt': # Output
                f.write('Title: ' + Title + '\n' + 'Link: ' + PureURL + '\n\n')
                Do.PrintAsPureText(title=Title,URL=PureURL)
            if FileFormat == '.md':
                f.write('['+ Title + ']' + '(' + PureURL + ')' + '\n\n')
                Do.PrintAsMarkDown(title=Title,URL=PureURL)
            if FileFormat == '.html':
                f.write("<a href=" + "\"" + PureURL + "\"" + ">" + Title + "</a>" + "\n")
                Do.PrintAsHTML(title=Title,URL=PureURL)
        # Tell the file to the user
        print('\n\n\n\n File saved as:' + os.getenv('HOME') + '/Documents/' + FileName + FileFormat) 
##Running##