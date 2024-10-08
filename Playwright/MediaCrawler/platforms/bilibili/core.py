import config

from typing import List, Optional
from playwright.async_api import Page, BrowserContext, async_playwright
from tools import utils

from basicCrawler.base_crawler import AbstractCrawler
from .client import BilibiliClient
from .login import BilibiliLogin


class BilibiliCrawler(AbstractCrawler):
    # 下面会涉及到的三个重要对象
    context_page: Page  # 交互对象
    bili_client: BilibiliClient  # 浏览器客户端: 交互 API
    browser_context: BrowserContext  # 管理浏览器状态和会话

    def __init__(self):
        self.index_url = 'https://www.bilibili.com'
        self.user_agent = utils.get_user_agent()

    async def start(self):
        playwright_proxy_format, httpx_proxy_format = None, None
        # ip 代理池: 避免因频繁访问而被封禁，也可提高匿名性
        if config.ENABLE_IP_PROXY:
            # Todo
            pass

        # 开始使用 playwright
        async with async_playwright() as p:
            # 启动一个浏览器上下文: 进入 bilibili 首页
            chromium = p.chromium
            self.browser_context = await self.launch_browser(
                chromium,
                None,
                self.user_agent,
                headless=config.HEADLESS
            )
            await self.browser_context.add_init_script(path="libs/stealth.min.js")  # 脚本: stealth.min.js 用于隐藏爬虫的特征
            self.context_page = await self.browser_context.new_page()
            await self.context_page.goto(self.index_url)

            # 创建 bilibili 客户端（尤其像是登录操作）: 便于API的调用
            # 1.创建 bili 客户端
            self.bili_client = await self.create_bilibili_client(httpx_proxy_format)
            # 2.检查登录状态
            if not await self.bili_client.pong():
                # Todo
                pass

            # crawler_type_var.set(config.CRAWLER_TYPE)
            if config.CRAWLER_TYPE == "search":
                # 搜索视频并检索评论信息
                await self.search()
            elif config.CRAWLER_TYPE == "detail":
                # 获取B站指定帖子的信息和评论
                await self.get_specified_videos(config.BILI_SPECIFIED_ID_LIST)
            elif config.CRAWLER_TYPE == "creator":
                # 根据创作者id执行任务
                for creator_id in config.BILI_CREATOR_ID_LIST:
                    await self.get_creator_videos(int(creator_id))
            else:
                pass

    async def create_bilibili_client(self, httpx_proxy: Optional[str]) -> BilibiliClient:
        cookie_str, cookie_dict = utils.convert_cookies(await self.browser_context.cookies())
        bilibili_client_obj = BilibiliClient(
            proxies=httpx_proxy,
            headers={
                "User-Agent": self.user_agent,
                "Cookie": cookie_str,
                "Origin": "https://www.bilibili.com",
                "Referer": "https://www.bilibili.com",
                "Content-Type": "application/json;charset=UTF-8"
            },
            playwright_page=self.context_page,
            cookie_dict=cookie_dict,
        )
        return bilibili_client_obj

    async def search(self):
        pass

    async def get_specified_videos(self, b_vid_list: List[str]):
        pass

    async def get_creator_videos(self, creator_id: int):
        pass
