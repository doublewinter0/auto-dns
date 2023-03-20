import logging
import pathlib
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyaml_env import parse_config

from src.constant import ConfigConstant, MainConstant, NumberConstant, TimeZoneConstant
from src.helper.singleton import Singleton
from src.log.main import LogConfig
from src.property import RecordProperty

logger = logging.getLogger(__name__)


def log_init(config: dict) -> None:
    LogConfig(config).log_setup()

    logger.info('Logger config finished...')


def get_app_config(stream) -> dict:
    try:
        return parse_config(data=stream, raise_if_na=False)
    except Exception as exp:
        logger.error(','.join(exp.args))
        sys.exit(-NumberConstant.ONE)


@Singleton
class AppConfig:
    def __init__(self):
        pass

    def app_config(self) -> None:
        self.__dir_config()
        self.__scheduler_task_config()

        logger.info('App config finished...')

    @classmethod
    def __dir_config(cls) -> None:
        pathlib.Path(MainConstant.TMP_DIR).mkdir(parents=True, exist_ok=True)

        logger.info('Dir config finished...')

    @classmethod
    def __scheduler_task_config(cls) -> None:
        from src.scheduler.task.main import CDN
        # def listener(event):
        #     pass

        scheduler = AsyncIOScheduler(timezone=TimeZoneConstant.SHANGHAI)
        scheduler.add_job(CDN.main, trigger=ConfigConstant.CRON, args=[RecordProperty().ids],
                          hour=NumberConstant.TEN)

        scheduler.start()

        logger.info("Scheduler task config finished...")
