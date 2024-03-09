import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import DoubanspiderItem
from scrapy import Request
import time


class DoubanDetailsSpiderSpider(scrapy.Spider):
    name = 'dbs'
    allowed_domains = ['movie.douban.com']
    start_urls = ["https://movie.douban.com/top250"]

    step_time = 5  # 停顿时间
    page_number = 0  # 控制页号，利用每一页25部电影进行传参换页

    # 数据分析
    def parse(self, response):
        # 提取当前页电影基础信息
        node_list = response.xpath('//div[@class="info"]')

        # 提取信息
        for msg in node_list:
            # 注意：循环体内为一部电影的数据处理，所以应该使用'./...'
            # 详情链接
            details_url = msg.xpath('./div[@class="hd"]/a/@href').extract()
            # 中文名称
            name_chinese = msg.xpath('./div[@class="hd"]/a/span[1]/text()').extract()
            # 原名
            name = msg.xpath('./div[@class="hd"]/a/span[2]/text()').extract()
            name = str(name).replace("\\xa0", "").replace("/", "")
            # 别名列表
            name_other_list = msg.xpath('./div[@class="hd"]/a/span[3]/text()').extract()
            name_other_list = str(name_other_list).replace("\\xa0", "").replace("/", "")
            # 播放状态
            player_type = msg.xpath('./div[@class="hd"]/span[@class="playable"]/text()').extract()
            player_type = str(player_type)[3:-3]
            # 评价人数
            number_evaluate = msg.xpath('./div[@class="bd"]/div[@class="star"]/span[4]/text()').extract()
            number_evaluate = str(number_evaluate)[2:-5]
            # 评分
            score = msg.xpath('./div[@class="bd"]/div[@class="star"]/span[@property="v:average"]/text()').extract()
            # 中心主题
            purpose = msg.xpath('./div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()').extract()

            # 使用管道保存
            # 管道可以对键值自动去重
            item_pipe = DoubanspiderItem()
            item_pipe["details_url"] = details_url
            item_pipe["name_chinese"] = name_chinese
            item_pipe["name"] = name
            item_pipe["name_other_list"] = name_other_list
            item_pipe["player_type"] = player_type
            item_pipe["number_evaluate"] = number_evaluate
            item_pipe["score"] = score
            item_pipe["purpose"] = purpose

            time.sleep(self.step_time)

            # 转交控制权，继续提取详情数据
            yield Request(details_url[0], callback=self.get_details, meta={"info": item_pipe})

        # 控制页号，利用每一页25部电影进行传参换页
        self.page_number += 1
        print(self.page_number)
        # 爬取其他页面
        if self.page_number < 10:
            time.sleep(3)
            page_url = 'https://movie.douban.com/top250?start={}&filter='.format(self.page_number * 25)
            yield scrapy.Request(page_url, callback=self.parse)

    # 获取详情页数据
    def get_details(self, response):
        # 以支持在item_pipe继续补充数据
        item_pipe = DoubanspiderItem()
        info = response.meta["info"]
        item_pipe.update(info)

        # 详情页基础信息
        response = response.xpath('//div[@id="info"]')
        # 编剧列表
        writer_list = response.xpath('./span[2]/span[@class="attrs"]/a/text()').extract() if response.xpath(
            './span[2]/span[@class="attrs"]/a/text()').extract() else ''
        # 导演列表
        director_list = response.xpath('./span[1]/span[@class="attrs"]/a/text()').extract() if response.xpath(
            './span[1]/span[@class="attrs"]/a/text()').extract() else ''
        # 主演列表
        star_list = response.xpath('string(./span[@class="actor"]/span[@class="attrs"])').extract() if response.xpath(
            'string(./span[@class="actor"]/span[@class="attrs"])').extract() else ''
        # 官方网站
        official_url = response.xpath('./a[@rel="nofollow" and @target="_blank"]/@href').extract() if response.xpath(
            './a[@rel="nofollow" and @target="_blank"]/@href').extract() else ''
        # 上映时间
        release_data = response.xpath('./span[@property="v:initialReleaseDate"]/text()').extract() if response.xpath(
            './span[@property="v:initialReleaseDate"]/text()').extract() else ''
        # 制片国，发现制片地区无法直接使用xpath直接定位，下面这样处理
        area = str(response.extract())
        area = area[area.index("制片国"):area.index("语言")].strip()
        area = area[area.index("</span>") + 7:area.index("<br>")].strip() if area[area.index("</span>") + 7:area.index(
            "<br>")].strip() else ''
        # 语言，同上处理
        languages = str(response.extract())
        languages = languages[languages.index("语言"):languages.index("上映")].strip()
        languages = languages[languages.index("</span>") + 7:languages.index("<br>")].strip()
        # 片长
        times = response.xpath('./span[@property="v:runtime"]/text()').extract()
        # 类型
        film_type = response.xpath('./span[@property="v:genre"]/text()').extract()

        item_pipe["writer_list"] = writer_list
        item_pipe["director_list"] = director_list
        item_pipe["star_list"] = star_list
        item_pipe["official_url"] = official_url
        item_pipe["release_data"] = release_data
        item_pipe["area"] = area
        item_pipe["languages"] = languages
        item_pipe["times"] = times
        item_pipe["film_type"] = film_type

        yield item_pipe
