from bilibili_api import sync, video_uploader, Credential
import config


async def main():
    credential = Credential(sessdata=config.SESS_DATA, bili_jct=config.BILI_JCT, buvid3=config.BUV_ID3)

    vu_meta = video_uploader.VideoMeta(tid=130,
                                       title='title',
                                       tags=['音乐综合', '音乐'],
                                       desc='BiliCrawler 视频上传测试',
                                       cover="./cover.jpg",
                                       no_reprint=True
                                       )

    page = video_uploader.VideoUploaderPage(
        path='./video.mp4',
        title='标题',
        description='简介',
    )
    uploader = video_uploader.VideoUploader([page], vu_meta, credential, line=video_uploader.Lines.QN)  # 自动测速选择最优线路

    @uploader.on("__ALL__")
    async def ev(data):
        print(data)

    await uploader.start()


sync(main())
