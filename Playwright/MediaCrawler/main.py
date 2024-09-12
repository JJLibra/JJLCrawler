import sys
import asyncio

import config
import cmd_arg
from basicCrawler.base_crawler import AbstractCrawler
from platforms.bilibili import BilibiliCrawler
from platforms.xiaohongshu import XiaoHongShuCrawler
from platforms.zhihu import ZhiHuCrawler


class CrawlerFactory:
    CRAWLERS = {
        'bili': BilibiliCrawler,
        'xhs': XiaoHongShuCrawler,
        'zhihu': ZhiHuCrawler
    }

    @staticmethod
    def create_crawler(platform: str) -> AbstractCrawler:
        crawler_class = CrawlerFactory.CRAWLERS.get(platform)
        if not crawler_class:
            raise ValueError("Invalid Platform. Currently only supported xhs or dy or ks or bili ..."
                             " Please check the usage list.")
        return crawler_class()


async def main():
    # parse cmd: 开始爬取之前必须等待命令行参数
    await cmd_arg.parse_cmd()

    # 开始爬取
    crawler = CrawlerFactory.create_crawler(platform=config.PLATFORM)
    await crawler.start()


if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        sys.exit()
