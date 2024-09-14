import json
from typing import Dict
from enum import Enum
from base.base_crawler import AbstractCrawler
from tools.utils import logger
from bilibili_api import emoji
from PyInquirer import prompt


class FormatType(Enum):
    TWIKOO = 'twikoo'
    OTHER = 'other'


class EmojiCrawler(AbstractCrawler):

    def __init__(self):
        """
        格式化类型将根据用户的选择动态确定，目前只支持 twikoo
        """
        super().__init__()
        self.format_type = self.select_format_type()

    async def start(self):
        try:
            logger.info(f"Start emoji crawling...")
            emoji_info = await emoji.get_emoji_list()

            if self.format_type == FormatType.TWIKOO:
                formatted_data = self.format_data_to_twikoo(emoji_info)
            elif self.format_type == FormatType.OTHER:
                formatted_data = self.format_data_to_other(emoji_info)
            else:
                raise ValueError("Unsupported format type")

            self.save_to_json(formatted_data)

        except Exception as e:
            logger.error(f'Error while crawling emoji: {e}')

    @staticmethod
    def format_data_to_twikoo(emoji_info: Dict):
        """
        将获取的 emoji 数据格式化为 twikoo 评论区的导入版本
        """
        formatted_data = {}

        for package in emoji_info['packages']:
            package_name = package['text']
            formatted_data[package_name] = {
                "type": "image",
                "container": [
                    {
                        "text": f'{package_name}-{i + 1}',
                        "icon": f"<img src='{item['url']}'>"
                    } for i, item in enumerate(package['emote'])
                ]
            }

        return formatted_data

    @staticmethod
    def format_data_to_other(emoji_info: Dict):
        """
        将获取的 emoji 数据格式化为其他评论区的导入版本（示例）
        """
        formatted_data = {}

        for package in emoji_info['packages']:
            package_name = package['text']
            formatted_data[package_name] = {
                "type": "emoji-list",
                "emojis": [
                    {
                        "name": f'{package_name}-{i + 1}',
                        "image_url": item['url']
                    } for i, item in enumerate(package['emote'])
                ]
            }

        return formatted_data

    @staticmethod
    def save_to_json(formatted_data: Dict):
        """
        将格式化的数据保存到 JSON 文件中
        """
        file_path = './results/twikoo_emoji.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(formatted_data, f, ensure_ascii=False, indent=4)
        logger.info(f"Emoji data saved to {file_path}")

    @staticmethod
    def select_format_type() -> FormatType:
        """
        使用 PyInquirer 提供格式选择
        :return: FormatType
        """
        questions = [
            {
                'type': 'list',
                'name': 'format_type',
                'message': 'Please choose the format type:',
                'choices': [
                    {'name': 'Twikoo (twikoo)', 'value': FormatType.TWIKOO},
                    {'name': 'Other (other)', 'value': FormatType.OTHER}
                ]
            }
        ]

        answers = prompt(questions)
        return answers['format_type']
