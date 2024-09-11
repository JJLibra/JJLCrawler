# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AjkzfspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    shi =scrapy.Field()
    ting=scrapy.Field()
    wei=scrapy.Field()
    mianji=scrapy.Field()
    louceng=scrapy.Field()
    jiage=scrapy.Field()
    xqname=scrapy.Field()
    address=scrapy.Field()
    huanjing=scrapy.Field()
    pass
