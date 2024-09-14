import os
import json


class FileHandler:
    def __init__(self, directory='./results'):
        """
        初始化文件处理类，设置保存文件的目录。
        :param directory: 文件保存的目录，默认为当前目录下的 'results' 文件夹
        """
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)  # 确保目录存在

    def save_json(self, file_name, data):
        """
        将数据保存为 JSON 文件。
        :param file_name: 文件名，不包含路径
        :param data: 要保存的数据（字典）
        :return: None
        """
        file_path = os.path.join(self.directory, file_name)
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"File saved to {file_path}")
