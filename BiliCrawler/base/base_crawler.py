from abc import ABC, abstractmethod


class AbstractCrawler(ABC):
    @abstractmethod
    async def start(self):
        """
        start crawler
        """
        pass
