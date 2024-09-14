import asyncio
from typing import Dict

from bilibili_api import emoji, sync
from handle_file import FileHandler


async def file_write_to_json(data: Dict):
    file_handler = FileHandler()
    file_handler.save_json(f'emoji.json', data=data)

info = sync(emoji.get_emoji_list())

asyncio.run(file_write_to_json(data=info))  # 保存到json文件中，方便阅读
