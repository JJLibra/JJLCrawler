import json

from bilibili_api import video, Credential, comment, sync
import config

credential = Credential(sessdata=config.SESS_DATA, bili_jct=config.BILI_JCT, buvid3=config.BUV_ID3)

v = video.Video(credential=credential, bvid='BV1ej421S7wn')

av_id = v.get_aid()

comments_dict = sync(comment.get_comments(oid=av_id, type_=comment.CommentResourceType.VIDEO,
                                          page_index=1, credential=credential))
unames = []
comments = []
for item in comments_dict['replies']:
    unames.append(item['member']['uname'])
    comments.append(item['content']['message'])
    print(f"{item['member']['uname']}: {item['content']['message']}")

print(f"\n\n共有 {comments_dict['page']['count']} 条评论（不含子评论）")


# with open('comments.json', 'w', encoding='utf-8') as f:
#     json.dump(comments, f, ensure_ascii=False, indent=4)
