import sys
import asyncio
import cmd_arg
import config
from base.base_crawler import AbstractCrawler
from modules.colu_section import SectionCrawler
from modules.emoji import EmojiCrawler
from modules.ip_address import IpCrawler
from modules.music import MusicCrawler
from modules.search import SearchCrawler
from modules.topic import TopicCrawler
from modules.user import UserCrawler
from modules.video import VideoCrawler


class CrawlerFactory:
    CRAWLERS = {
        'ip_address': IpCrawler,
        'video': VideoCrawler,
        'user': UserCrawler,
        'search': SearchCrawler,
        'topic': TopicCrawler,
        'emoji': EmojiCrawler,
        'section': SectionCrawler,
        'music': MusicCrawler
    }

    @staticmethod
    def create_crawler(module: str) -> AbstractCrawler:
        crawler_class = CrawlerFactory.CRAWLERS.get(module)
        if not crawler_class:
            raise ValueError("Invalid Module. Currently only supported search or user or video or topic ..."
                             " Please check the usage list.")
        return crawler_class()


async def main():
    # parse cmd
    await cmd_arg.parse_cmd()

    crawler = CrawlerFactory.create_crawler(module=config.MODULE)
    await crawler.start()


if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        sys.exit()
