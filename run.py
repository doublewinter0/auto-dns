import asyncio

import yaml

from src.config import AppConfig, log_init, get_app_config
from src.constant import MainConstant
from src.property import PropertyConfig


def main():
    with open(MainConstant.LOG_CONFIG, encoding=MainConstant.UTF8) as stream:
        log_init(yaml.load(stream, Loader=yaml.loader.SafeLoader))

    with open(MainConstant.CONFIG, encoding=MainConstant.UTF8) as stream:
        cfg_dict = get_app_config(stream)
        PropertyConfig(cfg_dict)
        AppConfig().app_config()

    loop = asyncio.get_event_loop()
    loop.run_forever()


if __name__ == MainConstant.MAIN:
    main()
