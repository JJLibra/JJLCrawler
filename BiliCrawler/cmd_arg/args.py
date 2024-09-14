import argparse
import config


async def parse_cmd():
    parser = argparse.ArgumentParser(description='BilibiliCrawler program.')

    parser.add_argument('--module', type=str, help='BilibiliCrawler module select (search | user | video | topic |'
                                                   ' music | emoji | ip_address)',
                        choices=['search', 'user', 'video', 'topic', 'music', 'emoji', 'ip_address'],
                        default=config.MODULE)
    parser.add_argument('--login', type=str, help='Login type (qrcode | phone | passwd)',
                        choices=['qrcode', 'phone', 'passwd'], default=config.LOGIN_TYPE)
    parser.add_argument('--start', type=int,
                        help='Number of start page', default=config.START_PAGE)

    args = parser.parse_args()

    # override config
    config.PLATFORM = args.module
    config.LOGIN_TYPE = args.login
    config.START_PAGE = args.start
