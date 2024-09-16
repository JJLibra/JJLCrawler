import argparse
import config


async def parse_cmd():
    parser = argparse.ArgumentParser(description='BilibiliCrawler program.')

    # search | user | topic | music | section
    parser.add_argument('--module', type=str, help='BilibiliCrawler module select (video | emoji | ip_address)',
                        choices=['video', 'emoji', 'ip_address'],
                        default=config.MODULE)
    parser.add_argument('--start', type=int,
                        help='Number of start page', default=config.START_PAGE)

    args = parser.parse_args()

    # override config
    config.MODULE = args.module
    config.START_PAGE = args.start
