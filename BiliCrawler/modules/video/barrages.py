import config
import time
from typing import List
from tools.utils import logger
from bilibili_api import video, Credential, Danmaku
from bilibili_api.user import User


async def fetch_video_barrages():
    logger.info("Fetching video barrages started. ")

    credential = Credential(sessdata=config.SESS_DATA, bili_jct=config.BILI_JCT, buvid3=config.BUV_ID3)

    bv_id = input("Please enter the BV ID of the video: ").strip()
    if not bv_id.startswith('BV') or len(bv_id) != 12:
        logger.error(f"Invalid BV ID: {bv_id}")
        print("Invalid BV ID. Currently, only 12-bit is supported, please make sure it's a valid Bilibili BV ID.")
        return

    v = video.Video(credential=credential, bvid=bv_id)

    barrages_list: List = await v.get_danmakus()
    if not barrages_list:
        logger.error("No barrages.")
        return

    for barrage in barrages_list:
        if barrage.text == '':
            continue
        assert isinstance(barrage, Danmaku)
        text, dm_time, crc32_id, send_time = (barrage.text, barrage.dm_time, barrage.crc32_id,
                                              time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(barrage.send_time)))
        try:
            uid = barrage.crack_uid(crc32_id)
            uname_info: dict = await User(uid=uid, credential=credential).get_user_info()
            uname = uname_info['name']
        except:
            uname = 'Unknown'

        # print(f"{send_time} {dm_time}s {uname}: {text}")

        with open(f'./results/{bv_id}_barrages.txt', 'a', encoding='utf-8') as f:
            f.write(f"{send_time} {dm_time}s {uname}: {text}\n")
            f.close()

    logger.info(f"Barrages saved at ./results/{bv_id}_barrages.txt successfully.")
    logger.info("Fetching video barrages finished successfully.")
