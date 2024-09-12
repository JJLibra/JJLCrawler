import scrapy

from ajkzfspider.items import AjkzfspiderItem


class AjksSpider(scrapy.Spider):
    name = 'ajks'
    allowed_domains = ['xa.zu.anjuke.com']
    start_urls = ['https://xa.anjuke.com/sale/gaoxinxa/']

    nextpage=''#下一页的数据

    def parse(self, response):
        #查看爬取的网页内容
        # print(str(response.body,'utf-8'))
        #获取所有的标题信息
        titles=response.xpath("//div[@class='property-content-title']/h3/text()")
        infos=response.xpath('//div[@class="property-content-info"]')
        prices=response.xpath('//span[@class="property-price-total-num"]/text()')
        xiaoqumingchengs=response.xpath('//p[@class="property-content-info-comm-name"]/text()')
        addresses=response.xpath('//p[@class="property-content-info-comm-address"]')
        envs=response.xpath('//span[@class="property-content-info-tag"]')
        #创建数据项对象items对象
        zfitem=AjkzfspiderItem()
        for title,info,price,xiaoqu,addr,env in zip(titles,infos,prices,xiaoqumingchengs,addresses,envs):
            zfitem = AjkzfspiderItem()
            #print(title.get())
            zfitem['title']=title.get()
            #print(info.get())
            #获取室的信息
            shi=info.xpath('./p[1]/span[1]/text()').get()
            #print(shi,"室")
            zfitem['shi'] = shi
            # 获取厅的信息
            ting = info.xpath("./p[1]/span[3]/text()").get()
            #print(ting, "厅")
            zfitem['ting'] = ting
            # 获取卫的信息
            wei = info.xpath("./p[1]/span[5]/text()").get()
            #print(wei, "卫")
            zfitem['wei'] = wei
            # 获取面积的信息
            mianji = info.xpath("./p[2]/text()").get()
            #print(mianji, "平米")
            zfitem['mianji'] = mianji

            #获取楼层信息
            louceng=info.xpath("./p[4]/text()").get()
            #print(louceng)
            zfitem['louceng'] = louceng

            #获取价格信息
            jiage=price.get()
            #print(jiage,'元/月')
            zfitem['jiage'] = jiage


            #获取小区名称
            xqname=xiaoqu.get()
            #print(xqname)
            zfitem['xqname'] = xqname


            #获取地址的值
            address=addr.get().strip()
            #print(address)
            zfitem['address'] = address


            #获取环境信息
            huanjing=env.xpath('span/text()').getall()
            #print(huanjing)
            zfitem['huanjing'] = huanjing
            yield zfitem
        for i in range(2,6):
            nextpage='https://xa.anjuke.com/sale/gaoxinxa/p'+str(i)
            print(nextpage)
            yield scrapy.Request(nextpage,callback=self.parse)
