from bilibili_api import video, sync, Credential
import config

credential = Credential(sessdata=config.SESS_DATA, bili_jct=config.BILI_JCT, buvid3=config.BUV_ID3)
v = video.Video(credential=credential, bvid='BV1ej421S7wn')

dms = sync(v.get_danmakus(page_index=0))

print(dms[0].text)
