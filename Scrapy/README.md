# Scrapy

这是一个很好用的框架，主要用于爬取静态资源网站内容，爬取难度不大。

### ajkSpider

目标网站：https://xa.anjuke.com/sale/gaoxinxa/

主要用于爬取安居客平台中的部分租房信息：具体信息请参照代码中的注释

使用以下命令即可将结果以 json、csv 格式保存在 result 文件夹中（请注意使用命令所在目录应为spiders）：

```python
python ajks.py
```

### dbSpider

目标网站：https://movie.douban.com

主要用于爬取豆瓣网前250电影信息：具体信息请参照代码中的注释

使用以下命令即可将结果以 json、csv 格式保存在 result 文件夹中（请注意使用命令所在目录应为spiders）：

```python
python dbs.py
```

### pksSpider

目标网站：https://packetstormsecurity.com/files/tags/exploit/

主要用于爬取漏洞报告：具体信息请参照代码中的注释

使用以下命令即可将结果以 json、csv 格式保存在 result 文件夹中（请注意使用命令所在目录应为spiders）：

```python
python pks.py
```

