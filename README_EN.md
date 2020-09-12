# TitleGetter
A Python Script which could be used to get the title of an URL or get the titles of the URLs in a list file.

What do you think it can be used for?

[Chinese](README.md)

## Bugs

The titles that gotten from some URLs (just some) may be unable to read because of encoding problem.

On non-batch mode, it has been fixed, just edit the value of `EncodingFix` to `true` in the file `config.toml`

On Batch mode, it's being tried our best to fix, so please waiting for the new version coming.

If you want to get the title from a English Website, don't care.

### URLs with unreadable titles

```
Title: Carty - 生成超大文字绘 文字图片。特殊字符，符号尽在 超酷表情 Mega Emoji
URL: https://www.megaemoji.com/cn/generators/carty/

Title: Deepin 2014 Alpha –准备进入全新的深度世界 · LinuxTOY
URL: https://linuxtoy.org/archives/linux-deepin-2014-alpha-into-new-deepin-world.html

```
## Python dependencies

Please install these Python libraries before running,`requests`、`bs4`、`toml`.
```
$ pip install requests bs4 toml
```

## Update log

* v 1.0.1

    Added batch mode, using toml configuration file.