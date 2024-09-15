"""
视频文件上传参数
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
ORIGINAL = False
MISSION_ID = None
SOURCE = None
RECREATE = None
NO_REPRINT = True
OPEN_ELEC = None
UP_SELECTION_REPLY = None
UP_CLOSE_DANMU = None
UP_CLOSE_REPLY = None
LOSSLESS_MUSIC = None
DOLBY = None
SUBTITLE = None
DYNAMIC = None
NEUTRAL_MARK = None
DELAY_TIME = None
PORDER = None
