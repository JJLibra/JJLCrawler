import httpx
import os
import config

from bilibili_api import video, Credential, HEADERS
from tqdm import tqdm
from tools.utils import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FFMPEG_PATH = os.path.join(BASE_DIR, "tools", "ffmpeg", "bin", "ffmpeg.exe")
DOWNLOAD_DIR = os.path.join(BASE_DIR, "download")

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


async def download_url(url: str, out: str, info: str):
    """下载视频或音频流到本地，并显示进度条"""
    try:
        async with httpx.AsyncClient(headers=HEADERS) as sess:
            resp = await sess.get(url)
            length = int(resp.headers.get('content-length', 0))
            process = 0

            with open(out, 'wb') as f, tqdm(
                total=length,
                unit='B',
                unit_scale=True,
                desc=f'下载 {info}',
                ncols=160,
                ascii=False,
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}{postfix}]",
                colour="green"
            ) as pbar:
                # 异步读取数据流并写入文件
                async for chunk in resp.aiter_bytes(1024):
                    if not chunk:
                        break
                    process += len(chunk)
                    f.write(chunk)
                    pbar.update(len(chunk))  # 更新进度条

    except Exception as e:
        logger.error(f"An error occurred while downloading {info}: {e}")
        raise e


async def download_video():
    """下载视频并处理合并操作"""
    logger.info("Downloading video started.")

    bv_id = input("Please enter the video BV_ID: ").strip()
    if not bv_id.startswith('BV') or len(bv_id) != 12:
        logger.error(f"Invalid BV ID: {bv_id}")
        print("Invalid BV ID. Currently, only 12-bit is supported, please make sure it's a valid Bilibili BV ID.")
        return

    try:
        credential = Credential(sessdata=config.SESS_DATA, bili_jct=config.BILI_JCT, buvid3=config.BUV_ID3)
        v = video.Video(bvid=bv_id, credential=credential)

        # 获取视频的下载链接
        download_url_data = await v.get_download_url(0)
        detector = video.VideoDownloadURLDataDetecter(data=download_url_data)
        streams = detector.detect_best_streams()

        # 判断视频流的格式
        if detector.check_flv_stream():
            # 下载 FLV 流
            flv_path = os.path.join(DOWNLOAD_DIR, "flv_temp.flv")
            mp4_path = os.path.join(DOWNLOAD_DIR, f"{bv_id}.mp4")
            await download_url(streams[0].url, flv_path, "FLV 视频流")
            # 转换为 MP4
            os.system(f'{FFMPEG_PATH} -i {flv_path} -c copy {mp4_path}')
            os.remove(flv_path)  # 删除临时文件
        else:
            # 下载 MP4 视频流和音频流
            video_path = os.path.join(DOWNLOAD_DIR, "video_temp.m4s")
            audio_path = os.path.join(DOWNLOAD_DIR, "audio_temp.m4s")
            mp4_path = os.path.join(DOWNLOAD_DIR, f"{bv_id}.mp4")
            await download_url(streams[0].url, video_path, "视频流")
            await download_url(streams[1].url, audio_path, "音频流")
            # 合并视频和音频流
            os.system(f'{FFMPEG_PATH} -i {video_path} -i {audio_path} -c copy {mp4_path}')
            # 删除临时文件
            os.remove(video_path)
            os.remove(audio_path)

        logger.info(f"Video downloaded successfully and saved to {mp4_path}")

    except Exception as e:
        logger.error(f"An error occurred while downloading the video: {e}")


