from base.base_crawler import AbstractCrawler
from PyInquirer import prompt
from tools.utils import logger
import info, upload, comments


class VideoCrawler(AbstractCrawler):

    async def start(self):
        logger.info("VideoCrawler started.")

        mode = await self.select_mode()

        if mode == 'download':
            await upload.upload_video()
        elif mode == 'info':
            await info.fetch_video_info()
        elif mode == 'comments':
            await comments.fetch_video_comments()
        else:
            logger.error("Invalid mode selected.")
            print("Invalid mode selected. Please choose 'upload', 'info', or 'comments'.")

        logger.info("VideoCrawler finished.")

    @staticmethod
    async def select_mode():
        questions = [
            {
                'type': 'list',
                'name': 'mode',
                'message': 'Please select the mode of VideoCrawler you want to use:',
                'choices': [
                    'Upload video',
                    'Fetch video info',
                    'Fetch video comments'
                ]
            }
        ]

        answers = prompt(questions)

        logger.info(f"Mode selected: {answers['mode']}")

        if answers['mode'] == 'Upload video':
            return 'download'
        elif answers['mode'] == 'Fetch video info':
            return 'info'
        elif answers['mode'] == 'Fetch video comments':
            return 'comments'

