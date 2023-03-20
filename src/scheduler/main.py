from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.helper.singleton import Singleton


@Singleton
class Scheduler:
    def __init__(self, config):
        self._scheduler = AsyncIOScheduler(config)
