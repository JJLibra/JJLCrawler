from PyInquirer import prompt

from modules.video import upload, info, comments, barrages
from base.base_crawler import AbstractCrawler
from tools.utils import logger


class VideoCrawler(AbstractCrawler):

    async def start(self):
        logger.info("VideoCrawler started.")

        mode = await self.select_mode()

        if mode == 'upload':
            await upload.upload_video()
        elif mode == 'info':
            await info.fetch_video_info()
        elif mode == 'comments':
            await comments.fetch_video_comments()
        elif mode == 'barrages':
            await barrages.fetch_video_barrages()
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
                    'Fetch video comments',
                    'Fetch video barrages'
                ]
            }
        ]

        answers = prompt(questions)

        logger.info(f"Mode selected: {answers['mode']}")

        if answers['mode'] == 'Upload video':
            return 'upload'
        elif answers['mode'] == 'Fetch video info':
            return 'info'
        elif answers['mode'] == 'Fetch video comments':
            return 'comments'
        elif answers['mode'] == 'Fetch video barrages':
            return 'barrages'

