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

    # 静态方法: 第一次使用，标记一下，其实就是一种不依赖于类实例的方法，使用当前类时可以直接调用，所以这里使用静态方法显然是合理的
    @staticmethod
    def create_crawler(platform: str) -> AbstractCrawler:
        crawler_class = CrawlerFactory.CRAWLERS.get(platform)
        if not crawler_class:
            # raise: 中断程序执行，主动抛出异常，除ValueError外，还有TypeError、KeyError...（看到这里就熟悉了，平时使用py程序时是不是遇到过？）
            raise ValueError("Invalid Platform. Currently only supported xhs or dy or ks or bili ..."
                             " Please check the usage list.")
        return crawler_class()


async def main():
    # parse cmd: 开始爬取之前必须等待命令行参数
    await cmd_arg.parse_cmd()

    # 开始爬取: 1.创建对应平台的爬虫类; 2.依赖子类执行指定的爬取任务
    crawler = CrawlerFactory.create_crawler(platform=config.PLATFORM)
    await crawler.start()


if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        sys.exit()
