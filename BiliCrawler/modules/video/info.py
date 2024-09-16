import json
from typing import Dict

import config

from tools.utils import logger
from bilibili_api import video, Credential


async def fetch_video_info():
    logger.info("Fetching video info started.")

    bv_id = input("Please enter the BV ID of the video: ").strip()
    if not bv_id.startswith('BV') or len(bv_id) != 12:
        logger.error(f"Invalid BV ID: {bv_id}")
        print("Invalid BV ID. Currently, only 12-bit is supported, please make sure it's a valid Bilibili BV ID.")
        return

    credential = Credential(sessdata=config.SESS_DATA, bili_jct=config.BILI_JCT, buvid3=config.BUV_ID3)
    v = video.Video(bvid=bv_id, credential=credential)

    try:
        info = await v.get_info()
        file_path = f"./results/{bv_id}.json"
        save_original_to_json(file_path, info)
        logger.info(f"Video info fetched and saved to {file_path} successfully.")
    except Exception as e:
        logger.error(f"Error occurred while fetching video info: {e}")


def save_original_to_json(file_path: str, data: Dict):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
