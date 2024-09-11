import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium.webdriver import Chrome
from scrapy import signals


class PksSpider(CrawlSpider):
    name = 'pks'
    allowed_domains = ['packetstormsecurity.com']
    start_urls = ['https://packetstormsecurity.com/files/tags/exploit/page1/']

    rules = (
        Rule(LinkExtractor(allow=r'/files/tags/exploit/page(.*?)'), callback='parse_vul_list', follow=True),
    )

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(PksSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.driver = Chrome()
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.driver.close()

    # 获取当前页漏洞网址链接
    def parse_vul_list(self, response):
        # print(response.text)
        counter = 0
        vul_list = response.xpath('//a[@class="ico text-plain"]/@href').extract()
        for vul in vul_list:
            counter += 1
            if counter >= 2:
                break
            vul_url = 'https://packetstormsecurity.com' + vul
            request = scrapy.Request(url=vul_url, callback=self.parse_vul_inf)
            yield request

    # 详情页数据分析
    def parse_vul_inf(self, response):
        item = {}

        item['title'] = response.xpath('//strong/text()').extract_first() if response.xpath(
            '//strong/text()').extract_first() else ''

        authors = response.xpath('//a[@class="person"]/text()').extract() if response.xpath(
            '//a[@class="person"]/text()').extract() else ''
        item['author'] = ','.join(authors)

        date = response.xpath('//dd[@class="datetime"]/a/@href').extract_first() if response.xpath(
            '//dd[@class="datetime"]/a/@href').extract_first() else ''
        pattern = re.compile(r'/files/date/(.*?)')
        item['date'] = pattern.findall(date)[0]

        item['des'] = response.xpath('//dd[@class="detail"]/p/text()').extract_first() if response.xpath(
            '//dd[@class="detail"]/p/text()').extract_first() else ''

        item['vul_type'] = ''

        cveid = response.xpath('//dd[@class="cve"]/a/text()').extract() if response.xpath(
            '//dd[@class="cve"]/a/text()').extract() else ''
        item['CVE-ID'] = ','.join(cveid)

        test = response.xpath('//div[@class="src"]/pre/code/text()').extract_first() if response.xpath(
            '//div[@class="src"]/pre/code/text()').extract_first() else ''
        s_replace = test.replace('<br>', '')
        s_replace = s_replace.replace('<code>', '')
        s_replace = s_replace.replace('</code>', '')
        item['poc'] = s_replace

        yield item
