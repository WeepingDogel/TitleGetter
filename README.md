# TitleGetter
用来获取链接标题的小爬虫...
（你觉得可以用来干嘛呢？）

[English](README_EN.md)



## Bugs

部分链接（比较少见）爬取下来可能会出现乱码，这是编码问题导致的......

非批量模式下已经修复，在 `config.toml` 文件里面将 `EncodingFix` 设置为 `true` 即可。

批量模式目前正在想办法..

### 以下链接会出现乱码
```
Title: Carty - 生成超大文字绘 文字图片。特殊字符，符号尽在 超酷表情 Mega Emoji
URL: https://www.megaemoji.com/cn/generators/carty/

Title: Deepin 2014 Alpha –准备进入全新的深度世界 · LinuxTOY
URL: https://linuxtoy.org/archives/linux-deepin-2014-alpha-into-new-deepin-world.html

```

## 依赖
运行前请安装这几个 Python 库，`requests`、`bs4`、`toml`

```
$ pip install requests bs4 toml
```
## 更新日志

* v 1.0.1

    更新了批量模式，采用了 toml 配置文件。