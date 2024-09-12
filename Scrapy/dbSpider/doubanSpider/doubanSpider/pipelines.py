# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
import pandas as pd
import numpy as np


class DoubanspiderPipeline(object):
    def open_spider(self, spider):
        self.item_list = ["详情链接", "中文名称", "原名", "别名列表", "播放状态",
                          "评论人数", "评分", "中心主题", "编剧列表", "导演列表", "主演列表",
                          "官方网站", "上映时间", "制片国/地区", "语言", "片长", "类型"]

        # 导出txt
        self.f_txt = open('result.txt', 'w+', encoding='utf-8')

        # 导出excel
        self.f_excel = pd.ExcelWriter("result.xlsx")
        self.data_excel = []

        # 导出json
        self.f_json = open('result.json', 'w+', encoding='utf-8')
        self.f_json.write("[")

    def process_item(self, item, spider):
        # 导出txt
        json_data = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.f_txt.write(json_data)

        # 导出excel
        li_temp = np.array(list(dict(item).values()))
        li_data = []
        for i in range(len(li_temp)):
            li_data.append(str(li_temp[i]).replace("[", "").replace("]", "").strip('"').strip("'").replace("', '", ","))
        self.data_excel.append(li_data)

        # 导出json
        self.f_json.write(json_data + ",")

        return item

    def close_spider(self, spider):
        # 导出txt
        self.f_txt.close()

        # 导出excel
        self.data_df = pd.DataFrame(self.data_excel)
        self.data_df.columns = self.item_list
        self.data_df.index = np.arange(1, len(self.data_df) + 1)
        self.data_df.to_excel(self.f_excel, float_format='%.5f')
        self.f_excel.save()

        # 导出json
        self.f_json.seek(self.f_json.tell() - 1, 0)  # 解决退格问题
        self.f_json.write("]")
        self.f_json.close()
