from scrapy import cmdline

cmdline.execute('scrapy crawl pks -o test3.json -t json'.split())
