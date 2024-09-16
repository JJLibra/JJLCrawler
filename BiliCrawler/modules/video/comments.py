from tools.utils import logger
from bilibili_api import comment, video, Credential
import config


async def fetch_video_comments():
    logger.info("Fetching video comments started.")

    credential = Credential(sessdata=config.SESS_DATA, bili_jct=config.BILI_JCT, buvid3=config.BUV_ID3)

    bv_id = input("Please enter the BV ID of the video: ").strip()
    if not bv_id.startswith('BV') or len(bv_id) != 12:
        logger.error(f"Invalid BV ID: {bv_id}")
        print("Invalid BV ID. Currently, only 12-bit is supported, please make sure it's a valid Bilibili BV ID.")
        return

    v = video.Video(credential=credential, bvid=bv_id)
    av_id = v.get_aid()
    logger.info(f"The AV ID of the video: {av_id}")

    lv_page, cmt = 1, 0
    while True:
        comments_dict: dict = await comment.get_comments(oid=av_id, type_=comment.CommentResourceType.VIDEO,
                                                         page_index=lv_page, credential=credential)
        if comments_dict['page']['count'] == 0:
            print("No comments found.")
            break

        for item in comments_dict['replies']:
            with open(f'./results/{bv_id}_comments.txt', 'a', encoding='utf-8') as f:
                f.write(f"{item['member']['uname']}: {item['content']['message']}\n")
                f.close()
        cmt += comments_dict['page']['size']

        if comments_dict['page']['count'] <= cmt:
            break

        lv_page += 1

    logger.info(f"There are {comments_dict['page']['count']} comments (no sub-comments).")
    logger.info("Fetching video comments finished.")
