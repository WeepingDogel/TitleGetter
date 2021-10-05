![](Pics/TitleGetter.png)



**titlegetter** is a little tool to get the title of the websites and format the title and the links to **markdown** or **html**.


## Project Tree

```
.
├── config
│   ├── config.toml
│   └── version
├── LICENSE
├── Pics
│   ├── 2020-09-13_00-17.png
│   ├── 2020-09-13_00-28.png
│   └── TitleGetter.png
├── README.md
└── titlegetter.py

2 directories, 8 files
```

## Dependency

* Python 3.6 +
* Python library
    * Requests
    * bs4
    * toml
    * lxml
    * argparse

## Installation

Simple install:
```
$ git clone https://github.com/WeepingDogel/TitleGetter.git
```
```
$ cd TitleGetter
```
```
$ python titlegetter.py
```

On Arch Linux (aur):
```
$ yay -S titlegetter
```