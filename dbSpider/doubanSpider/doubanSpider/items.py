# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    details_url = scrapy.Field()
    name_chinese = scrapy.Field()
    name = scrapy.Field()
    name_other_list = scrapy.Field()
    player_type = scrapy.Field()
    director_list = scrapy.Field()
    writer_list = scrapy.Field()
    star_list = scrapy.Field()
    official_url = scrapy.Field()
    release_data = scrapy.Field()
    area = scrapy.Field()
    languages = scrapy.Field()
    times = scrapy.Field()
    film_type = scrapy.Field()
    number_evaluate = scrapy.Field()
    score = scrapy.Field()
    purpose = scrapy.Field()
