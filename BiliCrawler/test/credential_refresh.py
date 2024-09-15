from bilibili_api import Credential, sync
import config

# 生成一个 Credential 对象
credential = Credential(sessdata=config.SESS_DATA, bili_jct=config.BILI_JCT, ac_time_value=config.AC_TIME_VALUE)

# 检查 Credential 是否需要刷新
print(sync(credential.check_refresh()))

# 刷新 Credential
sync(credential.refresh())

