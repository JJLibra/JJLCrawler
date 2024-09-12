import argparse
import config


async def parse_cmd():
    parser = argparse.ArgumentParser(description='JJLCrawler program.')

    parser.add_argument('--platform', type=str, help='JJLCrawler platform select (bili | xhs | zhihu)',
                        choices=['bili', 'xhs', 'zhihu'], default=config.PLATFORM)
    parser.add_argument('--login', type=str, help='Login type (qrcode | phone | cookie)',
                        choices=['qrcode', 'phone', 'cookie'], default=config.LOGIN_TYPE)
    parser.add_argument('--type', type=str, help='Crawler type (search | detail | creator)',
                        choices=['search', 'detail', 'creator'], default=config.CRAWLER_TYPE)
    parser.add_argument('--startP', type=int,
                        help='Number of start page', default=config.START_PAGE)

    args = parser.parse_args()

    # override config
    config.PLATFORM = args.platform
    config.LOGIN_TYPE = args.login
    config.CRAWLER_TYPE = args.type
    config.START_PAGE = args.startP

