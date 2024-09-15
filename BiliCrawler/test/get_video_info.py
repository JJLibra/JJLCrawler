import config
import asyncio

from typing import Dict
from bilibili_api import video, Credential
from handle_file import FileHandler


async def get_video_info():
    """
    example:
    Crawl https://www.bilibili.com/video/BV1ej421S7wn/?spm_id_from=333.788&vd_source=91a233ea2e45cea087336c119461d12b video information
    :return: None
    """
    bv_id = 'BV1ej421S7wn'

    credential = Credential(sessdata=config.SESS_DATA, bili_jct=config.BILI_JCT, buvid3=config.BUV_ID3)
    v = video.Video(bvid=bv_id, credential=credential)
    info = await v.get_info()  # 获取视频信息

    await file_write_to_json(bv_id=bv_id, data=info)  # 保存到json文件中，方便阅读
    # await v.like(True)  # 视频点赞


async def file_write_to_json(bv_id: str, data: Dict):
    file_handler = FileHandler()
    file_handler.save_json(f'{bv_id}.json', data=data)


asyncio.run(get_video_info())
