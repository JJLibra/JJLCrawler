from PyInquirer import prompt

from modules.video import upload, download, info, comments, barrages, votes, homepage, tab_video, online
from base.base_crawler import AbstractCrawler
from tools.utils import logger


class VideoCrawler(AbstractCrawler):

    async def start(self):
        logger.info("VideoCrawler started.")

        mode = await self.select_mode()

        if mode == 'upload':
            await upload.upload_video()
        elif mode == 'download':
            await download.download_video()
        elif mode == 'info':
            await info.fetch_video_info()
        elif mode == 'comments':
            await comments.fetch_video_comments()
        elif mode == 'barrages':
            await barrages.fetch_video_barrages()
        elif mode == 'votes':
            await votes.fetch_video_votes()
        elif mode == 'homepage':
            await homepage.fetch_homepage_videos()
        elif mode == 'tab_video':
            await tab_video.fetch_tab_videos()
        elif mode == 'online':
            await online.get_number_of_online_people()
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
                    'Download video',
                    'Fetch video info',
                    'Fetch video comments',
                    'Fetch video barrages',
                    'Fetch video votes',
                    'Fetch homepage videos'
                    'Get the video under the Videos tab'
                    'Get the number of currently online people'
                ]
            }
        ]

        answers = prompt(questions)

        logger.info(f"Mode selected: {answers['mode']}")

        if answers['mode'] == 'Upload video':
            return 'upload'
        elif answers['mode'] == 'Download video':
            return 'download'
        elif answers['mode'] == 'Fetch video info':
            return 'info'
        elif answers['mode'] == 'Fetch video comments':
            return 'comments'
        elif answers['mode'] == 'Fetch video barrages':
            return 'barrages'
        elif answers['mode'] == 'Fetch video votes':
            return 'votes'
        elif answers['mode'] == 'Fetch homepage videos':
            return 'homepage'
        elif answers['mode'] == 'Get the video under the Videos tab':
            return 'tab_video'
        elif answers['mode'] == 'Get the number of currently online people':
            return 'online'

