# Playwright

与 Selenium 类似的自动化工具

## bilibili-api-python

这是作者用于学习理解`B站`api的工具包，如果不熟悉bilibili的api，在 MediaCrawler 的学习过程中会遇到困难（像作者这样的初学者比较难理解有些代码的意义）

## MediaCrawler

原作者：[NanmiCoder/MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)

## 功能列表
| 平台  | 关键词搜索 | 指定帖子ID爬取 | 二级评论 | 指定创作者主页 | 登录态缓存 | IP代理池 | 生成评论词云图 |
|-----|-------|---------|-----|--------|-------|-------|-------|
| 小红书 | ✅     | ✅       | ✅   | ✅      | ✅     | ✅     | ✅    |
| 抖音  | ✅     | ✅       | ✅    | ✅       | ✅     | ✅     | ✅    |
| 快手  | ✅     | ✅       | ✅   | ✅      | ✅     | ✅     | ✅    |
| B 站 | ✅     | ✅       | ✅   | ✅      | ✅     | ✅     | ✅    |
| 微博  | ✅     | ✅       | ✅   | ✅      | ✅     | ✅     | ✅    |
| 贴吧  | ✅     | ✅       | ✅   | ✅      | ✅     | ✅     | ✅    |
| 知乎  | ✅     |   ❌      | ✅   | ❌      | ✅     | ✅     | ✅    |

## 使用方法

### 创建并激活 python 虚拟环境
   ```shell   
   # 进入项目根目录
   cd MediaCrawler
   
   # 创建虚拟环境
   # 我的python版本是：3.9.6，requirements.txt中的库是基于这个版本的，如果是其他python版本，可能requirements.txt中的库不兼容，自行解决一下。
   python -m venv venv
   
   # macos & linux 激活虚拟环境
   source venv/bin/activate

   # windows 激活虚拟环境
   venv\Scripts\activate

   ```

### 安装依赖库

   ```shell
   pip install -r requirements.txt
   ```

### 安装 playwright浏览器驱动

   ```shell
   playwright install
   ```

### 运行爬虫程序

   ```shell
   ### 项目默认是没有开启评论爬取模式，如需评论请在config/base_config.py中的 ENABLE_GET_COMMENTS 变量修改
   ### 一些其他支持项，也可以在config/base_config.py查看功能，写的有中文注释
   
   # 从配置文件中读取关键词搜索相关的帖子并爬取帖子信息与评论
   python main.py --platform xhs --lt qrcode --type search
   
   # 从配置文件中读取指定的帖子ID列表获取指定帖子的信息与评论信息
   python main.py --platform xhs --lt qrcode --type detail
  
   # 打开对应APP扫二维码登录
     
   # 其他平台爬虫使用示例，执行下面的命令查看
   python main.py --help    
   ```

### 数据保存
- 支持关系型数据库Mysql中保存（需要提前创建数据库）
    - 执行 `python db.py` 初始化数据库数据库表结构（只在首次执行）
- 支持保存到csv中（data/目录下）
- 支持保存到json中（data/目录下）