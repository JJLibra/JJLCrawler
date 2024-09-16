from tools.utils import logger
from bilibili_api import video


async def get_number_of_online_people():
    logger.info("Getting online people started.")

    bv_id = input("Please enter the BV ID of the video: ").strip()
    if not bv_id.startswith('BV') or len(bv_id) != 12:
        logger.error(f"Invalid BV ID: {bv_id}")
        print("Invalid BV ID. Currently, only 12-bit is supported, please make sure it's a valid Bilibili BV ID.")
        return

    v = video.Video(bvid=bv_id)

    online = await v.get_online()
    logger.info(f"总共 {online['total']} 人在观看，其中 {online['count']} 人在网页端观看")
    logger.info("Getting online people finished successfully.")
