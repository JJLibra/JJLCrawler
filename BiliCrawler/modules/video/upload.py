from typing import Type

import config
from tools.utils import logger
from bilibili_api import Credential, video_uploader


async def upload_video():
    """
    具体请参照文档：https://nemo2011.github.io/bilibili-api/#/modules/video_uploader
    """
    logger.info("Uploading video started.")

    credential = Credential(sessdata=config.SESS_DATA, bili_jct=config.BILI_JCT, buvid3=config.BUV_ID3)

    """
    必选项
    tid	                int	                            分区 ID。可以使用 channel 模块进行查询。
    title	            str	                            视频标题
    desc	            str	                            视频简介
    cover	            Picture	                        封面 URL
    tags	            Union[List[str], str]       	使用英文半角逗号分隔的标签组
    可选项，默认都关闭
    original	        bool	                        可选，是否为原创视频
    mission_id	        Optional[int]	                可选，任务 ID
    source	            Optional[str]	                可选，视频来源
    recreate	        Optional[bool]	                可选，是否允许重新上传
    no_reprint	        Optional[bool]	                可选，是否禁止转载
    open_elec	        Optional[bool]	                可选，是否展示充电信息
    up_selection_reply	Optional[bool]	                可选，是否开启评论精选
    up_close_danmu	    Optional[bool]	                可选，是否关闭弹幕
    up_close_reply	    Optional[bool]	                可选，是否关闭评论
    lossless_music	    Optional[bool]	                可选，是否启用无损音乐
    dolby	            Optional[bool]	                可选，是否启用杜比音效
    subtitle	        Optional[dict]	                可选，字幕设置
    dynamic	            Optional[str]	                可选，动态信息
    neutral_mark	    Optional[str]	                可选，创作者声明
    delay_time	        Optional[Union[int, datetime]]	可选，定时发布时间戳（秒）
    porder	            Optional[VideoPorderMeta]	    可选，商业相关参数
    """
    # tid 分区号可以参考：https://biliup.github.io/tid-ref.html#:~:text=%E9%9F%B3%E4%B9%90%E5%8C%BA%EF%BC%9A%20130%2C%E9%9F%B3%E4%B9%90%E7%BB%BC%E5%90%88%2029%2C%E9%9F%B3%E4%B9%90%E7%8E%B0%E5%9C%BA%2059%2C%E6%BC%94%E5%A5%8F%2031%2C%E7%BF%BB%E5%94%B1%20193%2CMV%2030%2CVOCALOID%C2%B7UTAU%20194%2C%E7%94%B5%E9%9F%B3,28%2C%E5%8E%9F%E5%88%9B%E9%9F%B3%E4%B9%90%20%E5%8A%A8%E7%94%BB%E5%8C%BA%EF%BC%9A%2024%2CMAD%C2%B7AMV%2025%2CMMD%C2%B73D%2027%2C%E7%BB%BC%E5%90%88%2047%2C%E7%9F%AD%E7%89%87%C2%B7%E6%89%8B%E4%B9%A6%C2%B7%E9%85%8D%E9%9F%B3%20210%2C%E6%89%8B%E5%8A%9E%C2%B7%E6%A8%A1%E7%8E%A9%2086%2C%E7%89%B9%E6%91%84
    def get_input_with_type(prompt, input_type=str, transform_func=lambda x: x):
        """
        通用输入获取函数，处理空输入、类型转换，并支持 'back' 回退功能。

        Args:
            prompt (str): 提示信息
            input_type (Type): 输入的预期类型
            transform_func (function): 转换函数，例如 str.split(',')

        Returns:
            转换后的用户输入，或 None 表示退出，'back' 表示回退到上一步
        """
        while True:
            user_input = input(prompt).strip()
            if user_input.lower() == "exit":
                return None
            if user_input.lower() == "back":
                return "back"
            if user_input == "":
                print("输入不能为空，请重新输入。")
            else:
                try:
                    return transform_func(input_type(user_input))
                except ValueError:
                    print(f"输入无效，请输入有效的 {input_type.__name__} 类型。")

    # 堆栈用于保存用户的输入步骤
    input_steps = []

    def step(prompt: str, input_type: Type = str, transform_func=lambda x: x):
        """
        管理用户输入步骤，并支持 'back' 回退功能。

        Args:
            prompt (str): 提示信息
            input_type (Type): 输入的预期类型
            transform_func (function): 转换函数，例如 str.split(',')

        Returns:
            转换后的输入值或 'back' 表示回退或 None 表示退出
        """
        while True:
            result = get_input_with_type(prompt, input_type, transform_func)
            if result == "back":
                if input_steps:
                    print("回退到上一步...")
                    input_steps.pop()
                else:
                    print("已经是第一步，无法回退。")
            elif result is None:
                return None  # 用户输入 'exit'，直接退出
            else:
                input_steps.append(result)  # 保存步骤
                return result

    # 获取用户输入
    tid = step("tid (eg. 130 is music): ", int)
    if tid is None:
        return

    title = step("title: ", str)
    if title is None:
        return

    tags = step("tags (eg. tag1, tag2,...): ", str, lambda x: x.split(','))
    if tags is None:
        return

    desc = step("desc: ", str)
    if desc is None:
        return

    cover = step("cover image (eg. ./upload/eg/cover.jpg): ", str)
    if cover is None:
        return

    path = step("video source (eg. ./upload/eg/video.mp4): ", str)
    if path is None:
        return

    logger.info("For other optional configuration items, please go to config/video.py.")

    vu_meta = video_uploader.VideoMeta(tid=tid,
                                       title=title,
                                       tags=tags,
                                       desc=desc,
                                       cover=cover,
                                       original=config.ORIGINAL,
                                       mission_id=config.MISSION_ID,
                                       source=config.SOURCE,
                                       recreate=config.RECREATE,
                                       no_reprint=config.NO_REPRINT,
                                       open_elec=config.OPEN_ELEC,
                                       up_selection_reply=config.UP_SELECTION_REPLY,
                                       up_close_danmu=config.UP_CLOSE_DANMU,
                                       up_close_reply=config.UP_CLOSE_REPLY,
                                       lossless_music=config.LOSSLESS_MUSIC,
                                       dolby=config.DOLBY,
                                       subtitle=config.SUBTITLE,
                                       dynamic=config.DYNAMIC,
                                       neutral_mark=config.NEUTRAL_MARK,
                                       delay_time=config.DELAY_TIME,
                                       porder=config.PORDER
                                       )

    page = video_uploader.VideoUploaderPage(
        path=path,
        title=title,
        description=desc,
    )
    # 自动测速选择最优线路，目前仅支持：BDA2-百度 QN-七牛 WS-网宿 BLDSA-bldsa
    uploader = video_uploader.VideoUploader([page], vu_meta, credential)

    @uploader.on("__ALL__")
    async def ev(data):
        print(data)

    await uploader.start()

    logger.info("Uploading video finished successfully.")
