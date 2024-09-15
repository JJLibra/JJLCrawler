from bilibili_api import video, Credential
import asyncio

import config

# 实例化
bv_id = 'BV1ej421S7wn'

credential = Credential(sessdata=config.SESSDATA, bili_jct=config.BILI_JCT, buvid3=config.BUVID3)
v = video.Video(bvid=bv_id, credential=credential)


@v.on('ONLINE')
async def on_online_update(event):
    """
    在线人数更新
    """
    print(event)


@v.on('DANMAKU')
async def on_danmaku(event):
    """
    收到实时弹幕
    """
    print(event)


asyncio.get_event_loop().run_until_complete(v.connect())
