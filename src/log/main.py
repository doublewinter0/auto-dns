import logging
import logging.config
import os
import sys

from src.constant import NumberConstant
from src.helper.singleton import Singleton


@Singleton
class LogConfig:
    def __init__(self, config: dict, default_level=logging.INFO):
        self.__config = config
        self.__default_level = default_level

    def log_setup(self):
        try:
            if self.__config:
                logging.config.dictConfig(self.__config)
            else:
                logging.basicConfig(level=self.__default_level)
        except ValueError as exp:
            inner_exp = exp.__context__
            if isinstance(inner_exp, FileNotFoundError):
                os.makedirs(os.path.dirname(inner_exp.filename))
            else:
                sys.exit(-NumberConstant.ONE)
